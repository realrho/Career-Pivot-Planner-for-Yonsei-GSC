# W4. 업무 흐름을 제한된 에이전트로 연결하기

> 검색·사례 조회·정책 버전 도구를 제한된 업무 흐름으로 묶고, 실행 경로와 실패를 추적한다.

2026-10-22 → 2026-10-28 · 총 22h (주당 계획 가정)

[Jira SCRUM-9](https://realrho-1790798942092.atlassian.net/browse/SCRUM-9) · [GitHub #4](https://github.com/realrho/test/issues/4) · [W3 선행 과정](https://app.notion.com/p/3ebc6f4a2c7e8116b6d0e972f595de78)

## 학습 목표와 시작 조건

**기술:** LangGraph · State/Node/Edge · Tool contracts · Retry · Checkpoint · PostgreSQL

**시작 조건:** W3 RAG·출력 schema·검색 평가. 검색 계약과 상태를 고정한 후 graph를 얹는다.

이 페이지는 학습 교재와 앞으로 구현할 작업이다. 문서가 작성된 것을 서비스 구현/평가 완료로 표시하지 않는다. 학습은 아래 4개 강의→손 실습→코드 실습→빌드→퀴즈→증거 제출 순서로 진행한다.

## 이번 주 시간표

- D1 3h: workflow/agent·state·graph 설계
- D2 3h: read-only tool 3개 계약/권한
- D3 3h: graph·routing·trace
- D4 3h: PostgreSQL schema·migration·repository
- D5 4h: retry/deadline/최대 호출·failure 처리
- D6 4h: 20경로·restart 검증·MVP 데모
- D7 2h: 회고·현직자 피드백 준비·버퍼

## 개념 강의

### 1. Workflow와 Agent: 어디까지 모델에 결정권을 줄까

Workflow는 미리 정한 순서와 분기로 실행된다. Agent는 모델이 다음 도구나 행동을 선택할 수 있다. 질문 하나에 문서 검색 한 번이면 deterministic RAG로 충분하다. 버전 확인·유사 사례 조회·정보 부족 재검색처럼 다음 단계가 달라질 때 모델 판단의 가치와 위험을 비교한다.

포트폴리오는 무제한 ReAct loop 대신 서버가 정한 graph 안에 작은 tool-selection node를 둔다. 3개 read-only 도구만 허용하고, 자동 정책 변경·외부 메시지·사용자 제재는 넣지 않는다. ‘agent를 사용했다’보다 ‘왜 이 node에만 판단을 맡겼고 어떻게 중단하는가’를 설명할 수 있어야 한다.

simple은 정책 FAQ, complex는 조건/유사 사례 비교, unsupported는 범위 밖 요청이다. 위험도 분류와 복잡도 분류는 별개다. 단순한 질문도 민감할 수 있다. routing은 서버 규칙+검증된 모델 출력으로 제한하고 unknown은 unsupported 또는 review로 보낸다.

### 2. State·Node·Edge: 업무를 명확한 상태 변화로 쓴다

State는 실행 과정에서 공유하는 데이터다. case_id, trusted_tenant_id, question, route, evidence, proposed_decision, tool_calls, error, status를 타입으로 정의한다. node는 상태를 읽고 변화분을 반환하는 한 단계, edge는 다음 단계 선택 규칙이다. node 안에 모든 로직을 넣으면 테스트와 오류 원인 추적이 어렵다.

목표 graph는 validate→route→retrieve→evidence_gate→analyze→output_gate→complete이며 근거 부족·지원 밖·실패 경로는 별도로 끝난다. 복잡한 사례는 get_policy_version·retrieve_similar_case를 추가 호출한다. 누적 trace list는 reducer가 필요하고, 같은 키를 여러 병렬 node가 동시에 덮어쓰지 않게 한다. W4에서는 순차 graph부터 검증한다.

graph가 있으면 자동으로 영속 실행되는 것이 아니다. checkpoint backend와 thread_id가 필요하고 state와 애플리케이션 cases 저장은 역할이 다르다. PostgreSQL은 사례·감사·승인 상태의 공유 저장소, checkpoint는 graph를 재개하는 실행 상태다. W4에 스키마·migration·transaction을 만들고 W5에 재개를 검증한다.

### 3. Tool calling은 함수 실행 요청이며 권한 부여가 아니다

모델은 도구 이름과 JSON 인자를 제안한다. 서버가 allowlist·schema·사용자 권한·정책 버전·호출 수를 검증한 뒤 실행한다. 사용자가 ‘tenant=B로 검색해’라고 말해도 실제 tenant는 인증 컨텍스트에서 강제한다. JSON schema는 모양을 제한하지만 업무 권한을 자동 해결하지 않는다.

search_policy(query, allowed_scope), retrieve_similar_case(case_id, allowed_scope), get_policy_version(policy_id, allowed_scope) 세 계약을 정한다. 외부 노출 인자에는 tenant 권한 변경을 넣지 않는다. 결과는 evidence IDs·version·status·truncated flag로 제한하고 원문 과다 반환을 막는다.

Tool stub은 성공 경로 형식을 시험하지만 실제 저장소 검색을 대체하지 않는다. provider adapter는 모델명·timeout·사용량 반환을 숨기지 않는 얇은 연결부로 둔다. 도구를 바꿔도 graph state와 응답 schema가 유지되는지를 계약 테스트로 확인한다.

### 4. Retry·timeout·idempotency: 실패는 설계의 일부다

timeout은 한 호출을 얼마나 기다릴지, deadline은 전체 요청 시간 예산이다. 각 도구에 최대 2회 retry, 전체 tool call 4회 같은 한도를 프로젝트 설정으로 정한다. 입력 오류·권한 거부는 retry하지 않고 429/일시 네트워크 장애에만 제한 재시도를 한다. retry가 비용과 전체 시간을 늘리는 것도 기록한다.

fallback은 실패를 숨기는 일반 답변이 아니라 명시된 결과다. 모델 장애면 검색 근거만 반환하거나 FAILED/의존 서비스 불가 상태를 사용한다. fixture 결과를 실제 모델 답변처럼 바꾸지 않는다. trace에는 route·node·tool 이름·duration·error category·request ID를 기록하되 원문 개인정보는 남기지 않는다.

idempotency는 재실행해도 중복 부작용을 만들지 않는 성질이다. 읽기 도구도 rate limit·비용이 있으므로 호출 수를 제한하고, 사례 생성과 감사 쓰기는 request ID와 UNIQUE 제약을 사용한다. LangGraph 재개·retry 때 node가 다시 실행될 수 있으니 W5 승인 전후 쓰기 위치를 검토한다.



## 따라 하는 실습과 예상 결과

simple/complex/unsupported 각 5개와 unknown tool·잘못된 인자·timeout·429·연속 실패를 포함한 최소 20개 경로 시험을 만든다. 각 요청에 기대 route·tool 호출 수·종료 상태를 라벨링한다. 정상은 tool trace와 evidence IDs가 남고, 최대 호출 수를 넘는 모델은 stop 상태로 끝나야 한다.

PostgreSQL migration으로 cases, audit_events를 만든다. 같은 idempotency key의 중복 접수, 다른 payload 충돌, 프로세스 재시작 뒤 조회를 재현한다. 기존 API의 202 계약을 유지할 경우 작업을 실제 실행하는 경로와 polling 상태를 연결한다. worker 큐가 없으면 개발용 동기 실행 범위를 분명히 설명하고 운영용 장기 큐를 구현했다고 쓰지 않는다.

## 코드로 확인하는 핵심 원리

먼저 모델 없이 routing 기준선을 만든다. 아래 규칙은 교육용이며 제품 수준 의미 분류기로 간주하지 않는다.

```python
def choose_route(question: str, is_supported: bool) -> str:
    """허용 범위 안의 질문을 제한된 실행 경로로 분류한다.

    Args:
        question: 정리된 사용자 질문.
        is_supported: 서버가 판정한 지원 여부.
    Returns:
        unsupported, complex, simple 중 하나.
    Raises:
        ValueError: question이 공백일 때.
    """
    if not question.strip():
        raise ValueError('question must not be blank')
    if not is_supported:
        return 'unsupported'
    # 학습용 규칙 기준선이다. 실제 복잡도는 라벨 데이터로 평가한다.
    return 'complex' if 'compare' in question.lower() else 'simple'

assert choose_route('Compare policy versions', True) == 'complex'
assert choose_route('Reset password', False) == 'unsupported'
```

**복잡도와 병목:** 예제 문자열 정리는 O(L), 공간 O(L). graph 비용은 실행 node·tool 횟수와 모델 token 수에 비례한다. bounded loop·외부 timeout이 전체 지연 상한을 관리한다.

## 프로젝트에서 빌드할 부분

### W4.1 Workflow·state·3개 도구 계약 확정 · 5h

**왜 필요한가:** 다음 구현을 판단할 계약·데이터·환경을 먼저 확정한다.

**수정/작성 위치:** app/agents/state.py, app/tools/, docs/contracts.md

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W3 완료 gate가 선행한다.

**완료 조건:** route·risk를 구분하고 tool allowlist·schema·trusted tenant·출력 limit·호출 한도를 문서화한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W4.2 LangGraph 실행·routing·tool trace 연결 · 6h

**왜 필요한가:** 개념을 실제 핵심 경로에 연결해 다음 검증의 기준선을 만든다.

**수정/작성 위치:** app/agents/graph.py, app/tools/, tests/agents/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W4.1의 산출물이 선행한다.

**완료 조건:** simple/complex/unsupported를 실제 데이터 경로로 실행하고 node/tool/evidence/종료 상태 trace를 남긴다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W4.3 PostgreSQL 영속 사례·멱등성·실패 제어 구현 · 6h

**왜 필요한가:** 실패·권한·복구 경계를 구현해 정상 시연만으로 놓치는 문제를 찾는다.

**수정/작성 위치:** app/repositories/, migrations/, tests/integration/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W4.2의 산출물이 선행한다.

**완료 조건:** 재시작 후 조회·중복 접수·충돌·timeout·429·최대 호출 경로를 검증하고 key/payload UNIQUE 처리를 기록한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W4.4 20경로 검증·Architecture v2·MVP 데모 · 5h

**왜 필요한가:** 검증 결과를 설계 결정과 다른 사람이 확인할 증거로 바꾼다.

**수정/작성 위치:** reports/w04/, docs/architecture.md, docs/evidence/w04.md

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W4.3의 산출물이 선행한다.

**완료 조건:** 20개 기대/실제 경로·실패 원인·현재/목표 구조·2분 MVP 설명을 남긴다. 모형/실제 도구 호출을 구분한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.



## 주차 완료 기준

- [ ] 3개 read-only tool이 schema·권한·호출 제한을 가진 실제 경로로 연결됨
- [ ] 20경로 시험과 전체 실행 trace가 존재함
- [ ] 사례 영속성·중복 방지·서비스 장애 종료 경로가 재현됨
- [ ] Architecture v2와 MVP 데모에 agent 선택 이유를 설명함

## 이해 확인 퀴즈

**Q1. Tool JSON이 유효하면 실행해도 되는가?**

<details>
<summary>해설 확인</summary>

schema 외에 권한·allowlist·scope·호출 한도 검증이 필요하다.

</details>

**Q2. graph를 쓰면 자동으로 프로세스 재시작을 복구하나?**

<details>
<summary>해설 확인</summary>

durable checkpoint와 thread ID·공유 저장·재실행 안전성이 따로 필요하다.

</details>

**Q3. 모든 오류를 retry하면 안전해지는가?**

<details>
<summary>해설 확인</summary>

입력/권한 오류는 개선되지 않고 비용만 늘어난다. transient failure만 시간 예산 안에서 재시도한다.

</details>



## 면접에서 설명할 한 문장

“이번 주에는 검색·사례 조회·정책 버전 도구를 제한된 업무 흐름으로 묶고, 실행 경로와 실패를 추적한다. 이를 확인한 증거는 ___이며, 아직 확인하지 못한 범위는 ___입니다.”

기술 이름을 외우기보다 선택 이유·실패 경우·측정 조건·대안을 자기 말로 설명한다.

## 공식 자료: 읽을 범위와 사용법

- [LangGraph workflows/agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [PostgreSQL transaction](https://www.postgresql.org/docs/current/tutorial-transactions.html) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.

문서 URL은 2026-10-01 확인. 설치/API 세부는 실습 시 사용 버전의 공식 문서를 다시 확인한다. 본 강의 설명·실습·프로젝트 판단 기준은 이 포트폴리오를 위해 작성한 교육 내용이다.

## 선택 심화·환경이 막힐 때

멀티에이전트·병렬 fan-out·장기 작업 큐는 선택 심화. 필수는 bounded graph와 재현 가능한 실패 처리다.

핵심 gate가 안 되면 Jira에 실패 증상·환경·시도·다음 행동을 기록한다. fixture로 계약 학습을 이어 갈 수 있지만 real DB/model/cloud/GPU 완료로 바꾸지 않는다.


## Jira 실행 작업 바로가기

| 순서 | 작업·시간 | 선행 |
|---|---|---|
| 4.1 | [SCRUM-26](https://realrho-1790798942092.atlassian.net/browse/SCRUM-26) · Workflow·state·3개 도구 계약 확정 · 5h | SCRUM-8 |
| 4.2 | [SCRUM-27](https://realrho-1790798942092.atlassian.net/browse/SCRUM-27) · LangGraph 실행·routing·tool trace 연결 · 6h | SCRUM-26 |
| 4.3 | [SCRUM-28](https://realrho-1790798942092.atlassian.net/browse/SCRUM-28) · PostgreSQL 영속 사례·멱등성·실패 제어 구현 · 6h | SCRUM-27 |
| 4.4 | [SCRUM-29](https://realrho-1790798942092.atlassian.net/browse/SCRUM-29) · 20경로 검증·Architecture v2·MVP 데모 · 5h | SCRUM-28 |

## 구현 레시피 · 도구 계약과 영속 상태

### 도구는 서버가 권한을 주입한다

모델이 제안하는 인자 예시:

~~~json
{"tool_name":"search_policy","arguments":{"query":"환불 접수 기간","top_k":5}}
~~~

trusted tenant는 모델 인자가 아니라 executor가 인증 컨텍스트에서 강제한다. 반환 값은 evidence IDs/version/status로 제한한다. unknown tool·top_k 범위 밖·허용 밖 case ID는 실행 전에 거절한다.

1. state.py에 case_id·trusted scope·route·evidence·tool trace·status 타입을 적는다.
2. graph.py는 validate→route→retrieve→evidence gate→analyze→output gate 순서부터 만든다.
3. 도구 3개는 repository/retriever를 호출하고 결과 제한·schema를 공유한다.
4. executor에 retry 대상·max attempts·deadline·max tool calls를 설정한다.
5. PostgreSQL migration에 cases·audit_events·idempotency-key UNIQUE와 상태 revision을 만든다.
6. API/service/repository/checkpoint 역할을 구분한다. 202 뒤 실제 작업 실행/polling이 연결되지 않으면 intake-only로 표시한다.
7. trace와 test를 같은 request_id/case_id로 연결한다.

### 상태 전이의 검증

~~~text
simple      → retrieve → evidence gate → analyze → output gate → COMPLETED
no evidence → retrieve → evidence gate → INSUFFICIENT_EVIDENCE
unsupported → route → UNSUPPORTED
tool outage → bounded retry → FAILED 또는 명시된 degraded 결과
~~~

5개씩 route 사례와 5개 실패/변조를 최소 20개 시험에 포함한다. process restart 뒤 저장 사례가 조회되고, 같은 idempotency-key+다른 payload가 409인지 확인한다.

### 막힐 때 확인 순서

node state 누락→schema/반환 키→edge 종료 조건→tool allowlist→scope→DB migration→deadline을 본다. 무한 loop를 recursion limit 숫자만 올려 해결하지 말고 종료 규칙과 호출 budget을 수정한다.
