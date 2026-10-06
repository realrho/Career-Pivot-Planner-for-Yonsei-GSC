# W5 학습 · 검색 고도화·벡터 DB와 영속성·트랜잭션

**기간:** 2026-10-30–2026-11-05 (Asia/Seoul) · **계획:** 22h · [Notion](https://app.notion.com/p/3ebc6f4a2c7e817e9825cec827df9013) · [GitHub #5](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/5)

**이번 주 통과 조건:** 다른 tenant/비활성 버전 근거가 나오지 않으며 DB 쓰기 실패 시 상태와 감사 기록이 함께 롤백된다. 재시작 후 조회 경로를 확인한다.

[전체 학습표](README.md) · [책 목차 원문](../book-toc.md) · [용어 사전](../glossary-ko-en.md) · [책/보충 범위](../book-gap-map.md)

## 1. 책 읽기와 필수 실습

**배정:** 11장 임베딩 학습·순위 재정렬 · 12장 벡터 DB·RAG 확장

11.1–11.5는 임베딩 학습·대조 학습·MNR loss·교차 인코더 순위 재정렬을 기본 검색 대비 개선 실험으로 읽는다. 12.1–12.4는 KNN/ANN·NSW/HNSW·m/ef 파라미터·Pinecone 연동을 실행한다. 12.5 멀티모달 예제는 흐름을 읽고 실행은 선택 심화로 둔다.

**필수 실습:** 기본 embedding+reranker 한 조합을 작은 corpus에 적용해 정확도/지연을 비교한다. Pinecone 공식 책 예제를 따라가거나 사용할 수 있는 로컬 벡터 backend 하나를 선택하고 차이를 ADR에 기록한다. 임베딩 미세 조정/GPU·다른 DB 추가·이미지 생성 전체 실행은 선택이다.

책 본문은 소유한 책에서 읽는다. [공식 코드](https://github.com/onlybooks/llm)·[정오표](https://www.onlybook.co.kr/entry/llm-errata)를 확인하고 환경/모델/패키지 버전을 기록한다. 선택 GPU/멀티모달 실습의 미실행은 필수 완료와 분리한다.

## 2. 실행 순서·시간·수용 기준

| 순서 | 작업 | 계획 시간 | 완료 기준 | 작업 ID |
|---|---|---|---|---|
| 1 | 책 11·12장 읽기·개념 노트 | 6h | 배정된 모든 절을 읽고 개념 관계·비교·질문을 자신의 말로 기록한다. | W5.1 |
| 2 | 책 필수 실습·환경/결과 기록 | 6h | 기본 embedding+reranker 한 조합을 작은 corpus에 적용해 정확도/지연을 비교한다. Pinecone 공식 책 예제를 따라가거나 사용할 수 있는 로컬 벡터 backend 하나를 선택하고 차이를 ADR에 기록한다. 임베딩 미세 조정/GPU·다른 DB 추가·이미지 생성 전체 실행은 선택이다. | W5.2 |
| 3 | SA 보충 강의·재사용 실습 자산 만들기 | 8h | 다른 tenant/비활성 버전 근거가 나오지 않으며 DB 쓰기 실패 시 상태와 감사 기록이 함께 롤백된다. 재시작 후 조회 경로를 확인한다. | W5.3 |
| 4 | 퀴즈·설명·증거·다음 주 준비 검토 | 2h | 3개 퀴즈를 해설 없이 설명하고 선택 벡터backend의 실제 검색 경로, PostgreSQL 사례/검토/감사 schema, 원자적 갱신 연습를 버전/실행 상태와 함께 저장한다. | W5.4 |

## 3. SA 보충 강의 · 개념→이유→예제→실습

### 3.1 벡터 검색과 업무 저장소 분리

KNN, k-Nearest Neighbors(k-최근접 이웃)은 거리상 가까운 k개를 찾는 방식이고 ANN, Approximate Nearest Neighbor(근사 최근접 이웃)는 정확도를 일부 교환해 검색을 빠르게 한다. HNSW, Hierarchical Navigable Small World(계층형 탐색 가능한 작은 세계)는 여러 층의 그래프를 탐색하는 인덱스다. m은 연결 수, ef_construction은 구축 탐색 폭, ef_search는 질의 탐색 폭에 관계한다. 높은 값은 메모리/구축/질의 비용을 늘릴 수 있으므로 Recall·지연·메모리를 같이 본다. 벡터 DB는 근거 유사 검색에, PostgreSQL은 사례 상태·검토·감사·제약에 사용하면 책임이 명확하다.

**작동 예시/실패 경계:** '문서와 비슷한 질문'은 벡터 검색으로 찾고 'case_id=123이 검토 대기인가'는 기본 키 조회로 확인한다. 벡터 검색 score를 업무 상태로 저장하거나 DB 전체를 하나로 바꾸려 하기 전에 필요한 질의와 일관성을 구분한다.

**직접 해 보기:** RAGBackend.search(query, trusted_scope, active_version, k)의 반환 형식을 하나로 정의한다. Pinecone/Milvus는 제품 이름이다. 이번 MVP는 검증한 하나만 사용하며 두 backend 비교는 추가 과제다.

### 3.2 ACID 트랜잭션과 동시 검토

ACID는 Atomicity(원자성), Consistency(일관성), Isolation(격리성), Durability(지속성)의 묶음이다. transaction(트랜잭션)은 관련 DB 변경을 함께 성공시키거나 롤백하는 단위다. 상태 변경과 감사 기록이 따로 성공하면 누가 무엇을 결정했는지 사라질 수 있으므로 함께 묶는다. 동시 검토자 두 명이 같은 case를 수정하면 마지막 쓰기가 앞 결정을 덮을 수 있다. optimistic concurrency(낙관적 동시성 제어)는 version 조건이 맞는 갱신만 허용하고 실패한 경쟁 요청을 거부한다.

**작동 예시/실패 경계:** UPDATE cases SET status='APPROVED', version=version+1 WHERE id=? AND version=? AND status='REVIEW_PENDING' 후 영향행이1인지 확인한다. 감사 INSERT도 같은 트랜잭션 안에서 수행한다. 0행이면409 충돌을 반환한다. DB 트랜잭션이 외부 이메일/모델 호출까지 자동 취소하지는 않는다.

**직접 해 보기:** SQLite로 원자성 원리를 연습한 뒤 PostgreSQL 실제 경로에서 실패 주입·재시작·동시 갱신을 검증한다. SQL은 바인딩하고 사례 tenant 조건도 포함한다. 시스템이 검토 요청을 생성한 것과 사람이 승인한 것은 다른 상태다.

### 3.3 멱등 ingestion과 버전 활성화

ingestion(데이터 수집·적재)은 원본을 읽어 정제/분할/임베딩/저장하는 과정이다. content hash(내용 해시)는 동일 내용 확인에, document version(문서 버전)은 정책 변화 추적에 쓰며 같은 개념이 아니다. tenant+source+version+chunk identity에 유일 제약을 두면 재실행 중복을 줄인다. 새 버전을 일부만 적재한 상태에서 검색을 열면 빠진 근거로 답할 수 있다. staging(준비 영역)에 새 인덱스를 만들고 검증 후 active version(활성 버전) 포인터를 바꾸는 절차가 안전하다.

**작동 예시/실패 경계:** v2를 준비하다 중간 실패하면 v1검색을 유지한다. v2검증 후 활성화하면서 v1캐시를 무효화한다. DB와 벡터 DB 사이에 단일 트랜잭션이 없으면 적재 manifest·상태·재시도 가능한 작업 기록으로 불일치를 복구한다.

**직접 해 보기:** 12개 문서를 두 번 적재해 같은 논리 청크 수가 유지되는지 확인한다. 실패 후 재시작하여 누락만 채우는지 본다. schema/mapping 변경 시 임베딩 차원·거리 함수·모델 버전도 manifest에 적는다.

### 3.4 권한 필터와 인덱스 평가

tenant(테넌트)는 서비스를 공유하는 고객/조직 경계다. 요청 본문에 적힌 tenant_id보다 검증된 사용자→tenant 매핑을 신뢰해야 한다. 검색 전에 범위를 제한하고 검색 결과를 반환하기 전 다시 확인하면 권한 밖 근거가 프롬프트/로그/캐시로 흐르는 위험을 줄일 수 있다. 제한 없는 전체 검색 후 단순히 상위 k에서 몇 개를 지우면 정답 근거가 사라질 수 있으므로 backend의 필터 지원과 검색 품질을 같이 확인한다. 불충분한 필터 구현이면 그 환경을 안전한 멀티테넌트 구현으로 보고하지 않는다.

**작동 예시/실패 경계:** tenant A의 정책코드 R-17 질문에 B의 더 가까운 벡터가 존재하도록 합성 데이터를 만든다. A조건 검색이 A근거를 반환하거나 명시적으로 보류해야 한다. 비활성 v1문서가 높은 점수여도 v2활성 조건에서 제외된다.

**직접 해 보기:** 교차tenant·버전변경·문서삭제·reranker오류 4개를 회귀 사례로 만든다. 조회할 수 없는 case가 존재하는지도 드러내지 않는404 계약을 선택할 수 있으며 이 결정을 ADR에 적는다.

## 4. 실행 가능한 기초 계약 실습

아래는 핵심 규칙을 작게 분리해 CPU에서 확인하는 접근이다. 라이브러리 설치나 실제 모델 호출 없이 개념을 검증한다. 프로젝트 통합 구현과 증거 수준을 구분한다.

실행: `python labs/week-05/contract_demo.py` (저장소 루트).

```python
"""W5: SQLite 실패 주입으로 상태/감사의 원자성만 검증한다."""
import sqlite3

def atomic_review(connection: sqlite3.Connection, fail_audit: bool = False) -> None:
    """상태와 감사 행을 한 트랜잭션으로 저장한다.

    Args:
        connection: 실습용 SQLite 연결.
        fail_audit: 감사 기록 전에 오류를 주입할지 여부.
    Returns:
        None. 성공하면 두 변경을 커밋한다.
    Raises:
        RuntimeError: 실패 주입 시 발생하며 상태 변경도 롤백된다.
        sqlite3.Error: SQL 실행이 실패한 경우.
    """
    with connection:  # context manager는 예외 시 DB 변경을 롤백한다.
        connection.execute("UPDATE cases SET status = ? WHERE id = ?", ("APPROVED", 1))
        if fail_audit:
            raise RuntimeError("injected audit failure")
        connection.execute("INSERT INTO audit(case_id) VALUES (?)", (1,))

connection = sqlite3.connect(":memory:")
connection.executescript("CREATE TABLE cases(id INTEGER PRIMARY KEY, status TEXT);"
                         "CREATE TABLE audit(case_id INTEGER);"
                         "INSERT INTO cases VALUES(1, 'REVIEW_PENDING');")
try:
    atomic_review(connection, fail_audit=True)
except RuntimeError:
    pass
assert connection.execute("SELECT status FROM cases").fetchone()[0] == "REVIEW_PENDING"
assert connection.execute("SELECT count(*) FROM audit").fetchone()[0] == 0
atomic_review(connection)
assert connection.execute("SELECT count(*) FROM audit").fetchone()[0] == 1
connection.close()
print("W5 SQLite atomicity: passed; PostgreSQL/concurrency not validated")
```

**복잡도/병목:** 상수 개수 DB 연산. 실제 DB 비용은 인덱스·락·I/O에 좌우된다. PostgreSQL·동시성·백업은 별도 검증한다.

## 5. 학습 중 만들 재사용 자산 · 상세 작업

아래 app/data/deployment 파일은 **앞으로 작성할 예정 경로**다. 현재 구현된 것으로 읽지 않는다. 작은 계약 실습을 실제 저장소/모델 경로로 확장하는 작업이다.

### 5.1 관계형 schema와 제약

예정 `app/repositories/postgres.py`와 DB migration에 cases(id,tenant_id,status,version), reviews(case_id,actor,decision), audit(case_id,actor,old/new_status,run_id)를 정의한다. 외래 키·유일 키·조회 인덱스와 tenant 조건을 명시한다.

### 5.2 원자적 검토 갱신

상태·기존 version 조건을 가진 UPDATE와 audit INSERT를 한 트랜잭션으로 묶는다. 영향 행 0이면 충돌·잘못된 전이로 처리한다. 감사 실패를 주입해 case 상태도 원래대로 남는지 검증한다. SQLite 연습 뒤 PostgreSQL 실제 연결로 확인한다.

### 5.3 벡터 backend 하나 확정

책의 Pinecone 또는 호환 로컬 backend 하나를 정한다. Milvus는 Windows에서 공식 지원하는 Docker/WSL2 환경을 확인한다. 검색 adapter는 tenant/version 조건과 evidence ID를 반환해야 한다. 비용·운영·데이터 경계 ADR을 쓴다.

### 5.4 적재/활성화/복구

같은 corpus를 두 번 적재하고 논리 중복이 없음을 확인한다. v2 준비 영역 적재 실패 시 v1 활성 검색을 유지한다. 임베딩 차원·인덱스 설정·활성 버전·캐시 무효화 절차를 기록한다.

### 5.5 회귀와 지속성

교차 tenant·비활성 버전·없는 case·동시 갱신·프로세스 재시작 조회를 검증한다. 재시작 지속성과 별도 백업 복원은 구분한다.

**다음 통합에 넘길 것:** 선택 벡터backend의 실제 검색 경로, PostgreSQL 사례/검토/감사 schema, 원자적 갱신 연습

## 6. 이해 확인 · 해설을 보기 전에 설명하기

**Q1. 트랜잭션이면 외부 모델 호출도 롤백되는가?**

<details>
<summary>해설</summary>

DB 내부 변경 범위다. 외부 부작용은 별도 멱등/복구 설계가 필요하다.

</details>

**Q2. 캐시TTL만으로 정책 갱신 즉시 반영을 보장하는가?**

<details>
<summary>해설</summary>

아니다. 활성버전/캐시 키/무효화 절차를 함께 설계한다.

</details>

**Q3. ANN 인덱스 설정을 크게 하면 항상 좋은가?**

<details>
<summary>해설</summary>

메모리·구축/질의시간 비용이 증가할 수 있어 같은 데이터로 정확도와 비용을 측정한다.

</details>

## 7. 공식 자료 · 읽을 범위

- [PostgreSQL: transaction](https://www.postgresql.org/docs/current/tutorial-transactions.html) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.
- [Pinecone 공식 문서](https://docs.pinecone.io/) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.
- [Milvus 공식 문서](https://milvus.io/docs) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.

## 증거와 완료 상태

학습 노트에는 읽은 절·자신의 설명·실습 명령·Python/패키지/장치·데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 문서/fixture/실제DB·모델/클라우드·GPU의 수준을 구분한다. 자료 작성만으로 본인의 학습 또는 서비스 제작을 완료 처리하지 않는다. 막히면 증상·시도·다음 행동과 일정 영향을 남긴다.
