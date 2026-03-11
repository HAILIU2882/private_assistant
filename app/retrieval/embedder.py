import requests
from typing import List
import random


def get_embedding(text: str, model: str = "nomic-embed-text") -> List[float]:
    text = (text or "").strip()
    if not text:
        return [0.0] * 768  # 空文本兜底，维度按模型可调整

    resp = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": model, "prompt": text},
        timeout=120,
    )
    resp.raise_for_status()

    data = resp.json()
    emb = data.get("embedding", [])
    if not emb:
        raise ValueError("Empty embedding returned from Ollama")
    return emb


def mock_get_embedding(text: str, dim: int = 256) -> List[float]:
    seed = hash(text) & 0xFFFFFFFF
    rng = random.Random(seed)
    return [rng.uniform(-1, 1) for _ in range(dim)]
