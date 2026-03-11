# Private Assistant (Week 1 Progress)

这是你当前已经跑通的最小 RAG 系统（本地文档版）：

- 文档读取：TXT / MD / PDF / DOCX
- 文本切块：chunk + overlap
- 向量化：本地 Ollama embedding（`nomic-embed-text`）
- 向量库：Chroma 本地持久化
- 检索问答：Top-K 检索 + 本地 Ollama 回答（`llama3`）
- 引用来源：返回 `chunk_id/title/source_path/distance`

---

## 1. 当前目录结构（核心）

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

## 2. 环境准备

```bash
cd /Users/hailiu/Desktop/private_assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install chromadb requests
```

---

## 3. 本地模型准备（Ollama）

```bash
brew install ollama
ollama serve
ollama pull nomic-embed-text
ollama pull llama3
```

> `nomic-embed-text` 用于 embedding，`llama3` 用于回答生成。

---

## 4. 运行步骤

### Step A: 文档解析自测

```bash
cd /Users/hailiu/Desktop/private_assistant
source .venv/bin/activate
PYTHONPATH=. python scripts/test_ingest.py
```

### Step B: 建立/重建索引

```bash
cd /Users/hailiu/Desktop/private_assistant
source .venv/bin/activate
rm -rf data/chroma
PYTHONPATH=. python scripts/test_index.py
```

### Step C: 交互式对话（可自由输入问题）

```bash
cd /Users/hailiu/Desktop/private_assistant
source .venv/bin/activate
PYTHONPATH=. python scripts/test_query.py
```

输入 `exit` / `quit` / `q` 退出。

---

## 5. 当前问答输出格式

系统会返回：

- `answer`: 回答内容
- `sources`: 命中来源列表
  - `chunk_id`
  - `title`
  - `source_path`
  - `distance`

这保证回答可追溯（citation）。

---

## 6. 常见问题

### Q1. `No module named 'app'`
在项目根目录运行，并带上：

```bash
PYTHONPATH=. python scripts/test_xxx.py
```

### Q2. `Collection expecting embedding with dimension ...`
索引和查询使用了不同 embedding 模型/维度。处理方式：

1. 保证 `test_index.py` 和 `test_query.py` 都使用同一个 `get_embedding`
2. 删除旧索引后重建：`rm -rf data/chroma && python scripts/test_index.py`

### Q3. 文档变了要不要重建？
当前版本建议重跑索引（至少对变更文档重建）。

---

## 7. Week 1 已完成项（文档主链路）

- [x] 初始化项目骨架
- [x] 文档读取（PDF/DOCX/TXT/MD）
- [x] chunk + metadata
- [x] embedding + 向量入库
- [x] 基础检索 + 问答
- [x] citation 输出

下一个阶段：邮件接入（只读最近 90 天）+ 增量更新。

---

## 8. 四周计划（保留原始规划）

> Start date: 2026-03-10  
> Duration: 4 weeks (30 days)  
> Goal: 做出一个可用、可评估、可持续迭代的私人 AI 助理系统，不只是 demo。

### Week 1（Day 1-7）— 打地基：数据接入 + 可查询
**交付物：能查到文档和邮件，返回带来源的答案**

- [x] 初始化 repo（目录结构、requirements、env 示例）
- [x] 文档解析模块：PDF/DOCX/TXT/MD
- [ ] 邮件接入模块：先只读抓取最近 90 天
- [x] chunk + embedding + 向量库入库
- [x] 基础检索 + 问答（RAG v1）
- [x] 返回 citation（文件名/路径/chunk 距离）
- [x] 写 `ARCHITECTURE.md`（最小版）

**验收标准（Week 1）**
- [ ] 随机 20 个问题中，>=12 个回答可用且有来源
- [x] 新增 1 个文件后可手动触发索引并被检索

### Week 2（Day 8-14）— 增量更新 + 自动累计知识
**交付物：系统可持续更新，不是一次性导入**

- [ ] 文件增量检测（mtime/hash）
- [ ] 邮件增量拉取（按 UID / timestamp）
- [ ] 每日知识汇总任务（新增内容 -> summary cards）
- [ ] 记忆层设计：`raw_chunks` / `summaries` / `entities/topics`
- [ ] 去重策略（内容 hash + 语义相似去重）
- [ ] 失败重试 + 死信记录（最小版）

### Week 3（Day 15-21）— 质量评测 + Prompt/检索优化
**交付物：可量化改进，不靠“感觉好用”**

- [ ] 建立 50-100 条私有评测问答集
- [ ] 指标：correctness / citation precision / hallucination / latency
- [ ] 2 轮优化实验（chunk、top-k/rerank、prompt）
- [ ] 输出 `EVAL_REPORT.md`（before vs after）

### Week 4（Day 22-30）— 工程化收尾 + 可演示版本
**交付物：能展示给面试官的工程项目**

- [ ] FastAPI 服务化（/ask /ingest /health）
- [ ] Docker 化，一条命令启动
- [ ] 权限与隐私保护（本地优先、敏感字段脱敏）
- [ ] 日志与成本追踪
- [ ] README 完整化 + demo（可选）+ 面试讲稿

---

## 9. 每周执行节奏（原计划）

### 每周
- [ ] 周一：定范围 + 风险
- [ ] 周三：中期自测 + 砍 scope
- [ ] 周五：验收 + 写周报
- [ ] 周末：补文档 + 清理技术债

### 每天（60-120 分钟）
- [ ] 10 分钟：看昨天失败日志
- [ ] 60-90 分钟：实现 1 个可验收小任务
- [ ] 10 分钟：更新 TODO 勾选
- [ ] 10 分钟：记录 learnings 到 `journal/`
