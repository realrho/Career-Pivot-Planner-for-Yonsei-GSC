# Enterprise AI Knowledge & Risk Copilot

Solution Architect learning: **8 weeks study + 2 weeks MVP integration**, based on Michael Albada's **『AI 에이전트 엔지니어링』 (Hanbit Media)**, all 13 chapters. Updated with 10 approved Korean YouTube learning groups on 2026-10-06.

**Current implementation:** FastAPI intake/lookup scaffold with in-memory state. Actual model/retrieval/persistent DB/authorization/deployment remain build tasks. Curriculum publication does not imply implementation or learning completion.

## Start here

- [10-week book → video → hands-on roadmap](docs/curriculum/README.md)
- [Approved Korean videos: selected lessons and follow-up practice](docs/video-resources.md)
- [13-chapter contents](docs/book-toc.md)
- [SA gaps and stack choices](docs/book-gap-map.md)
- [English/Korean acronyms and concepts](docs/glossary-ko-en.md)
- [Study method and environments](docs/getting-started-ko.md)
- [MVP scope and architecture contracts](docs/project-blueprint.md)
- [Notion learning hub](https://app.notion.com/p/3ebc6f4a2c7e81dca9d6f2cf630b9602)
- [Jira epic SCRUM-5](https://realrho-1790798942092.atlassian.net/browse/SCRUM-5)

## Schedule and learning scope

2026-10-02–2026-12-10 (Asia/Seoul),22h/week. Existing dates and progress are preserved. Python/HTTP/SQL foundations are excluded; API contracts,input validation,transactions and async processing are practiced in the project. Docker and local Kubernetes deployment/rollback are required learning labs. Production HA/cloud deployment are optional.

| Week | Book / focus | Selected video groups | Course |
|---|---|---|---|
| W1 | 1·2·3장 · 에이전트 설계·UX와 API 계약·입력 검증 | 1·4 | [W1](docs/curriculum/week-01.md) |
| W2 | 6장 · 지식·메모리·RAG와 정책·권한 필터 | Practice / integration | [W2](docs/curriculum/week-02.md) |
| W3 | 9장 · 평가 세트·근거 검증·부하 시험 | 9·5 | [W3](docs/curriculum/week-03.md) |
| W4 | 4·5장 · 도구·오케스트레이션·비동기 처리 | 3 | [W4](docs/curriculum/week-04.md) |
| W5 | 8·12장 · 멀티 에이전트·영속 상태·트랜잭션·보안 | 2·6 | [W5](docs/curriculum/week-05.md) |
| W6 | 7·11장 · 학습·개선 루프·실험·비용·인프라 코드 | 8·10 | [W6](docs/curriculum/week-06.md) |
| W7 | 10장 · 관측·Docker·Kubernetes·CI/CD·복구 | 4·5·7 | [W7](docs/curriculum/week-07.md) |
| W8 | 13장 · 인간 협업·거버넌스·고객 제안·제작 준비 | 10 | [W8](docs/curriculum/week-08.md) |
| W9 | MVP · MVP 통합 — 근거 응답·영속 상태·권한 있는 검토 | Practice / integration | [W9](docs/curriculum/week-09.md) |
| W10 | MVP · MVP 검증 — 최종 평가·복구·포트폴리오 시연 | Practice / integration | [W10](docs/curriculum/week-10.md) |

Read6h + book-concept practice6h + selected video/SA practice8h + explanation/evidence review2h. Video allocation totals12.5h within the176h study budget. Each weekly document specifies exact URLs,when to watch,selected lessons and immediate practice. W8 readiness is required before the44-hour build estimate applies.

## Run the current API scaffold


Python 3.11+ (3.12 learning baseline). From the repository root in PowerShell:

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install 'fastapi>=0.115' 'uvicorn[standard]>=0.30' 'pydantic>=2.0' 'pytest>=8.0' 'httpx>=0.27'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
~~~

Open http://127.0.0.1:8000/docs. GET /health returns process status. POST /cases/analyze accepts a case and returns HTTP 202 with status received. GET /cases/{case_id} retrieves it while the process remains alive. This is intake, not AI analysis; restarting clears the current in-memory state. Dependency ranges reflect the existing scaffold; W7 must pin the tested runtime and deployment versions.



## Earlier contract lab examples

Existing labs/week-01..08 were created for the previous textbook plan. They remain available as small contract examples and are documented in [labs/README.md](labs/README.md). They are not new-week acceptance evidence.

## MVP target and evidence

Trusted identity/tenant → active-version retrieval → one model → evidence/output gate → answer/abstain/authorized review → PostgreSQL case/review/audit. Use one validated search backend,one bounded workflow and Compose. Complete the local Kubernetes API deployment/rollback learning lab separately and compare execution platforms in an ADR.

Evaluation: dev20 and frozen holdout30,reported separately. Keep raw outputs,configuration,run IDs,versions,latency/cost,failures and limitations. [Blueprint](docs/project-blueprint.md).

## Repository organization

- app/: existing API scaffold
- labs/: earlier small contract examples
- docs/curriculum/week-01..10.md: active weekly study and build materials
- docs/video-resources.md: approved Korean lessons and mapping
- docs/book-toc.md,book-gap-map.md,glossary-ko-en.md: book and SA references
- docs/curriculum/archive-book-v2/: previous16-chapter plan snapshot
- docs/templates/ and docs/evidence/: decision/experiment templates and execution evidence

[Contributing](CONTRIBUTING.md): use codex/wNN-<topic>,link weekly issue/Jira,and complete only with actual acceptance evidence. Earlier v1 materials remain in [archive-v1.md](docs/curriculum/archive-v1.md).
