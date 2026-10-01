# Enterprise AI Knowledge & Risk Copilot

Book-first Solution Architect learning: **8 weeks of study + 2 weeks of MVP integration (10 weeks total)**, based on 허정준's 『LLM을 활용한 실전 AI 애플리케이션 개발』.

**Current implementation:** FastAPI intake/lookup scaffold with in-memory state and four baseline tests. Actual AI analysis, retrieval, persistent DB, authorization/review and deployment remain planned. The new eight standard-library labs demonstrate small contracts; they do not implement the full service.

## Start here

- [10-week Korean roadmap and weekly textbooks](docs/curriculum/README.md)
- [Full user-supplied book contents](docs/book-toc.md)
- [Book coverage and SA supplements](docs/book-gap-map.md)
- [107 English/Korean technical terms](docs/glossary-ko-en.md)
- [Study method and separate environments](docs/getting-started-ko.md)
- [Two-week MVP scope and architecture contracts](docs/project-blueprint.md)
- [Notion learning hub](https://app.notion.com/p/3ebc6f4a2c7e81dca9d6f2cf630b9602)
- [Jira 10-week epic](https://realrho-1790798942092.atlassian.net/browse/SCRUM-5)

## Schedule

Planning baseline: October2–December10,2026 (Asia/Seoul),22hours/week. The confirmed duration is8+2weeks; dates and hours remain planning assumptions.

| Week | Book / focus | Course | Tracking |
|---|---|---|---|
| W1 | 1·2·3장 · LLM 기초를 이해하고 Python·Git·API 계약 세우기 | [W1](docs/curriculum/week-01.md) | [#1](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/1) · [SCRUM-6](https://realrho-1790798942092.atlassian.net/browse/SCRUM-6) |
| W2 | 4·5·6장 · 학습 원리·GPU 효율과 SQL·평가 데이터 설계 | [W2](docs/curriculum/week-02.md) | [#2](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/2) · [SCRUM-7](https://realrho-1790798942092.atlassian.net/browse/SCRUM-7) |
| W3 | 7·8장 · 추론·서빙과 네트워크·타임아웃·비용 계산 | [W3](docs/curriculum/week-03.md) | [#3](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/3) · [SCRUM-8](https://realrho-1790798942092.atlassian.net/browse/SCRUM-8) |
| W4 | 9·10장 · RAG·하이브리드 검색과 근거·평가 계약 | [W4](docs/curriculum/week-04.md) | [#4](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/4) · [SCRUM-9](https://realrho-1790798942092.atlassian.net/browse/SCRUM-9) |
| W5 | 11·12장 · 검색 고도화·벡터 DB와 영속성·트랜잭션 | [W5](docs/curriculum/week-05.md) | [#5](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/5) · [SCRUM-10](https://realrho-1790798942092.atlassian.net/browse/SCRUM-10) |
| W6 | 13장 · LLMOps·평가와 보안·사람 검토 경계 | [W6](docs/curriculum/week-06.md) | [#6](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/6) · [SCRUM-11](https://realrho-1790798942092.atlassian.net/browse/SCRUM-11) |
| W7 | 14·15장 · 멀티모달·에이전트와 배포·관측·복구 | [W7](docs/curriculum/week-07.md) | [#7](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/7) · [SCRUM-12](https://realrho-1790798942092.atlassian.net/browse/SCRUM-12) |
| W8 | 16장 · 새 아키텍처 이해·SA 설계 리뷰·제작 준비 동결 | [W8](docs/curriculum/week-08.md) | [#8](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/8) · [SCRUM-13](https://realrho-1790798942092.atlassian.net/browse/SCRUM-13) |
| W9 | MVP · MVP 통합 — 근거 응답·영속 상태·권한 있는 검토 | [W9](docs/curriculum/week-09.md) | [#9](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/9) · [SCRUM-47](https://realrho-1790798942092.atlassian.net/browse/SCRUM-47) |
| W10 | MVP · MVP 검증 — 최종 평가·복구·포트폴리오 시연 | [W10](docs/curriculum/week-10.md) | [#10](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/10) · [SCRUM-48](https://realrho-1790798942092.atlassian.net/browse/SCRUM-48) |

W1–W8: read all16chapters, complete representative book labs and32original SA supplements. GPU training, full multimodal generation and additional frameworks are optional. W9–W10: integrate prepared API/retrieval/DB/security/deployment/evaluation assets into a text-only synthetic-policy MVP. Six W8 readiness gates must pass before the44-hour integration estimate is used.

## Run the current API scaffold


Python 3.11+ (3.12 learning baseline). From the repository root in PowerShell:

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install 'fastapi>=0.115' 'uvicorn[standard]>=0.30' 'pydantic>=2.0' 'pytest>=8.0' 'httpx>=0.27'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
~~~

Open http://127.0.0.1:8000/docs. GET /health returns process status. POST /cases/analyze accepts a case and returns HTTP 202 with status received. GET /cases/{case_id} retrieves it while the process remains alive. This is intake, not AI analysis; restarting clears the current in-memory state. Dependency ranges reflect the existing scaffold; W7 must pin the tested runtime and deployment versions.


## Run the new contract labs

```powershell
python labs/week-01/contract_demo.py
```

W1–W8 have separate standard-library CPU exercises. Their file docstrings and weekly textbook explain scope, failure cases and complexity. No real model/GPU/cloud run is implied.

## MVP target and evidence

Trusted identity/tenant → active-version retrieval → one model → structured evidence/output gate → answer/abstain/authorized review → PostgreSQL case/review/audit. Use one validated vector backend, one bounded workflow and Compose. Redis, new GPU training, multi-agent/multimodal work, multiple providers and Kubernetes HA are extensions.

Evaluation uses20development questions and30frozen holdout questions, reported separately. Preserve raw outputs, configuration, run IDs, versions, measured latency/cost, failures and limitations. A target is not a measured result. Local demo identity is not internet authentication. [Blueprint](docs/project-blueprint.md).

## Repository organization

```text
app/                       Existing API scaffold
labs/week-01..08/           Small executable contract exercises
docs/curriculum/week-01..10.md  Weekly study and build materials
docs/book-toc.md            Supplied book contents
docs/book-gap-map.md        Coverage and SA supplements
docs/glossary-ko-en.md      English/Korean term dictionary
docs/project-blueprint.md  MVP scope, architecture and contracts
docs/templates/            ADR, experiment and evidence templates
docs/evidence/             Actual preparation/validation records
```

Prior materials are preserved in [Git history/Notion archive](docs/curriculum/archive-v1.md). [Contributing](CONTRIBUTING.md): use codex/wNN-<topic>, link the weekly issue/Jira key, and mark complete only with real acceptance evidence.
