from typing import List, Dict
import chromadb


class LocalVectorStore:
    def __init__(self, persist_dir: str = "./data/chroma", collection_name: str = "docs"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def upsert_chunks(self, chunks: List[Dict], embeddings: List[List[float]]) -> None:
        ids = [c["chunk_id"] for c in chunks]
        docs = [c["content"] for c in chunks]
        metas = [
            {
                "source_path": c.get("source_path", ""),
                "file_type": c.get("file_type", ""),
                "title": c.get("title", ""),
                "loaded_at": c.get("loaded_at", ""),
            }
            for c in chunks
        ]
        self.collection.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=embeddings)

    def query(self, query_embedding: List[float], top_k: int = 3) -> List[Dict]:
        res = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        ids = res.get("ids", [[]])[0]
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        dists = res.get("distances", [[]])[0]

        hits = []
        for i in range(len(ids)):
            hits.append(
                {
                    "chunk_id": ids[i],
                    "content": docs[i],
                    "metadata": metas[i] if i < len(metas) else {},
                    "distance": dists[i] if i < len(dists) else None,
                }
            )
        return hits

    def count(self) -> int:
        return self.collection.count()
