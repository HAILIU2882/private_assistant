from typing import List, Dict
import requests


def build_context(hits: List[Dict]) -> str:
    blocks = []
    for i, h in enumerate(hits, start=1):
        meta = h.get("metadata", {})
        title = meta.get("title", "unknown")
        source = meta.get("source_path", "")
        content = h.get("content", "")
        blocks.append(f"[Source {i}] title={title} path={source}\n{content}")
    return "\n\n".join(blocks)


def answer_with_context(question: str, context: str, model: str = "llama3") -> str:
    prompt = (
        "Answer ONLY from the context. If insufficient, say you don't know.\n\n"
        f"Question:\n{question}\n\nContext:\n{context}"
    )

    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json().get("response", "")
