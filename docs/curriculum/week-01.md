# W1. 고객 요구사항을 API 계약으로 바꾸기

> 고객의 모호한 요청을 요구사항·상태·API 계약으로 표현하고, 기존 API 뼈대를 직접 설명하고 검증한다.

2026-10-01 → 2026-10-07 · 총 22h (주당 계획 가정)

[Jira SCRUM-6](https://realrho-1790798942092.atlassian.net/browse/SCRUM-6) · [GitHub #1](https://github.com/realrho/test/issues/1) · [프로젝트 홈](https://app.notion.com/p/3ebc6f4a2c7e81dca9d6f2cf630b9602)

## 학습 목표와 시작 조건

**기술:** Python · Git · HTTP · FastAPI · SQL · Architecture v0

**시작 조건:** Python 함수·리스트·딕셔너리를 읽을 수 있으면 시작. 어렵다면 D1에 기초 복습 2시간을 추가하고 선택 심화를 생략한다.

이 페이지는 학습 교재와 앞으로 구현할 작업이다. 문서가 작성된 것을 서비스 구현/평가 완료로 표시하지 않는다. 학습은 아래 4개 강의→손 실습→코드 실습→빌드→퀴즈→증거 제출 순서로 진행한다.

## 이번 주 시간표

- D1 3h: Python·Git 복습, 고객 문제 1페이지 작성
- D2 3h: HTTP/입출력 모델·상태 계약 작성
- D3 3h: 기존 API 실행과 현재 한계 재현
- D4 3h: 검증·예외 처리와 테스트 개선
- D5 4h: SQLite·repository 연습, Architecture v0
- D6 4h: 전체 검증·ADR·영어 2분 설명
- D7 2h: 복습·내부이동 질문 준비·지연 버퍼

## 개념 강의

### 1. SA가 해결하는 문제: 기능보다 판단 기준을 먼저 정한다

가상의 고객은 두 개 사업부를 가진 SaaS 회사다. 지원 담당자는 합성 운영정책을 검색하고 고객 사례를 검토한다. 현재 문제를 ‘AI가 필요하다’로 쓰면 어떤 답변이 좋은지 결정할 수 없다. 대신 ‘담당자가 출처를 확인할 수 있고, 오래된 정책과 근거 부족 사례는 검토 대기열로 보내야 한다’로 정의한다. 사용자, 현재 업무, 입력, 출력, 실패 비용, 성공 기준을 순서대로 기록한다.

기능 요구사항은 시스템이 해야 하는 행동이다. 예: 사례 등록, 최신 정책 검색, 출처 반환, 검토 요청. 비기능 요구사항은 그 행동의 품질과 제약이다. 예: 동시 요청 수, 응답 지연, 개인정보 보존, 복구 시간. ‘빠르게’ 대신 ‘정의한 환경·입력 크기·동시성에서 자동 응답 경로 P95 5초 이내를 목표로 한다’라고 쓴다. 목표와 측정 결과는 별도 칸이다.

PoC는 불확실한 기술 가능성을 검증하고, MVP는 최소 사용자 흐름을 완성한다. 이 프로젝트는 운영을 고려한 포트폴리오 프로토타입이다. 고객 전환·채용 확정이나 실제 서비스 운영을 완료 기준으로 삼지 않는다. 필수 데모는 정상 사례, 근거 부족 사례, 사람 검토 사례 세 가지다.

### 2. Python과 모듈 경계: 타입·예외·async를 이유와 함께 이해한다

타입 힌트는 함수가 어떤 데이터를 받는지 알려 주지만 일반 Python 실행에서 모든 입력을 자동 검사하지 않는다. Pydantic 모델은 API 경계에서 입력과 출력의 형태를 검증한다. ‘text: str’과 ‘text가 공백이 아니어야 함’은 다른 조건이므로 공백 정리와 길이 검증을 명시한다.

예외는 실패를 호출자에게 전달하는 수단이다. 입력 오류는 422, 존재하지 않는 사례는 404, 같은 키의 다른 요청은 409, 일시적인 의존 서비스 장애는 503처럼 의미를 구분한다. 모든 예외를 잡고 200을 반환하면 클라이언트가 실패를 성공으로 오해한다.

async/await는 네트워크나 DB를 기다리는 동안 다른 요청을 처리하게 한다. CPU 임베딩 계산이 자동으로 빨라지는 것은 아니다. async 함수 안의 긴 CPU 작업·동기 HTTP 호출은 이벤트 루프를 막을 수 있다. W1에서는 간단한 API를 읽고, W2에서는 임베딩 배치 작업을 요청 처리와 분리한다.

API 라우터는 HTTP 변환, service는 사례 처리 규칙, repository는 저장을 담당하게 한다. 필요하지 않은 추상 클래스 계층을 만들지 말고 실제로 바꿀 저장소·모델 연결 부분에만 작은 계약을 둔다.

### 3. HTTP와 상태: 202는 분석 완료가 아니다

HTTP 요청은 method·path·header·body로 구성된다. GET은 조회, POST는 생성/행동 요청이다. JSON은 구조화된 데이터 표현이고 OpenAPI는 엔드포인트와 모델의 설명이다. Swagger 화면에서 요청이 된다고 기능 검증이 끝난 것은 아니다.

기존 POST /cases/analyze는 202와 received를 반환하고 메모리에 사례 ID만 남긴다. 현재는 분석기·백그라운드 워커·영속 저장이 없다. 이를 ‘AI 분석이 된다’고 표현하면 잘못이다. W1은 이 한계를 재현하고 계약을 정리한다. W2~W4에서 저장·검색·실행 경로를 채운다.

목표 상태를 RECEIVED → PROCESSING → COMPLETED / INSUFFICIENT_EVIDENCE / HUMAN_REVIEW / FAILED로 정의한다. HTTP 응답 코드와 업무 상태를 구분한다. 접수 성공 202 안에서도 나중 분석은 FAILED일 수 있다. 재시도용 request_id와 case_id를 나누고, 동일 Idempotency-Key에 동일 payload는 같은 사례 ID, 다른 payload는 409가 되게 설계한다.

### 4. Git·SQL·아키텍처: 다음 주가 의존할 기반을 만든다

Git commit은 변경 스냅샷이고 branch는 작업 흐름의 이름이다. PR에는 변경 이유와 검증 결과를 담는다. Jira는 실행 기준, Notion은 학습 해설, GitHub는 코드와 증거의 기준으로 사용한다. 커밋 메시지에 SCRUM-6을 넣어 추적한다.

관계형 DB는 cases·reviews처럼 일관된 레코드와 상태를 보관한다. transaction은 묶인 쓰기를 모두 성공하거나 취소하게 한다. 예: 사례 상태 변경과 감사 이벤트를 함께 저장한다. W1은 SQLite로 저장소·스키마 개념을 연습하고 W4/W7에서 PostgreSQL로 운영 경로를 만든다. in-memory 딕셔너리는 프로세스 재시작과 여러 worker에서 내용이 공유되지 않는다.

구조 그림에는 사용자·API·저장·검색·모델과 데이터 경계를 그린다. ADR은 ‘상황→선택지→결정→대가→재검토 조건’이다. FastAPI를 선택한 이유만 쓰지 말고 초기 단순성의 이점과 장기 작업 워커가 필요한 시점을 함께 쓴다. 고객에게는 컴포넌트 이름보다 어떤 실패를 감당하고 어떤 품질을 보장하려는지 설명한다.



## 따라 하는 실습과 예상 결과

기존 API를 실행해 사례 접수→조회→프로세스 재시작→재조회 순서로 실험한다. 최초 조회는 200·received, 재시작 뒤 같은 ID 조회는 404가 예상된다. 이는 버그를 숨기는 시험이 아니라 현재 저장 방식의 한계를 확인하는 실험이다. 별도 SQLite 연습 DB에 cases(id, text, status, created_at) 테이블을 만들고 transaction 내 insert→select를 실행해 차이를 설명한다.

테스트 표에는 정상 입력, 빈 문자열, 공백만 입력, 10,000자 경계, 10,001자, text 누락, 잘못된 타입, 없는 ID, 접수 후 조회, 재시작 시 저장 한계를 넣는다. 기존 테스트는 4개이며 10개는 앞으로의 완료 목표다. 공백 검증 등 미구현 항목은 먼저 실패로 기록하고 수정한다.

## 코드로 확인하는 핵심 원리

먼저 현재 API의 행동을 관찰한다. 아래는 애플리케이션을 바꾸지 않는 계약 확인 실습이다.

```python
from fastapi.testclient import TestClient
from app.main import app

# 현재 구현이 실제로 약속하는 것은 접수와 조회뿐이다.
client = TestClient(app)
created = client.post('/cases/analyze', json={'text': 'Synthetic policy case'})
assert created.status_code == 202
case_id = created.json()['case_id']
assert client.get(f'/cases/{case_id}').json()['status'] == 'received'
assert client.get('/cases/missing').status_code == 404
```

**복잡도와 병목:** 현재 딕셔너리 조회는 평균 O(1), 저장 공간은 접수 사례 수에 따라 O(n). 입력 검증은 문자열 길이 O(L). 프로세스 메모리와 영속성 부재가 실제 병목이다.

## 프로젝트에서 빌드할 부분

### W1.1 고객 문제·요구사항·상태/API 계약 작성 · 5h

**왜 필요한가:** 다음 구현을 판단할 계약·데이터·환경을 먼저 확정한다.

**수정/작성 위치:** docs/requirements.md, docs/contracts.md

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. 요구사항 진단부터 시작한다.

**완료 조건:** 고객·입력·출력·FR 6개·NFR 5개·상태 전이·정상/실패 시나리오 3개를 작성하고 모든 수치를 목표로 표시한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W1.2 Python·HTTP 실습과 입력/오류 경계 보강 · 6h

**왜 필요한가:** 개념을 실제 핵심 경로에 연결해 다음 검증의 기준선을 만든다.

**수정/작성 위치:** app/main.py, app/api/, app/schemas.py

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W1.1의 산출물이 선행한다.

**완료 조건:** 3개 기존 엔드포인트를 설명하고 공백·길이·누락·404 계약을 구현 또는 한계로 명시한다. 202를 AI 완료로 표현하지 않는다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W1.3 저장소·transaction 연습 및 의미 있는 API 검증 · 6h

**왜 필요한가:** 실패·권한·복구 경계를 구현해 정상 시연만으로 놓치는 문제를 찾는다.

**수정/작성 위치:** app/repositories/, tests/, docs/evidence/w01.md

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W1.2의 산출물이 선행한다.

**완료 조건:** 10개 경계/상태 시나리오의 예상·실제 결과를 남긴다. SQLite 연습과 메모리 재시작 한계를 재현하고 API 상태와 영속성 한계를 구분한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W1.4 Architecture v0·ADR·주차 데모와 회고 · 5h

**왜 필요한가:** 검증 결과를 설계 결정과 다른 사람이 확인할 증거로 바꾼다.

**수정/작성 위치:** docs/architecture.md, docs/adr/, docs/evidence/w01.md

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W1.3의 산출물이 선행한다.

**완료 조건:** 현재/목표 그림을 분리하고 실행 명령·테스트 결과·commit SHA·2분 설명을 남긴다. BytePlus 업무/stack/면접 질문 6개를 준비한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.



## 주차 완료 기준

- [ ] 고객 요구사항·API/상태 계약·Architecture v0·ADR가 연결됨
- [ ] README 실행 순서와 현재 API 3개를 스스로 설명함
- [ ] 10개 의미 있는 API/경계 검증의 실제 결과와 한계를 기록함
- [ ] 영속 저장·AI 분석·실제 운영이 미완료인 부분을 명확히 표시함

## 이해 확인 퀴즈

**Q1. type hint가 있으면 잘못된 JSON이 자동 거부되는가?**

<details>
<summary>해설 확인</summary>

아니다. 실행 경계의 Pydantic 검증과 타입 힌트를 구분해야 한다.

</details>

**Q2. 202 received를 성공적인 AI 판단으로 보고해도 되는가?**

<details>
<summary>해설 확인</summary>

접수만 의미한다. 완료 상태와 실제 실행 증거가 필요하다.

</details>

**Q3. worker를 3개로 늘리면 in-memory 사례가 공유되는가?**

<details>
<summary>해설 확인</summary>

각 프로세스의 메모리가 분리된다. 공유 DB와 transaction이 필요하다.

</details>



## 면접에서 설명할 한 문장

“이번 주에는 고객의 모호한 요청을 요구사항·상태·API 계약으로 표현하고, 기존 API 뼈대를 직접 설명하고 검증한다. 이를 확인한 증거는 ___이며, 아직 확인하지 못한 범위는 ___입니다.”

기술 이름을 외우기보다 선택 이유·실패 경우·측정 조건·대안을 자기 말로 설명한다.

## 공식 자료: 읽을 범위와 사용법

- [Python: 함수·자료구조·예외](https://docs.python.org/3/tutorial/) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [Git: commit·branch·merge](https://git-scm.com/book/en/v2) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [FastAPI: body·response·errors·testing](https://fastapi.tiangolo.com/tutorial/) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [SQL transaction](https://www.postgresql.org/docs/current/tutorial-transactions.html) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.

문서 URL은 2026-10-01 확인. 설치/API 세부는 실습 시 사용 버전의 공식 문서를 다시 확인한다. 본 강의 설명·실습·프로젝트 판단 기준은 이 포트폴리오를 위해 작성한 교육 내용이다.

## 선택 심화·환경이 막힐 때

JWT/OAuth 상세 구현과 복잡한 worker 큐는 W7/추가 과정. Python 기초가 부족하면 아키텍처를 줄이지 말고 선택 심화를 빼고 기초를 먼저 보완한다.

핵심 gate가 안 되면 Jira에 실패 증상·환경·시도·다음 행동을 기록한다. fixture로 계약 학습을 이어 갈 수 있지만 real DB/model/cloud/GPU 완료로 바꾸지 않는다.


## Jira 실행 작업 바로가기

| 순서 | 작업·시간 | 선행 |
|---|---|---|
| 1.1 | [SCRUM-14](https://realrho-1790798942092.atlassian.net/browse/SCRUM-14) · 고객 문제·요구사항·상태/API 계약 작성 · 5h | 환경/요구사항 진단 |
| 1.2 | [SCRUM-15](https://realrho-1790798942092.atlassian.net/browse/SCRUM-15) · Python·HTTP 실습과 입력/오류 경계 보강 · 6h | SCRUM-14 |
| 1.3 | [SCRUM-16](https://realrho-1790798942092.atlassian.net/browse/SCRUM-16) · 저장소·transaction 연습 및 의미 있는 API 검증 · 6h | SCRUM-15 |
| 1.4 | [SCRUM-17](https://realrho-1790798942092.atlassian.net/browse/SCRUM-17) · Architecture v0·ADR·주차 데모와 회고 · 5h | SCRUM-16 |

## 구현 레시피 · 입력·상태·파일별 작업

### API 계약을 먼저 표로 적기

| 경로 | 현재 동작 | W1 검증 / 다음 확장 |
|---|---|---|
| GET /health | 200, status=ok | 프로세스 응답; 의존성 준비는 W7 |
| POST /cases/analyze | 202, case_id/status=received | 접수; AI 분석 완료와 구분 |
| GET /cases/{case_id} | 저장된 ID 조회 / 404 | 재시작 한계; 영속성은 W4 |

1. docs/contracts.md에 위 표와 JSON 필드·길이·상태를 적는다.
2. app/schemas.py에 입력/출력 모델을 옮기고 공백 trim 후 길이를 검사한다. input을 변형한다면 저장하는 원문/정규화본 기준도 적는다.
3. app/api/cases.py는 HTTP 오류/응답 변환만 담당하고 service 함수 호출로 연결한다.
4. app/repositories/에 save/get 계약과 SQLite 연습 구현을 만든다. 기존 API 저장을 교체하지 않았다면 두 경로를 명시한다.
5. tests/에 정상/경계/실패를 넣고 실패하는 계약을 먼저 확인한 뒤 수정한다.

### 상태 JSON 설계 예시

아래는 **향후 응답 계약 예시**다. 현재 API에 아직 없는 필드를 실행 결과로 기록하지 않는다.

~~~json
{"case_id":"case-001","request_id":"req-001","status":"RECEIVED","decision":null,"evidence":[],"review_reason":null}
~~~

인증 컨텍스트는 별도다. local demo는 서버가 보관한 test-user→tenant/role 매핑으로 검증하고, arbitrary tenant header를 신뢰하는 것을 권한 구현으로 간주하지 않는다. 배포 경로에서는 실제 issuer/audience/만료 검증 또는 검증된 인증 프록시 계약이 필요하다. 직접 암호 알고리즘을 만들지 않는다.

### 막힐 때 확인 순서

import 오류→현재 Python/.venv 경로→실행 폴더→패키지 설치→app.main:app 경로를 확인한다. 422는 body 필드/타입/길이 계약을 보고, 404는 ID·저장소·프로세스 재시작 여부를 확인한다. 오류를 모두 200으로 바꾸어 해결하지 않는다.
