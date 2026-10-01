# Architecture · current and target

Current: client→FastAPI→in-memory intake/lookup. No actual model/retrieval/review/persistent DB execution is implemented in this scaffold.

Target: trusted identity/tenant→bounded workflow→active-version retrieval→one model→output/evidence/risk gate→answer/abstain/review; PostgreSQL stores case/review/audit atomically. Choose one validated vector backend. Compose is the required deployment baseline. Redis/LangGraph/Milvus/AWS/K8s are chosen when justified; every named component is not simultaneously mandatory.

[Full architecture, contracts and trade-offs](project-blueprint.md) · [10-week roadmap](curriculum/README.md)
