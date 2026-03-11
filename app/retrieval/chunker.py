from typing import List, Dict
import hashlib

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be < chunk_size")

    text = (text or "").strip()
    if not text:
        return []

    chunks: List[str] = []
    start = 0
    step = chunk_size - overlap

    while start < len(text):
        end = start + chunk_size
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        start += step

    return chunks


def chunk_document(doc: Dict[str, str], chunk_size: int = 800, overlap: int = 120) -> List[Dict[str, str]]:
    raw_text = doc.get("content", "")
    source_path = doc.get("source_path", "unknown")
    pieces = chunk_text(raw_text, chunk_size=chunk_size, overlap=overlap)

    results: List[Dict[str, str]] = []
    for i, piece in enumerate(pieces, start=1):
        raw_id = f"{source_path}|{i}|{piece[:80]}"
        chunk_hash = hashlib.sha1(raw_id.encode("utf-8")).hexdigest()[:16]

        results.append(
            {
                "chunk_id": f"chunk-{chunk_hash}",
                "content": piece,
                "source_path": doc.get("source_path", ""),
                "file_type": doc.get("file_type", ""),
                "title": doc.get("title", ""),
                "loaded_at": doc.get("loaded_at", ""),
            }
        )

    return results
