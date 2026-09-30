# W6. 품질·지연·비용으로 모델과 캐시를 선택하기

> 같은 평가 조건에서 모델 2개를 비교하고, 비용과 품질을 보존하는 cache/routing 결정을 제시한다.

2026-11-05 → 2026-11-11 · 총 22h (주당 계획 가정)

[Jira SCRUM-11](https://realrho-1790798942092.atlassian.net/browse/SCRUM-11) · [GitHub #6](https://github.com/realrho/test/issues/6) · [W5 선행 과정](https://app.notion.com/p/3ebc6f4a2c7e817e9825cec827df9013)

## 학습 목표와 시작 조건

**기술:** P50/P95 · Token accounting · Benchmark design · Redis · Cache invalidation · Model routing

**시작 조건:** W5 안전 gate·평가셋·공유 저장·실행 trace. 실제 모델 API 권한과 예산이 필요하며 없으면 측정은 Blocked로 둔다.

이 페이지는 학습 교재와 앞으로 구현할 작업이다. 문서가 작성된 것을 서비스 구현/평가 완료로 표시하지 않는다. 학습은 아래 4개 강의→손 실습→코드 실습→빌드→퀴즈→증거 제출 순서로 진행한다.

## 이번 주 시간표

- D1 3h: latency/throughput/cost 손계산·예산
- D2 3h: 2모델 adapter·usage/환경 기록
- D3 3h: 동일 조건 baseline benchmark
- D4 3h: Redis key/TTL/version·장애 실습
- D5 4h: context/cache/concurrency 단일 변수 실험
- D6 4h: Pareto 비교·routing ADR·비용 표
- D7 2h: 복습·확인된 skill gap 보완·버퍼

## 개념 강의

### 1. Latency는 평균 한 숫자로 설명되지 않는다

End-to-end latency는 접수·검증·검색·모델·검증·저장 시간을 합한 자동응답 경로다. 사람 승인 대기 시간은 별도 지표로 분리한다. P50은 중앙값, P95는 대부분 요청이 경험하는 꼬리 지연을 보여 준다. streaming TTFT와 최종 응답 완료 시간도 다르다.

Throughput은 초당 처리 요청 수이고 concurrency는 동시에 진행하는 요청 수다. concurrency를 늘리면 rate limit·큐 대기·DB connection 때문에 P95가 오를 수 있다. timeout 요청을 latency 평균에서 빼면 성능이 좋아 보이므로 attempted/succeeded/failed/timed_out 수와 timeout 비율을 같이 보고한다.

같은 머신·지역·질문·context 길이·모델 설정을 고정한다. warm-up을 먼저 실행하고 cold/warm cache를 나눠 측정한다. 최소 모델 2개×50질문×2반복=200 요청을 출발 계획으로 잡되 예산을 먼저 계산한다. 작은 표본의 P95는 불안정하므로 n·반복·날짜·실행 환경을 꼭 쓴다.

### 2. Cost: token 요금 외에도 비용이 있다

모델 요청 비용은 input_tokens×input_unit_price + output_tokens×output_unit_price다. 단가가 백만 token당이면 1,000,000으로 나눈다. 실제 provider usage를 기록하고 cached input·reasoning·retry 등이 청구 규칙에 어떻게 반영되는지 해당 provider 공식 요금과 확인한다. 지금 강의에 특정 모델 가격을 고정해 쓰지 않는다.

교육용 예: 입력 1,000 token·출력 200 token, 가상 단가 input $1/M·output $4/M이면 한 요청 $0.0018, 같은 분포 1,000건 $1.80다. 이는 실제 가격/견적이 아니다. embedding·reranker·cache·DB·VM·네트워크·실패 재시도 비용을 별도 항목으로 더한다.

Cost per 1K attempts와 per 1K successful answers를 나누면 실패 많은 저가 모델을 잘못 추천하지 않게 된다. 사람 검토로 넘긴 비율·검토 시간도 운영 비용 가정이다. 비용 문서에는 출처 URL·조회 날짜·region·currency·usage 계산식을 기록한다. 예산 상한을 configuration으로 두고 초과 전 중단한다.

### 3. Cache: 빠른 답변이 오래된 답변이면 실패다

Redis cache는 반복 조회를 줄이는 저장소다. 검색 cache와 최종 답변 cache를 구분한다. key는 trusted tenant, normalized query hash, policy/index version, prompt version, model version, 권한 범위를 포함한다. 같은 질문이라도 tenant·정책·권한이 다르면 같은 답을 재사용하면 안 된다.

TTL은 최대 보관 시간이다. 정책 변경 때 TTL만 기다리면 오래된 답변이 나갈 수 있으므로 policy/index version을 key에 넣거나 명시적으로 invalidate한다. PII 입력은 저장을 피하거나 허용된 redacted 표현만 쓰고 key에 raw text를 넣지 않는다. HUMAN_REVIEW 결정이나 일시적인 오류를 성공 답변처럼 캐시하지 않는다.

Cache hit율은 특정 반복 질문 분포에서만 의미가 있다. 모든 요청이 서로 다른 benchmark와 반복 FAQ benchmark를 나눠 보고한다. cache가 잠깐 죽으면 miss로 처리해 본 경로가 동작하도록 하되 모델에 갑자기 부하가 몰릴 수 있어 rate limit과 queue capacity를 함께 고려한다.

### 4. Model routing과 Pareto 선택: 한 모델의 최고 점수가 목적이 아니다

작은/저렴한 모델은 쉬운 FAQ에, 어려운 조건 비교는 더 강한 모델에 맡기는 가설을 세울 수 있다. 그러나 routing 실패·재호출·두 모델 비용이 추가된다. W4 route 라벨을 활용하고 동일 guardrail·citation 계약을 모든 모델에 적용한다. 고위험 gate를 값싼 모델의 높은 confidence로 우회하지 않는다.

각 모델은 품질, citation validity, correct abstention, unsafe rate, P50/P95, token usage, 단가로 비교한다. 어떤 모델이 품질·속도·비용 모두에서 나쁘면 dominated option이다. 품질을 조금 올리지만 비용이 크게 늘어나는 선택은 고객의 최소 품질·예산 제약에 따라 결정한다.

최종 ADR은 ‘자동응답 경로 기준선 유지’, ‘특정 route만 상위 모델’, ‘context 축소+cache 적용’ 중 실제 결과에 맞는 결론을 쓴다. local open model·vLLM은 GPU·VRAM·driver·운영 시간이 따로 들어간다. API 모델과 GPU 모델을 이름만 비교한 견적은 measured benchmark가 아니다. 실제 접근 가능한 API 두 개를 먼저 완성한다.



## 따라 하는 실습과 예상 결과

모델 2개·동일 50문항·2반복·warmup 계획을 budget dry-run으로 먼저 확인한다. baseline, context 축소, cache on은 한 번에 하나만 바꾼다. 결과 JSONL에는 request/route/model/prompt/index version, input/output tokens, elapsed_ms, status, cache_hit, error, run_id를 담는다.

별도 concurrency 1/5/10 실험은 요청 속도 제한과 예산 안에서 각각 고정 표본으로 수행한다. Redis 장애·정책 버전 변경·tenant A/B·cache hit/miss가 안전하게 처리되는지 시험한다. API 접근이 없으면 fixture latency·가상 단가 계산만 실행하고 real 모델 비교는 미완료로 표시한다.

## 코드로 확인하는 핵심 원리

실제 모델 단가를 넣기 전에 가상 가격으로 계산식을 검증한다. provider별 청구 규칙과 사용량 검증은 별도다.

```python
def token_cost_usd(input_tokens: int, output_tokens: int,
                   input_price_per_million: float,
                   output_price_per_million: float) -> float:
    """교육용 token 비용 추정치를 USD로 반환한다.

    Args:
        input_tokens: 입력 token 수.
        output_tokens: 출력 token 수.
        input_price_per_million: 가정한 백만 입력 token 단가.
        output_price_per_million: 가정한 백만 출력 token 단가.
    Returns:
        이 단순 요금 모델의 추정 비용.
    Raises:
        ValueError: token 수나 단가가 음수일 때.
    """
    if min(input_tokens, output_tokens, input_price_per_million,
           output_price_per_million) < 0:
        raise ValueError('usage and prices must be non-negative')
    # provider별 cached/reasoning/기타 요금은 별도로 합산해야 한다.
    return (input_tokens * input_price_per_million
            + output_tokens * output_price_per_million) / 1_000_000

assert abs(token_cost_usd(1000, 200, 1.0, 4.0) - 0.0018) < 1e-9
```

**복잡도와 병목:** 비용 계산 O(1). percentile을 정렬로 계산하면 n개 표본 O(n log n)·O(n) 저장. 외부 모델 rate limit, token 길이, cache miss 시 burst가 주요 병목이다.

## 프로젝트에서 빌드할 부분

### W6.1 벤치마크 프로토콜·모델 접근·예산 확정 · 5h

**왜 필요한가:** 다음 구현을 판단할 계약·데이터·환경을 먼저 확정한다.

**수정/작성 위치:** docs/benchmark-protocol.md, configs/benchmark.json

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W5 완료 gate가 선행한다.

**완료 조건:** 2모델·50질문·2반복·warmup·동시성·가격 출처/날짜·budget cap과 측정/가정 구분을 작성한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W6.2 실제 모델 2개 baseline·usage/실패 기록 · 6h

**왜 필요한가:** 개념을 실제 핵심 경로에 연결해 다음 검증의 기준선을 만든다.

**수정/작성 위치:** app/adapters/llm.py, eval/benchmark.py, reports/w06/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W6.1의 산출물이 선행한다.

**완료 조건:** 동일 조건의 실제 요청 200개 계획을 예산 안에서 실행하고 attempted/success/timeout·token usage·P50/P95·품질을 기록한다. 접근 부재는 Blocked다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W6.3 Redis 안전 cache·context/동시성 실험 · 6h

**왜 필요한가:** 실패·권한·복구 경계를 구현해 정상 시연만으로 놓치는 문제를 찾는다.

**수정/작성 위치:** app/cache/, tests/cache/, reports/w06/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W6.2의 산출물이 선행한다.

**완료 조건:** tenant/version/prompt/model key·TTL·정책 갱신·장애 fallback을 검증하고 cold/warm·concurrency 결과를 분리한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W6.4 품질·지연·비용 비교·routing ADR · 5h

**왜 필요한가:** 검증 결과를 설계 결정과 다른 사람이 확인할 증거로 바꾼다.

**수정/작성 위치:** docs/benchmark.md, docs/cost-model.md, docs/adr/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W6.3의 산출물이 선행한다.

**완료 조건:** per-1K attempts/success 비용·subset 품질·P95·review율·인프라 가정과 추천 routing/한계를 제시한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.



## 주차 완료 기준

- [ ] 실제 모델 2개 동일 조건 비교와 원본 usage/latency/오류 기록
- [ ] cache 권한·version·무효화·장애 동작 검증
- [ ] 비용 계산·요금 출처·날짜·예산 상한 명시
- [ ] 품질/지연/비용 trade-off에 근거한 모델/routing ADR

## 이해 확인 퀴즈

**Q1. timeout을 latency 표에서 빼도 되는가?**

<details>
<summary>해설 확인</summary>

완료 요청 percentile은 별도 계산 가능하지만 전체 실패/timeout 수·시간을 반드시 함께 보고해야 한다.

</details>

**Q2. 같은 질문이면 tenant가 달라도 cache를 재사용할까?**

<details>
<summary>해설 확인</summary>

권한·tenant·정책 version 등이 다르면 다른 key가 필요하다.

</details>

**Q3. 1K 성공 비용과 1K 시도 비용이 왜 다른가?**

<details>
<summary>해설 확인</summary>

실패·재시도·보류 비용까지 포함하면 같은 성공 수를 얻기 위한 시도가 달라지기 때문이다.

</details>



## 면접에서 설명할 한 문장

“이번 주에는 같은 평가 조건에서 모델 2개를 비교하고, 비용과 품질을 보존하는 cache/routing 결정을 제시한다. 이를 확인한 증거는 ___이며, 아직 확인하지 못한 범위는 ___입니다.”

기술 이름을 외우기보다 선택 이유·실패 경우·측정 조건·대안을 자기 말로 설명한다.

## 공식 자료: 읽을 범위와 사용법

- [Redis Search/AI 문서 시작점](https://redis.io/docs/latest/develop/ai/search-and-query/) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [AWS GenAI workload 검토](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [LangGraph workflow 설계](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.

문서 URL은 2026-10-01 확인. 설치/API 세부는 실습 시 사용 버전의 공식 문서를 다시 확인한다. 본 강의 설명·실습·프로젝트 판단 기준은 이 포트폴리오를 위해 작성한 교육 내용이다.

## 선택 심화·환경이 막힐 때

vLLM/LoRA는 GPU·계정·시간이 확보된 경우 별도 실습. 필수 2모델 API 평가·Redis 안전 cache를 대체하지 않는다.

핵심 gate가 안 되면 Jira에 실패 증상·환경·시도·다음 행동을 기록한다. fixture로 계약 학습을 이어 갈 수 있지만 real DB/model/cloud/GPU 완료로 바꾸지 않는다.


## Jira 실행 작업 바로가기

| 순서 | 작업·시간 | 선행 |
|---|---|---|
| 6.1 | [SCRUM-34](https://realrho-1790798942092.atlassian.net/browse/SCRUM-34) · 벤치마크 프로토콜·모델 접근·예산 확정 · 5h | SCRUM-10 |
| 6.2 | [SCRUM-35](https://realrho-1790798942092.atlassian.net/browse/SCRUM-35) · 실제 모델 2개 baseline·usage/실패 기록 · 6h | SCRUM-34 |
| 6.3 | [SCRUM-36](https://realrho-1790798942092.atlassian.net/browse/SCRUM-36) · Redis 안전 cache·context/동시성 실험 · 6h | SCRUM-35 |
| 6.4 | [SCRUM-37](https://realrho-1790798942092.atlassian.net/browse/SCRUM-37) · 품질·지연·비용 비교·routing ADR · 5h | SCRUM-36 |

## 구현 레시피 · benchmark raw record와 캐시

### 원본 측정 레코드

~~~json
{"run_id":"run-001","case_id":"q-001","model":"MODEL_A","prompt_version":"p1","index_version":"idx1","concurrency":1,"cache_hit":false,"elapsed_ms":null,"input_tokens":null,"output_tokens":null,"status":"NOT_RUN"}
~~~

null/NOT_RUN은 빈 템플릿이다. 실API 실행 결과만 actual latency/usage로 채운다. 한 요청이 실패해도 attempt record를 남긴다.

1. configuration에 2개 model ID·temperature/max output·timeout·budget cap·subset·repeats를 넣는다.
2. model adapter는 structured output·실usage·error category를 반환한다.
3. runner는 warm-up을 별도 기록하고 baseline 요청을 고정 분포로 실행한다.
4. aggregate는 성공 latency와 모든 attempt 실패율을 별도 계산한다.
5. Redis key는 trusted scope/query hash/policy/index/prompt/model version으로 만들고 raw text를 제외한다.
6. policy 갱신·tenant 차이·Redis 장애·cache hit/miss를 검증한다.
7. context 길이·cache·concurrency를 하나씩 바꾸고 품질이 유지되는지 확인한다.
8. 가격 출처/날짜·실usage와 인프라 가정으로 1K 비용을 산출한다.

### 추천 결정의 조건

품질 hard gate를 못 지키는 모델은 비용만으로 추천하지 않는다. 높은 review율로 안전해 보이는 설정은 reviewer workload도 같이 제시한다. 동일 모델이라도 API region·output length·retry·cache 분포가 달라지면 재측정한다.

### 막힐 때 확인 순서

429→rate limit/concurrency/budget, token usage 없음→provider 응답 계약, 비용 차이→cached/reasoning/retry·청구 규칙, stale answer→policy/index/prompt cache key를 확인한다. fixture 시간을 실모델 latency 표에 섞지 않는다.
