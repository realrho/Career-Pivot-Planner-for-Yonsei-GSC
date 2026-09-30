# W3. 근거 있는 답변과 평가 기준선 만들기

> 검색 실패와 생성 실패를 나눠 측정하고, 출처가 있는 답변 또는 근거 부족을 일관되게 반환한다.

2026-10-15 → 2026-10-21 · 총 22h (주당 계획 가정)

[Jira SCRUM-8](https://realrho-1790798942092.atlassian.net/browse/SCRUM-8) · [GitHub #3](https://github.com/realrho/test/issues/3) · [W2 선행 과정](https://app.notion.com/p/3ebc6f4a2c7e819fae0cd5cb69a99181)

## 학습 목표와 시작 조건

**기술:** Hybrid retrieval · RRF · Citation RAG · Abstention · Recall/MRR · 실험 설계

**시작 조건:** W2 corpus·real Milvus 검색·metadata filter. 인프라가 막혔으면 fixture 평가와 실제 검색 평가를 따로 진행한다.

이 페이지는 학습 교재와 앞으로 구현할 작업이다. 문서가 작성된 것을 서비스 구현/평가 완료로 표시하지 않는다. 학습은 아래 4개 강의→손 실습→코드 실습→빌드→퀴즈→증거 제출 순서로 진행한다.

## 이번 주 시간표

- D1 3h: dense/lexical/RRF·지표 손계산
- D2 3h: 50질문 라벨·dev/holdout 분리
- D3 3h: dense 기준선 결과 저장
- D4 3h: RRF 검색·citation schema
- D5 4h: 모델 연결·근거 부족·citation 검증
- D6 4h: 고정 설정 평가·실패 10개·Architecture v1
- D7 2h: 복습·SA 피드백 준비·버퍼

## 개념 강의

### 1. Hybrid retrieval: 의미와 정확한 단어를 함께 쓴다

Dense retrieval은 임베딩의 의미 유사도를 이용한다. Lexical retrieval은 단어·문서 빈도처럼 텍스트 일치에 의존한다. ‘계정 탈취 의심’ 같은 표현 변화는 dense가 유리할 수 있지만 ‘POL-017’, 숫자 한도, 버전명은 lexical이 유리할 수 있다. 같은 질문 집합에서 둘의 실패를 관찰한 다음 결합한다.

BM25 점수와 cosine 점수는 척도가 달라 그대로 더하면 해석하기 어렵다. Reciprocal Rank Fusion은 점수 대신 각 결과의 순위를 이용한다. 한 문서의 fusion 값은 각 검색기의 1/(c+rank) 합이다. c=60은 출발 설정이지 보편 최적값이 아니다. tenant/version filter는 두 검색 경로 모두 적용한다.

reranker는 먼저 가져온 후보와 질문을 같이 읽고 순서를 다시 정한다. 전체 corpus를 rerank하면 느리므로 후보 20개→재정렬→최종 5개처럼 범위를 정한다. W3 필수는 dense 기준선 대비 lexical+RRF 한 가지 개선이다. reranker/query rewriting은 선택 과정으로 미룬다. 구성요소가 늘었다는 이유만으로 품질 개선을 주장하지 않는다.

### 2. Generation과 citation: 근거를 줘도 사실 확인은 별도다

Prompt는 역할·작업·허용된 근거·출력 schema·근거 부족 처리로 구성한다. 사용자 사례와 검색 문서는 신뢰할 수 없는 데이터로 구분해서 전달한다. 출력은 decision, rationale, evidence_ids, policy_version, status 구조다. 모델이 임의 URL을 만들게 하지 말고 서버가 evidence ID를 corpus metadata에 연결해 URL/section을 채운다.

citation 검증은 두 층이다. 구조 검증은 ID가 존재하고 허용 tenant·활성 버전·검색 context 안에 있는지 확인한다. 의미 검증은 해당 문장이 실제 결론을 지지하는지 확인한다. 존재하는 section ID라고 그 답변을 뒷받침한다는 뜻은 아니다. 숫자·기간·예외 조건을 원문과 대조하고 사람이 검토한 라벨을 남긴다.

근거 없음은 INSUFFICIENT_EVIDENCE로 끝내거나 W5의 사람 검토 대상으로 보낸다. 무조건 답하도록 지시하면 정답률 지표가 높아 보여도 위험한 추측이 늘 수 있다. 올바른 보류를 별도 지표로 측정한다. 문서가 충돌하거나 오래됐으면 최신이라는 단어를 모델이 말한 것에 기대지 말고 metadata와 유효일로 판단한다.

### 3. 지표를 손으로 계산해야 보고서가 의미를 가진다

질문 q의 정답 section 집합 G와 top-k 검색 집합 R에 대해 Recall@k = 교집합 개수 / G 개수다. Hit@k는 정답이 하나라도 있으면 1이다. MRR@k는 첫 정답의 순위 역수이며 k 안에 없으면 0이다. 정답이 여러 개면 Hit와 Recall의 차이가 커진다.

예: G={A,B}, R=[X,A,Y]이면 Recall@3=1/2, Hit@3=1, reciprocal rank=1/2다. 질문별 값을 평균하되 query 수와 answerable subset을 명시한다. 정답 문서가 없는 no-evidence 질문은 Recall 분모가 0이므로 제외하고 올바른 보류 비율로 따로 측정한다.

답변 평가는 groundedness·정답/조건 충족·citation precision·보류 정확도를 나눈다. LLM judge 점수는 자동 진단 신호로 사용하고 실제 정답으로 부르지 않는다. 사람이 본 10~20개와 judge 결과가 어디서 다른지 확인해야 한다. 보고서에는 metric 정의, dataset 버전, prompt/model/index/commit, 실패 사례를 함께 남긴다.

### 4. 실험 설계: 평가 질문을 답안지로 사용하지 않는다

W3에 50개 라벨 질문을 만든다: 정상 30, 조건/예외 10, 근거 없음 10. 30개 development와 20개 holdout으로 나누고 policy/case template 가족 단위로 분리해 표현만 바뀐 같은 질문이 양쪽에 섞이지 않게 한다. 원문 근거는 corpus에 있어야 하지만 질문의 정답 설명과 라벨을 index에 넣으면 안 된다.

chunk/top-k/prompt는 development로 고른다. 최종 설정을 고정한 뒤 holdout을 한 번 보고, 그 결과로 설정을 바꾸면 새 holdout이 필요하거나 해당 집합을 development로 재분류한다. 기준선과 개선안은 같은 질문·권한·버전·embedding을 사용하고 latency도 함께 비교한다.

‘정확도 90%’를 목표로만 쓰지 말고 어떤 데이터에 어느 유형에서 실패했는지 쓰자. 임의의 모든 품질 수치를 강제하기보다 hard gate는 권한 누출·잘못된 citation·근거 없는 자동확정을 0으로 잡고, 품질 수치는 기준선·개선 폭·통계 한계로 설명한다. 포트폴리오의 50개 synthetic 결과는 실제 고객 분포의 성능 증거가 아니다.



## 따라 하는 실습과 예상 결과

50개 질문과 gold section ID·expected status를 JSONL로 작성한다. dense baseline과 dense+lexical RRF를 동일 dev set에서 비교한다. query별 ranked IDs·first relevant rank·answer·citations·latency를 저장한다. 실험은 두 설정만으로 시작해 실패 10개를 ‘ingestion/chunk/retrieval/권한·버전/generation/citation’ 중 원인으로 분류한다.

손계산 연습: q1 G={A,B}, R=[X,A,B] → Recall=1, Hit=1, RR=1/2. q2 G={C}, R=[C,D,E] → 1,1,1. q3 G={F}, R=[A,B,C] → 0,0,0. 세 질문의 평균 Recall=2/3, Hit=2/3, MRR=1/2. 근거 없는 q4는 이 평균에 넣지 않는다. 개선안이 못 이기면 그대로 보고하고 왜 baseline을 유지하는지 ADR로 남긴다.

## 코드로 확인하는 핵심 원리

평가 라이브러리를 붙이기 전에 Recall을 직접 계산한다. no-evidence 질문은 별도 평가로 보내도록 예외를 둔다.

```python
def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    """중복 section을 제거한 top-k 근거 recall을 반환한다.

    Args:
        retrieved: 순위가 있는 section ID 목록.
        relevant: 사람이 라벨링한 정답 section 집합.
        k: 평가할 양수 cutoff.
    Returns:
        회수한 정답 근거 비율.
    Raises:
        ValueError: k가 양수가 아니거나 정답 집합이 없을 때.
    """
    if k < 1 or not relevant:
        raise ValueError('positive k and answerable gold set required')
    # 반복된 section이 정답 개수를 부풀리지 않도록 집합으로 센다.
    return len(set(retrieved[:k]) & relevant) / len(relevant)

assert recall_at_k(['X', 'A', 'Y'], {'A', 'B'}, 3) == 0.5
```

**복잡도와 병목:** 위 함수는 정답 집합이 주어졌을 때 시간 O(min(k,n)), 추가 공간 O(min(k,n)). RRF 후보 병합·정렬은 후보 m개 기준 O(m log m); 생성 token 수와 reranker가 주요 지연 원인이다.

## 프로젝트에서 빌드할 부분

### W3.1 50질문 gold set·split·지표 정의 확정 · 5h

**왜 필요한가:** 다음 구현을 판단할 계약·데이터·환경을 먼저 확정한다.

**수정/작성 위치:** eval/rag_dev.jsonl, eval/rag_holdout.jsonl, docs/evaluation-protocol.md

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W2 완료 gate가 선행한다.

**완료 조건:** 30/20 split·template family·정답 section·no-evidence 상태를 기록하고 손계산 3개와 코드 계산이 일치한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W3.2 Dense 기준선과 lexical+RRF 검색 비교 · 6h

**왜 필요한가:** 개념을 실제 핵심 경로에 연결해 다음 검증의 기준선을 만든다.

**수정/작성 위치:** app/retrieval/hybrid.py, reports/w03/retrieval.jsonl

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W3.1의 산출물이 선행한다.

**완료 조건:** 동일 질문·권한·version으로 Recall/Hit/MRR와 latency를 비교하고 개선이 없을 때도 실제 결과를 남긴다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W3.3 Citation RAG·보류·출력 검증 구현 · 6h

**왜 필요한가:** 실패·권한·복구 경계를 구현해 정상 시연만으로 놓치는 문제를 찾는다.

**수정/작성 위치:** app/services/rag.py, app/adapters/llm.py, tests/integration/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W3.2의 산출물이 선행한다.

**완료 조건:** 허용 context 밖의 citation을 거부하고 근거 없음·충돌·폐기 버전을 자동확정하지 않는다. mock과 real 모델 실행을 구분한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W3.4 Holdout 평가·실패 분석·Architecture v1 · 5h

**왜 필요한가:** 검증 결과를 설계 결정과 다른 사람이 확인할 증거로 바꾼다.

**수정/작성 위치:** docs/evaluation.md, reports/w03/, docs/architecture.md

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W3.3의 산출물이 선행한다.

**완료 조건:** dataset/model/prompt/index/commit·subset별 metric·실패 10개·baseline 유지 또는 개선 선택 이유를 남긴다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.



## 주차 완료 기준

- [ ] 50개 라벨 질문의 split·provenance·평가 프로토콜 존재
- [ ] dense와 RRF 결과·latency·실패 분석이 재현 가능
- [ ] 실제 LLM citation 답변 또는 근거 부족 상태를 검증
- [ ] 허용 밖 citation/권한 누출을 막고 평가 수치를 실제 결과로만 표시

## 이해 확인 퀴즈

**Q1. 정답 근거가 2개인데 하나를 찾으면 Hit와 Recall은?**

<details>
<summary>해설 확인</summary>

Hit=1, Recall=0.5다. 여러 근거가 필요한 질문에서 Hit만 보고하면 품질을 과장한다.

</details>

**Q2. 없는 답 질문의 Recall은 0인가?**

<details>
<summary>해설 확인</summary>

정답 집합이 비어 분모가 0이다. answerable retrieval과 올바른 abstention을 분리한다.

</details>

**Q3. reranker가 항상 이기지 않으면 실패한 프로젝트인가?**

<details>
<summary>해설 확인</summary>

아니다. 성능·지연·비용의 측정으로 baseline을 선택하는 것도 설계 판단의 증거다.

</details>



## 면접에서 설명할 한 문장

“이번 주에는 검색 실패와 생성 실패를 나눠 측정하고, 출처가 있는 답변 또는 근거 부족을 일관되게 반환한다. 이를 확인한 증거는 ___이며, 아직 확인하지 못한 범위는 ___입니다.”

기술 이름을 외우기보다 선택 이유·실패 경우·측정 조건·대안을 자기 말로 설명한다.

## 공식 자료: 읽을 범위와 사용법

- [Milvus hybrid retrieval](https://milvus.io/docs/multi-vector-search.md) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [Sentence Transformers](https://www.sbert.net/docs/package_reference/sentence_transformer/model.html) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [AWS GenAI 설계 검토](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.

문서 URL은 2026-10-01 확인. 설치/API 세부는 실습 시 사용 버전의 공식 문서를 다시 확인한다. 본 강의 설명·실습·프로젝트 판단 기준은 이 포트폴리오를 위해 작성한 교육 내용이다.

## 선택 심화·환경이 막힐 때

Cross-encoder reranker 한 가지 또는 query rewrite 한 가지를 선택 실험. 동시에 추가하지 않는다.

핵심 gate가 안 되면 Jira에 실패 증상·환경·시도·다음 행동을 기록한다. fixture로 계약 학습을 이어 갈 수 있지만 real DB/model/cloud/GPU 완료로 바꾸지 않는다.


## Jira 실행 작업 바로가기

| 순서 | 작업·시간 | 선행 |
|---|---|---|
| 3.1 | [SCRUM-22](https://realrho-1790798942092.atlassian.net/browse/SCRUM-22) · 50질문 gold set·split·지표 정의 확정 · 5h | SCRUM-7 |
| 3.2 | [SCRUM-23](https://realrho-1790798942092.atlassian.net/browse/SCRUM-23) · Dense 기준선과 lexical+RRF 검색 비교 · 6h | SCRUM-22 |
| 3.3 | [SCRUM-24](https://realrho-1790798942092.atlassian.net/browse/SCRUM-24) · Citation RAG·보류·출력 검증 구현 · 6h | SCRUM-23 |
| 3.4 | [SCRUM-25](https://realrho-1790798942092.atlassian.net/browse/SCRUM-25) · Holdout 평가·실패 분석·Architecture v1 · 5h | SCRUM-24 |

## 구현 레시피 · 평가 레코드와 답변 검증

### 평가 JSONL 한 줄

~~~json
{"id":"q-001","family":"refund-deadline","split":"dev","tenant":"synthetic-a","question":"배송 완료 8일 후 환불 가능한가?","gold_sections":["REFUND-001:v2:eligibility"],"expected_status":"COMPLETED","expected_facts":["7일 이내 접수"]}
~~~

같은 family 변형 질문을 dev/holdout 양쪽에 섞지 않는다. 모델 답변을 그대로 gold로 쓰지 말고 사람이 정책 원문과 대조한다.

1. eval loader는 ID 중복·split/family 충돌·존재하지 않는 gold section을 검사한다.
2. retriever adapter를 고정하고 dense 결과를 baseline JSONL로 저장한다.
3. lexical+RRF를 구현하고 두 경로에 동일 scope/version을 적용한다.
4. rag service는 retrieved evidence와 사용자 text를 데이터로 구분해 모델에 넣고 구조화된 출력을 요청한다.
5. citation validator는 context ID·tenant·활성 version·필드 schema를 검사한다.
6. 정답/조건/근거 지지 여부는 사람 라벨 평가로 보완하고 구조 검증과 별도 수치로 남긴다.
7. config 고정 후 holdout을 실행하고 실패 10개를 원인별로 쓴다.

### 기대 출력 계약

~~~json
{"status":"COMPLETED","decision":"not_eligible","rationale":"접수 기간 조건을 넘었다.","evidence_ids":["REFUND-001:v2:eligibility"],"policy_version":"v2"}
~~~

근거 부족이면 status=INSUFFICIENT_EVIDENCE, decision=null로 두며 임의 citation을 만들지 않는다. 정책 충돌은 확정하지 않고 이유를 기록한다.

### 보고서 표 구성

Baseline / Variant / Answerable n / Recall@5 / MRR@5 / Correct abstention / Citation validity / P95 / run_id. 값은 실제 실행 뒤 채운다. 통과하지 못한 metric은 빈칸이나 실패로 남기고 교육 예시 수치를 복사하지 않는다.
