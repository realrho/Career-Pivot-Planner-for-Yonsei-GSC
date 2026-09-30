# Enterprise AI Knowledge & Risk Copilot

8-week Solution Architect transition portfolio project.

## Goal
Design, implement, evaluate, and productionize one enterprise AI solution that demonstrates end-to-end Solution Architect capability:

customer problem → requirements → architecture → prototype → evaluation/guardrails → performance/cost trade-offs → deployment → demo.

## Constraints
- Use only public or synthetic data.
- Do not use company-internal policies, screenshots, metrics, or confidential datasets.
- Every week must leave evidence: code, tests, architecture decisions, evaluation results, or demo material.

## 8-Week Roadmap
| Week | Focus | Jira |
|---|---|---|
| W1 | Python/FastAPI + Requirements + Architecture v0 | SCRUM-6 |
| W2 | RAG + Milvus | SCRUM-7 |
| W3 | Advanced RAG + Retrieval Evaluation | SCRUM-8 |
| W4 | LangGraph Agent + Tool Calling | SCRUM-9 |
| W5 | HITL + Guardrails + Evaluation | SCRUM-10 |
| W6 | Model / Latency / Cost Benchmark | SCRUM-11 |
| W7 | Docker + Productionization + Kubernetes Basics | SCRUM-12 |
| W8 | Portfolio Packaging + Demo + Interview Prep | SCRUM-13 |

## Target Architecture

```text
Client / Demo UI
      |
   FastAPI
      |
 LangGraph Agent
 ├─ Request Router
 ├─ RAG Retriever
 ├─ Case Analyzer
 ├─ Guardrails
 ├─ Confidence Gate
 └─ Human Review
      |
      ├─ Milvus
      ├─ PostgreSQL
      ├─ Redis
      └─ LLM API / optional local model
```

## Repository Structure

```text
app/
  api/
  agents/
  retrieval/
  guardrails/
  evaluation/
data/
tests/
deployment/
  docker/
  kubernetes/
docs/
  requirements.md
  architecture.md
  evaluation.md
  benchmark.md
  guardrails.md
  adr/
```

## Definition of Portfolio Done
- Working AI agent
- Architecture diagram
- Customer requirements document
- Evaluation report
- Model/cost benchmark
- Guardrail & failure analysis
- 5-minute English demo
