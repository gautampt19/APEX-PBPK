import torch
from colpali_engine.models import ColPali, ColPaliProcessor
from PIL import Image
import io

def retrieve_top_k_pages(pdf_path: str, queries: list[str], top_k: int = 5):
    # This requires pdf2image to convert PDF pages to PIL Images
    from pdf2image import convert_from_path
    
    print(f"Converting {pdf_path} to images...")
    images = convert_from_path(pdf_path)
    
    model_name = "vidore/colpali-v1.3-hf"
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    
    print(f"Loading ColPali model on {device}...")
    model = ColPali.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map=device
    ).eval()
    processor = ColPaliProcessor.from_pretrained(model_name)
    
    print("Embedding pages...")
    # Process images in batches to save memory
    with torch.no_grad():
        batch_images = processor.process_images(images).to(device)
        image_embeddings = model(**batch_images)
        
        print("Embedding queries...")
        batch_queries = processor.process_queries(queries).to(device)
        query_embeddings = model(**batch_queries)
        
        # Compute scores (MaxSim)
        scores = processor.score_multi_vector(query_embeddings, image_embeddings)
        
    # Aggregate scores across all queries (e.g., max or sum)
    # scores shape is (num_queries, num_pages)
    combined_scores = scores.sum(dim=0)
    
    # Get top-k indices
    top_k_indices = combined_scores.topk(k=min(top_k, len(images))).indices.cpu().tolist()
    
    top_k_images = [images[idx] for idx in top_k_indices]
    
    # Free memory
    del model
    del processor
    torch.cuda.empty_cache()
    
    return top_k_images, top_k_indices
