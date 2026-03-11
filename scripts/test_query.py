from app.retrieval.vector_store import LocalVectorStore
from app.retrieval.embedder import get_embedding
from app.retrieval.rag import build_context, answer_with_context


def ask_once(store: LocalVectorStore, question: str, top_k: int = 3):
    query_vec = get_embedding(question)
    hits = store.query(query_vec, top_k=top_k)
    context = build_context(hits)
    answer = answer_with_context(question, context)

    result = {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "chunk_id": h.get("chunk_id"),
                "title": h.get("metadata", {}).get("title", ""),
                "source_path": h.get("metadata", {}).get("source_path", ""),
                "distance": h.get("distance"),
            }
            for h in hits
        ],
    }
    return result


def main():
    store = LocalVectorStore()
    print("RAG chat ready. Type your question. Type 'exit' to quit.")

    while True:
        question = input("\nYou> ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit", "q"}:
            print("Bye!")
            break

        try:
            result = ask_once(store, question, top_k=3)
            print("\nAssistant>", result["answer"])
            print("Sources:")
            for s in result["sources"]:
                print(f"- {s['title']} | {s['source_path']} | dist={s['distance']}")
        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
