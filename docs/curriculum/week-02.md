# W2. 문서를 검색 가능한 근거로 만들기

> 버전과 접근 범위가 있는 합성 문서를 중복 없이 수집하고, 질문에 맞는 근거를 검색한다.

2026-10-08 → 2026-10-14 · 총 22h (주당 계획 가정)

[Jira SCRUM-7](https://realrho-1790798942092.atlassian.net/browse/SCRUM-7) · [GitHub #2](https://github.com/realrho/test/issues/2) · [W1 선행 과정](https://app.notion.com/p/3ebc6f4a2c7e817e9b59e2ed884085ed)

## 학습 목표와 시작 조건

**기술:** RAG · Embedding · Chunking · Milvus · Metadata · Docker 기초

**시작 조건:** W1 API 계약·입력 검증. Docker/WSL 확인은 D1. Windows native Milvus Lite 경로를 전제하지 않는다.

이 페이지는 학습 교재와 앞으로 구현할 작업이다. 문서가 작성된 것을 서비스 구현/평가 완료로 표시하지 않는다. 학습은 아래 4개 강의→손 실습→코드 실습→빌드→퀴즈→증거 제출 순서로 진행한다.

## 이번 주 시간표

- D1 3h: RAG/벡터 개념·WSL/Docker 환경 확인
- D2 3h: 합성 corpus 24개·manifest·버전 구조
- D3 3h: chunk·임베딩·collection 구성
- D4 3h: ingestion·stable ID·중복 방지
- D5 4h: search API·tenant/version filter
- D6 4h: 20질문·단일 변수 실험·실패 분석
- D7 2h: 복습·설치 장애 버퍼·기술 우선순위 조정

## 개념 강의

### 1. RAG는 기억을 학습하는 것이 아니라 근거를 찾아 주는 과정이다

RAG는 Retrieval Augmented Generation의 약자다. 질문과 관련된 문서를 먼저 검색하고 그 결과를 모델 입력에 넣는다. 학습된 모델 가중치를 바꾸는 fine-tuning과 다르다. 정책이 자주 바뀌거나 출처를 보여 줘야 하는 고객 문제에는 검색 문서를 갱신하는 방식부터 검증하는 편이 설명하기 쉽다.

전체 과정은 offline ingestion과 online query 두 경로다. ingestion은 문서 읽기→정리→문단 분할→임베딩→저장. query는 사용자 인증/범위 결정→질문 임베딩→허용된 최신 문서 검색→근거 반환이다. 이번 주는 검색 품질을 먼저 관찰하고 생성 답변은 W3에서 붙인다. 모델이 말을 잘하는지보다 맞는 근거가 검색되는지 분리해야 원인을 찾을 수 있다.

### 2. Embedding·cosine·top-k: 숫자 점수의 의미와 한계

Embedding은 텍스트를 숫자 벡터로 변환해 의미가 가까운 텍스트를 비교하게 한다. 동일 모델·차원·전처리로 문서와 질문을 변환해야 한다. 단위 길이로 정규화하면 cosine similarity는 내적과 같아진다. cosine이 0.82라고 정답 확률이 82%인 것은 아니다. 점수 분포는 모델과 데이터에 따라 달라진다.

예를 들어 ‘환불 접수 기간’과 ‘반품 신청 마감’은 단어가 다르지만 의미가 가까울 수 있다. 반대로 ‘P-017’ 같은 정확한 정책 ID는 의미 검색이 약할 수 있어 W3에서 lexical 검색과 비교한다. top-k=5는 높은 순서 5개 후보를 가져오는 규칙이며 ‘5개가 모두 맞다’는 뜻이 아니다.

작은 데이터에서 벡터 전체 비교는 n개 문서·d차원 기준 O(nd)다. 근사 인덱스는 더 큰 집합에서 속도·메모리·검색 누락을 교환한다. 포트폴리오 크기에서는 단순 FLAT 기준선으로 시작하고 HNSW 튜닝은 측정이 필요할 때 선택한다. 더 큰 DB를 쓰는 것과 더 좋은 근거를 얻는 것은 별개다.

### 3. Chunking: 문서의 의미와 출처가 함께 남아야 한다

Chunk는 모델과 검색에 넣는 작은 문서 조각이다. 너무 작으면 예외·조건·표제 정보를 잃고, 너무 크면 관련 없는 문장이 섞여 검색과 토큰 비용이 나빠진다. 300/600/1000은 tokenizer 기준 token 수로 정의하고 overlap도 token 수로 기록한다. 한국어에서는 글자 수와 token 수를 혼동하지 않는다.

먼저 제목·절·문단 경계로 나누고 제한 길이를 넘으면 추가 분할한다. 제목, policy_id, policy_version, section_id, source_url, tenant_id, effective_at, content_hash를 함께 보관한다. 예: ‘환불 가능’이라는 문장만 자르면 ‘배송 완료 7일 이내’ 조건을 놓친다. 질문이 조건을 요구하는지 검사하고 주변 문맥을 넣는다.

임베딩 모델을 바꾸면 차원과 공간이 달라질 수 있으므로 별도 collection 또는 version을 사용해 재색인한다. chunk_id는 policy/version/section/hash를 바탕으로 안정적으로 만든다. 같은 문서를 재실행해도 벡터 수가 늘어나지 않게 upsert 또는 ingestion manifest로 관리한다.

### 4. Metadata와 배포: 권한·버전은 프롬프트로 대신할 수 없다

tenant_id는 사용자 입력이나 LLM 출력으로 믿지 말고 서버가 검증한 사용자 컨텍스트에서 가져온다. tenant와 활성 버전 조건은 검색 시점에 적용한다. 결과를 받은 뒤 숨기기만 하면 unauthorized 문서가 이미 모델 context나 로그에 들어갔을 수 있다. SQL·벡터 filter 문자열은 입력을 직접 이어 붙이지 말고 허용값을 검증한다.

Windows 학습 경로는 WSL2 Ubuntu의 Milvus Lite를 우선하며 Python과 데이터도 같은 WSL 환경에서 사용한다. Docker Desktop+WSL2의 Milvus Standalone은 리소스가 충분할 때 대안이다. 공식 Lite 문서는 Ubuntu/macOS를 지원 환경으로 적고, Standalone 문서는 RAM 8G 요구·16G 권장을 제시한다. 설치 안내는 공식 문서를 따른다.

환경이 막히면 같은 Retriever 계약에 순수 Python fixture 검색을 붙여 API·테스트를 진행한다. fixture는 연결 경로 검증일 뿐 real embedding/Milvus 검색 품질이 아니다. W2 종료 시 Milvus 검증이 안 됐다면 해당 항목은 Blocked로 남긴다. 설치 실패로 모든 학습을 멈추거나 가짜 결과를 쓰지 않는다.



## 따라 하는 실습과 예상 결과

직접 작성한 합성 정책 24개를 두 가상 tenant로 나눈다. 환불·계정접근·보안·개인정보·에스컬레이션·정책버전 주제별 4개로 만들고 서로 충돌하는 v1/v2와 tenant 전용 문서를 포함한다. corpus manifest에 작성자·synthetic·버전·사용 범위를 적는다. 질문 20개와 정답 section ID를 사람이 먼저 정한다.

600 token/overlap 80/top-k 5를 시작 설정으로 사용한다. chunk 크기와 k를 동시에 다 바꾸지 말고 chunk 3개 실험 뒤 k 3개 실험으로 나눈다. 질문별 상위 결과·score·section·version·latency를 CSV/JSONL에 저장한다. 동일 manifest를 두 번 ingest해 개수가 같고, 다른 tenant·폐기 버전은 검색되지 않는지 확인한다.

## 코드로 확인하는 핵심 원리

임베딩 연결 전에 두 벡터의 점수를 손으로 계산한다. 이 예시는 수학 실습이며 의미 검색의 성능 결과는 아니다.

```python
from math import sqrt


def cosine_similarity(left: list[float], right: list[float]) -> float:
    """동일 차원 벡터의 cosine을 반환한다.

    Args:
        left: 문서 벡터.
        right: 질문 벡터.
    Returns:
        정규화된 유사도. 정답 확률이 아니다.
    Raises:
        ValueError: 벡터가 비었거나 차원이 다르거나 영벡터일 때.
    """
    if not left or len(left) != len(right):
        raise ValueError('non-empty matching dimensions required')
    denominator = sqrt(sum(x*x for x in left) * sum(y*y for y in right))
    if denominator == 0:
        raise ValueError('zero vector has no cosine direction')
    # 길이 영향을 없애 방향의 가까움을 비교한다.
    return sum(x*y for x, y in zip(left, right)) / denominator

assert round(cosine_similarity([1.0, 0.0], [1.0, 1.0]), 4) == 0.7071
```

**복잡도와 병목:** cosine 한 번 O(d), 추가 공간 O(1). 전체 문서 선형 검색 O(nd); 임베딩 배치의 메모리와 외부 호출 속도가 ingestion 병목이다.

## 프로젝트에서 빌드할 부분

### W2.1 RAG 실습 환경·합성 corpus/manifest 준비 · 5h

**왜 필요한가:** 다음 구현을 판단할 계약·데이터·환경을 먼저 확정한다.

**수정/작성 위치:** data/synthetic/policies/, data/manifest.json, docs/data-card.md

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W1 완료 gate가 선행한다.

**완료 조건:** 24개 합성 정책·2 tenant·v1/v2·20개 질문/정답 section을 준비하고 Lite/Standalone 환경 또는 blocker를 기록한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W2.2 Chunk·embedding·멱등 ingestion 구현 · 6h

**왜 필요한가:** 개념을 실제 핵심 경로에 연결해 다음 검증의 기준선을 만든다.

**수정/작성 위치:** app/retrieval/ingest.py, app/retrieval/chunking.py, app/adapters/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W2.1의 산출물이 선행한다.

**완료 조건:** stable chunk ID·version·hash·embedding model/dimension을 기록하고 재실행 후 중복이 없음을 확인한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W2.3 Milvus 검색 API와 tenant/version 필터 구현 · 6h

**왜 필요한가:** 실패·권한·복구 경계를 구현해 정상 시연만으로 놓치는 문제를 찾는다.

**수정/작성 위치:** app/retrieval/search.py, app/api/search.py, tests/integration/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W2.2의 산출물이 선행한다.

**완료 조건:** 실제 embedding+Milvus의 검색 결과를 반환하고 다른 tenant/폐기 버전 누출이 0인 테스트 증거를 남긴다. fixture는 별도 표시한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W2.4 20질문 기준선·chunk/k 실험·ADR 기록 · 5h

**왜 필요한가:** 검증 결과를 설계 결정과 다른 사람이 확인할 증거로 바꾼다.

**수정/작성 위치:** eval/retrieval_dev.jsonl, reports/w02/, docs/adr/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W2.3의 산출물이 선행한다.

**완료 조건:** 단일 변수 비교표·query별 결과·latency·실패 원인 5개·선택 설정을 기록하고 실제/fixture 결과를 구분한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.



## 주차 완료 기준

- [ ] 24개 합성 문서의 provenance·version·tenant·hash가 존재함
- [ ] 실제 ingest→Milvus 검색→API 흐름과 중복 방지 검증 완료
- [ ] 권한/활성 버전 필터를 검색 전에 적용하고 누출 시험 통과
- [ ] 20개 라벨 질문 기준선·실패 분석·설정 선택 근거를 기록함

## 이해 확인 퀴즈

**Q1. cosine 0.9는 정답 확률 90%인가?**

<details>
<summary>해설 확인</summary>

아니다. retrieval similarity이며 라벨 데이터로 별도 평가해야 한다.

</details>

**Q2. 정책 업데이트 때 모델을 다시 학습해야 하나?**

<details>
<summary>해설 확인</summary>

RAG는 corpus·index를 갱신한다. 모델 교체가 아니라 문서/검색 버전 관리가 우선이다.

</details>

**Q3. 권한 필터를 모델 프롬프트에 적으면 충분한가?**

<details>
<summary>해설 확인</summary>

서버가 신뢰하는 tenant 범위를 검색에 강제하고 이후 생성·로그에도 허용된 근거만 넘겨야 한다.

</details>



## 면접에서 설명할 한 문장

“이번 주에는 버전과 접근 범위가 있는 합성 문서를 중복 없이 수집하고, 질문에 맞는 근거를 검색한다. 이를 확인한 증거는 ___이며, 아직 확인하지 못한 범위는 ___입니다.”

기술 이름을 외우기보다 선택 이유·실패 경우·측정 조건·대안을 자기 말로 설명한다.

## 공식 자료: 읽을 범위와 사용법

- [Milvus Lite: 지원 환경/연결](https://milvus.io/docs/milvus_lite.md) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [Milvus Standalone: Windows/메모리 조건](https://milvus.io/docs/prerequisite-docker.md) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [SentenceTransformer encode](https://www.sbert.net/docs/package_reference/sentence_transformer/model.html) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [Docker port 개념](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.

문서 URL은 2026-10-01 확인. 설치/API 세부는 실습 시 사용 버전의 공식 문서를 다시 확인한다. 본 강의 설명·실습·프로젝트 판단 기준은 이 포트폴리오를 위해 작성한 교육 내용이다.

## 선택 심화·환경이 막힐 때

GPU embedding·distributed Milvus·HNSW 상세 튜닝은 제외. 로컬 실임베딩 CPU 실행 또는 예산이 정해진 embedding API 중 한 경로만 선택한다.

핵심 gate가 안 되면 Jira에 실패 증상·환경·시도·다음 행동을 기록한다. fixture로 계약 학습을 이어 갈 수 있지만 real DB/model/cloud/GPU 완료로 바꾸지 않는다.


## Jira 실행 작업 바로가기

| 순서 | 작업·시간 | 선행 |
|---|---|---|
| 2.1 | [SCRUM-18](https://realrho-1790798942092.atlassian.net/browse/SCRUM-18) · RAG 실습 환경·합성 corpus/manifest 준비 · 5h | SCRUM-6 |
| 2.2 | [SCRUM-19](https://realrho-1790798942092.atlassian.net/browse/SCRUM-19) · Chunk·embedding·멱등 ingestion 구현 · 6h | SCRUM-18 |
| 2.3 | [SCRUM-20](https://realrho-1790798942092.atlassian.net/browse/SCRUM-20) · Milvus 검색 API와 tenant/version 필터 구현 · 6h | SCRUM-19 |
| 2.4 | [SCRUM-21](https://realrho-1790798942092.atlassian.net/browse/SCRUM-21) · 20질문 기준선·chunk/k 실험·ADR 기록 · 5h | SCRUM-20 |

## 구현 레시피 · 검색 데이터와 실행 순서

### 문서와 chunk의 최소 계약

~~~json
{"policy_id":"REFUND-001","version":"v2","tenant_id":"synthetic-a","section_id":"eligibility","effective_at":"2026-01-01","source_type":"synthetic","text":"환불 요청은 배송 완료 7일 이내 접수한다."}
~~~

chunk 레코드는 위 필드에 chunk_id·content_hash·embedding_model·dimension·index_version을 더한다. 정답 라벨은 corpus가 아니라 eval 파일에만 저장한다. vector와 질문은 같은 embedding 모델/version을 사용한다.

1. data/synthetic/policies/ 문서를 작성하고 data-card/manifest에 provenance·허용 범위를 적는다.
2. chunking.py는 문단/제목을 보존하고 tokenizer 기준 max/overlap을 받는다. min-length/빈 chunk도 처리한다.
3. ingest.py는 manifest→hash 비교→변경된 문서 분할/임베딩→upsert→삭제/비활성 버전 관리 순서다.
4. search.py는 서버에서 받은 trusted scope를 filter에 강제하고 top-k section/text/version/score를 반환한다.
5. search API는 query·k를 검증하고 사용자가 scope를 바꾸는 인자를 허용하지 않는다.
6. query 20개로 raw 결과를 남기고 같은 ingest를 재실행해 count와 IDs가 유지되는지 확인한다.

### 예상 검색 응답 예시

~~~json
{"index_version":"idx-001","hits":[{"chunk_id":"c-001","policy_id":"REFUND-001","version":"v2","section_id":"eligibility","score":0.81}],"measurement_type":"example_only"}
~~~

이 score는 교육 예시이며 정답 확률/측정값이 아니다. API가 실제 검색을 한 경우 provider/embedding/index/version·실제 score를 별도 기록한다.

### 막힐 때 확인 순서

Lite import/실행 오류→지원 OS와 WSL Python 경로를 확인한다. connection refused→서버 상태·host/container 주소·port를 확인한다. dimension mismatch→model/dimension/collection version을 확인한다. 결과 없음→tenant·활성 버전·effective date·문서 count→query embedding을 순서대로 본다. 권한 filter를 끄고 정상 결과라고 보고하지 않는다.
