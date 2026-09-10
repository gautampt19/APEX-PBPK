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


# ── Table Region Protection ──────────────────────────────────────────────────
# Sentinel used to mark lines that must survive header/footer stripping.
# Protects: table rows, the caption line directly above, and up to 3 footnote
# lines below each table (where units and statistical notes typically live).
_TABLE_SENTINEL = "\x00TABLE\x00"
_TABLE_ROW_RE = re.compile(r"^\s*\|")


# Footnote markers: lines starting with superscript letters, *, †, a–z, numbers
# followed by a space/text — typical table footnote patterns in papers.
_FOOTNOTE_RE = re.compile(
    r"^\s*(?:[a-z]|\d|\*|†|‡|§|\^[a-z0-9]+)\s+\S",  # e.g. "a Values", "* p < 0.05"
    re.IGNORECASE,
)
# "Table X." or "Figure X." captions
_CAPTION_RE = re.compile(r"^\s*(Table|Figure|Fig\.?)\s+[\dIVX]+", re.IGNORECASE)


def protect_table_regions(text: str) -> str:
    """Mark table rows, their captions (1 line above) and genuine footnotes
    (up to 3 lines below matching _FOOTNOTE_RE) with a sentinel prefix, so
    suppress_headers_footers() never removes them.

    Only *footnote-looking* lines are sentinelled after the table, preventing
    repeating journal headers that happen to follow a table from being shielded.
    """
    lines = text.split("\n")
    protected = list(lines)
    n = len(lines)
    in_table = False

    for i, line in enumerate(lines):
        is_row = bool(_TABLE_ROW_RE.match(line))
        if is_row:
            protected[i] = _TABLE_SENTINEL + lines[i]
            # Protect the line immediately above if it looks like a table caption
            if i > 0 and not protected[i - 1].startswith(_TABLE_SENTINEL):
                prev = lines[i - 1].strip()
                if _CAPTION_RE.match(prev) or prev.lower().startswith("table"):
                    protected[i - 1] = _TABLE_SENTINEL + lines[i - 1]
            in_table = True
        elif in_table and not is_row:
            in_table = False
            # Protect up to 3 lines after table end, but ONLY if they look like
            # footnotes (superscript markers, *, †) or are blank spacer lines.
            for j in range(i, min(i + 3, n)):
                candidate = lines[j].strip()
                is_footnote = bool(_FOOTNOTE_RE.match(candidate))
                is_blank = (candidate == "")
                if (is_footnote or is_blank) and not protected[j].startswith(_TABLE_SENTINEL):
                    protected[j] = _TABLE_SENTINEL + lines[j]
                elif not is_blank and not is_footnote:
                    break  # stop at first non-footnote, non-blank line

    return "\n".join(protected)


def unprotect_table_regions(text: str) -> str:
    """Remove the sentinel prefix after cleaning is complete."""
    return text.replace(_TABLE_SENTINEL, "")


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
    """Remove repeating headers, footers, page markers, and publisher stamps.

    NOTE: Lines prefixed with _TABLE_SENTINEL are always preserved — call
    protect_table_regions() before this function and unprotect_table_regions()
    afterwards to shield table captions and footnotes.
    """
    # 1. Remove <PAGE> markers
    text = _PAGE_MARKER_RE.sub("", text)

    # 2. Remove "Page X of Y ..." lines
    text = _PAGE_X_OF_Y_RE.sub("", text)

    # 3. Detect repeating lines across ALL lines (including sentinelled).
    #    Strip only non-sentinelled repeats; sentinelled table lines always survive.
    repeating = _detect_repeating_lines(
        "\n".join(
            line.replace(_TABLE_SENTINEL, "")  # strip sentinel for counting
            for line in text.split("\n")
        )
    )
    if repeating:
        cleaned_lines = []
        for line in text.split("\n"):
            if line.startswith(_TABLE_SENTINEL):
                cleaned_lines.append(line)  # always keep (table row/caption/footnote)
            else:
                normalised = re.sub(r"\s+", " ", line).strip()
                if normalised not in repeating:
                    cleaned_lines.append(line)
        text = "\n".join(cleaned_lines)

    # 4. Remove standalone page numbers — skip sentinelled lines
    lines = text.split("\n")
    text = "\n".join(
        line for line in lines
        if line.startswith(_TABLE_SENTINEL) or not _STANDALONE_PAGE_NUM_RE.match(line)
    )

    # 5. Collapse excessive blank lines (3+ → 2)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ── Smart Chunking ───────────────────────────────────────────────────────────


def remove_references_section(text: str) -> str:
    """
    Finds the References section and removes it, preserving anything after it
    (like Appendices, Supplementary Data, etc.) that starts with a heading.
    """
    import re
    # Often the reference heading is # References or ## References. Sometimes it has no #.
    # The OCR from MinerU might just output "References" on a line by itself.
    ref_heading_re = re.compile(r"^(?:#{1,4}\s*)?(?:References?|Bibliography)\s*$", re.IGNORECASE | re.MULTILINE)
    
    match = ref_heading_re.search(text)
    if not match:
        return text
    
    start_idx = match.start()
    
    # Look for the NEXT heading to determine where references end
    next_heading_re = re.compile(r"^#{1,4}\s+(?!References?|Bibliography)", re.IGNORECASE | re.MULTILINE)
    next_match = next_heading_re.search(text, match.end())
    
    if next_match:
        end_idx = next_match.start()
    else:
        end_idx = len(text)
        
    # Replace the reference block with a placeholder
    before = text[:start_idx]
    after = text[end_idx:]
    
    return before + "\n\n> [!NOTE]\n> References section removed for context efficiency.\n\n" + after


def chunk_text(
    text: str,
    chunk_size: int = 8000,
    overlap_words: int = 15,
) -> List[str]:
    """Split *text* into chunks at paragraph boundaries.
    Crucially, this ensures markdown tables (lines starting with '|') are NEVER split, 
    even if they exceed chunk_size, because splitting a table separates the rows 
    from the headers and breaks LLM extraction.
    """
    lines = text.split('\n')
    blocks = []
    current_block = []
    
    for line in lines:
        is_table_row = bool(re.match(r"^\s*\|", line))
        # We consider a block boundary if it's a blank line AND the previous line wasn't a table row
        # (MinerU sometimes has blank lines inside or right after tables)
        if not line.strip() and not (current_block and bool(re.match(r"^\s*\|", current_block[-1]))):
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        else:
            current_block.append(line)
            
    if current_block:
        blocks.append("\n".join(current_block))
        
    chunks = []
    current_chunk = []
    current_length = 0
    
    for block in blocks:
        block_len = len(block)
        if current_length + block_len <= chunk_size:
            current_chunk.append(block)
            current_length += block_len
        else:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
            
            if block_len > chunk_size:
                # If a single block (like a huge table) is > chunk_size, we just keep it as an oversized chunk!
                # Splitting it by sentence would destroy the table formatting.
                chunks.append(block)
                current_chunk = []
                current_length = 0
            else:
                current_chunk = [block]
                current_length = block_len
                
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
        
    # Add overlap between chunks for context continuity
    for i in range(1, len(chunks)):
        overlap_text = chunks[i - 1].split()[-overlap_words:]
        chunks[i] = " ".join(overlap_text) + "\n\n" + chunks[i]

    return chunks


# ── Public API ───────────────────────────────────────────────────────────────

def clean_markdown(
    md_text: str,
    max_words_before_chunking: int = 10_000,
    chunk_size: int = 8000,
) -> str:
    """Full cleaning pipeline.  Returns the cleaned text (single string)."""
    # Protect table regions before stripping, restore afterwards
    # Remove references before any protection/stripping
    no_refs   = remove_references_section(md_text)
    protected = protect_table_regions(no_refs)
    stripped  = suppress_headers_footers(protected)
    cleaned   = unprotect_table_regions(stripped)

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
