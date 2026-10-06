# W4 학습 · RAG·하이브리드 검색과 근거·평가 계약

**기간:** 2026-10-23–2026-10-29 (Asia/Seoul) · **계획:** 22h · [Notion](https://app.notion.com/p/3ebc6f4a2c7e81b798f7e962553f93f9) · [GitHub #4](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/4)

**이번 주 통과 조건:** 근거 ID·문서 버전·tenant가 모든 chunk에 있고 응답 인용 ID가 검색 결과에 속한다. 검색 품질과 답변 품질을 따로 보고한다.

[전체 학습표](README.md) · [책 목차 원문](../book-toc.md) · [용어 사전](../glossary-ko-en.md) · [책/보충 범위](../book-gap-map.md)

## 1. 책 읽기와 필수 실습

**배정:** 9장 LLM 애플리케이션 개발하기 · 10장 임베딩·의미/하이브리드 검색

9.1–9.4는 RAG 저장/검색/프롬프트 통합·응답 캐시·데이터 검증·로깅을 직접 따라간다. 10.1–10.5는 단어 표현→문장 임베딩→바이 인코더→의미 검색→BM25/RRF 하이브리드 순서로 읽는다. 책에 이미 있는 내용을 '없는 기술'로 다시 분류하지 않는다.

**필수 실습:** 공식 9장 기본 RAG와 10장 의미/하이브리드 검색을 작은 텍스트 corpus로 실행한다. 공급자 접근이 없으면 검색까지 실행하고 생성은 fixture로 분리한다. 질문 10개에 대해 keyword/dense/hybrid 검색 결과와 gold 근거 포함 여부를 표로 비교한다.

책 본문은 소유한 책에서 읽는다. [공식 코드](https://github.com/onlybooks/llm)·[정오표](https://www.onlybook.co.kr/entry/llm-errata)를 확인하고 환경/모델/패키지 버전을 기록한다. 선택 GPU/멀티모달 실습의 미실행은 필수 완료와 분리한다.

## 2. 실행 순서·시간·수용 기준

| 순서 | 작업 | 계획 시간 | 완료 기준 | 작업 ID |
|---|---|---|---|---|
| 1 | 책 9·10장 읽기·개념 노트 | 6h | 배정된 모든 절을 읽고 개념 관계·비교·질문을 자신의 말로 기록한다. | W4.1 |
| 2 | 책 필수 실습·환경/결과 기록 | 6h | 공식 9장 기본 RAG와 10장 의미/하이브리드 검색을 작은 텍스트 corpus로 실행한다. 공급자 접근이 없으면 검색까지 실행하고 생성은 fixture로 분리한다. 질문 10개에 대해 keyword/dense/hybrid 검색 결과와 gold 근거 포함 여부를 표로 비교한다. | W4.2 |
| 3 | SA 보충 강의·재사용 실습 자산 만들기 | 8h | 근거 ID·문서 버전·tenant가 모든 chunk에 있고 응답 인용 ID가 검색 결과에 속한다. 검색 품질과 답변 품질을 따로 보고한다. | W4.3 |
| 4 | 퀴즈·설명·증거·다음 주 준비 검토 | 2h | 3개 퀴즈를 해설 없이 설명하고 합성 문서12–24개, chunk manifest, 검색 결과 계약, 개발 질문20개를 버전/실행 상태와 함께 저장한다. | W4.4 |

## 3. SA 보충 강의 · 개념→이유→예제→실습

### 3.1 문서→청크→근거의 계약

RAG, Retrieval-Augmented Generation(검색 증강 생성)은 외부 검색 결과를 모델 입력에 넣어 답변을 만드는 방법이다. chunk(청크)는 검색할 문서 조각이고 metadata(메타데이터)는 그 조각의 출처·버전·권한 정보를 담는다. chunk_id·source_id·tenant_id·document_version·text·content_hash를 저장하면 '어떤 문서의 어느 버전으로 답했는가'를 추적할 수 있다. 긴 청크는 문맥을 보존하지만 검색이 둔해지고, 짧은 청크는 정확한 문장을 찾기 쉽지만 조건이 잘릴 수 있다. overlap(겹침)은 경계 손실을 줄이지만 중복과 비용을 늘린다.

**작동 예시/실패 경계:** 합성 tenant A/B 정책에서 같은 환불 질문의 답을 각각 7일/14일로 정한다. tenant A 요청의 검색 결과에 B 정책이 들어오면 생성 모델에 보내기 전부터 실패다. 문서에 적힌 tenant_id를 그대로 권한으로 신뢰하지 않는다.

**직접 해 보기:** 문서12개를 수작업으로 검사하고 200/400 토큰 또는 문단 단위 청크 두 구성을 비교한다. ID 생성 규칙과 중복 입력 시 갱신 규칙을 적는다. 실제 토큰 수는 선택 토크나이저로 잰다.

### 3.2 검색 지표와 실험 설계

Recall@k(상위 k 검색 재현율)는 정답 근거 중 상위 k에 찾은 비율이다. MRR, Mean Reciprocal Rank(평균 역순위)는 첫 정답의 순위 역수 평균으로 정답이 빨리 나오는 정도를 본다. 관련성 정답이 여러 개면 Recall의 분모에 해당 질문의 모든 gold 근거를 넣는다. score(검색 점수)는 확률이 아니므로 0.8을 바로 80% 신뢰도라고 부를 수 없다. 비교에서는 같은 질문·같은 corpus·같은 권한 조건을 유지하고 청크 크기/k/모델 중 하나를 바꿔 원인을 분리한다.

**작동 예시/실패 경계:** gold={a,b}, 검색=[x,a,y], k=3이면 Recall@3=1/2, reciprocal rank=1/2다. 10개 dev 질문의 k를 조정한 뒤 holdout은 고정 설정으로 한 번 평가한다. 20개 작은 표본이면 지표의 한계도 함께 적는다.

**직접 해 보기:** 개발20질문을 정답 가능·정답 없음·tenant 혼동·버전 혼동 유형으로 나눈다. raw 검색 순위와 버전 config를 JSONL로 남긴다. 전체 평균만 보고하지 말고 유형별 실패를 읽는다.

### 3.3 인용·구조화 출력·답변 보류

citation(인용)은 주장의 근거 출처를 가리킨다. grounding(근거 연결)은 답의 내용이 실제 근거로 뒷받침되는 성질이다. 근거 ID가 존재하는 것은 필요 조건이지만 의미가 맞는다는 충분 조건은 아니다. structured output(구조화 출력)은 JSON 필드/열거값처럼 형태를 제한한다. abstention(답변 보류)은 근거가 부족하거나 범위 밖일 때 답을 만들지 않는 결정이다. 근거 없음·권한 없음·버전 충돌·형식 오류·고위험 조건을 모델 밖의 명시적 규칙과 사람이 확인하는 평가로 연결한다.

**작동 예시/실패 경계:** 모델 결과에 answer, evidence_ids, decision=ANSWER/ABSTAIN/REVIEW를 사용한다. evidence_ids가 검색 결과 밖이면 거부한다. 승인되지 않은 인용을 모델이 '확실하다'고 말해도 통과시키지 않는다. 근거가 질문과 다른 내용을 말하면 ID 검사 이후 의미 평가에서 실패한다.

**직접 해 보기:** 정답 가능/불가능 질문 쌍을 만든다. 검색 근거 ID와 반환 ID의 부분집합 검사를 구현한다. 근거 문장과 답변의 실질적 일치 여부는 사람 평가표에 별도 열로 둔다.

### 3.4 BM25·RRF와 캐시를 운영으로 연결

BM25, Best Matching 25(베스트 매칭25)는 키워드 일치·문서 길이·빈도를 이용하는 검색 점수 방식이다. RRF, Reciprocal Rank Fusion(역순위 융합)은 서로 다른 검색기의 점수 스케일 대신 순위를 합친다. 예를 들어 검색기별 1/(c+rank)를 더하며 c는 실험 설정 상수다. dense retrieval(밀집 벡터 검색)은 의미 유사성에 유리하고 lexical retrieval(어휘 검색)은 정책 코드·고유명사 일치에 유리하다. 어느 하나가 항상 우수하지 않다. 9장의 응답 캐시는 tenant·권한 범위·문서/index·모델·프롬프트·정규화 입력을 구분해야 한다.

**작동 예시/실패 경계:** A/v1에서 얻은 '7일' 응답을 B/v2에 재사용하면 높은 적중률도 실패다. TTL, Time To Live(유효 수명)는 오래된 캐시를 줄이는 시간 장치이고 정책 버전 변경의 즉시 무효화를 보장하지 않는다.

**직접 해 보기:** 세 검색 방식의 Recall/MRR/지연을 비교한다. 캐시 키 명세를 만들고 tenant 또는 버전 하나만 바꾸어 miss가 나는지 확인한다. 실습은 실제 Redis가 없어도 키 계산부터 할 수 있지만 Redis 운영 검증으로 쓰지 않는다.

## 4. 실행 가능한 기초 계약 실습

아래는 핵심 규칙을 작게 분리해 CPU에서 확인하는 접근이다. 라이브러리 설치나 실제 모델 호출 없이 개념을 검증한다. 프로젝트 통합 구현과 증거 수준을 구분한다.

실행: `python labs/week-04/contract_demo.py` (저장소 루트).

```python
"""W4: 다중 정답 검색의 Recall@k와 첫 정답 역순위를 계산한다."""
def retrieval_metrics(ranked_ids: list[str], gold_ids: set[str], k: int) -> tuple[float, float]:
    """하나의 질문에 대한 검색 지표를 계산한다.

    Args:
        ranked_ids: 높은 순위부터 나열한 중복 없는 검색 ID.
        gold_ids: 사람이 정한 정답 근거 ID 집합.
        k: 평가할 상위 검색 개수.
    Returns:
        (Recall@k, 상위 k 안 첫 정답의 역순위). 정답 미검색이면 역순위 0.
    Raises:
        ValueError: k가 양수가 아니거나 gold가 없거나 검색 ID가 중복된 경우.
    """
    if k < 1 or not gold_ids or len(set(ranked_ids)) != len(ranked_ids):
        raise ValueError("invalid metric input")
    top_ids = ranked_ids[:k]
    recall = len(set(top_ids) & gold_ids) / len(gold_ids)
    # 질문별 역순위의 평균을 내면 MRR@k가 된다.
    reciprocal_rank = next((1 / rank for rank, item in enumerate(top_ids, 1)
                            if item in gold_ids), 0.0)
    return recall, reciprocal_rank

assert retrieval_metrics(["x", "a", "y"], {"a", "b"}, 3) == (0.5, 0.5)
assert retrieval_metrics(["x"], {"a"}, 1) == (0.0, 0.0)
print("W4 retrieval arithmetic: passed")
```

**복잡도/병목:** 검색 ID 수 n, gold 수 g, 시간/공간 O(n+g). 실제 검색 엔진 성능을 측정한 코드가 아니다.

## 5. 학습 중 만들 재사용 자산 · 상세 작업

아래 app/data/deployment 파일은 **앞으로 작성할 예정 경로**다. 현재 구현된 것으로 읽지 않는다. 작은 계약 실습을 실제 저장소/모델 경로로 확장하는 작업이다.

### 5.1 합성 corpus와 청크 manifest

예정 `data/synthetic/`에 tenant A/B 각 6–12개의 텍스트 정책을 만든다. source/version/chunk/hash를 정의하고 같은 질문의 답이 tenant·버전에 따라 달라지는 쌍을 넣는다. 개인·회사 원본은 사용하지 않는다.

### 5.2 책 RAG 경로를 작은 라이브러리로 추출

책의 LlamaIndex 예제로 저장→검색→근거 통합을 실행한다. 예정 `app/retrieval/`에 논리 입출력 계약을 남긴다. backend를 여러 개 새로 구현하지 말고 한 경로를 검증한다.

### 5.3 검색 비교표 만들기

keyword/dense/hybrid를 같은 dev 질문에서 비교한다. k·chunk·embedding 버전을 기록하고 gold 근거 포함 여부·순위·지연을 저장한다. 지표 계산 실습을 실제 검색 결과와 연결한다.

### 5.4 구조화 응답의 소속 검사

예정 `app/validation/evidence.py`에서 반환 인용 ID가 권한 범위 내 검색 ID 집합에 속하는지 검사한다. 의미 일치·답변 가능 여부는 사람 평가로 별도 확인한다. 근거가 없으면 ABSTAIN으로 종료한다.

### 5.5 개발 평가 질문 동결 초안

dev 20질문에 answerable/goldIDs/tenant/version을 붙인다. 최종 holdout은 별도 구성하고 dev로 선택한 설정의 조정에 사용하지 않는다.

**다음 통합에 넘길 것:** 합성 문서12–24개, chunk manifest, 검색 결과 계약, 개발 질문20개

## 6. 이해 확인 · 해설을 보기 전에 설명하기

**Q1. 검색 점수0.8은 정답 확률80%인가?**

<details>
<summary>해설</summary>

점수 체계와 검증이 달라 확률로 바로 해석할 수 없다.

</details>

**Q2. 인용 ID가 존재하면 답의 의미도 맞는가?**

<details>
<summary>해설</summary>

형식/소속 검사와 의미 일치 평가는 별개다.

</details>

**Q3. gold2개 중1개가2위면 Recall@3과 reciprocal rank는?**

<details>
<summary>해설</summary>

각각0.5,0.5다. 질문별 계산 후 평균한다.

</details>

## 7. 공식 자료 · 읽을 범위

- [LlamaIndex: RAG·retrieval](https://developers.llamaindex.ai/python/framework/) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.
- [Sentence Transformers](https://www.sbert.net/) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.

## 증거와 완료 상태

학습 노트에는 읽은 절·자신의 설명·실습 명령·Python/패키지/장치·데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 문서/fixture/실제DB·모델/클라우드·GPU의 수준을 구분한다. 자료 작성만으로 본인의 학습 또는 서비스 제작을 완료 처리하지 않는다. 막히면 증상·시도·다음 행동과 일정 영향을 남긴다.
