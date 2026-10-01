# Customer requirements · 10-week plan

Synthetic-policy assistant for grounded answers, explicit abstention and authorized human review. Scope:12–24text documents,2tenants,oneactive policy version,one validated model and vector backend.

Functional requirements: ingest/search with trusted tenant and version conditions; return structured answers with valid citations; abstain when evidence is insufficient; route high-risk cases to review; persist case/review/audit; reject unauthorized or conflicting reviews.

Quality requirements: reproducible Compose,tenant/role isolation,atomic database writes,restart persistence,backup restoration,and measured retrieval/answer quality,latency and cost with traceable versions/raw results.

Evaluation:20development questions plus30frozen holdout questions,reported separately. Larger200+sets are extensions. Freeze quality/latency targets with conditions in W8 and compare actual measurements. Model confidence is not a calibrated approval criterion.

[Full requirements,states and acceptance gates](project-blueprint.md)
