# W1 학습 — 에이전트(agent) 설계·UX와 API 계약(API contract)·입력 검증(input validation)

**주교재:** 『AI 에이전트 엔지니어링』 · **책 범위:** 1장 에이전트 / 2장 에이전트 시스템 설계 / 3장 에이전트 시스템을 위한 UX 디자인

**일정:** 2026-10-02–2026-10-08 (Asia/Seoul) · **총 계획:** 22h

[Notion 주차](https://app.notion.com/p/3ebc6f4a2c7e817e9b59e2ed884085ed) · [GitHub #1](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/1)

## 1. 이번 주 목표와 책 읽기

1.1–1.11: 에이전트(agent)·워크플로(workflow)·모델 선택과 조직 전략. 2.1–2.10: 도구·메모리·오케스트레이션(orchestration)·설계 트레이드오프(trade-off)와 평가(evaluation). 3.1–3.6: 자율성·동기/비동기 경험·불확실성·실패·신뢰. 세 장의 모든 절을 읽고 고객의 업무와 연결한다.

**필수 실습:** 정책 질문 사례 3개를 대상으로 업무 단계·사용자 역할·성공/보류/검토 경로를 그린다. 모델 2개를 품질·지연(latency)·비용·데이터 조건으로 비교하되 구현은 한 경로를 선택한다. 접수와 완료를 구분한 화면·응답 예제를 작성한다.

**재사용 산출물(deliverables):** 요구사항(requirements) 1쪽, 모델 선택표, 입력/결과 API 계약(API contract), 검증 실패 사례, Docker 입문 기록

**완료 기준:** 공백·잘못된 타입·길이 초과를 거부하고 서버가 검증한 신원과 본문 입력을 구분한다. 202 접수와 분석 완료를 설명하고 워크플로/에이전트 선택 이유를 말할 수 있다.

## 2. 책·영상·실습을 연결한 22h 실행 순서

| 순서 | 활동 | 계획 시간 | 결과/목적 |
|---|---|---|---|
| 1 | 책 읽기·설계 노트 | 6h | 1.1–1.11: 에이전트(agent)·워크플로(workflow)·모델 선택과 조직 전략. 2.1–2.10: 도구·메모리·오케스트레이션(orchestration)·설계 트레이드오프(trade-off)와 평가(evaluation). 3.1–3.6: 자율성·동기/비동기 경험·불확실성·실패·신뢰. 세 장의 모든 절을 읽고 고객의 업무와 연결한다. |
| 2 | API 전체 수업·Docker 입문 시청 | 2h | FastAPI 공개 기본편 6개 전체(약 65분) + Docker 입문(약 42분)과 간단한 메모. 따라 하기·연결 실습은 SA 실습 6h에 포함한다. |
| 3 | 책 개념 프로젝트 실습 | 6h | 정책 질문 사례 3개를 대상으로 업무 단계·사용자 역할·성공/보류/검토 경로를 그린다. 모델 2개를 품질·지연(latency)·비용·데이터 조건으로 비교하되 구현은 한 경로를 선택한다. 접수와 완료를 구분한 화면·응답 예제를 작성한다. |
| 4 | 영상과 연결한 SA 실습 | 6h | 요구사항(requirements) 1쪽, 모델 선택표, 입력/결과 API 계약(API contract), 검증 실패 사례, Docker 입문 기록 |
| 5 | 설명·퀴즈·증거 검토 | 2h | 공백·잘못된 타입·길이 초과를 거부하고 서버가 검증한 신원과 본문 입력을 구분한다. 202 접수와 분석 완료를 설명하고 워크플로/에이전트 선택 이유를 말할 수 있다. |

영상 배정은 주간 시간 안에 포함된 선택 시청·메모 시간이다. 영상마다 아래 시청 직후 실습을 이어서 수행한다. 순서는 진행 안내이며 주차 체크리스트 네 작업은 읽기6h·개념 실습6h·영상/SA8h·검토2h로 시간을 집계한다.

## 3. 이번 주에 볼 한국어 영상과 연결 실습

### 영상 1. API 전체 수업 · 학습 묶음 1

**보는 시점:** 2장 도구와 API 계약(API contract) 개념 다음.

- [FastAPI 첫걸음 — API 전체 재생목록(공개 기본편 6개)](https://youtube.com/playlist?list=PL8kmk2VivDmQyPLmc4zF6yLEl-Rc6D9lg&si=iKuEUs7JNHJV-N7R) — hatemogi, 한국어 수업.

**볼 범위:** ‘FastAPI 첫걸음’ 재생목록의 공개 기본편 6개를 목록 순서대로 모두 학습한다(약 65분). API 소개 → uv 환경 준비 → API 서버 만들기 → 경로 데코레이터·경로 함수 → Pydantic 입력 검증(input validation) → CRUD. 재생목록에 있는 환경 준비도 함께 따라 하되 별도의 Python·HTTP·SQL 기초 과정은 추가하지 않는다.

**시청 직후 실습:** 각 영상의 예제를 직접 실행한 뒤 정책 질문 API로 바꿔 본다. 요청·응답 계약과 생성·조회·수정·삭제 경로를 정리하고, 정상 입력 1개와 공백·잘못된 타입·길이 초과·허용하지 않은 필드의 실패 4개를 검증한다. REST, Representational State Transfer(자원 표현을 통한 상태 전달), CRUD, Create·Read·Update·Delete(생성·조회·수정·삭제), JSON, JavaScript Object Notation(데이터 교환 형식)의 뜻을 자신의 말로 설명한다.

**학습 기록:** 6개 영상 각각 시청·예제 실행을 체크하고 실행 명령·환경 버전·결과·남은 질문을 남긴다. 영상 시청과 메모는 Docker 입문 약 42분을 합쳐 2h, 따라 하기와 업무 API 적용은 아래 SA 실습 6h에 포함한다. 유료 심화 과정은 W1 필수 범위에 포함하지 않는다.

### 영상 2. Docker · 학습 묶음 4

**보는 시점:** 실행 환경을 구분한 API 계약(API contract) 다음.

- [생활코딩 Docker 입구 수업](https://www.youtube.com/playlist?list=PLuHgQVnccGMDeMJsGq2O-55Ymtx0IdKWf) — 생활코딩, 한국어 수업.

**볼 범위:** Docker 입구 수업 8편(약 42분): 이미지/컨테이너(container)·명령·네트워크(network)·마운트.

**시청 직후 실습:** 같은 이미지로 컨테이너를 재생성하고 포트(port)·볼륨(volume)을 확인한다. 이미지 제작과 Compose는 W7에서 이어간다.


## 4. 영어·한국어 개념 강의

### 1.1 Agent·Workflow·UX — 에이전트(agent)·워크플로(workflow)·사용자 경험

AI, Artificial Intelligence(인공지능)를 이용한 agent(에이전트)는 목표를 위해 모델이 다음 행동이나 도구를 선택하는 시스템이다. workflow(워크플로)는 정해 둔 단계와 분기를 따라간다. LLM, Large Language Model(대규모 언어 모델)이 들어간다고 모든 프로그램이 에이전트가 되는 것은 아니다. 선택 자유도가 커지면 예상하지 못한 행동·지연(latency)·비용도 늘어나므로 고객 업무가 필요로 하는 자율성부터 정한다. UX, User Experience(사용자 경험)는 완료 결과뿐 아니라 진행 상태·실패·사용자 개입을 포함한다.

**업무 예시:** 정책 검색→근거 검증(grounding validation)→응답/보류/검토는 제한된 워크플로로 시작한다. 모델이 임의로 승인 버튼을 누르는 권한(permissions)은 주지 않는다. 사용자가 기다리는 화면에는 접수·처리 중·검토 대기를 서로 다르게 표시한다.

**직접 할 일:** 고객 역할·행동·실패·성공 기준을 적고 워크플로와 에이전트 중 선택 이유를 3문장으로 설명한다.

### 1.2 API Contract — 입력·출력 계약

API, Application Programming Interface(응용 프로그램 인터페이스)는 호출자와 서비스가 합의한 사용 규칙이다. contract(계약)는 필드·타입·필수 여부·실패 의미·상태 전이(state transition)를 포함한다. OpenAPI는 API 설명을 기계가 읽을 수 있게 표현하는 명세 이름이다. API 기초 통신 문법을 다시 배우는 대신, 입력과 결과가 어느 단계에서 유효한지 정의한다. 작업 ID를 반환하는 접수와 근거를 포함한 완료 결과는 다른 약속이다.

**업무 예시:** POST /cases/analyze가 case_id와 RECEIVED를 반환했다면 접수만 확인된 것이다. GET 조회에는 tenant 경계가 적용되어야 하며 request_id(요청 추적 ID)와 case_id(업무 사례 ID)를 구분한다.

**직접 할 일:** 요청·접수·완료·오류 예제와 허용 상태 전이표를 docs/contracts.md의 예정 산출물(deliverables)로 만든다. 삭제/재시도(retry) 시 계약도 적는다.

### 1.3 Input Validation — 입력 검증(input validation)과 신뢰 경계(trust boundary)

input validation(입력 검증)은 외부 값을 업무 로직에 전달하기 전에 계약과 맞는지 확인하는 과정이다. schema(스키마)는 값의 구조와 제약이다. Pydantic·FastAPI는 제품 이름이며 타입 선언만으로 모든 업무 규칙이 해결되는 것은 아니다. 공백 제거 같은 normalization(정규화)을 먼저 하고 길이를 검사해야 공백만 있는 입력을 잡는다. 클라이언트가 보낸 tenant나 reviewer 값은 권한(permissions) 증거가 아니다. 인증(authentication)된 서버 컨텍스트(context)에서 권한을 얻는다.

**업무 예시:** '   '·문자열 아닌 값·한도 초과를 거부한다. 정상 입력에는 검증된 객체만 서비스에 전달한다. 필드가 valid해도 다른 고객사의 문서 접근은 authorization(인가) 검사에서 거부한다.

**직접 할 일:** Pydantic v2 공식 문서와 비교하며 정상 1개·실패 4개를 검증한다. 엄격한 타입/자동 변환 선택 이유와 오류 응답을 기록한다.

### 1.4 Container·Image — 컨테이너(container)와 실행 환경

Docker는 컨테이너를 만들고 실행하는 도구 이름이다. image(이미지)는 실행에 필요한 파일·의존성·명령을 담는 배포(deployment) 단위이고 container(컨테이너)는 이미지를 실행한 인스턴스다. 앱과 데이터의 생명주기는 달라야 한다. volume(볼륨)은 컨테이너 밖에 데이터를 유지하는 저장 경로이며 백업(backup)과 동일하지 않다. 태그 이름만으로 동일 환경을 보장하지 못하므로 검증한 이미지 버전·digest(내용 식별값)를 기록한다.

**업무 예시:** API 컨테이너를 없앴다가 다시 만들 수 있어도 DB 데이터까지 없어지면 안 된다. 로컬 포트(port)와 컨테이너 포트를 매핑하고 외부 노출 범위를 확인한다.

**직접 할 일:** 영상 4의 입문 8편을 보고 이미지 pull·컨테이너 run·파일 마운트를 합성 자료로 확인한다. Dockerfile·Compose 제작은 W7에서 이어간다.

## 5. 확인 퀴즈

### Q1. 에이전트(agent)가 워크플로(workflow)보다 항상 좋은가?

**해설:** 업무가 정해진 순서와 명확한 검토 경계를 요구하면 워크플로가 더 단순하고 예측 가능하다. 자율성은 필요와 검증 증거에 맞춰 선택한다.

### Q2. 본문 tenant 필드가 올바른 문자열이면 접근을 허용해도 되는가?

**해설:** 구조 검증과 인가(authorization)는 다르다. 서버가 검증한 신원의 tenant/role과 대조해야 한다.

### Q3. 202와 case_id를 받았으면 AI 분석이 끝났는가?

**해설:** 접수만 확인됐다. 처리 상태와 결과·근거를 조회하고 실제 완료 경로를 검증해야 한다.

## 6. 주차 체크리스트·수용 기준(acceptance criteria, AC)

- **W1.1 · 책 1·2·3장 읽기·설계/개념 노트 (6h)**
  - 선행: 없음.
  - 수용 기준: 1.1–1.11: 에이전트(agent)·워크플로(workflow)·모델 선택과 조직 전략. 2.1–2.10: 도구·메모리·오케스트레이션(orchestration)·설계 트레이드오프(trade-off)와 평가(evaluation). 3.1–3.6: 자율성·동기/비동기 경험·불확실성·실패·신뢰. 세 장의 모든 절을 읽고 고객의 업무와 연결한다. 산출물(deliverables): 핵심 용어의 영어·한글 뜻과 업무 설계 메모.
- **W1.2 · 책 개념을 적용한 프로젝트 실습 (6h)**
  - 선행: W1.1.
  - 수용 기준: 정책 질문 사례 3개를 대상으로 업무 단계·사용자 역할·성공/보류/검토 경로를 그린다. 모델 2개를 품질·지연(latency)·비용·데이터 조건으로 비교하되 구현은 한 경로를 선택한다. 접수와 완료를 구분한 화면·응답 예제를 작성한다. 산출물: 정상/실패 expected/actual·raw 결과.
- **W1.3 · 영상·SA 보충 실습 — 에이전트 설계·UX와 API 계약(API contract)·입력 검증(input validation) (8h)**
  - 선행: W1.2.
  - 수용 기준: API 공개 재생목록 6개 전체와 Docker 입문 시청·메모 2h + 따라 하기·연결 실습 6h. 각 영상의 예제를 직접 실행한 뒤 정책 질문 API로 바꿔 본다. 요청·응답 계약과 생성·조회·수정·삭제 경로를 정리하고, 정상 입력 1개와 공백·잘못된 타입·길이 초과·허용하지 않은 필드의 실패 4개를 검증한다. REST, Representational State Transfer(자원 표현을 통한 상태 전달), CRUD, Create·Read·Update·Delete(생성·조회·수정·삭제), JSON, JavaScript Object Notation(데이터 교환 형식)의 뜻을 자신의 말로 설명한다. 요구사항(requirements) 1쪽·모델 선택표·입력/결과 API 계약·Docker 입문 기록을 저장한다.
- **W1.4 · 퀴즈·본인 설명·증거·다음 주 준비 검토 (2h)**
  - 선행: W1.3.
  - 수용 기준: 퀴즈 3개를 자신의 말로 설명하고 정상/실패 증거와 다음 주 선행 조건을 검토한다.

## 7. 공식 문서와 증거

- [API·입력 검증](https://fastapi.tiangolo.com/tutorial/body/) — 현재 API·설치·보안(security) 설정을 확인한다.
- [Pydantic v2](https://docs.pydantic.dev/latest/concepts/models/) — 현재 API·설치·보안 설정을 확인한다.
- [Docker Compose](https://docs.docker.com/compose/) — 현재 API·설치·보안 설정을 확인한다.

[책 공식 소개](https://www.hanbit.co.kr/books/ai-에이전트-엔지니어링?code=B1562725816) · [저자 예제 코드](https://github.com/michaelalbada/BuildingApplicationsWithAIAgents) · [승인 영상과 선정 근거](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/video-resources.md) · [13장 목차](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-toc.md) · [SA 보완 영역](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-gap-map.md) · [영어·한글 용어 사전](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/glossary-ko-en.md)

읽은 절·자신의 설명·실습 명령·환경/패키지/데이터/모델/프롬프트(prompt)/인덱스(index) 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 계획과 실행, fixture와 실제 모델/검색/DB 실행, 목표와 실측을 구분한다. 자료 갱신만으로 학습 또는 구현을 Done 처리하지 않는다.
