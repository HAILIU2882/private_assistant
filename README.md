# 30-Day AI Engineer Project Plan
## Project 1: 私人 AI 助理（本地文档 + 邮件 + 自动累计知识）

> Start date: 2026-03-10
> Duration: 4 weeks (30 days)
> Goal: 做出一个可用、可评估、可持续迭代的私人 AI 助理系统，不只是 demo。

---

## 1) 项目目标（对齐你转 AI Engineer 的短板）

这个项目要补齐的能力：
- [ ] LLM/RAG 系统设计与实现
- [ ] 数据管道（文档 + 邮件）与增量更新
- [ ] 评测体系（正确率、召回、幻觉率）
- [ ] 服务化部署（API + CLI/Web）
- [ ] 可观测性（日志、成本、延迟）
- [ ] 产品化闭环（反馈 -> 知识更新 -> 质量提升）

---

## 2) MVP 范围（先做小，再做全）

### 必做（MVP）
- [ ] 读取本地文档（PDF/DOCX/TXT/MD）
- [ ] 读取邮件（建议先 Gmail API 或 IMAP 只读）
- [ ] RAG 问答（引用来源）
- [ ] 增量索引（新文件/新邮件自动入库）
- [ ] 简单知识库记忆层（summary + metadata + tags）
- [ ] 最小 UI（CLI 或本地 Web）

### 暂不做（避免失控）
- [ ] 多 agent 复杂编排
- [ ] 语音/多模态
- [ ] 花哨前端

---

## 3) 建议技术栈（够用且工程化）

- Language: Python 3.11+
- LLM: OpenAI / Anthropic（可替换）
- Framework: FastAPI
- Parsing: pypdf / python-docx / unstructured
- Email: IMAPClient 或 Gmail API
- Embedding + Retrieval: pgvector (Postgres) 或 Chroma
- Orchestration: cron + Python jobs
- Eval: 自建评测集 + RAGAS（可选）
- Observability: structured logging + simple metrics dashboard
- Packaging: Docker

---

## 4) 30 天时间规划（按周）

## Week 1（Day 1-7）— 打地基：数据接入 + 可查询
**交付物：能查到文档和邮件，返回带来源的答案**

- [ ] 初始化 repo（目录结构、requirements、env 示例）
- [ ] 文档解析模块：PDF/DOCX/TXT/MD
- [ ] 邮件接入模块：先只读抓取最近 90 天
- [ ] chunk + embedding + 向量库入库
- [ ] 基础检索 + 问答（RAG v1）
- [ ] 返回 citation（文件名/邮件主题/时间）
- [ ] 写 `ARCHITECTURE.md`（一页架构图 + 数据流）

**验收标准（Week 1）**
- [ ] 随机 20 个问题中，>=12 个回答可用且有来源
- [ ] 新增 1 个文件后可手动触发索引并被检索

---

## Week 2（Day 8-14）— 增量更新 + 自动累计知识
**交付物：系统可持续更新，不是一次性导入**

- [ ] 文件增量检测（mtime/hash）
- [ ] 邮件增量拉取（按 UID / timestamp）
- [ ] 每日知识汇总任务（新增内容 -> summary cards）
- [ ] 记忆层设计：
  - [ ] `raw_chunks`
  - [ ] `summaries`
  - [ ] `entities/topics`
- [ ] 去重策略（内容 hash + 语义相似去重）
- [ ] 失败重试 + 死信记录（最小版）

**验收标准（Week 2）**
- [ ] 连续 3 天自动运行无中断
- [ ] 每天生成知识摘要并可检索
- [ ] 重复内容不重复入库（重复率显著下降）

---

## Week 3（Day 15-21）— 质量评测 + Prompt/检索优化
**交付物：可量化改进，不靠“感觉好用”**

- [ ] 建立 50-100 条私有评测问答集
- [ ] 设计指标：
  - [ ] answer correctness
  - [ ] citation precision
  - [ ] hallucination rate
  - [ ] latency p50/p95
- [ ] 做 2 轮优化实验：
  - [ ] chunk size/overlap
  - [ ] top-k + rerank
  - [ ] system prompt 改进
- [ ] 输出 `EVAL_REPORT.md`（before vs after）

**验收标准（Week 3）**
- [ ] 正确率相比 Week 1 提升 >= 20%
- [ ] 幻觉率降低（有明确定义和数据）
- [ ] p95 延迟可接受（你自定义阈值，如 <8s）

---

## Week 4（Day 22-30）— 工程化收尾 + 可演示版本
**交付物：能展示给面试官的工程项目**

- [ ] FastAPI 服务化（/ask /ingest /health）
- [ ] Docker 化，一条命令启动
- [ ] 基础权限与隐私保护（本地优先、敏感字段脱敏）
- [ ] 日志与成本追踪（每次 query token/cost）
- [ ] README 完整化（架构、运行、限制、roadmap）
- [ ] 录制 3-5 分钟 demo（可选）
- [ ] 准备面试讲稿（STAR + 技术权衡）

**验收标准（Week 4）**
- [ ] 新机器上 30 分钟内可跑起来
- [ ] 能稳定回答你日常 10 个高频问题
- [ ] 代码和文档可公开展示（或脱敏后可展示）

---

## 5) 每周固定节奏（执行模板）

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

---

## 6) Repo 结构建议

```txt
ai-eng-30d-private-assistant/
  README.md
  ARCHITECTURE.md
  EVAL_REPORT.md
  .env.example
  app/
    api/
    ingest/
    retrieval/
    memory/
    eval/
  scripts/
  data/               # 本地，不进 git
  tests/
  journal/
    week1.md
    week2.md
    week3.md
    week4.md
```

---

## 7) 面试可复用成果（你最终要拿到的）

- [ ] 一个真实 AI 助理项目（不是教程克隆）
- [ ] 一套评测方法（数据驱动优化）
- [ ] 一份工程文档（架构 + tradeoff）
- [ ] 一段可讲清楚的项目故事：
  - [ ] 为什么这么设计
  - [ ] 如何权衡成本/质量/速度
  - [ ] 怎么做增量更新与可靠性保障

---

## 8) 风险与防跑偏清单

- [ ] 任何新需求先问：是否影响 30 天交付？
- [ ] 每周最多引入 1 个新框架
- [ ] 若连续 2 天卡住，降级为更小 MVP
- [ ] 先可用，再优雅

---

## 9) Day 1 立即行动（今天就能做）

- [ ] 创建 git repo + 初始目录
- [ ] 写 `.env.example`
- [ ] 做文档 ingest（先 PDF）
- [ ] 打通 “提问 -> 检索 -> 回答 + citation” 的最小链路
- [ ] 记录第一个 baseline（正确率/延迟）

---

你可以把这个文件当主 checklist，用 markdown 勾选一路推进。
