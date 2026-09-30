# W7. 재현 가능한 배포와 장애 복구 만들기

> 새 환경에서 같은 버전으로 실행하고, 의존 서비스 장애와 복구를 관찰할 수 있는 배포 패키지를 완성한다.

2026-11-12 → 2026-11-18 · 총 22h (주당 계획 가정)

[Jira SCRUM-12](https://realrho-1790798942092.atlassian.net/browse/SCRUM-12) · [GitHub #7](https://github.com/realrho/test/issues/7) · [W6 선행 과정](https://app.notion.com/p/3ebc6f4a2c7e8156b65ddfe5240f458e)

## 학습 목표와 시작 조건

**기술:** Docker Compose · Networking · Health/Readiness · Observability · CI · AWS 설계 · Kubernetes 기초

**시작 조건:** W6 전체 기능·PostgreSQL·Milvus·Redis·guardrail. Docker는 W2부터 필요한 부분을 학습했으며 이번 주에 전체 서비스로 통합한다.

이 페이지는 학습 교재와 앞으로 구현할 작업이다. 문서가 작성된 것을 서비스 구현/평가 완료로 표시하지 않는다. 학습은 아래 4개 강의→손 실습→코드 실습→빌드→퀴즈→증거 제출 순서로 진행한다.

## 이번 주 시간표

- D1 3h: image/Compose/network/volume·버전 고정
- D2 3h: full stack·migration/ingest 실행 순서
- D3 3h: live/ready·dependency 장애·restart
- D4 3h: JSON trace·metrics·fixture CI
- D5 4h: backup/restore·runbook·AWS reference
- D6 4h: clean run 검증·K8s 선택 실습·readiness 리뷰
- D7 2h: 복습·운영 한계 정리·버퍼

## 개념 강의

### 1. Container·image·network·volume: 무엇이 실행되고 어디에 저장되는가

Image는 실행 환경과 파일의 스냅샷, container는 이를 실행하는 프로세스 환경이다. Dockerfile은 image 생성 절차이고 Compose는 여러 service의 설정과 연결을 표현한다. ‘내 PC에서는 된다’를 줄이려면 runtime·패키지·image 버전을 고정하고 실제로 검증한 조합을 기록한다. latest tag나 느슨한 의존성은 나중에 같은 결과를 보장하지 않는다.

Container 안의 localhost는 그 container 자신이다. API에서 postgres:5432·redis:6379·milvus:19530처럼 service DNS 이름으로 연결하고, host에 꼭 필요한 port만 publish한다. 사용자 데모는 localhost bind를 기본으로 한다. secret을 Dockerfile/README/commit에 넣지 말고 실행 환경에서 제공한다.

Volume은 container 교체 뒤에도 데이터를 보존한다. Postgres 데이터·Milvus 데이터와 그 의존 저장소·필요 checkpoint를 어디에 보관하는지 그린다. Milvus Standalone은 단일 app 프로세스만이 아니라 공식 구성의 etcd/object storage 같은 의존성을 포함할 수 있으므로 그 compose를 기준으로 묶는다. image에서 DB 파일을 복사한 것을 백업 전략이라 부르지 않는다.

### 2. Liveness·readiness·startup: 의존성 장애로 재시작 폭풍을 만들지 않는다

Liveness는 프로세스가 살아 응답할 수 있는지, readiness는 요청을 받을 준비가 됐는지, startup은 긴 초기화를 기다리는 조건이다. DB가 잠깐 느리다고 liveness를 실패시키면 모든 app이 재시작하고 부하가 커질 수 있다. 외부 LLM API는 readiness 매번 호출하지 말고 내부 상태·최근 장애·실행 예산과 별도 관측을 사용한다.

/health/live는 프로세스 응답, /health/ready는 필수 저장소와 schema 준비를 확인한다. Redis는 optional cache라 장애가 나면 miss로 처리하고 서비스 전체를 무조건 unavailable로 만들지 않는다. Milvus나 Postgres가 필수인 기능은 503이나 명확한 degraded 상태를 반환한다. healthcheck 통과는 end-to-end 정답 품질 보증이 아니다.

retry·connection pool·rate limit·request size 제한을 함께 잡고 graceful shutdown 때 새 작업 접수를 멈추고 진행 중 작업을 정리한다. cases/reviews 영속 상태와 작업 큐 보장을 혼동하지 않는다. 오래 걸리는 작업은 별도 durable queue가 필요하며 미구현이면 운영 한계로 문서화한다.

### 3. Logs·metrics·traces·CI: 문제의 위치를 증거로 찾는다

Log는 이벤트 기록, metric은 집계 수치, trace는 요청이 각 단계에서 보낸 시간과 경로다. JSON log에 request_id/case_id/route/node/model/index version/status/duration/token/error category를 남긴다. 질문 원문·PII·API key는 제외한다. trace_id 하나로 검색→모델→검증→저장 단계를 따라갈 수 있어야 한다.

주요 지표는 성공/실패/timeout/abstain/review율·P95·cache hit·token 비용·검토 queue 길이다. 운영 alert는 단일 느린 요청보다 지속 오류율·budget 소진·대기열 증가처럼 행동으로 이어질 신호를 사용한다. runbook에는 증상→확인할 로그/지표→완화→복구→검증 순서를 적는다.

CI는 PR마다 unit/contract 검증을 재현한다. real LLM 테스트는 비용·비결정성·secret 의존성이 있어 fixture CI와 별도 opt-in integration job으로 나눈다. fixture 통과를 실제 모델/클라우드 운영 증거로 쓰지 않는다. workflow 최소 권한·비밀 관리·실패 로그를 정하고 검증 환경의 버전을 남긴다.

### 4. Cloud와 Kubernetes: 배포 경로를 요구사항으로 설명한다

AWS reference는 HTTPS 진입·app runtime·private data services·secret store·logs·budget alarm 경계를 그린다. 학습 규모에서는 단일 VM+Compose가 단순하지만 HA·backup·patch 부담을 가진다. 관리형 DB는 운영 부담을 줄이지만 비용·연결·egress를 고려한다. Milvus를 ECS의 가벼운 단일 stateless container처럼 설명하면 저장 의존성을 놓친다.

이번 주 필수는 로컬 full stack 재현과 AWS 설계/비용/보안 문서다. 실제 cloud 배포는 계정·region·예산·public demo 범위가 정해진 경우에만 선택한다. 설계 그림·Terraform 파일만으로 실제 배포를 완료했다고 쓰지 않는다. 권한·실행 비용은 구현 검증 결과와 구분한다.

Kubernetes의 Pod는 실행 단위, Deployment는 복제본/rolling update 관리, Service는 안정적인 접근점, ConfigMap은 설정, Secret은 민감값 참조다. base64 자체는 암호화가 아니다. 로컬 kind/minikube에서 API replica 1→3·readiness·rolling update를 실습할 수 있다. 공유 Postgres/checkpoint 없이 replica를 늘리면 HITL/사례 조회가 깨질 수 있다. vector DB distributed cluster는 이 과정 필수가 아니다.



## 따라 하는 실습과 예상 결과

새 환경 또는 깨끗한 실행 경로에서 버전이 고정된 Compose로 API+Postgres+Milvus+Redis를 실행한다. migration→ingest→정상 분석→근거 부족→사람 검토→restart→resume를 검증한다. Redis 중단은 cache miss fallback, Milvus 중단은 해당 검색 기능 명시 실패, Postgres 중단은 쓰기 실패를 관찰한다.

backup→새 테스트 volume에 restore→사례/정책 version/검토 상태 확인을 수행한다. 실제 데이터를 파괴하는 down -v는 일반 실행 안내에 넣지 않는다. local K8s는 리소스가 되면 API만 1→3 replica·readiness·rolling update를 하고 real cloud/HA 테스트는 별도 기록한다.

## 코드로 확인하는 핵심 원리

관측을 붙일 때 데이터 최소화부터 연습한다. 아래 helper는 trace backend가 아니라 JSON log shape 실습이다.

```python
import json


def safe_event(request_id: str, elapsed_ms: float, status: str) -> str:
    """허용된 운영 필드만 포함한 JSON 이벤트를 반환한다.

    Args:
        request_id: 원문을 담지 않는 요청 추적 ID.
        elapsed_ms: 측정한 처리 시간(ms).
        status: 완료/실패 등 업무 상태.
    Returns:
        JSON 문자열. 사용자 text/secret은 포함하지 않는다.
    Raises:
        ValueError: ID가 비었거나 처리 시간이 음수일 때.
    """
    if not request_id or elapsed_ms < 0:
        raise ValueError('request ID and non-negative duration required')
    # payload 전체를 로그로 복사하지 않고 필요한 필드만 allowlist한다.
    return json.dumps({'request_id': request_id,
                       'elapsed_ms': elapsed_ms, 'status': status})

assert 'text' not in json.loads(safe_event('req-001', 12.0, 'COMPLETED'))
```

**복잡도와 병목:** 고정 필드 log serialization은 필드 길이에 비례. 운영 병목은 model rate limit·DB connection·vector memory·queue이며 replica 수만 늘려 해결되지 않는다.

## 프로젝트에서 빌드할 부분

### W7.1 버전 고정 full-stack Compose·실행 순서 · 5h

**왜 필요한가:** 다음 구현을 판단할 계약·데이터·환경을 먼저 확정한다.

**수정/작성 위치:** deployment/docker/, compose.yaml, docs/runbook.md

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W6 완료 gate가 선행한다.

**완료 조건:** API/Postgres/Milvus/Redis·의존 저장·volume·service DNS·migration/ingest 실행을 새 환경에서 재현한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W7.2 Health/readiness·장애·restart·restore 검증 · 6h

**왜 필요한가:** 개념을 실제 핵심 경로에 연결해 다음 검증의 기준선을 만든다.

**수정/작성 위치:** app/api/health.py, tests/integration/, reports/w07/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W7.1의 산출물이 선행한다.

**완료 조건:** Redis/Milvus/Postgres 장애 동작·재시작 HITL·별도 volume restore를 검증하고 데이터 손실 여부를 기록한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W7.3 민감값 없는 관측·fixture CI·runbook · 6h

**왜 필요한가:** 실패·권한·복구 경계를 구현해 정상 시연만으로 놓치는 문제를 찾는다.

**수정/작성 위치:** .github/workflows/, app/observability/, docs/runbook.md

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W7.2의 산출물이 선행한다.

**완료 조건:** 단계별 trace와 주요 metric을 남기고 fixture CI를 재현한다. 실제 LLM/cloud 검증과 구분하며 secret/PII를 기록하지 않는다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W7.4 AWS reference·운영 trade-off·K8s 기초 리뷰 · 5h

**왜 필요한가:** 검증 결과를 설계 결정과 다른 사람이 확인할 증거로 바꾼다.

**수정/작성 위치:** docs/cloud-reference.md, docs/architecture.md, deployment/kubernetes/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W7.3의 산출물이 선행한다.

**완료 조건:** HTTPS/IAM/secret/private storage/budget/backup 경계를 설명한다. K8s는 실행/미실행 상태를 기록하고 cloud는 계정/예산 없으면 설계로 표시한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.



## 주차 완료 기준

- [ ] clean setup에서 Compose full-stack·migration·ingest·3개 데모 흐름 재현
- [ ] 의존 서비스 장애·restart·backup/restore 검증 결과
- [ ] JSON 관측·fixture CI·runbook·실제/모의 실행 구분
- [ ] AWS 설계/비용 경계·K8s 학습/실행 상태·운영 한계 문서화

## 이해 확인 퀴즈

**Q1. 컨테이너에서 localhost:5432는 다른 DB 컨테이너인가?**

<details>
<summary>해설 확인</summary>

자기 컨테이너다. Compose service DNS를 사용한다.

</details>

**Q2. DB 장애면 모든 app liveness를 실패시켜야 하나?**

<details>
<summary>해설 확인</summary>

readiness와 기능 장애로 다뤄 재시작 폭풍을 피한다. 프로세스 생존과 준비 상태를 나눈다.

</details>

**Q3. 3 replica면 고가용성 검증 완료인가?**

<details>
<summary>해설 확인</summary>

공유 상태·의존 DB·복구·load·배포 조건을 검증해야 한다. local replica 실습만으로 HA를 주장하지 않는다.

</details>



## 면접에서 설명할 한 문장

“이번 주에는 새 환경에서 같은 버전으로 실행하고, 의존 서비스 장애와 복구를 관찰할 수 있는 배포 패키지를 완성한다. 이를 확인한 증거는 ___이며, 아직 확인하지 못한 범위는 ___입니다.”

기술 이름을 외우기보다 선택 이유·실패 경우·측정 조건·대안을 자기 말로 설명한다.

## 공식 자료: 읽을 범위와 사용법

- [Docker port publishing](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [Milvus 운영 환경 조건](https://milvus.io/docs/prerequisite-docker.md) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [Kubernetes probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [GitHub Actions 개념](https://docs.github.com/en/actions/get-started/understand-github-actions) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [AWS GenAI lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.

문서 URL은 2026-10-01 확인. 설치/API 세부는 실습 시 사용 버전의 공식 문서를 다시 확인한다. 본 강의 설명·실습·프로젝트 판단 기준은 이 포트폴리오를 위해 작성한 교육 내용이다.

## 선택 심화·환경이 막힐 때

실제 AWS 배포·Terraform·local K8s replica 실습은 환경/예산에 따라 심화. 로컬 full-stack과 장애/복구 검증은 필수.

핵심 gate가 안 되면 Jira에 실패 증상·환경·시도·다음 행동을 기록한다. fixture로 계약 학습을 이어 갈 수 있지만 real DB/model/cloud/GPU 완료로 바꾸지 않는다.


## Jira 실행 작업 바로가기

| 순서 | 작업·시간 | 선행 |
|---|---|---|
| 7.1 | [SCRUM-38](https://realrho-1790798942092.atlassian.net/browse/SCRUM-38) · 버전 고정 full-stack Compose·실행 순서 · 5h | SCRUM-11 |
| 7.2 | [SCRUM-39](https://realrho-1790798942092.atlassian.net/browse/SCRUM-39) · Health/readiness·장애·restart·restore 검증 · 6h | SCRUM-38 |
| 7.3 | [SCRUM-40](https://realrho-1790798942092.atlassian.net/browse/SCRUM-40) · 민감값 없는 관측·fixture CI·runbook · 6h | SCRUM-39 |
| 7.4 | [SCRUM-41](https://realrho-1790798942092.atlassian.net/browse/SCRUM-41) · AWS reference·운영 trade-off·K8s 기초 리뷰 · 5h | SCRUM-40 |

## 구현 레시피 · 새 환경·장애·복구

1. Dockerfile에 runtime·실검증 dependency version·non-root 실행·health 경로를 정한다.
2. Compose에 API·Postgres·Redis·Milvus 공식 구성 의존 service/volume을 선언한다. 외부 secret은 파일/환경 참조로 받고 저장소에 넣지 않는다.
3. service DNS·internal port·localhost publish·connection pool·resource limit을 정한다.
4. migration→ingestion→API 준비 순서를 실제로 검사한다. service가 실행 중인 것과 query 가능 상태는 다르다.
5. live/ready·optional Redis degraded behavior·필수 DB/Milvus failure를 시험한다.
6. fixture CI는 secret 없이 돌리고 실제 모델 integration은 opt-in으로 분리한다.
7. 백업을 별도 테스트 volume에 복원하고 case/version/review 상태를 확인한다.
8. AWS reference는 public entry·private services·IAM/secret/log/budget/backup을 그린다.
9. resource가 되면 local K8s API 1→3 replica·readiness·rolling update를 추가한다.

### 운영 확인 명령의 의미

다음 파일은 W7에 직접 만들 파일이다. 지금 root에 compose.yaml이 없는 상태에서는 실행되지 않는다.

~~~powershell
# 구현된 compose 파일이 있는 폴더에서만 실행한다.
docker compose config
docker compose up -d --build
docker compose ps
docker compose logs --tail 100 api
~~~

config는 설정 해석, up은 생성/시작, ps는 service 상태, logs는 실행 기록 확인이다. logs에 secret/원문 PII가 섞였는지 확인한다. 데이터 volume을 지우는 명령은 정상 종료 안내에 사용하지 않는다.

### 검증 표

clean setup·normal·abstain·HITL·Redis outage·Milvus outage·DB outage·process restart·backup/restore·optional K8s 각각 expected/actual/status/run ID를 적는다. local Compose 성공을 cloud HA 검증으로 표현하지 않는다.
