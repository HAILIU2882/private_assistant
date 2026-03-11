from app.ingest.document_loader import load_document
from app.retrieval.chunker import chunk_document
from app.retrieval.embedder import get_embedding, mock_get_embedding
from app.retrieval.vector_store import LocalVectorStore

sample_files = [
    "data/sample.txt",
    "data/sample.md",
    "data/sample.pdf",
    "data/sample.docx",
]

all_chunks = []
for fp in sample_files:
    doc = load_document(fp)
    all_chunks.extend(chunk_document(doc, chunk_size=300, overlap=50))

print("total chunks:", len(all_chunks))

embeddings = [get_embedding(c["content"]) for c in all_chunks]
# embeddings = [mock_get_embedding(c["content"]) for c in all_chunks]

store = LocalVectorStore()
store.upsert_chunks(all_chunks, embeddings)

print("indexed count:", store.count())
