# Private Assistant (Week 1 Progress)

This repository contains your current working minimum RAG system (local document version):

- Document ingestion: TXT / MD / PDF / DOCX
- Text chunking: chunk + overlap
- Embeddings: local Ollama embedding model (`nomic-embed-text`)
- Vector store: local persistent Chroma DB
- Retrieval QA: Top-K retrieval + local Ollama generation (`llama3`)
- Citations: returns `chunk_id/title/source_path/distance`

---

## 1) Current Project Structure (Core)

```txt
app/
  ingest/document_loader.py
  retrieval/chunker.py
  retrieval/embedder.py
  retrieval/vector_store.py
  retrieval/rag.py
scripts/
  test_ingest.py
  test_index.py
  test_query.py
data/
  sample.txt / sample.md / sample.pdf / sample.docx
```

---

## 2) Environment Setup

```bash
cd /Users/hailiu/Desktop/private_assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install chromadb requests
```

---

## 3) Local Model Setup (Ollama)

```bash
brew install ollama
ollama serve
ollama pull nomic-embed-text
ollama pull llama3
```

> `nomic-embed-text` is used for embeddings, `llama3` is used for answer generation.

---

## 4) Run Steps

### Step A: Ingestion self-test

```bash
cd /Users/hailiu/Desktop/private_assistant
source .venv/bin/activate
PYTHONPATH=. python scripts/test_ingest.py
```

### Step B: Build / Rebuild index

```bash
cd /Users/hailiu/Desktop/private_assistant
source .venv/bin/activate
rm -rf data/chroma
PYTHONPATH=. python scripts/test_index.py
```

### Step C: Interactive QA (free input)

```bash
cd /Users/hailiu/Desktop/private_assistant
source .venv/bin/activate
PYTHONPATH=. python scripts/test_query.py
```

Type `exit` / `quit` / `q` to quit.

---

## 5) Current QA Output Format

The system returns:

- `answer`: generated answer
- `sources`: matched source list
  - `chunk_id`
  - `title`
  - `source_path`
  - `distance`

This ensures answer traceability (citation).

---

## 6) Common Issues

### Q1. `No module named 'app'`
Run from project root and include:

```bash
PYTHONPATH=. python scripts/test_xxx.py
```

### Q2. `Collection expecting embedding with dimension ...`
Index and query are using different embedding models/dimensions. Fix by:

1. Ensure both `test_index.py` and `test_query.py` use the same `get_embedding`
2. Delete old index and rebuild: `rm -rf data/chroma && python scripts/test_index.py`

### Q3. Should I rebuild if documents changed?
For the current version, yes—re-index after document changes (at least for changed files).

---

## 7) Week 1 Completed Items (Document RAG Pipeline)

- [x] Initialize project skeleton
- [x] Document parsing (PDF/DOCX/TXT/MD)
- [x] Chunking + metadata
- [x] Embedding + vector upsert
- [x] Basic retrieval + QA
- [x] Citation output

Next stage: email ingestion (read-only last 90 days) + incremental updates.

---

## 8) Four-Week Plan (Original Plan Kept)

> Start date: 2026-03-10  
> Duration: 4 weeks (30 days)  
> Goal: Build a usable, measurable, and continuously improvable private AI assistant system (not just a demo).

### Week 1 (Day 1-7) — Foundation: data access + queryability
**Deliverable: searchable docs/emails with source-grounded answers**

- [x] Initialize repo (structure, requirements, env template)
- [x] Document parser module: PDF/DOCX/TXT/MD
- [ ] Email ingestion module: read-only for last 90 days
- [x] Chunk + embedding + vector indexing
- [x] Basic retrieval + QA (RAG v1)
- [x] Citation output (file path/chunk distance)
- [x] `ARCHITECTURE.md` (minimal version)

**Acceptance (Week 1)**
- [ ] >= 12/20 random questions are usable and cited
- [x] New file can be manually indexed and retrieved

### Week 2 (Day 8-14) — Incremental updates + accumulated knowledge
**Deliverable: continuously updating system, not one-shot import**

- [ ] File change detection (mtime/hash)
- [ ] Incremental email fetch (UID/timestamp)
- [ ] Daily knowledge summary job (new content -> summary cards)
- [ ] Memory layer design: `raw_chunks` / `summaries` / `entities/topics`
- [ ] Dedup strategy (content hash + semantic dedup)
- [ ] Retry + dead-letter handling (minimal)

### Week 3 (Day 15-21) — Evaluation + prompt/retrieval optimization
**Deliverable: measurable improvements, not just subjective feel**

- [ ] Build a 50-100 private QA evaluation set
- [ ] Metrics: correctness / citation precision / hallucination / latency
- [ ] Two optimization rounds (chunking, top-k/rerank, prompt)
- [ ] `EVAL_REPORT.md` (before vs after)

### Week 4 (Day 22-30) — Engineering polish + demo-ready version
**Deliverable: interview-ready engineering project**

- [ ] FastAPI service (`/ask`, `/ingest`, `/health`)
- [ ] Dockerized one-command startup
- [ ] Access/privacy controls (local-first, sensitive field masking)
- [ ] Logging and cost tracking
- [ ] Complete README + optional demo + interview story

---

## 9) Weekly Execution Rhythm (Original Plan)

### Every Week
- [ ] Monday: define scope + risks
- [ ] Wednesday: mid-week self-test + cut scope if needed
- [ ] Friday: acceptance + weekly report
- [ ] Weekend: docs update + tech debt cleanup

### Daily (60-120 mins)
- [ ] 10 min: review yesterday's failure logs
- [ ] 60-90 min: deliver one testable task
- [ ] 10 min: update TODO checkboxes
- [ ] 10 min: log learnings to `journal/`
