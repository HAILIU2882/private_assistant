import os

from dotenv import load_dotenv

from app.ingest.email_loader import load_recent_emails_from_env
from app.retrieval.chunker import chunk_document


def main() -> None:
    load_dotenv()

    required = ["IMAP_HOST", "IMAP_USER", "IMAP_PASSWORD"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        print("[SKIP] Missing IMAP env vars:", ", ".join(missing))
        print("Please set them in .env before running this script.")
        return

    emails = load_recent_emails_from_env()
    print(f"fetched emails: {len(emails)}")

    total_chunks = 0
    for e in emails[:5]:
        chunks = chunk_document(e, chunk_size=300, overlap=50)
        total_chunks += len(chunks)

        print("=" * 60)
        print("title:", e.get("title", ""))
        print("source_path:", e.get("source_path", ""))
        print("date:", e.get("email_date", ""))
        print("preview:", e.get("content", "")[:200])
        if chunks:
            print("first_chunk_id:", chunks[0]["chunk_id"])
            print("first_chunk_preview:", chunks[0]["content"][:160])

    print("total chunks (first 5 emails):", total_chunks)


if __name__ == "__main__":
    main()
