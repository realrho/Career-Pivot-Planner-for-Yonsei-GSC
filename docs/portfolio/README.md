# Portfolio packaging checklist (W8 planned delivery)

This file is a checklist, not a completed slide deck or recorded demo.

- [ ] Runnable bounded copilot: normal, insufficient-evidence and authorized-review paths.
- [ ] Customer requirements and API/state contracts.
- [ ] Architecture with ADRs and revisit conditions.
- [ ] Synthetic dev/holdout evaluation and failure analysis.
- [ ] Real model latency/quality/usage/cost comparison.
- [ ] Guardrail, threat model and operations runbook.
- [ ] Measured five-minute English demo and interview answers.

## Demo timing

0:00–0:40 customer problem; 0:40–1:20 architecture; 1:20–2:20 normal answer and evidence; 2:20–3:00 abstention; 3:00–4:00 review and authorized resume; 4:00–4:40 measured quality/latency/cost; 4:40–5:00 limits and next step.

## Ten-slide narrative

Problem → FR/NFR → architecture → retrieval/version/access → bounded tools → HITL/guardrails → eval/failures → latency/cost → deployment/runbook → recommendation/limits.

## Interview prompts

Why RAG? Why bounded agent? Where are tenant permissions enforced? What makes a citation valid? How is confidence calibrated? What if Redis/model/DB fails? How does review survive a restart? Why this model? What changes at 10x traffic? What is still unverified?

Answer using requirement, alternatives, decision, actual evidence, limitations and revisit conditions.
