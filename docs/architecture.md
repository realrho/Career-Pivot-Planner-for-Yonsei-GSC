# Architecture · current and target

Current: client→FastAPI→in-memory intake/lookup. No actual model/retrieval/review/persistent DB execution is implemented in this scaffold.

Target: trusted identity/tenant→bounded workflow→active-version retrieval→one model→output/evidence/risk gate→answer/abstain/review; PostgreSQL stores case/review/audit atomically. Choose one validated vector backend. Compose is the full-stack demo baseline. Docker and a local Kubernetes API Deployment/Service/probe/rollback lab are required learning exercises. Production Kubernetes HA and actual cloud deployment are optional. Redis, a broker or an agent framework is selected when a documented requirement justifies it; not every candidate is mandatory.

[Full architecture, contracts and trade-offs](project-blueprint.md) · [10-week roadmap](curriculum/README.md)
