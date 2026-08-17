"""
colpali_retriever.py — Visual document retrieval for PBPK scientific papers.

Uses ColPali (vision-language late-interaction model) to identify the most
relevant pages in a PDF by visual similarity to PBPK-specific queries,
completely bypassing OCR.

Flow:
  1. Convert PDF pages → PIL images (via PyMuPDF)
  2. Load ColPali model and encode all page images
  3. Encode domain-specific text queries
  4. Score pages via late-interaction (MaxSim)
  5. Return top-K most relevant page images + page numbers
"""

import os
import io
import logging
from typing import List, Tuple, Optional

import torch
from PIL import Image

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ── Default PBPK retrieval queries ───────────────────────────────────────────

DEFAULT_PBPK_QUERIES = [
    "Table of physiological parameters: organ blood flows, organ volumes, partition coefficients",
    "PBPK model compartment diagram showing tissue connections and blood flow",
    "Differential equations for mass balance, ODE system, dA/dt",
    "Pharmacokinetic parameters: Vmax, Km, clearance, absorption rate, fraction unbound",
    "Drug dose, body weight, cardiac output, species information",
]


# ── PDF to images ────────────────────────────────────────────────────────────

def pdf_to_images(pdf_path: str, dpi: int = 200, max_size: int = 1024) -> List[Image.Image]:
    """
    Convert all pages of a PDF to PIL Images using PyMuPDF.
    Returns a list of PIL Image objects (one per page).
    """
    import fitz  # PyMuPDF

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    images = []

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        pix = page.get_pixmap(dpi=dpi)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data)).convert("RGB")

        # Resize large images to keep memory manageable
        if img.width > max_size or img.height > max_size:
            img.thumbnail((max_size, max_size), Image.LANCZOS)

        images.append(img)

    doc.close()
    logging.info(f"Converted {len(images)} PDF pages to images (dpi={dpi})")
    return images


def save_page_images(images: List[Image.Image], output_dir: str) -> List[str]:
    """Save PIL images to disk and return their file paths."""
    os.makedirs(output_dir, exist_ok=True)
    paths = []
    for idx, img in enumerate(images):
        path = os.path.join(output_dir, f"page_{idx + 1:04d}.png")
        img.save(path, format="PNG")
        paths.append(path)
    return paths


# ── ColPali Model ────────────────────────────────────────────────────────────

class ColPaliRetriever:
    """
    Visual document retriever using ColPali late-interaction embeddings.

    Usage:
        retriever = ColPaliRetriever()
        top_pages = retriever.retrieve(pdf_path, queries, top_k=5)
    """

    def __init__(self, model_name: str = "vidore/colpali-v1.3-hf", device: str = None):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.processor = None

    def _load_model(self):
        """Lazy-load ColPali model and processor."""
        if self.model is not None:
            return

        logging.info(f"Loading ColPali model: {self.model_name} on {self.device}")

        from transformers import ColPaliForRetrieval, ColPaliProcessor

        self.model = ColPaliForRetrieval.from_pretrained(
            self.model_name,
            torch_dtype=torch.bfloat16 if self.device == "cuda" else torch.float32,
            device_map=self.device,
        ).eval()

        self.processor = ColPaliProcessor.from_pretrained(self.model_name)
        logging.info("ColPali model loaded successfully.")

    def _encode_images(self, images: List[Image.Image], batch_size: int = 4) -> torch.Tensor:
        """Encode page images into multi-vector embeddings."""
        all_embeddings = []
        for i in range(0, len(images), batch_size):
            batch = images[i:i + batch_size]
            inputs = self.processor(images=batch, return_tensors='pt').to(self.model.device)
            with torch.no_grad():
                embeddings = self.model(**inputs)
            if hasattr(embeddings, 'embeddings'):
                all_embeddings.append(embeddings.embeddings.cpu())
            else:
                all_embeddings.append(embeddings.cpu())
        return torch.cat(all_embeddings, dim=0)

    def _encode_queries(self, queries: List[str]) -> torch.Tensor:
        """Encode text queries into multi-vector embeddings."""
        inputs = self.processor(text=queries, return_tensors='pt').to(self.model.device)
        with torch.no_grad():
            embeddings = self.model(**inputs)
        if hasattr(embeddings, 'embeddings'):
            return embeddings.embeddings.cpu()
        return embeddings.cpu()

    def _score_pages(
        self,
        query_embeddings: torch.Tensor,
        image_embeddings: torch.Tensor,
    ) -> List[float]:
        """
        Compute per-page relevance scores by aggregating MaxSim across all queries.
        Returns a list of scores (one per page).
        """
        n_pages = image_embeddings.shape[0]
        page_scores = [0.0] * n_pages

        for q_idx in range(query_embeddings.shape[0]):
            q_emb = query_embeddings[q_idx]  # [n_query_tokens, dim]
            for p_idx in range(n_pages):
                p_emb = image_embeddings[p_idx]  # [n_patches, dim]
                # MaxSim: for each query token, find max similarity across patches
                sim_matrix = torch.matmul(q_emb, p_emb.T)  # [n_query_tokens, n_patches]
                max_sim_per_token = sim_matrix.max(dim=1).values  # [n_query_tokens]
                score = max_sim_per_token.sum().item()
                page_scores[p_idx] += score

        return page_scores

    def retrieve(
        self,
        pdf_path: str,
        queries: List[str] = None,
        top_k: int = 5,
        dpi: int = 200,
    ) -> List[Tuple[int, float, Image.Image]]:
        """
        Retrieve the top-K most relevant pages from a PDF.

        Args:
            pdf_path: Path to the PDF file.
            queries: List of text queries. Defaults to PBPK-specific queries.
            top_k: Number of pages to return.
            dpi: Resolution for PDF-to-image conversion.

        Returns:
            List of (page_number, score, pil_image) tuples, sorted by relevance.
        """
        self._load_model()

        if queries is None:
            queries = DEFAULT_PBPK_QUERIES

        # Convert PDF to images
        page_images = pdf_to_images(pdf_path, dpi=dpi)
        logging.info(f"Encoding {len(page_images)} page images with ColPali...")

        # Encode
        image_embeddings = self._encode_images(page_images)
        query_embeddings = self._encode_queries(queries)

        # Score
        page_scores = self._score_pages(query_embeddings, image_embeddings)

        # Rank and select top-K
        scored_pages = [
            (idx + 1, score, page_images[idx])
            for idx, score in enumerate(page_scores)
        ]
        scored_pages.sort(key=lambda x: x[1], reverse=True)
        top_pages = scored_pages[:top_k]

        logging.info(f"ColPali top-{top_k} pages: {[(p[0], f'{p[1]:.1f}') for p in top_pages]}")
        return top_pages


# ── Convenience function ─────────────────────────────────────────────────────

def retrieve_relevant_pages(
    pdf_path: str,
    model_name: str = "vidore/colpali-v1.3-hf",
    queries: List[str] = None,
    top_k: int = 5,
    output_dir: str = None,
) -> Tuple[List[Image.Image], List[int], List[str]]:
    """
    High-level convenience function for the pipeline.

    Returns:
        (page_images, page_numbers, saved_paths)
        - page_images: List of PIL Images for top-K pages
        - page_numbers: Corresponding 1-indexed page numbers
        - saved_paths: File paths if output_dir was specified, else empty list
    """
    retriever = ColPaliRetriever(model_name=model_name)
    results = retriever.retrieve(pdf_path, queries=queries, top_k=top_k)

    page_images = [r[2] for r in results]
    page_numbers = [r[0] for r in results]
    saved_paths = []

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        for page_num, _, img in results:
            path = os.path.join(output_dir, f"colpali_page_{page_num:04d}.png")
            img.save(path, format="PNG")
            saved_paths.append(path)
        logging.info(f"Saved {len(saved_paths)} retrieved page images to {output_dir}")

    return page_images, page_numbers, saved_paths


# ── CLI for standalone testing ───────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="ColPali Visual Document Retrieval for PBPK Papers"
    )
    parser.add_argument("--pdf", required=True, help="Path to the input PDF")
    parser.add_argument("--top-k", type=int, default=5, help="Number of pages to retrieve")
    parser.add_argument("--output-dir", default=None, help="Directory to save retrieved page images")
    parser.add_argument("--model", default="vidore/colpali-v1.3-hf", help="ColPali model name")

    args = parser.parse_args()

    images, page_nums, paths = retrieve_relevant_pages(
        pdf_path=args.pdf,
        model_name=args.model,
        top_k=args.top_k,
        output_dir=args.output_dir,
    )

    print(f"\n{'='*60}")
    print(f"  ColPali Retrieved {len(images)} Pages")
    print(f"{'='*60}")
    for i, pnum in enumerate(page_nums):
        print(f"  Rank {i+1}: Page {pnum}")
        if paths:
            print(f"           Saved: {paths[i]}")
    print(f"{'='*60}")
