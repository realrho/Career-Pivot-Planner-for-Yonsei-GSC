# Customer Requirements

## Customer problem
A global enterprise needs a grounded AI assistant that can search public policy/operating documents, analyze synthetic cases, cite evidence, and escalate uncertain or high-risk cases to a human reviewer.

## Functional requirements
- Ingest public documents.
- Retrieve relevant evidence.
- Return structured decisions with citations.
- Abstain when evidence is insufficient.
- Route low-confidence/high-risk cases to human review.
- Record evaluation and operational traces.

## Non-functional requirements
- API-first service.
- Reproducible local deployment.
- Measurable accuracy, retrieval quality, latency, and cost.
- Safe handling of prompt injection and malformed input.
- No confidential company data.

## Initial targets
These are project targets, not measured results.
- P95 latency target: < 5 seconds for the prototype.
- Evaluation set: at least 50 cases by W3 and 200 cases by W5/W6.
- Every generated decision must include evidence or abstain.
