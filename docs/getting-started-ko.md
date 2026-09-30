# 시작하기 · 학습법·환경·핵심 용어

> **학습 기준:** 8주 × 22h = 176h. 날짜는 기존 2026-10-01~2026-11-25 계획을 유지했다. 22h는 확인되지 않은 학습 시간 가정이며 시간이 부족하면 선택 심화부터 줄인다.

## 어떻게 공부할까

1. 주차의 목표와 선행 조건을 먼저 읽는다.
2. 개념 강의를 한 절씩 읽고 예제를 자기 말로 설명한다.
3. 손계산·예상 결과를 적은 뒤 코드 실습을 실행한다.
4. Wn.1→Wn.2→Wn.3→Wn.4 순서로 작은 구현과 검증을 반복한다.
5. 퀴즈를 답하고 해설을 확인한 뒤 실제 결과/한계를 Evidence에 남긴다.

강의 6h·빌드 11h·검증 3h·회고/영어/내부이동 준비 2h를 출발 배분으로 사용한다. 각 Jira 작업의 5/6/6/5h 안에 학습·검증도 포함되므로 시간을 이중으로 더하지 않는다. 시간이 주당 12h 정도라면 동일 범위를 8주에 억지로 넣기보다 12~16주로 늘리거나 optional cloud/K8s/GPU를 제외한다.

## 시작 전 진단

- [ ] Python 함수·dict/list·예외를 읽고 간단한 JSON 처리를 할 수 있다.
- [ ] Git clone·status·branch·commit의 차이를 설명한다.
- [ ] POST body·GET·HTTP 202/404/422 의미를 안다.
- [ ] VS Code/터미널에서 Python 환경을 구분한다.
- [ ] Docker/WSL·API 접근·비용 허용 범위를 확인할 수 있다.

앞의 세 가지가 어렵다면 W1 D1에 Python/Git 기초를 추가하고 선택 심화를 줄인다. 문법을 모두 외운 뒤 시작할 필요는 없지만 설명 없이 코드를 복사해 완료 처리하지 않는다.

## PowerShell 첫 실행

현재 저장소는 접수/조회 API 뼈대와 테스트 4개가 있다. 아래는 현재 뼈대 실행 순서이며 이후 주차 기능을 실행하는 명령이 아니다. runtime은 Python 3.11 이상; 학습 기준은 3.12다. .venv를 직접 호출하면 PowerShell activation 정책을 바꿀 필요가 없다.

~~~powershell
# 첫 checkout에서만 실행한다. 이미 checkout이 있다면 그 폴더를 사용한다.
git clone https://github.com/realrho/test.git
Set-Location test
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install 'fastapi>=0.115' 'uvicorn[standard]>=0.30' 'pydantic>=2.0' 'pytest>=8.0' 'httpx>=0.27'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
~~~

브라우저에서 http://127.0.0.1:8000/docs 를 연다. 별도 PowerShell에서 GET /health와 POST /cases/analyze를 실행하고 받은 case_id로 GET /cases/{case_id}를 조회한다. 현재 결과는 received이며 실제 AI 분석은 아직 없다. 실행한 환경 버전과 테스트 결과는 직접 기록한다. 패키지 설치의 느슨한 범위는 현재 뼈대 기준이며 W7에 실제 검증한 lock/버전으로 고정한다.

## 환경·접근 의존성

| 항목 | 필요 주차 | 필수/대안/검증 |
|---|---|---|
| Python·Git·pytest | W1~W8 | 필수. 환경·commit·test 결과 기록 |
| WSL2 Ubuntu/Milvus Lite | W2~ | Windows 학습 우선 경로; native Windows Lite를 전제하지 않음 |
| Docker/Milvus Standalone | W2~W7 | 리소스 충분할 때 대안. 공식 compose/요구사항 확인 |
| 실제 embedding | W2~ | CPU 로컬 모델 또는 허용된 API 하나. fixture는 실검색 품질이 아님 |
| LLM API·예산 | W3·W6 | 실모델 RAG/2모델 측정에 필요. 없는 경우 해당 gate Blocked |
| Postgres·Redis | W4·W6~ | 공유 사례/검토 저장·캐시; 실제 연결 검증 필요 |
| Cloud 계정·region·예산 | W7 선택 | 기본은 설계 문서. 실제 배포는 별도 실행 증거 |
| GPU/vLLM/LoRA | 선택 심화 | API/CPU 과정 완료와 분리. 미측정 수치를 쓰지 않음 |



## 자주 쓰는 용어

| 용어 | 이 프로젝트에서의 의미 |
|---|---|
| SA | 고객 요구사항을 기술 선택·설계·실행 가능한 검증으로 연결하는 역할 |
| FR/NFR | 해야 하는 행동 / 품질·제약 |
| PoC/MVP | 불확실성 검증 / 최소 사용자 흐름 |
| HTTP/API | 요청·응답 규칙 / 시스템 사용 계약 |
| Schema | 데이터 필드·타입·제약 |
| Type hint | 코드의 데이터 형태 설명; 런타임 검증과 다름 |
| async/await | I/O 대기 동안 다른 작업 처리 |
| Transaction | 묶인 DB 변경을 함께 성공/취소 |
| Idempotency | 재실행해도 같은 결과/중복 부작용 없음 |
| RAG | 검색한 근거로 모델 답변을 생성 |
| Embedding | 텍스트를 비교 가능한 벡터로 표현 |
| Chunk | 검색·모델에 넣는 문서 조각 |
| Metadata | 출처·버전·권한·유효일 같은 부가정보 |
| Dense/Lexical | 의미 벡터 / 단어 일치 검색 |
| RRF | 점수 척도 대신 순위를 합치는 방법 |
| Recall/Hit/MRR | 정답 회수 비율 / 하나라도 적중 / 첫 정답 순위 |
| Citation | 답변이 참조한 근거 |
| Abstention | 근거 부족으로 답변을 확정하지 않음 |
| Holdout | 설정 선택에 쓰지 않는 최종 평가 집합 |
| Agent/Workflow | 모델이 다음 행동 선택 / 정해진 경로 실행 |
| Tool calling | 모델의 도구 실행 제안; 서버 검증이 필요 |
| Checkpoint | 재개를 위한 실행 상태 저장 |
| HITL | 사람이 검토하고 재개하는 흐름 |
| Prompt injection | 데이터 안 지시로 시스템 행동을 바꾸려는 공격 |
| Calibration | 점수와 실제 결과의 관계를 검증 |
| P50/P95 | 중앙·꼬리 응답 시간 지표 |
| Throughput/Concurrency | 초당 완료량 / 동시 작업 수 |
| Cache/TTL | 결과 재사용 / 보관 시간 |
| Image/Container | 실행 환경 스냅샷 / 실행 인스턴스 |
| Readiness/Liveness | 요청 받을 준비 / 프로세스 생존 |
| ADR | 설계 결정과 대가·재검토 조건 기록 |



## 증거와 완료 상태

- 학습 문서: 설명·예시·계획이 작성됐다는 상태.
- fixture validated: 고정 입력/모형으로 계약·제어 경로를 확인한 상태.
- real validated: 실제 DB/embedding/LLM/cloud를 해당 환경에서 실행한 상태.
- measured: 데이터셋·설정·환경·원본 결과가 있는 수치.
- Planned/Blocked: 실행하지 못한 항목. 원인과 다음 행동을 적는다.

Jira AC가 실행 기준이다. Notion은 강의와 회고, GitHub는 구현·보고서·commit 증거다. 문서 편집만으로 기존 W1 진행 중/W2~W8 시작 전 상태를 Done으로 바꾸지 않는다.

## 주간 회고·내부 이동

매주 ‘무엇을 이해했나 / 어떤 실패를 재현했나 / 왜 이 선택을 했나 / 증거는 어디 있나 / 다음 blocker는 무엇인가’를 5줄로 남긴다. 기존 Internal Transfer 트랙은 유지한다. 연락 요청 초안과 현직자 질문은 개인이 직접 보내며, 이 정리는 동료에게 자동 메시지를 보내는 작업이 아니다.

공식 자료: [Python](https://docs.python.org/3/tutorial/), [Git](https://git-scm.com/book/en/v2), [FastAPI](https://fastapi.tiangolo.com/tutorial/), [Milvus 환경](https://milvus.io/docs/prerequisite-docker.md).