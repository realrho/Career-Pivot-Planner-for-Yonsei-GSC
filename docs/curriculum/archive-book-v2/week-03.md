# W3 학습 · 추론·서빙과 네트워크·타임아웃·비용 계산

**기간:** 2026-10-16–2026-10-22 (Asia/Seoul) · **계획:** 22h · [Notion](https://app.notion.com/p/3ebc6f4a2c7e8116b6d0e972f595de78) · [GitHub #3](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/3)

**이번 주 통과 조건:** 모델 응답 지연을 구간으로 나누고 429·timeout·4xx 처리 차이를 설명한다. 가상의 요금과 실제 청구를 구분한다.

[전체 학습표](README.md) · [책 목차 원문](../book-toc.md) · [용어 사전](../glossary-ko-en.md) · [책/보충 범위](../book-gap-map.md)

## 1. 책 읽기와 필수 실습

**배정:** 7장 모델 가볍게 만들기 · 8장 sLLM 서빙하기

7.1–7.3의 토큰 생성·KV 캐시·양자화·증류를 읽고 8.1–8.4의 정적/동적/연속 배치, FlashAttention, PagedAttention, 추측 디코딩, 오프라인/온라인 서빙을 연결한다. GPU 커널을 새로 구현할 필요는 없다. vLLM 경로의 요청→대기→prefill→decode→응답을 그려 본다.

**필수 실습:** 7장 KV 캐시 크기를 간단한 조건으로 계산한다. 공식 8장 vLLM 노트북의 서버/클라이언트 입력과 응답을 설명한다. 호환 GPU가 있으면 짧은 서빙 호출만 측정한다. 없으면 지연/비용 계산 fixture를 실행하고 vLLM 속도 향상을 측정했다는 주장을 하지 않는다.

책 본문은 소유한 책에서 읽는다. [공식 코드](https://github.com/onlybooks/llm)·[정오표](https://www.onlybook.co.kr/entry/llm-errata)를 확인하고 환경/모델/패키지 버전을 기록한다. 선택 GPU/멀티모달 실습의 미실행은 필수 완료와 분리한다.

## 2. 실행 순서·시간·수용 기준

| 순서 | 작업 | 계획 시간 | 완료 기준 | 작업 ID |
|---|---|---|---|---|
| 1 | 책 7·8장 읽기·개념 노트 | 6h | 배정된 모든 절을 읽고 개념 관계·비교·질문을 자신의 말로 기록한다. | W3.1 |
| 2 | 책 필수 실습·환경/결과 기록 | 6h | 7장 KV 캐시 크기를 간단한 조건으로 계산한다. 공식 8장 vLLM 노트북의 서버/클라이언트 입력과 응답을 설명한다. 호환 GPU가 있으면 짧은 서빙 호출만 측정한다. 없으면 지연/비용 계산 fixture를 실행하고 vLLM 속도 향상을 측정했다는 주장을 하지 않는다. | W3.2 |
| 3 | SA 보충 강의·재사용 실습 자산 만들기 | 8h | 모델 응답 지연을 구간으로 나누고 429·timeout·4xx 처리 차이를 설명한다. 가상의 요금과 실제 청구를 구분한다. | W3.3 |
| 4 | 퀴즈·설명·증거·다음 주 준비 검토 | 2h | 3개 퀴즈를 해설 없이 설명하고 모델 호출 계약·timeout/retry 정책, 지연/비용 표, AWS 네트워크 설계 초안를 버전/실행 상태와 함께 저장한다. | W3.4 |

## 3. SA 보충 강의 · 개념→이유→예제→실습

### 3.1 DNS·TCP·TLS·HTTPS 요청 경로

DNS, Domain Name System(도메인 이름 시스템)은 이름을 IP 주소로 해석한다. IP, Internet Protocol(인터넷 프로토콜)은 네트워크 주소와 전달 규칙이며 TCP, Transmission Control Protocol(전송 제어 프로토콜)은 순서 있는 바이트 전송을 제공한다. TLS, Transport Layer Security(전송 계층 보안)는 전송 암호화와 인증서 기반 서버 신원 확인을 제공한다. HTTPS, HTTP over TLS(TLS를 사용하는 HTTP)는 HTTP를 보호된 연결로 전송한다. 요청 경로는 이름 해석→연결→TLS→HTTP→서버 처리→응답이다. LLM이 느린 것처럼 보여도 DNS 실패·연결 풀 대기·DB 지연일 수 있으므로 구간을 나눠 본다.

**작동 예시/실패 경계:** 401은 인증 문제, 403은 권한 거부, 429는 요청량 제한을 의미하는 대표 상태다. CORS, Cross-Origin Resource Sharing(교차 출처 리소스 공유)은 브라우저의 출처 접근 규칙이며 서버 인증을 대신하지 않는다. TLS도 애플리케이션의 tenant 권한을 대신하지 않는다.

**직접 해 보기:** 모델 API 호출 경로를 화살표로 그린다. 오류 메시지를 DNS/연결/TLS/HTTP/본문 검증으로 분류한다. 비밀 값을 출력하지 않고 호스트·오류 종류·request_id만 기록한다.

### 3.2 시간 제한·재시도·멱등성

timeout(시간 제한)은 작업을 기다리는 최대 시간이다. connect/read/전체 deadline을 구분하면 연결과 처리의 병목을 찾기 쉽다. retry(재시도)는 일시 실패를 다시 시도하는 동작이며 exponential backoff(지수형 대기)와 jitter(무작위 분산)는 동시에 재시도하는 부하를 줄인다. 모든 오류를 재시도하면 잘못된 입력도 비용을 반복 소모한다. idempotency(멱등성)는 같은 작업을 반복해도 추가 부작용이 생기지 않는 성질이다. 요청 시간 초과는 서버가 아무 작업도 하지 않았다는 뜻이 아니므로 쓰기 요청은 중복 방지가 중요하다.

**작동 예시/실패 경계:** 일시 429/일부5xx는 공급자 지침과 전체 deadline 안에서 최대 2회 추가 시도한다. 401·422는 수정 없이 반복하지 않는다. 케이스 접수는 Idempotency-Key와 본문 해시를 묶고 같은 키/다른 본문이면 409로 거부한다. 공급자 모델 호출의 과금 중복 가능성은 별도 추적한다.

**직접 해 보기:** docs/contracts.md에 오류별 재시도 표와 최대 총 호출 수를 쓴다. 실패 fixture로 재시도 횟수와 예산 초과 중단을 확인한다. 랜덤 지연 때문에 결과가 달라지면 테스트에서는 고정 난수를 쓴다.

### 3.3 KV 캐시와 응답 캐시·성능 수치

KV, Key-Value(키·값)는 어텐션의 이전 토큰 계산을 재사용하기 위한 캐시다. 9장 LLM 응답 캐시는 입력에 대한 결과 재사용으로 다른 계층이다. KV 캐시는 모델 추론 내부에, 응답 캐시는 서비스/공급자 계층에 있을 수 있다. prefill(입력 토큰 처리)은 프롬프트를 읽는 단계, decode(출력 생성)는 다음 토큰을 반복 생성하는 단계다. TTFT, Time To First Token(첫 토큰까지 시간), TPOT, Time Per Output Token(출력 토큰당 시간), end-to-end latency(전체 응답 지연)를 구분한다. throughput(처리량)은 시간당 처리 요청/토큰이며 낮은 지연과 항상 같이 좋아지지 않는다.

**작동 예시/실패 경계:** 연속 배치는 끝난 요청 자리에 새 요청을 넣어 자원 활용을 높일 수 있다. 대기열이 길면 처리량은 높아도 개별 요청 P95는 악화할 수 있다. P95는 95백분위 수치이며 표본·동시성·warm/cold 조건을 붙여 보고한다.

**직접 해 보기:** 요청량이 같은 조건에서 입력 길이·출력 길이·배치를 한 가지씩 바꾼다. GPU 미실행이면 계산 결과를 예상값으로 표기한다. 실제 모델 호출의 TTFT가 없으면 전체 지연만 보고한다.

### 3.4 클라우드 네트워크와 비용·용량

AWS, Amazon Web Services(아마존 웹 서비스)는 클라우드 서비스군이다. VPC, Virtual Private Cloud(가상 사설 클라우드)는 논리적으로 분리된 네트워크 공간, subnet(서브넷)은 그 안의 주소 범위, route table(라우팅 테이블)은 패킷의 다음 경로를 정한다. security group(보안 그룹)은 리소스에 붙는 트래픽 허용 규칙이다. 공개 API 입구와 비공개 DB를 분리하고 앱만 DB 포트에 접근하도록 설계한다. 비용은 토큰뿐 아니라 컴퓨트·DB·스토리지·전송·운영 시간을 포함한다. RPM, Requests Per Minute(분당 요청 수), TPM, Tokens Per Minute(분당 토큰 수)은 서로 다른 제한이다.

**작동 예시/실패 경계:** 가상 입력단가 $1/백만 토큰, 출력 $4/백만 토큰이면 2,000입력+300출력 요청은 $0.0032다. 1만 요청은 재시도/검색/저장비 없이 $32다. 현재 공급자 가격으로 착각하지 않는다. DB를 인터넷 전체에 공개해 연결 문제를 해결하지 않는다.

**직접 해 보기:** 요금은 실습 당일 공식 가격을 기록하고 사용 상한을 정한다. API→앱→DB→모델 공급자 경로에 주소·포트·인증·외부 송신 여부를 표시한다. AWS 실제 생성은 선택이고 설계만 했으면 설계 증거로 기록한다.

## 4. 실행 가능한 기초 계약 실습

아래는 핵심 규칙을 작게 분리해 CPU에서 확인하는 접근이다. 라이브러리 설치나 실제 모델 호출 없이 개념을 검증한다. 프로젝트 통합 구현과 증거 수준을 구분한다.

실행: `python labs/week-03/contract_demo.py` (저장소 루트).

```python
"""W3: 가상 단가로 토큰 비용을 계산한다. 실제 청구/성능 결과가 아니다."""
from decimal import Decimal

def token_cost(input_tokens: int, output_tokens: int,
               input_per_million: Decimal, output_per_million: Decimal) -> Decimal:
    """입력/출력 토큰의 가상 사용료 합계를 계산한다.

    Args:
        input_tokens: 입력 토큰 개수.
        output_tokens: 출력 토큰 개수.
        input_per_million: 입력 백만 토큰당 가상 단가.
        output_per_million: 출력 백만 토큰당 가상 단가.
    Returns:
        같은 통화 단위의 비용. 검색/재시도/저장 비용은 제외한다.
    Raises:
        ValueError: 개수 또는 단가가 음수인 경우.
    """
    if min(input_tokens, output_tokens, input_per_million, output_per_million) < 0:
        raise ValueError("negative usage or price")
    # 이진 부동소수점 반올림 영향을 줄이기 위해 Decimal로 계산한다.
    million = Decimal(1_000_000)
    return (Decimal(input_tokens) * input_per_million
            + Decimal(output_tokens) * output_per_million) / million

assert token_cost(2000, 300, Decimal("1"), Decimal("4")) == Decimal("0.0032")
print("W3 fictional token cost:", token_cost(2000, 300, Decimal("1"), Decimal("4")))
```

**복잡도/병목:** 시간/추가 공간 O(1), 임의 정밀 숫자의 표현 비용은 제외한 작은 입력 기준이다.

## 5. 학습 중 만들 재사용 자산 · 상세 작업

아래 app/data/deployment 파일은 **앞으로 작성할 예정 경로**다. 현재 구현된 것으로 읽지 않는다. 작은 계약 실습을 실제 저장소/모델 경로로 확장하는 작업이다.

### 5.1 모델 호출 어댑터 계약

예정 `app/adapters/model.py`에 generate(prompt, deadline, budget)의 출력 text/usage/model_version과 timeout/rate_limit/invalid_output을 명시한다. 책 8장의 자체 서빙과 외부 API를 같은 논리 계약으로 이해하되 구현은 하나만 사용한다.

### 5.2 재시도와 지연 구간 기록

연결·읽기·전체 deadline을 정한다. 429/일시 5xx와 401/422를 분리한다. 최대 2회 추가 시도, 공급자의 Retry-After 존중, 총예산 초과 중단을 명시한다. fixture로 호출 횟수를 확인하고 실제 공급자에서는 재시도 과금도 추적한다.

### 5.3 비용 계산 도구 만들기

`labs/week-03/` 예제를 실제 가격표 입력과 연결할 수 있도록 확장한다. 가상 단가·실제 단가 날짜·모델명·input/output usage·재시도 수를 별도 열로 저장한다.

### 5.4 네트워크 초안

`docs/deployment/network.md`에 공개 API 입구→앱→비공개 DB→외부 모델 흐름을 그린다. DNS·TLS·보안 그룹·DB 포트·외부 송신 경계를 표시한다. 실제 AWS 생성은 선택이다.

### 5.5 검증 범위 표시

실제 API를 호출했으면 요청 ID·총지연·usage를 남긴다. GPU/vLLM 미실행이면 배치·KV 계산만 확인했으며 서빙 성능은 측정하지 않았다고 명시한다.

**다음 통합에 넘길 것:** 모델 호출 계약·timeout/retry 정책, 지연/비용 표, AWS 네트워크 설계 초안

## 6. 이해 확인 · 해설을 보기 전에 설명하기

**Q1. timeout은 모델이 실행되지 않았다는 뜻인가?**

<details>
<summary>해설</summary>

서버 작업/과금은 이미 발생했을 수 있다. 작업 ID·멱등 키·공급자 응답을 추적한다.

</details>

**Q2. KV 캐시를 켜면 tenant별 응답 캐시가 안전해지는가?**

<details>
<summary>해설</summary>

다른 계층이다. 응답 캐시는 tenant·권한·문서 버전 등을 키와 검증에 반영해야 한다.

</details>

**Q3. P95와 처리량 중 무엇이 중요할까?**

<details>
<summary>해설</summary>

고객 요구에 따라 둘 다 조건과 목표를 정한다. 배치 개선이 두 지표를 모두 개선한다고 가정하지 않는다.

</details>

## 7. 공식 자료 · 읽을 범위

- [HTTP 공식 개요](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.
- [AWS VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.
- [vLLM 공식 문서](https://docs.vllm.ai/en/latest/) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.

## 증거와 완료 상태

학습 노트에는 읽은 절·자신의 설명·실습 명령·Python/패키지/장치·데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 문서/fixture/실제DB·모델/클라우드·GPU의 수준을 구분한다. 자료 작성만으로 본인의 학습 또는 서비스 제작을 완료 처리하지 않는다. 막히면 증상·시도·다음 행동과 일정 영향을 남긴다.
