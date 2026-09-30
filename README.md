# Enterprise AI Knowledge & Risk Copilot

An eight-week Solution Architect portfolio: turn customer requirements into a grounded, bounded AI workflow, measure its behavior, and explain the trade-offs.

**Current implementation:** API intake and lookup scaffold with in-memory state. AI analysis, persistent storage, retrieval, agents, review, caching and deployment are planned work. The existing source contains four baseline API tests. Curriculum completion does not imply implementation or production readiness.

## Start here

- [Korean learning guide and environment setup](docs/getting-started-ko.md)
- [Eight-week course: concepts, labs, quizzes and build instructions](docs/curriculum/README.md)
- [Customer scenario, scope and architecture contracts](docs/project-blueprint.md)
- [Notion learning hub](https://app.notion.com/p/3ebc6f4a2c7e81dca9d6f2cf630b9602)
- [Jira execution epic](https://realrho-1790798942092.atlassian.net/browse/SCRUM-5)

## Schedule and delivery gates

October 1–November 25, 2026 (Asia/Seoul). The planning assumption is 22 hours/week, including study, implementation, validation and communication. Four tasks per week are tracked as Jira subtasks SCRUM-14–45; the original weekly stories SCRUM-6–13 and GitHub issues #1–8 remain the primary milestones.

| Week | Study and build | Course | Issue |
|---|---|---|---|
| W1 | Python · Git · HTTP · FastAPI · SQL · Architecture v0 | [W1](docs/curriculum/week-01.md) | [#1](https://github.com/realrho/test/issues/1) |
| W2 | RAG · Embedding · Chunking · Milvus · Metadata · Docker 기초 | [W2](docs/curriculum/week-02.md) | [#2](https://github.com/realrho/test/issues/2) |
| W3 | Hybrid retrieval · RRF · Citation RAG · Abstention · Recall/MRR · 실험 설계 | [W3](docs/curriculum/week-03.md) | [#3](https://github.com/realrho/test/issues/3) |
| W4 | LangGraph · State/Node/Edge · Tool contracts · Retry · Checkpoint · PostgreSQL | [W4](docs/curriculum/week-04.md) | [#4](https://github.com/realrho/test/issues/4) |
| W5 | HITL · Prompt injection · PII · Authorization · Confidence calibration · Evaluation | [W5](docs/curriculum/week-05.md) | [#5](https://github.com/realrho/test/issues/5) |
| W6 | P50/P95 · Token accounting · Benchmark design · Redis · Cache invalidation · Model routing | [W6](docs/curriculum/week-06.md) | [#6](https://github.com/realrho/test/issues/6) |
| W7 | Docker Compose · Networking · Health/Readiness · Observability · CI · AWS 설계 · Kubernetes 기초 | [W7](docs/curriculum/week-07.md) | [#7](https://github.com/realrho/test/issues/7) |
| W8 | Customer narrative · Architecture trade-offs · Evidence audit · Demo · Interview · Internal transfer | [W8](docs/curriculum/week-08.md) | [#8](https://github.com/realrho/test/issues/8) |


## Run the current API scaffold

Python 3.11+ (3.12 learning baseline). From the repository root in PowerShell:

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install 'fastapi>=0.115' 'uvicorn[standard]>=0.30' 'pydantic>=2.0' 'pytest>=8.0' 'httpx>=0.27'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
~~~

Open http://127.0.0.1:8000/docs. GET /health returns process status. POST /cases/analyze accepts a case and returns HTTP 202 with status received. GET /cases/{case_id} retrieves it while the process remains alive. This is intake, not AI analysis; restarting clears the current in-memory state. Dependency ranges reflect the existing scaffold; W7 must pin the tested runtime and deployment versions.

## Target workflow

Synthetic policy/case → trusted tenant scope → version-filtered retrieval → structured answer with evidence → output/risk gate → answer, abstain or authorized human review. The target stores cases, reviews, audit and checkpoints in PostgreSQL, evidence in Milvus, and scoped/versioned cache entries in Redis. [Blueprint and trade-offs](docs/project-blueprint.md).

## Evidence and limitations

Use public or synthetic data only. Keep target values, fictional pricing, fixture results and real measurements distinct. Each claim needs a commit, run ID, configuration, dataset/model/prompt/index version, environment and raw results. Windows Milvus Lite follows the WSL2 Ubuntu path; official deployment requirements apply. Real model evaluation needs provider access and a budget; real cloud/GPU work is optional and must be recorded separately.

## Repository navigation

~~~text
app/                     Existing API scaffold; future modules in weekly build guides
tests/                   Existing baseline API tests
docs/curriculum/         Eight complete Korean course chapters and index
docs/project-blueprint.md Customer scenario, contracts and target architecture
docs/getting-started-ko.md Environment, study cadence and glossary
docs/templates/          ADR, experiment and evidence templates
docs/portfolio/          Portfolio checklist and narrative prompts
docs/evidence/           Actual validation records; not aspirational results
.github/                 Issue and pull request templates
~~~

Future retrieval/agents/guardrails/adapters/evaluation/deployment files are specified in each chapter. Planned paths do not imply implemented components.

## Contributing and delivery

Use codex/wNN-<topic> branches. Reference the weekly GitHub issue and Jira key in each PR. Include expected/actual behavior, relevant validation, evidence links and remaining limitations. See [CONTRIBUTING](CONTRIBUTING.md) and the [PR template](.github/PULL_REQUEST_TEMPLATE.md). Mark a weekly milestone complete only when its Jira acceptance criteria have real evidence.
