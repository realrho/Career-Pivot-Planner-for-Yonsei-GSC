# 8주 SA 학습·빌드 교재

2026-10-01~2026-11-25 · 주당 22h 가정 · 176h · 32개 개념 강의 / 8개 실습 / 24개 해설 퀴즈 / 32개 빌드 작업.

[시작하기](../getting-started-ko.md) → [프로젝트 설계서](../project-blueprint.md) → 아래 주차 교재.
[Notion 홈](https://app.notion.com/p/3ebc6f4a2c7e81dca9d6f2cf630b9602) · [Jira Epic](https://realrho-1790798942092.atlassian.net/browse/SCRUM-5)

| 주차·기간 | 교재·학습 | 빌드 결과 | 추적 |
|---|---|---|---|
| W1 · 2026-10-01~2026-10-07 | [고객 요구사항을 API 계약으로 바꾸기](week-01.md)<br>Python · Git · HTTP · FastAPI · SQL · Architecture v0 | 고객의 모호한 요청을 요구사항·상태·API 계약으로 표현하고, 기존 API 뼈대를 직접 설명하고 검증한다. | [Jira](https://realrho-1790798942092.atlassian.net/browse/SCRUM-6) · [Issue #1](https://github.com/realrho/test/issues/1) |
| W2 · 2026-10-08~2026-10-14 | [문서를 검색 가능한 근거로 만들기](week-02.md)<br>RAG · Embedding · Chunking · Milvus · Metadata · Docker 기초 | 버전과 접근 범위가 있는 합성 문서를 중복 없이 수집하고, 질문에 맞는 근거를 검색한다. | [Jira](https://realrho-1790798942092.atlassian.net/browse/SCRUM-7) · [Issue #2](https://github.com/realrho/test/issues/2) |
| W3 · 2026-10-15~2026-10-21 | [근거 있는 답변과 평가 기준선 만들기](week-03.md)<br>Hybrid retrieval · RRF · Citation RAG · Abstention · Recall/MRR · 실험 설계 | 검색 실패와 생성 실패를 나눠 측정하고, 출처가 있는 답변 또는 근거 부족을 일관되게 반환한다. | [Jira](https://realrho-1790798942092.atlassian.net/browse/SCRUM-8) · [Issue #3](https://github.com/realrho/test/issues/3) |
| W4 · 2026-10-22~2026-10-28 | [업무 흐름을 제한된 에이전트로 연결하기](week-04.md)<br>LangGraph · State/Node/Edge · Tool contracts · Retry · Checkpoint · PostgreSQL | 검색·사례 조회·정책 버전 도구를 제한된 업무 흐름으로 묶고, 실행 경로와 실패를 추적한다. | [Jira](https://realrho-1790798942092.atlassian.net/browse/SCRUM-9) · [Issue #4](https://github.com/realrho/test/issues/4) |
| W5 · 2026-10-29~2026-11-04 | [사람 검토와 안전성의 실제 경계 만들기](week-05.md)<br>HITL · Prompt injection · PII · Authorization · Confidence calibration · Evaluation | 불확실하거나 고위험인 사례를 승인 대기 상태로 멈추고, 권한 있는 검토자가 재개하도록 만든다. | [Jira](https://realrho-1790798942092.atlassian.net/browse/SCRUM-10) · [Issue #5](https://github.com/realrho/test/issues/5) |
| W6 · 2026-11-05~2026-11-11 | [품질·지연·비용으로 모델과 캐시를 선택하기](week-06.md)<br>P50/P95 · Token accounting · Benchmark design · Redis · Cache invalidation · Model routing | 같은 평가 조건에서 모델 2개를 비교하고, 비용과 품질을 보존하는 cache/routing 결정을 제시한다. | [Jira](https://realrho-1790798942092.atlassian.net/browse/SCRUM-11) · [Issue #6](https://github.com/realrho/test/issues/6) |
| W7 · 2026-11-12~2026-11-18 | [재현 가능한 배포와 장애 복구 만들기](week-07.md)<br>Docker Compose · Networking · Health/Readiness · Observability · CI · AWS 설계 · Kubernetes 기초 | 새 환경에서 같은 버전으로 실행하고, 의존 서비스 장애와 복구를 관찰할 수 있는 배포 패키지를 완성한다. | [Jira](https://realrho-1790798942092.atlassian.net/browse/SCRUM-12) · [Issue #7](https://github.com/realrho/test/issues/7) |
| W8 · 2026-11-19~2026-11-25 | [설계 판단을 증거와 영어 데모로 전달하기](week-08.md)<br>Customer narrative · Architecture trade-offs · Evidence audit · Demo · Interview · Internal transfer | 고객 문제에서 설계 선택·측정·한계까지 10분 안에 설명하는 포트폴리오로 완성한다. | [Jira](https://realrho-1790798942092.atlassian.net/browse/SCRUM-13) · [Issue #8](https://github.com/realrho/test/issues/8) |


## 진행 방식

개념 4개→손 실습→코드→빌드 4개→정상/실패 검증→퀴즈→증거. 하위 작업은 5/6/6/5h이며 모든 학습·검증 시간을 포함한다.

필수는 API/SQL·Milvus RAG·평가·bounded LangGraph·HITL·guardrail·실모델 benchmark·Redis·local full-stack·영어 demo다. reranker·query rewrite·real cloud/K8s/GPU는 선택 심화다. 실환경 검증이 안 되면 해당 gate는 Blocked로 두고 fixture 학습과 구분한다.

현재 구현은 API 접수/조회 뼈대다. 교재 작성은 미래 기능 구현이나 실제 측정 결과가 아니다. 모든 강의 예제는 교육용이며 각 코드 블록 아래의 복잡도·한계를 확인한다.
