# W7 학습 · 멀티모달·에이전트와 배포·관측·복구

**기간:** 2026-11-13–2026-11-19 (Asia/Seoul) · **계획:** 22h · [Notion](https://app.notion.com/p/3ebc6f4a2c7e81909714e0d4739b893f) · [Jira SCRUM-12](https://realrho-1790798942092.atlassian.net/browse/SCRUM-12) · [GitHub #7](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/7)

**이번 주 통과 조건:** 워크플로가 최대 횟수 안에 종료되고 검토가 자동 승인되지 않는다. 컨테이너 재시작 후 DB 자료를 조회하고 readiness/liveness 차이를 설명한다.

[전체 학습표](README.md) · [책 목차 원문](../book-toc.md) · [용어 사전](../glossary-ko-en.md) · [책/보충 범위](../book-gap-map.md)

## 1. 책 읽기와 필수 실습

**배정:** 14장 멀티모달 · 15장 LLM 에이전트

14.1–14.4는 CLIP·디퓨전·DALL-E·LLaVA의 입력/출력과 표현 연결을 읽는다. 15.1–15.4는 에이전트의 모델·감각·행동·단일/다중 형태와 평가를 읽고 AutoGen 기본 예제 한 경로를 따라간다. 멀티모달/멀티에이전트 전체 구현은 핵심 MVP 밖이다.

**필수 실습:** 15장 단일/RAG 에이전트 호출 구조를 추적하고 도구 하나에 최대 호출수·timeout·권한 조건을 붙인다. 14장 예제는 입력 이미지→표현/생성 경로를 설명하는 비교표를 만든다. GPU/유료이미지 생성은 선택으로 두고 원본 출처와 실행 상태를 적는다.

책 본문은 소유한 책에서 읽는다. [공식 코드](https://github.com/onlybooks/llm)·[정오표](https://www.onlybook.co.kr/entry/llm-errata)를 확인하고 환경/모델/패키지 버전을 기록한다. 선택 GPU/멀티모달 실습의 미실행은 필수 완료와 분리한다.

## 2. 실행 순서·시간·수용 기준

| 순서 | 작업 | 계획 시간 | 완료 기준 | Jira |
|---|---|---|---|---|
| 1 | 책 14·15장 읽기·개념 노트 | 6h | 배정된 모든 절을 읽고 개념 관계·비교·질문을 자신의 말로 기록한다. | [SCRUM-38](https://realrho-1790798942092.atlassian.net/browse/SCRUM-38) |
| 2 | 책 필수 실습·환경/결과 기록 | 6h | 15장 단일/RAG 에이전트 호출 구조를 추적하고 도구 하나에 최대 호출수·timeout·권한 조건을 붙인다. 14장 예제는 입력 이미지→표현/생성 경로를 설명하는 비교표를 만든다. GPU/유료이미지 생성은 선택으로 두고 원본 출처와 실행 상태를 적는다. | [SCRUM-39](https://realrho-1790798942092.atlassian.net/browse/SCRUM-39) |
| 3 | SA 보충 강의·재사용 실습 자산 만들기 | 8h | 워크플로가 최대 횟수 안에 종료되고 검토가 자동 승인되지 않는다. 컨테이너 재시작 후 DB자료를 조회하고 readiness/liveness 차이를 설명한다. | [SCRUM-40](https://realrho-1790798942092.atlassian.net/browse/SCRUM-40) |
| 4 | 퀴즈·설명·증거·다음 주 준비 검토 | 2h | 3개 퀴즈를 해설 없이 설명하고 제한된 workflow 계약, Compose기동/지속 볼륨·관측필드·복구runbook 초안를 버전/실행 상태와 함께 저장한다. | [SCRUM-41](https://realrho-1790798942092.atlassian.net/browse/SCRUM-41) |

## 3. SA 보충 강의 · 개념→이유→예제→실습

### 3.1 에이전트와 제한된 워크플로 선택

agent(에이전트)는 목표를 위해 모델의 판단과 도구 실행을 반복하는 시스템이다. workflow(워크플로)는 미리 정한 상태/순서를 따라 작업을 수행한다. node(노드)는 단계, edge(간선)는 다음 연결, checkpoint(체크포인트)는 재개에 필요한 상태 저장이다. AutoGen/LangGraph는 제품 이름이며 영어 약어의 확장 이름을 만들어 붙이지 않는다. 정책검색→출력검증→위험분기→검토 요청처럼 경로가 분명하면 작은 상태 기계만으로 시작할 수 있다. 여러 에이전트를 추가하면 조정 비용·실패 경우·평가 대상이 늘어난다.

**작동 예시/실패 경계:** 모델이 도구를 반복 호출하려 해도 max_steps=3·총 deadline·토큰 예산에서 중단한다. retry는 일시 오류에 제한하고 resume은 checkpoint버전/권한/활성정책을 다시 확인한다. 검토 승인도구를 모델의 허용 목록에 넣지 않는다.

**직접 해 보기:** 입력 상태·노드별 출력·허용 전이·실패 상태를 표로 쓴다. 시작/시간초과/도구 오류/검토 대기/재개 다섯 경로를 fixture로 검증한 뒤 한 실제 도구로 통합한다.

### 3.2 Docker 이미지·컨테이너·Compose

Docker(도커)는 컨테이너 관련 도구의 제품 이름이다. image(이미지)는 실행 코드/의존성의 템플릿, container(컨테이너)는 그 이미지를 실행한 프로세스 환경이다. volume(볼륨)은 컨테이너 수명과 별개로 데이터를 유지하는 저장 장치다. Docker Compose(도커 컴포즈)는 여러 서비스의 설정/연결/기동을 선언하는 도구다. 컨테이너 내부 localhost는 자기 컨테이너를 가리키므로 앱에서 DB호스트는 서비스이름 db로 지정한다. 파일 설치 버전과 이미지태그를 검증해 고정해야 재현성이 높아진다.

**작동 예시/실패 경계:** 서비스는 API+PostgreSQL+선택 벡터backend만 필수다. Pinecone같은 외부backend면 로컬컨테이너가 아니라 외부의존성을 명시한다. Redis는 캐시가 필요하고 검증했을 때만 추가한다. 순서 있는 기동만으로 DB준비가 보장되지는 않는다.

**직접 해 보기:** Dockerfile/compose초안을 작성해 healthcheck와 DB 볼륨을 연결한다. 비밀은 이미지에 굽지 않는다. 새 환경에서기동 → 의존성준비확인→케이스저장→API재시작→조회 순으로 검증한다.

### 3.3 관측과 SLI·SLO·릴리스 경계

observability(관측 가능성)는 외부 신호로 시스템 내부 상태를 설명할 수 있는 정도다. log(로그)는 사건 기록, metric(메트릭)은 수치 시계열, trace(트레이스)는 한 요청의 여러 구간 연결이고 span(스팬)은 그 안의 한 작업이다. OTel, OpenTelemetry(오픈텔레메트리)는 이런 신호를 계측/전달하는 프로젝트다. SLI, Service Level Indicator(서비스 수준 지표)는 실제 측정치, SLO, Service Level Objective(서비스 수준 목표)는 내부 목표, SLA, Service Level Agreement(서비스 수준 계약)는 고객과의 합의다. CI, Continuous Integration(지속적 통합)은 변경의 자동검증, CD는 이 계획에서 Continuous Delivery(지속적 전달)로 사용하며 배포 준비와 실제 배포를 구분한다.

**작동 예시/실패 경계:** 프로세스 liveness(살아 있음)와 readiness(요청 처리 준비)를 나눈다. DB가 죽었을 때 liveness200/readiness503을 기대할 수 있다. P95 5초라는 목표에는 요청길이·동시성·환경·모델을 붙이며 실제 결과를 별도 기록한다.

**직접 해 보기:** request_id와 case_id로 intake/retrieve/generate/validate/persist의 시간·성공·오류종류를 연결한다. CI에서입력/권한/상태/검색필터회귀를실행한다. 토큰/원문비밀은로그에서제외한다. 실제 계측없으면관측설계문서만완료한다.

### 3.4 백업·RTO/RPO·Kubernetes의 위치

RTO, Recovery Time Objective(복구 시간 목표)는 서비스 복구까지 허용할 시간, RPO, Recovery Point Objective(복구 시점 목표)는 허용할 데이터 손실 구간이다. backup(백업)은 복구할 사본이며 restore(복원)로 읽을 수 있는지 확인해야 의미가 있다. 컨테이너 재시작 후 데이터가 남는 것은 지속성 증거지만 디스크 손실 복구 증거와 다르다. Kubernetes(쿠버네티스, K8s)는 컨테이너 배포/운영을 조정하는 플랫폼이다. Pod는 배포 단위, Deployment는 복제/업데이트 관리, Service는 안정된 연결 입구다. 운영체계가 커질 때 유용하지만 이번2주MVP에 새클러스터 구축을 필수로 넣지 않는다.

**작동 예시/실패 경계:** 실습목표 RTO30분/RPO24시간은 가상의 설계값이다. DB 볼륨과 별도의백업을 준비해 새 DB로복원한 뒤 케이스·감사행을 조회하고 걸린시간을 잰다. Kubernetes설계도와 실제 배포 완료를 구분한다.

**직접 해 보기:** 복구runbook에증상→확인→복원→검증→재개를 적는다. 잘못된마이그레이션/모델 API중단/DB중단에대한fallback을 정의한다. 시간이 부족하면 K8s는 개념·ADR만 남기고 Compose복구를완료한다.

## 4. 실행 가능한 기초 계약 실습

아래는 핵심 규칙을 작게 분리해 CPU에서 확인하는 접근이다. 라이브러리 설치나 실제 모델 호출 없이 개념을 검증한다. 프로젝트 통합 구현과 증거 수준을 구분한다.

실행: `python labs/week-07/contract_demo.py` (저장소 루트).

```python
"""W7: 에이전트 도구 호출을 제한하는 순수 함수 실습."""
def bounded_workflow(actions: list[str], max_steps: int = 3) -> str:
    """허용된 도구만 최대 단계 수 안에서 처리한다.

    Args:
        actions: 모델이 제안했다고 가정한 도구 이름의 fixture 목록.
        max_steps: 허용할 최대 도구 개수.
    Returns:
        완료 시 COMPLETED, review 요청 시 REVIEW_PENDING.
    Raises:
        ValueError: 최대 단계가 양수가 아니거나 횟수 초과인 경우.
        PermissionError: 허용 목록 밖의 도구인 경우.
    """
    if max_steps < 1 or len(actions) > max_steps:
        raise ValueError("step budget exceeded")
    for action in actions:
        if action not in {"retrieve", "validate", "request_review"}:
            raise PermissionError("tool not allowed")
        if action == "request_review":
            return "REVIEW_PENDING"  # 검토 요청은 자동 승인과 다르다.
    return "COMPLETED"

assert bounded_workflow(["retrieve", "validate", "request_review"]) == "REVIEW_PENDING"
for actions in [["approve"], ["retrieve"] * 4]:
    try:
        bounded_workflow(actions)
    except (PermissionError, ValueError):
        pass
    else:
        raise AssertionError("unbounded or unauthorized action")
print("W7 workflow fixture: passed; real agent/deployment not validated")
```

**복잡도/병목:** 허용 단계 수 n에 시간 O(n), 추가 공간 O(1). 실제 LLM·도구·checkpoint·타임아웃은 별도 통합한다.

## 5. 학습 중 만들 재사용 자산 · 상세 작업

아래 app/data/deployment 파일은 **앞으로 작성할 예정 경로**다. 현재 구현된 것으로 읽지 않는다. 작은 계약 실습을 실제 저장소/모델 경로로 확장하는 작업이다.

### 5.1 작은 workflow 연결

예정 `app/workflows/analyze.py`는 retrieve→generate→validate→riskroute→persist 순서를 명시한다. max_steps/deadline/토큰 예산·실패 상태를 정한다. 이미 실습한 라이브러리 하나 또는 단순 상태 기계만 사용한다.

### 5.2 Compose 환경

예정 Dockerfile·compose.yaml은 API·DB·선택 backend를 구성한다. 이미지/패키지 버전·DB 볼륨·서비스 DNS·healthcheck·환경변수 설정을 남긴다. Redis/전체 OTel 스택/K8s 클러스터는 필수로 추가하지 않는다.

### 5.3 관측 필드 최소 구현

request_id·case_id·단계·duration·오류 종류·usage·버전을 연결하는 구조화 로그를 설계·실행한다. 원문·비밀은 제외한다. /health와 /readiness는 의존성 준비 실패를 구분한다.

### 5.4 CI와 복구 초안

예정 `.github/workflows/ci.yml`에 계약·권한·상태·필터 회귀를 연결한다. `docs/runbooks/recovery.md`에 DB 백업→새 DB 복원→조회 확인 절차를 쓴다. 실제 실행한 명령·결과만 완료로 표시한다.

### 5.5 재개 검증

검토 대기 case가 재시작 후 같은 상태인지 확인한다. checkpoint에 policy/model/prompt 버전을 저장하고 resume 시 권한·활성 버전을 재검사한다. 모델이 검토를 자동 승인하지 못하게 한다.

**다음 통합에 넘길 것:** 제한된 workflow 계약, Compose기동/지속 볼륨·관측필드·복구runbook 초안

## 6. 이해 확인 · 해설을 보기 전에 설명하기

**Q1. 컨테이너를 재시작해 데이터가 남으면 백업 검증도 끝인가?**

<details>
<summary>해설</summary>

지속성만 확인했다. 별도 사본에서 새저장소로 복원하는 검증이 필요하다.

</details>

**Q2. readiness와liveness는 같은가?**

<details>
<summary>해설</summary>

프로세스존재와처리준비를 다르게 확인한다. 의존성장애를 구분한다.

</details>

**Q3. 에이전트가 자율적이면 권한도 스스로 결정하는가?**

<details>
<summary>해설</summary>

서버의검증된신원·허용도구·상태계약이 결정한다.

</details>

## 7. 공식 자료 · 읽을 범위

- [Docker Compose](https://docs.docker.com/compose/) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.
- [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.
- [Kubernetes overview](https://kubernetes.io/docs/concepts/overview/) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.

## 증거와 완료 상태

학습 노트에는 읽은 절·자신의 설명·실습 명령·Python/패키지/장치·데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 문서/fixture/실제DB·모델/클라우드·GPU의 수준을 구분한다. 자료 작성만으로 본인의 학습 또는 서비스 제작을 완료 처리하지 않는다. 막히면 증상·시도·다음 행동과 일정 영향을 남긴다.
