# W8 학습 · 새 아키텍처 이해·SA 설계 리뷰·제작 준비 동결

**기간:** 2026-11-20–2026-11-26 (Asia/Seoul) · **계획:** 22h · [Notion](https://app.notion.com/p/3ebc6f4a2c7e81aa88beca3d312c0854) · [Jira SCRUM-13](https://realrho-1790798942092.atlassian.net/browse/SCRUM-13) · [GitHub #8](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/8)

**이번 주 통과 조건:** API 계약·실제 검색·영속 DB·권한/검토·기동·평가 질문이 준비되어야 W9 제작 2주를 시작한다. 미완료 핵심 자산이 있으면 일정 또는 범위를 조정한다.

[전체 학습표](README.md) · [책 목차 원문](../book-toc.md) · [용어 사전](../glossary-ko-en.md) · [책/보충 범위](../book-gap-map.md)

## 1. 책 읽기와 필수 실습

**배정:** 16장 새로운 아키텍처

16.1–16.5를 읽고 Transformer와 SSM/S4/Mamba의 순차 상태·선택 메커니즘·장단점을 설명한다. 새로운 모델을 이번 MVP에 도입하지 않아도 된다. 1–15장의 관계를 한 장의 지도에 정리하고 각 장의 남은 실행 과제를 표시한다.

**필수 실습:** 16장의 맘바 코드를 읽어 입력/상태/출력 흐름을 설명하고 필요 환경을 기록한다. 하드웨어가 지원되면 소규모예제만 실행한다. 모든 장의 읽기·필수 실습·선택 GPU실행 상태를 점검하고 W1–W7 재사용 자산을 새 환경에서 smoke check한다.

책 본문은 소유한 책에서 읽는다. [공식 코드](https://github.com/onlybooks/llm)·[정오표](https://www.onlybook.co.kr/entry/llm-errata)를 확인하고 환경/모델/패키지 버전을 기록한다. 선택 GPU/멀티모달 실습의 미실행은 필수 완료와 분리한다.

## 2. 실행 순서·시간·수용 기준

| 순서 | 작업 | 계획 시간 | 완료 기준 | Jira |
|---|---|---|---|---|
| 1 | 책 16장 읽기·개념 노트 | 6h | 배정된 모든 절을 읽고 개념 관계·비교·질문을 자신의 말로 기록한다. | [SCRUM-42](https://realrho-1790798942092.atlassian.net/browse/SCRUM-42) |
| 2 | 책 필수 실습·환경/결과 기록 | 6h | 16장의 맘바 코드를 읽어 입력/상태/출력 흐름을 설명하고 필요 환경을 기록한다. 하드웨어가 지원되면 소규모예제만 실행한다. 모든 장의 읽기·필수 실습·선택 GPU실행 상태를 점검하고 W1–W7 재사용 자산을 새 환경에서 smoke check한다. | [SCRUM-43](https://realrho-1790798942092.atlassian.net/browse/SCRUM-43) |
| 3 | SA 보충 강의·재사용 실습 자산 만들기 | 8h | API계약·실제 검색·영속 DB·권한/검토·기동·평가 질문이 준비되어야 W9제작2주를 시작한다. 미완료핵심자산이 있으면 주말추가가정 대신 일정/범위를 조정한다. | [SCRUM-44](https://realrho-1790798942092.atlassian.net/browse/SCRUM-44) |
| 4 | 퀴즈·설명·증거·다음 주 준비 검토 | 2h | 3개 퀴즈를 해설 없이 설명하고 고객요구사항·ADR·아키텍처/권한/비용표·제작 준비 체크리스트·동결config를 버전/실행 상태와 함께 저장한다. | [SCRUM-45](https://realrho-1790798942092.atlassian.net/browse/SCRUM-45) |

## 3. SA 보충 강의 · 개념→이유→예제→실습

### 3.1 SA의 고객 발견과 요구사항

SA, Solution Architect(솔루션 아키텍트)는 고객 문제와 제약을 이해하고 여러 기술을 연결하는 설계를 설명·검증하는 역할이다. discovery(요구 파악)는 사용자·현재 업무·실패 비용·데이터·권한·예산·운영 주체를 확인하는 과정이다. FR, Functional Requirement(기능 요구사항)는 수행 행동, NFR, Non-Functional Requirement(비기능 요구사항)는 품질과 운영 조건이다. PoC, Proof of Concept(개념 검증)는 특정 가능성을 확인하며 MVP, Minimum Viable Product(최소 기능 제품)는 제한된 사용자 문제를 끝까지 처리하는 범위다. demo(데모)는 시연이며 운영 준비를 자동으로 증명하지 않는다.

**작동 예시/실패 경계:** 고객은 'AI 챗봇'보다 '새 정책에 근거해 검토 시간을 줄이고 위험 판정은 사람이 승인'하는 행동을 원한다. FR은 근거 응답과 검토, NFR은 tenant 격리·지연·추적성이다. 2주 MVP 대상은 합성 자료의 텍스트 정책이며 실제 회사 민감 자료 통합은 별도 범위다.

**직접 해 보기:** 질문 10개로 고객 시나리오를 정리하고 성공 지표·실패 비용·운영 책임을 각각 쓴다. 영어 90초 설명은 problem→constraints→decision→evidence→limits 순으로 연습한다.

### 3.2 ADR과 대안을 비교하는 방법

ADR, Architecture Decision Record(아키텍처 결정 기록)는 맥락·선택·대안·이유·결과·재검토 조건을 남기는 문서다. 장점만 나열하면 판단을 보여주지 못한다. build versus buy(직접 구현 대 구매/관리형)는 운영 시간·데이터 경계·비용·유연성을 포함해야 한다. 한 모델·한 벡터 backend·단순 workflow를 선택해도 교체 계약과 재검토 조건이 있으면 설계 근거를 보일 수 있다. Transformer·SSM·Mamba 선택도 최신성보다 업무 길이·품질·호환성·서빙 증거를 우선한다.

**작동 예시/실패 경계:** Pinecone 관리형은 운영 부담을 줄일 수 있지만 외부 데이터 경계와 비용을 검토한다. Milvus 로컬은 제어 가능하지만 설치·백업 운영 부담이 있다. 비교한 후 검증한 하나만 MVP 필수로 동결한다. SQL·비밀·권한을 제품 기능이 전부 해결한다고 가정하지 않는다.

**직접 해 보기:** 모델·vector backend·workflow·배포 범위의 네 ADR을 각각 1페이지로 작성한다. 결정 날짜·실제 검증 결과·미검증 항목·언제 대안을 택할지를 쓴다.

### 3.3 비용·수용 기준·증거 수준

TCO, Total Cost of Ownership(총소유비용)는 사용료 외 개발·운영·장애 대응 비용도 포함한다. FinOps, Financial Operations(재무 운영, 클라우드 비용 관리 실천)는 비용을 업무 가치와 연결해 관리하는 접근이다. acceptance criteria(수용 기준)는 완료를 판단하는 관찰 가능한 조건이다. 품질 목표를 정한 뒤 실제 미달해도 결과를 숨기지 말고 이유를 분석해야 한다. 문서 작성 완료·fixture 실행·실제 DB/모델 통합·운영 환경 측정은 서로 다른 증거 수준이다.

**작동 예시/실패 경계:** 최종 50질문은 개발 20 + 동결 holdout 30으로 보고한다. 품질 0.8/P95 5초 같은 목표는 예시이며 W8 조건에 맞춰 동결한다. 권한 누출·무권한 승인은 작성한 필수 테스트에서 0이어야 하고 미통과면 MVP 안전 gate를 완료하지 않는다.

**직접 해 보기:** 각 주차 증거표에 commit/run_id/환경/데이터·모델·프롬프트·인덱스 버전/raw 결과/한계를 넣는다. 숫자가 어디서 왔는지 추적할 수 없는 슬라이드 항목은 제외한다.

### 3.4 8주 자산을 2주 MVP로 조립하기

8주 실습은 공부 과정에서 작은 모듈을 검증하는 단계이며 W9–W10은 완성된 모듈의 통합·최종 평가·문서화에 집중한다. 프로젝트 2주를 새 기술 전부를 처음 배우고 만드는 기간으로 잡으면 일정이 불안정해진다. scope freeze(범위 동결)는 필수 행동·모델·backend·데이터·평가·배포 수준을 확정하는 절차다. 일정은 주 22시간 총 44시간 추정으로 상한을 둔다. 신규 GPU 학습·멀티모달·멀티에이전트·K8s HA·여러 공급자 벤치마크는 추가 과제로 분리한다.

**작동 예시/실패 경계:** W8에 실제 검색이 없으면 W9 첫날부터 구축 시간이 추가되므로 2주 완성 조건을 충족하지 못한다. 계획을 연장하거나 한 backend로 축소하고 누락을 명시한다. gate를 문서 체크만으로 통과시키지 않는다.

**직접 해 보기:** 준비 체크리스트를 실제 실행 출력과 연결해 검토한다. W9 통합 테스트 입력과 W10 최종 시연 3경로를 선정하고 준비 상태를 Jira에 남긴다.

## 4. 실행 가능한 기초 계약 실습

아래는 핵심 규칙을 작게 분리해 CPU에서 확인하는 접근이다. 라이브러리 설치나 실제 모델 호출 없이 개념을 검증한다. 프로젝트 통합 구현과 증거 수준을 구분한다.

실행: `python labs/week-08/contract_demo.py` (저장소 루트).

```python
"""W8: 실제 증거 유무를 직접 입력받는 제작 준비 체크 실습."""
REQUIRED_ASSETS = frozenset({"api_contract", "real_retrieval", "persistent_db",
                             "authorization_review", "reproducible_start", "evaluation_set"})

def missing_assets(evidence: dict[str, bool]) -> list[str]:
    """필수 준비 항목 중 실행 증거가 없는 항목을 찾는다.

    Args:
        evidence: 실제 기록을 확인한 뒤 입력하는 자산별 준비 여부.
    Returns:
        누락된 항목의 정렬된 이름 목록.
    Raises:
        TypeError: 준비 여부가 bool이 아닌 경우.
    """
    if any(not isinstance(value, bool) for value in evidence.values()):
        raise TypeError("evidence flags must be boolean")
    # 자동 실행 검증기가 아니다. True를 쓰기 전에 연결된 실제 증거를 읽어야 한다.
    return sorted(asset for asset in REQUIRED_ASSETS if evidence.get(asset) is not True)

assert len(missing_assets({})) == 6
assert missing_assets({asset: True for asset in REQUIRED_ASSETS}) == []
print("W8 readiness predicate: passed; actual project readiness not asserted")
```

**복잡도/병목:** 필수 자산 수 n에 정렬 포함 O(n log n) 시간/O(n) 공간. 증거 값은 자동 판정하지 않는다.

## 5. 학습 중 만들 재사용 자산 · 상세 작업

아래 app/data/deployment 파일은 **앞으로 작성할 예정 경로**다. 현재 구현된 것으로 읽지 않는다. 작은 계약 실습을 실제 저장소/모델 경로로 확장하는 작업이다.

### 5.1 읽기·실습 상태 점검

부록과 1–16장별 읽기·필수 실습·선택 GPU 실행 표를 작성한다. 선택 미실행과 필수 미완료를 따로 표시한다. Mamba는 현재 MVP에 필수로 도입하지 않는다.

### 5.2 재사용 자산 실제 확인

API 계약·실제 검색·영속 DB·권한 검토·새 환경 기동·dev20/holdout30이 각각 실행 증거와 연결되는지 확인한다. 순수 함수 self-check만으로 실제 통합 준비를 판정하지 않는다.

### 5.3 범위와 config 동결

합성 text corpus 12–24문서·2tenant·활성 버전·모델1개·backend1개·검토 역할·단순 workflow·Compose를 고정한다. prompt/index/schema revision을 기록한다.

### 5.4 설계·비용·목표 리뷰

고객 문제·FR/NFR·권한/네트워크도·모델/backend/workflow ADR·예산 상한·품질/지연 목표를 확정한다. 실제 AWS 배포는 선택이다.

### 5.5 W9 시작 gate

필수 자산이 미완료면 증상·다음 행동·소요 추정을 Jira에 쓴다. 제작 시작일을 옮기거나 범위를 줄인다. 44시간 통합 추정을 무조건 완성 약속으로 쓰지 않는다.

**다음 통합에 넘길 것:** 고객요구사항·ADR·아키텍처/권한/비용표·제작 준비 체크리스트·동결config

## 6. 이해 확인 · 해설을 보기 전에 설명하기

**Q1. 책16장 새 모델을 포트폴리오에 반드시 써야 하는가?**

<details>
<summary>해설</summary>

개념과 트레이드오프를 학습한다. 업무·호환성·검증 이유가 없다면 기존 한 모델 경로를 유지한다.

</details>

**Q2. 8주 학습 후 2주 제작의 전제는 무엇인가?**

<details>
<summary>해설</summary>

재사용 실습 자산과 환경·평가가 준비되어 통합·검증 범위가 44시간 안에 들어오는 것이다.

</details>

**Q3. 학습 문서가 작성됐으면 Jira를 Done으로 바꿀까?**

<details>
<summary>해설</summary>

학습·실습 수용 기준에 본인 설명과 실행 증거가 있을 때 완료한다. 자료 작성은 사용자 학습 완료가 아니다.

</details>

## 7. 공식 자료 · 읽을 범위

- [AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.
- [Mamba 원 논문](https://arxiv.org/abs/2312.00752) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.
- [S4 원 논문](https://arxiv.org/abs/2111.00396) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.

## 증거와 완료 상태

학습 노트에는 읽은 절·자신의 설명·실습 명령·Python/패키지/장치·데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 문서/fixture/실제DB·모델/클라우드·GPU의 수준을 구분한다. 자료 작성만으로 본인의 학습 또는 서비스 제작을 완료 처리하지 않는다. 막히면 증상·시도·다음 행동과 일정 영향을 남긴다.
