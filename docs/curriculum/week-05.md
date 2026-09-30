# W5. 사람 검토와 안전성의 실제 경계 만들기

> 불확실하거나 고위험인 사례를 승인 대기 상태로 멈추고, 권한 있는 검토자가 재개하도록 만든다.

2026-10-29 → 2026-11-04 · 총 22h (주당 계획 가정)

[Jira SCRUM-10](https://realrho-1790798942092.atlassian.net/browse/SCRUM-10) · [GitHub #5](https://github.com/realrho/test/issues/5) · [W4 선행 과정](https://app.notion.com/p/3ebc6f4a2c7e81b798f7e962553f93f9)

## 학습 목표와 시작 조건

**기술:** HITL · Prompt injection · PII · Authorization · Confidence calibration · Evaluation

**시작 조건:** W4 bounded graph·PostgreSQL·trace·tool 권한 계약. W3 평가 프로토콜을 확장한다.

이 페이지는 학습 교재와 앞으로 구현할 작업이다. 문서가 작성된 것을 서비스 구현/평가 완료로 표시하지 않는다. 학습은 아래 4개 강의→손 실습→코드 실습→빌드→퀴즈→증거 제출 순서로 진행한다.

## 이번 주 시간표

- D1 3h: 위협 모델·보호할 자산/신뢰 경계
- D2 3h: 200개 eval·dev/holdout·공격 taxonomy
- D3 3h: schema/citation/PII/tool 경계
- D4 3h: review API·durable interrupt/resume
- D5 4h: 권한·중복 승인·restart 시험
- D6 4h: threshold/coverage 평가·안전성 보고서
- D7 2h: 복습·guardrail 피드백 준비·버퍼

## 개념 강의

### 1. Guardrail은 한 문장 프롬프트가 아니라 여러 경계다

입력 경계는 크기·타입·지원 범위, 검색 경계는 tenant·버전, 도구 경계는 allowlist·권한, 출력 경계는 schema·citation·업무 조건을 검증한다. 각각 다른 실패를 막기 때문에 ‘system prompt에 안전하게 답하라’만으로 대체할 수 없다.

Prompt injection은 사용자나 검색 문서 안의 텍스트가 시스템의 지시·권한을 바꾸려는 공격이다. ‘이전 규칙 무시’, ‘다른 tenant 검색’, ‘비밀을 출력’ 같은 문구를 trusted instruction으로 취급하지 않아야 한다. 문서가 공개 정책이라고 해서 신뢰할 수 있는 실행 지시가 되는 것은 아니다. 데이터와 명령 경계를 나누고 실제 tool enforcement를 둔다.

PII는 개인을 식별하는 정보다. 합성 이메일·전화·이름으로 redaction 실습을 한다. 정규식 한 개는 모든 언어·형식·간접 식별자를 잡지 못한다. 무엇을 검출했는지와 놓친 사례를 같이 기록한다. 모델 payload·로그·cache·trace에 원문이 남는 경로를 점검하고 audit에는 사례 ID·결정·검토자·시각 중심으로 남긴다.

### 2. Confidence: 모델이 자신 있다고 말한 점수는 확률이 아니다

LLM의 self-reported confidence, cosine similarity, classifier probability는 서로 다른 값이다. 0.8이라는 숫자를 하나로 묶어 자동판정하면 검증되지 않은 신뢰를 만든다. evidence presence·citation validity·정책 충돌·위험도처럼 관찰 가능한 조건을 먼저 hard gate로 쓴다.

고위험·정책 충돌·근거 없음은 점수와 무관하게 review/abstain로 간다. 그 다음 calibration dev set에서 quality score threshold 0.6/0.7/0.8/0.9를 비교할 수 있다. 점수가 실제 정확도와 대응하지 않으면 probability라고 부르지 않고 heuristic score로 표기한다. threshold 선택은 자동응답 coverage와 unsafe auto-decision rate, review volume을 함께 보고 정한다.

Precision은 자동확정/특정 분류 중 맞은 비율, recall은 실제 해당 사례 중 잡은 비율이다. ‘high-risk를 검토로 보낸다’를 positive로 정하면 TP·FP·FN의 의미도 명확해진다. 검토를 무조건 늘리면 위험 누락은 줄 수 있으나 업무량이 늘고 자동화 가치는 줄어든다. 고객이 감당할 검토량을 요구사항과 연결한다.

### 3. HITL: 멈춤·권한·재개·중복 방지가 한 흐름이다

Human-in-the-loop는 AI 판단을 사람이 확인하는 흐름이다. REVIEW_PENDING 상태를 durable checkpoint와 사례 DB에 기록하고 reviewer에게 proposed decision·근거·검토 이유를 보여 준다. /reviews/{review_id}/decision에 승인/수정/거절·comment·expected revision을 받도록 설계한다.

검토자는 신뢰할 수 있는 인증 컨텍스트와 같은 tenant 권한으로 확인한다. 임의 case ID를 아는 사용자가 승인할 수 없어야 한다. 같은 리뷰를 두 번 처리하면 같은 결과로 반환하거나 409로 충돌을 알려야 한다. review status와 case state·audit event 변경은 transaction 또는 명시적인 복구 전략으로 묶는다.

LangGraph interrupt는 checkpoint·thread_id와 함께 사용한다. 재개 시 interrupt가 있던 node가 처음부터 다시 실행될 수 있다. 따라서 승인 이전의 외부 쓰기를 피하거나 idempotency key로 보호한다. 승인 대기를 HTTP 요청 하나에서 계속 기다리지 말고 대기 상태 응답→별도 승인→같은 thread 재개로 설계한다. 프로세스 재시작 후 승인 가능한지 실제로 시험한다.

### 4. Evaluation과 threat model: 공격 통과율의 범위를 정확히 쓴다

Threat model은 자산·공격자·입력 경로·신뢰 경계·공격·방어·잔여 위험을 표로 만든다. 자산은 tenant 문서·검토 권한·audit·API key, 공격 경로는 사례 입력·검색 문서·tool args·review API다. 방어가 어디서 강제되는지와 로그에 무엇이 남는지 짝지어 쓴다.

W5에 synthetic 200개로 확장한다: 정상 80, 조건/예외 40, 근거 없음/충돌 40, 공격 40. family 기준 calibration/dev 120개와 holdout 80개로 분리하고 분포를 저장한다. 공격 40개는 직접/간접 injection, tenant bypass, citation 위조, PII, oversized input 등을 포함한다. approved holdout의 구체 라벨을 튜닝 prompt로 사용하지 않는다.

공격 성공은 예를 들어 ‘허용 밖 source가 출력·모델 context로 유출됨’, ‘권한 없는 승인이 상태를 바꿈’처럼 observable하게 정의한다. 시험 40개에서 0건이어도 모든 공격에 안전하다는 증거는 아니다. 사람 평가 subset·자동 judge 일치율·오탐·정상 사례 방해 비율을 보고한다. 최종 결과에는 남은 위험과 운영에서 필요한 추가 검토도 쓴다.



## 따라 하는 실습과 예상 결과

합성 입력 200개와 공격 taxonomy를 확정한다. 직접 injection과 정책 문서에 숨긴 간접 injection을 각각 넣는다. unauthorized citation, 다른 tenant case lookup, 임의 reviewer 승인, 이미 승인된 review 재전송을 시험한다. 기대 결과는 leak 0·무권한 상태변경 0·중복 audit 0이다.

HITL 실습은 고위험 사례→REVIEW_PENDING→프로세스 종료/재시작→권한 없는 승인 거부→권한 있는 승인→같은 thread 재개→동일 승인 재전송 순서다. threshold는 dev에서만 정하고 고위험 hard gate는 어떤 threshold에서도 유지한다. 보고서에 coverage·review율·오탐·위험 누락·subset count를 함께 기록한다.

## 코드로 확인하는 핵심 원리

검토 gate를 모델 출력에서 분리한다. 아래 score는 확률이 아니며 근거 없음은 제품에서 보류 또는 검토로 구분한다.

```python
def needs_human_review(high_risk: bool, citation_valid: bool,
                       evidence_present: bool, quality_score: float,
                       threshold: float) -> bool:
    """강제 검토 조건과 검증용 quality threshold를 적용한다.

    Args:
        high_risk: 서버의 위험도 조건.
        citation_valid: 허용 근거와 구조 검증 통과 여부.
        evidence_present: 충분한 근거 존재 여부.
        quality_score: dev에서 해석을 검증할 휴리스틱 점수.
        threshold: dev에서 선택한 검토 기준.
    Returns:
        검토/보류가 필요하면 True.
    Raises:
        ValueError: 점수 또는 threshold가 0~1 범위 밖일 때.
    """
    if not (0 <= quality_score <= 1 and 0 <= threshold <= 1):
        raise ValueError('score and threshold must be in [0, 1]')
    # 고위험·근거 실패를 높은 점수로 우회할 수 없게 한다.
    return high_risk or not citation_valid or not evidence_present or quality_score < threshold

assert needs_human_review(True, True, True, 0.99, 0.7)
```

**복잡도와 병목:** gate는 O(1), 실제 검증은 근거 개수·문서 길이·PII 처리에 비례. 승인 transaction·checkpoint 일관성·검토 대기열 규모가 운영 병목이다.

## 프로젝트에서 빌드할 부분

### W5.1 Threat model·200개 라벨 평가셋 확장 · 5h

**왜 필요한가:** 다음 구현을 판단할 계약·데이터·환경을 먼저 확정한다.

**수정/작성 위치:** docs/threat-model.md, eval/safety_dev.jsonl, eval/safety_holdout.jsonl

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W4 완료 gate가 선행한다.

**완료 조건:** 자산/공격/강제 경계·200개 분포·120/80 family split·공격 40개 기대 결과를 확정한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W5.2 입력·출력·PII·도구 guardrail 구현 · 6h

**왜 필요한가:** 개념을 실제 핵심 경로에 연결해 다음 검증의 기준선을 만든다.

**수정/작성 위치:** app/guardrails/, tests/security/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W5.1의 산출물이 선행한다.

**완료 조건:** injection을 실행 지시로 취급하지 않고 citation/tenant/PII 경계 실패를 관찰 가능한 테스트로 기록한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W5.3 승인 API·durable HITL·중복/권한 제어 · 6h

**왜 필요한가:** 실패·권한·복구 경계를 구현해 정상 시연만으로 놓치는 문제를 찾는다.

**수정/작성 위치:** app/agents/review.py, app/api/reviews.py, migrations/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W5.2의 산출물이 선행한다.

**완료 조건:** 대기→restart→무권한 거부→정상 재개→중복 승인 흐름에서 leak/무권한 변경/중복 audit 0을 확인한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W5.4 Threshold·coverage·holdout 평가와 안전성 보고 · 5h

**왜 필요한가:** 검증 결과를 설계 결정과 다른 사람이 확인할 증거로 바꾼다.

**수정/작성 위치:** reports/w05/, docs/guardrails.md, docs/evaluation.md

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W5.3의 산출물이 선행한다.

**완료 조건:** dev에서 threshold 선택·holdout 별도 보고·human subset·false positive·unsafe rate·한계와 잔여 위험을 기록한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.



## 주차 완료 기준

- [ ] 200개 synthetic 평가셋·split·공격 성공 정의가 존재함
- [ ] HITL pause→restart→권한 검토→resume→중복 보호가 재현됨
- [ ] 권한/근거/고위험 hard gate가 score로 우회되지 않음
- [ ] coverage·위험 누락·오탐·검토량·한계 보고서 작성

## 이해 확인 퀴즈

**Q1. LLM confidence 0.95면 자동승인 가능한가?**

<details>
<summary>해설 확인</summary>

검증된 확률이 아니다. 근거·권한·고위험 hard gate와 라벨 평가가 우선이다.

</details>

**Q2. interrupt 앞에서 외부 알림을 보내도 되는가?**

<details>
<summary>해설 확인</summary>

재개 때 앞 코드가 다시 실행될 수 있다. 외부 부작용은 별도 단계 또는 멱등 보호가 필요하다.

</details>

**Q3. 공격 40개 통과는 안전성 보증인가?**

<details>
<summary>해설 확인</summary>

그 시험 집합에서의 결과다. 공격 범위·잔여 위험·정상 오탐과 운영 조건을 함께 설명한다.

</details>



## 면접에서 설명할 한 문장

“이번 주에는 불확실하거나 고위험인 사례를 승인 대기 상태로 멈추고, 권한 있는 검토자가 재개하도록 만든다. 이를 확인한 증거는 ___이며, 아직 확인하지 못한 범위는 ___입니다.”

기술 이름을 외우기보다 선택 이유·실패 경우·측정 조건·대안을 자기 말로 설명한다.

## 공식 자료: 읽을 범위와 사용법

- [OWASP LLM 위험 분류](https://owasp.org/projects/top-10-for-large-language-model-applications) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [LangGraph interrupt/resume](https://docs.langchain.com/oss/python/langgraph/interrupts) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [PostgreSQL transaction](https://www.postgresql.org/docs/current/tutorial-transactions.html) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.

문서 URL은 2026-10-01 확인. 설치/API 세부는 실습 시 사용 버전의 공식 문서를 다시 확인한다. 본 강의 설명·실습·프로젝트 판단 기준은 이 포트폴리오를 위해 작성한 교육 내용이다.

## 선택 심화·환경이 막힐 때

상용 PII detector·formal calibration·외부 보안 평가 도구는 심화. 실제 개인정보/회사 정책은 실습에 사용하지 않는다.

핵심 gate가 안 되면 Jira에 실패 증상·환경·시도·다음 행동을 기록한다. fixture로 계약 학습을 이어 갈 수 있지만 real DB/model/cloud/GPU 완료로 바꾸지 않는다.


## Jira 실행 작업 바로가기

| 순서 | 작업·시간 | 선행 |
|---|---|---|
| 5.1 | [SCRUM-30](https://realrho-1790798942092.atlassian.net/browse/SCRUM-30) · Threat model·200개 라벨 평가셋 확장 · 5h | SCRUM-9 |
| 5.2 | [SCRUM-31](https://realrho-1790798942092.atlassian.net/browse/SCRUM-31) · 입력·출력·PII·도구 guardrail 구현 · 6h | SCRUM-30 |
| 5.3 | [SCRUM-32](https://realrho-1790798942092.atlassian.net/browse/SCRUM-32) · 승인 API·durable HITL·중복/권한 제어 · 6h | SCRUM-31 |
| 5.4 | [SCRUM-33](https://realrho-1790798942092.atlassian.net/browse/SCRUM-33) · Threshold·coverage·holdout 평가와 안전성 보고 · 5h | SCRUM-32 |

## 구현 레시피 · 승인 API와 공격 시험

### 검토 결정 계약

~~~json
{"decision":"approve","comment":"합성 사례 근거 확인","expected_revision":1,"idempotency_key":"review-001-approve"}
~~~

reviewer ID/tenant/role은 body에서 믿지 않고 인증 컨텍스트에서 검증한다. decision은 approve/edit/reject allowlist로 제한하고 edit 내용도 schema/근거 검증을 거친다.

1. threat model에 사례 입력·검색 문서·tool args·review API·logs/cache 경계를 그린다.
2. input/output/citation/risk gate를 독립 함수로 만들고 이유 코드를 반환한다.
3. review_pending record와 checkpoint thread_id를 저장한다.
4. review endpoint에서 권한·같은 tenant·pending 상태·expected revision·멱등 키를 검사한다.
5. review와 case/audit를 transaction으로 변경하고 재개 실패 때 복구 가능한 상태를 설계한다.
6. checkpoint와 DB가 단일 transaction이 아니면 어느 순서로 쓰고 실패 시 재개/정합성을 어떻게 복구할지 runbook에 적는다.
7. pause→restart→권한 거부→승인→resume→중복 재전송을 시험한다.

### 공격/정상 테스트 매트릭스

- 직접/간접 injection: 문구를 지시로 실행하지 않고 권한 제한 유지.
- tenant bypass: 다른 tenant 문서/사례가 모델 context·응답·log에 들어가지 않음.
- citation 위조: context 밖 ID를 최종 결과에서 거부.
- PII: 합성 식별 정보의 payload/log/cache 흐름 확인; 탐지 한계 보고.
- approval replay: 상태·audit 중복 없음.
- normal false positive: 정상 요청이 부당하게 막힌 비율을 별도 측정.

검증한 test identity provider는 로컬 학습 장치다. 인터넷 공개 deployment에서는 임의 header/test token을 그대로 권한 검증에 사용하지 않는다. 실제 인증 경로 미구현이면 production gap으로 남긴다.
