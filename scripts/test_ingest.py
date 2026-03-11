from app.ingest.document_loader import load_document
from app.retrieval.chunker import chunk_document

sample_files = [
    "data/sample.txt",
    "data/sample.md",
    "data/sample.pdf",
    "data/sample.docx",
]

for fp in sample_files:
    try:
        doc = load_document(fp)
        chunks = chunk_document(doc,chunk_size=300,overlap=50)

        result = load_document(fp)
        print("=" * 60)
        print("file_type:", result["file_type"])
        print("title:", result["title"])
        print("preview:", result["content"][:300])

        if chunks:
            print("first_chunk_id", chunks[0]["chunk_id"])
            print("first_chunk_preview",chunks[0]["content"][:200])
    except Exception as e:
        print(f"[ERROR] {fp}: {e}")
