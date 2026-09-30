# ADR 0001: Use an API-first architecture

## Status
Accepted

## Context
The portfolio should demonstrate a production-oriented enterprise AI solution rather than a notebook-only prototype.

## Decision
Use FastAPI as the external application boundary and keep business logic separable from the API layer as the system grows.

## Consequences
- Easier integration testing and future containerization.
- Clear interface for agent/RAG components.
- Slightly more setup than a notebook or single script.
