# Architecture

## Version 0 — Week 1

```text
Client
  |
FastAPI
  |
Application Service
  |
Future components:
  +-- LangGraph Agent
  +-- Milvus RAG
  +-- PostgreSQL
  +-- Redis Cache
  +-- LLM API / Local Model
```

## Architecture decisions
- FastAPI is the API boundary for the prototype.
- RAG, agent orchestration, evaluation, and infrastructure are intentionally added incrementally so each architectural decision can be measured.
- Public or synthetic data only.
