"""
clean_markdown.py — Pre-process OCR Markdown before LLM extraction.

Features:
  1. Header/Footer Suppression: Detects and removes repeating running headers,
     publisher watermarks, page markers, and standalone page numbers.
  2. Smart Chunking: For large documents (>10k words), splits text at sentence
     boundaries with configurable overlap so each chunk fits inside an LLM's
     context window. Returns either the cleaned full text or a list of chunks.
"""

import re
import argparse
import os
from typing import List, Optional
from collections import Counter


# ── Header / Footer Suppression ──────────────────────────────────────────────

# Patterns commonly emitted by the Unlimited-OCR model
_PAGE_MARKER_RE = re.compile(r"^\s*<PAGE>\s*$", re.MULTILINE)
_STANDALONE_PAGE_NUM_RE = re.compile(r"^\s*\d{1,4}\s*$", re.MULTILINE)
_PAGE_X_OF_Y_RE = re.compile(r"^\s*Page\s+\d+\s+of\s+\d+.*$", re.MULTILINE | re.IGNORECASE)


def _detect_repeating_lines(text: str, min_occurrences: int = 3) -> set:
    """Find lines that repeat ≥ min_occurrences times (likely headers/footers)."""
    lines = text.split("\n")
    # Normalise whitespace for comparison but keep original for matching
    normalised = [re.sub(r"\s+", " ", line).strip() for line in lines]
    counts = Counter(normalised)
    repeating = {
        line for line, count in counts.items()
        if count >= min_occurrences and 3 < len(line) < 120  # ignore very short or very long
    }
    return repeating


def suppress_headers_footers(text: str) -> str:
    """Remove repeating headers, footers, page markers, and publisher stamps."""
    # 1. Remove <PAGE> markers
    text = _PAGE_MARKER_RE.sub("", text)

    # 2. Remove "Page X of Y ..." lines
    text = _PAGE_X_OF_Y_RE.sub("", text)

    # 3. Detect and remove repeating lines (journal name, publisher, etc.)
    repeating = _detect_repeating_lines(text)
    if repeating:
        cleaned_lines = []
        for line in text.split("\n"):
            normalised = re.sub(r"\s+", " ", line).strip()
            if normalised not in repeating:
                cleaned_lines.append(line)
        text = "\n".join(cleaned_lines)

    # 4. Remove standalone page numbers (lines that are just a number)
    text = _STANDALONE_PAGE_NUM_RE.sub("", text)

    # 5. Collapse excessive blank lines (3+ → 2)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ── Smart Chunking ───────────────────────────────────────────────────────────

def chunk_text(
    text: str,
    chunk_size: int = 8000,
    overlap_words: int = 15,
) -> List[str]:
    """Split *text* into chunks at paragraph/sentence boundaries.

    Inspired by the llm_aided_ocr project's chunking logic.
    Each chunk is at most *chunk_size* characters.  Consecutive chunks share
    *overlap_words* trailing words from the previous chunk for context continuity.
    """
    paragraphs = re.split(r"\n\s*\n", text)
    chunks: List[str] = []
    current_chunk: List[str] = []
    current_length = 0

    for paragraph in paragraphs:
        para_len = len(paragraph)
        if current_length + para_len <= chunk_size:
            current_chunk.append(paragraph)
            current_length += para_len
        else:
            # Flush current chunk
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
            # If the paragraph itself is bigger than chunk_size, split by sentence
            if para_len > chunk_size:
                sentences = re.split(r"(?<=[.!?])\s+", paragraph)
                current_chunk = []
                current_length = 0
                for sentence in sentences:
                    s_len = len(sentence)
                    if current_length + s_len <= chunk_size:
                        current_chunk.append(sentence)
                        current_length += s_len
                    else:
                        if current_chunk:
                            chunks.append(" ".join(current_chunk))
                        current_chunk = [sentence]
                        current_length = s_len
            else:
                current_chunk = [paragraph]
                current_length = para_len

    # Flush remaining
    if current_chunk:
        chunks.append("\n\n".join(current_chunk) if len(current_chunk) > 1 else current_chunk[0])

    # Add overlap between chunks for context continuity
    for i in range(1, len(chunks)):
        overlap_text = chunks[i - 1].split()[-overlap_words:]
        chunks[i] = " ".join(overlap_text) + " " + chunks[i]

    return chunks


# ── Public API ───────────────────────────────────────────────────────────────

def clean_markdown(
    md_text: str,
    max_words_before_chunking: int = 10_000,
    chunk_size: int = 8000,
) -> str:
    """Full cleaning pipeline.  Returns the cleaned text (single string)."""
    cleaned = suppress_headers_footers(md_text)
    word_count = len(cleaned.split())
    if word_count > max_words_before_chunking:
        chunks = chunk_text(cleaned, chunk_size=chunk_size)
        print(f"  ℹ️  Document chunked into {len(chunks)} pieces ({word_count} words)")
        # For extraction we rejoin; the extractor can optionally re-chunk if needed
        cleaned = "\n\n---CHUNK_BREAK---\n\n".join(chunks)
    return cleaned


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Clean OCR Markdown: remove headers/footers and optionally chunk."
    )
    parser.add_argument("-i", "--input", required=True, help="Input markdown file")
    parser.add_argument("-o", "--output", required=True, help="Output cleaned markdown file")
    parser.add_argument(
        "--chunk-size", type=int, default=8000,
        help="Max characters per chunk (default: 8000)"
    )
    args = parser.parse_args()

    print(f"Reading: {args.input}")
    with open(args.input, "r", encoding="utf-8") as f:
        raw = f.read()

    print(f"  Raw size: {len(raw):,} chars, {len(raw.split()):,} words")
    cleaned = clean_markdown(raw, chunk_size=args.chunk_size)
    print(f"  Cleaned size: {len(cleaned):,} chars, {len(cleaned.split()):,} words")

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"✅ Cleaned markdown saved to '{args.output}'")


if __name__ == "__main__":
    main()
