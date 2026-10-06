# W7 학습 — 관측·Docker·Kubernetes·CI/CD·복구

**주교재:** 『AI 에이전트 엔지니어링』 · **책 범위:** 10장 운영 환경 모니터링

**일정:** 2026-11-13–2026-11-19 (Asia/Seoul) · **총 계획:** 22h

[Notion 주차](https://app.notion.com/p/3ebc6f4a2c7e81909714e0d4739b893f) · [GitHub #7](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/7)

## 1. 이번 주 목표와 책 읽기

10.1–10.10 전체: 모니터링 스택 선택·OpenTelemetry 계측·시각화/알림·섀도/카나리·회귀 트레이스·자가 치유·피드백·분포 변화·지표 소유권. 9.4 배포 준비와 8.9 상태/영속성도 복습한다.

**필수 실습:** Dockerfile과 Compose로 앱/DB를 재현 기동한다. 관측 필드·트레이스를 연결하고 DB 재시작/별도 백업 복원을 확인한다. 로컬 Kubernetes에서 API Deployment·Service·설정·probes·자원 제한·롤백을 실습한다. CI는 테스트·이미지 빌드 한 경로를 만든다.

**재사용 산출물:** Dockerfile·Compose, 로컬 Kubernetes 설정/배포 기록, CI workflow, 구조화 로그·트레이스, 백업/복구 runbook

**완료 기준:** 같은 버전으로 재현 기동하고 readiness/liveness를 구분한다. 로컬 배포·롤백·상태 확인과 DB 백업 복원 증거가 있으며 비밀 값이 Git/로그에 없다.

## 2. 책·영상·실습을 연결한 22h 실행 순서

| 순서 | 활동 | 계획 시간 | 결과/목적 |
|---|---|---|---|
| 1 | 책 읽기·설계 노트 | 6h | 10.1–10.10 전체: 모니터링 스택 선택·OpenTelemetry 계측·시각화/알림·섀도/카나리·회귀 트레이스·자가 치유·피드백·분포 변화·지표 소유권. 9.4 배포 준비와 8.9 상태/영속성도 복습한다. |
| 2 | 승인 영상 선택 시청 | 4.5h | 묶음 4·5·7. 아래 보는 시점·범위를 따른다. |
| 3 | 책 개념 프로젝트 실습 | 6h | Dockerfile과 Compose로 앱/DB를 재현 기동한다. 관측 필드·트레이스를 연결하고 DB 재시작/별도 백업 복원을 확인한다. 로컬 Kubernetes에서 API Deployment·Service·설정·probes·자원 제한·롤백을 실습한다. CI는 테스트·이미지 빌드 한 경로를 만든다. |
| 4 | 영상과 연결한 SA 실습 | 3.5h | Dockerfile·Compose, 로컬 Kubernetes 설정/배포 기록, CI workflow, 구조화 로그·트레이스, 백업/복구 runbook |
| 5 | 설명·퀴즈·증거 검토 | 2h | 같은 버전으로 재현 기동하고 readiness/liveness를 구분한다. 로컬 배포·롤백·상태 확인과 DB 백업 복원 증거가 있으며 비밀 값이 Git/로그에 없다. |

영상 배정은 주간 시간 안에 포함된 선택 시청·메모 시간이다. 영상마다 아래 시청 직후 실습을 이어서 수행한다. 순서는 진행 안내이며 주차 체크리스트 네 작업은 읽기6h·개념 실습6h·영상/SA8h·검토2h로 시간을 집계한다.

## 3. 이번 주에 볼 한국어 영상과 연결 실습

### 영상 1. Docker · 학습 묶음 4

**보는 시점:** 10장 관측 필드와 배포 대상 이해 다음.

- [도커: 이미지 만드는 법 - Dockerfile & build](https://www.youtube.com/watch?v=0kQC19w0gTI) — 생활코딩, 한국어 수업.
- [Docker Compose](https://www.youtube.com/watch?v=EK6iYRCIjYs) — 생활코딩, 한국어 수업.

**볼 범위:** W1에 이어 Dockerfile/build 약 18분 + Compose 약 16분. 같은 입문 목록 전체를 반복하지 않는다.

**시청 직후 실습:** API 이미지, DB 볼륨, healthcheck, 설정/비밀 분리를 구현하고 Compose 재기동 및 DB 복원을 확인한다.

### 영상 2. Kubernetes · 학습 묶음 5

**보는 시점:** Docker 이미지·상태/설정 분리 다음.

- [[따배쿠] 쿠버네티스 시리즈](https://www.youtube.com/playlist?list=PLApuRlvrZKohaBHvXAOhUD-RxD0uQ3z0c) — TTABAE-LEARN, 한국어 수업.

**볼 범위:** 5-2 probes, 5-6 자원, 6-3 Deployment, 7-1 Service, 10 ConfigMap, 11 Secret을 선택한다. 실행에 필요한 예제부터 보고 남는 심화는 추가 시간에 본다.

**시청 직후 실습:** W3 로컬 클러스터에 API를 Deployment/Service로 배포한다. readiness/liveness·requests/limits·ConfigMap/Secret·로그·롤백을 실제 확인한다. Secret의 base64는 암호화가 아니다.

### 영상 3. CI/CD · 학습 묶음 7

**보는 시점:** 로컬 배포가 재현된 뒤 다음.

- [[10분 테코톡] 도비의 CI/CD와 Github Action](https://www.youtube.com/watch?v=SKILL1pT6f4) — 우아한테크, 한국어 수업.

**볼 범위:** CI/CD와 GitHub Actions 개념을 보고 공식 문서로 프로젝트용 최소 workflow를 만든다.

**시청 직후 실습:** 검증→테스트→이미지 빌드 단계와 실패 차단을 확인한다. 자동 운영 배포 권한은 설계에서 검토한다.


**AWS 연결 실습:** W5 사용자 지정 AWS 영상/교안의 서버 접속·배포 흐름을 기존 FastAPI/Compose 로컬 실습에 적용한다. Express/Spring 문법을 새로 배우지 않고 실행 명령·포트·환경 변수·로그·재시작/복원 증거를 남긴다. EC2 실제 배포는 선택 심화다.

## 4. 영어·한국어 개념 강의

### 7.1 Dockerfile·Compose — 이미지 제작과 서비스 묶음

Dockerfile은 이미지를 만들 절차, Compose는 여러 서비스·네트워크·볼륨의 구성을 선언한다. build-time(빌드 시점)과 runtime(실행 시점)의 설정을 구분한다. 비밀정보를 이미지 층이나 Git에 넣지 않고 검증한 의존성·이미지 버전을 기록한다. DB 볼륨이 남는 것과 독립 백업에서 복원되는 것은 다른 검증이다.

**업무 예시:** API와 DB를 별도 서비스로 만들고 DB 준비 실패를 관측한다. 컨테이너 생성 순서만으로 DB 준비가 끝났다고 가정하지 않는다.

**직접 할 일:** Dockerfile/build·Compose 영상을 보고 예정 Dockerfile·compose.yaml을 작성한다. 깨끗한 기동·종료·재기동·의존성 실패를 기록한다.

### 7.2 Deployment·Probe·Secret — Kubernetes 운영 경계

Deployment는 업데이트와 복제 상태를 관리하고 Service는 Pod 교체와 독립된 접근 지점을 제공한다. readiness probe(준비 상태 검사)는 요청 수신 가능 여부, liveness probe(생존 상태 검사)는 재시작 판단, startup probe(시작 검사)는 느린 초기화를 다룬다. requests/limits(요청 자원/제한)는 스케줄링과 자원 사용에 영향을 준다. ConfigMap은 일반 설정, Secret은 민감 값을 위한 자원이다. base64 인코딩 자체는 암호화가 아니다.

**업무 예시:** 외부 모델 장애마다 liveness를 실패시키면 재시작 폭풍이 생길 수 있다. readiness 실패와 업무 오류를 구분하고 운영 요구에 맞는 검사 범위를 정한다.

**직접 할 일:** 따배쿠 5-2·5-6·6-3·7-1·10·11을 선별한다. 최신 공식 로컬 환경에서 API Deployment/Service·설정 주입·롤백을 실행한다. 영속 볼륨·RBAC·Ingress/Gateway 선택은 설계표로 보충한다.

### 7.3 CI/CD·Release — 검증과 배포 절차

CI, Continuous Integration(지속적 통합)는 변경마다 자동 검증을 수행한다. CD는 Continuous Delivery(지속적 전달) 또는 Continuous Deployment(지속적 배포)를 뜻하며 승인 방식에 따라 구분한다. GitHub Actions는 실행 자동화 제품이다. 테스트 성공·이미지 빌드·배포·배포 후 확인을 다른 단계로 기록하고 실패하면 다음 단계로 진행하지 않게 한다.

**업무 예시:** 테스트 통과가 실제 모델 품질이나 복구 성공을 증명하지는 않는다. 비밀 키를 YAML에 쓰지 않고 제한된 실행 권한을 사용한다.

**직접 할 일:** 영상 7 후 공식 문서로 테스트→이미지 빌드 workflow를 만든다. 로컬/검토 환경의 배포 후 상태 확인과 롤백 명령을 작성한다.

### 7.4 Observability·Recovery — 관측과 복구 증거

observability(관측 가능성)는 로그·지표·트레이스로 내부 실패를 설명할 수 있는 정도다. OpenTelemetry는 계측 표준/도구, Langfuse는 모델 실행 관측 제품이다. trace(트레이스)는 요청의 단계와 지연을 연결한다. SLO, Service Level Objective(서비스 수준 목표)는 품질/가용성 목표다. RTO, Recovery Time Objective(목표 복구 시간), RPO, Recovery Point Objective(목표 복구 시점)는 복구 시간과 허용 데이터 손실 기준이다.

**업무 예시:** request_id·case_id·run_id로 검색·모델·검증·DB 구간을 연결한다. 민감한 원문·토큰을 통째로 로그에 남기지 않는다. 백업 파일 생성만으로 복구 성공이라 보고하지 않는다.

**직접 할 일:** 한 관측 경로를 선택하고 장애→알림→진단→복원→검증을 runbook(운영 절차서)으로 적는다. 별도 백업에서 실제 조회까지 확인한다.

## 5. 확인 퀴즈

### Q1. readiness와 liveness는 같은 검사인가?

**해설:** 요청을 받을 준비와 재시작 필요 판단은 다르다. 외부 의존성 실패를 무조건 생존 실패로 처리하지 않는다.

### Q2. Kubernetes Secret은 base64라서 안전하게 암호화되는가?

**해설:** base64는 인코딩이다. 최소 권한·저장 암호화·노출 방지 등 별도 보호가 필요하다.

### Q3. 백업 파일이 생성됐으면 복구 검증도 끝나는가?

**해설:** 복원 후 실제 상태·데이터 조회와 시간/손실 조건을 확인해야 한다.

## 6. 주차 체크리스트·수용 기준

- **W7.1 · 책 10장 읽기·설계/개념 노트 (6h)**
  - 선행: W6.
  - 수용 기준: 10.1–10.10 전체: 모니터링 스택 선택·OpenTelemetry 계측·시각화/알림·섀도/카나리·회귀 트레이스·자가 치유·피드백·분포 변화·지표 소유권. 9.4 배포 준비와 8.9 상태/영속성도 복습한다. 산출물: 핵심 용어의 영어·한글 뜻과 업무 설계 메모.
- **W7.2 · 책 개념을 적용한 프로젝트 실습 (6h)**
  - 선행: W7.1.
  - 수용 기준: Dockerfile과 Compose로 앱/DB를 재현 기동한다. 관측 필드·트레이스를 연결하고 DB 재시작/별도 백업 복원을 확인한다. 로컬 Kubernetes에서 API Deployment·Service·설정·probes·자원 제한·롤백을 실습한다. CI는 테스트·이미지 빌드 한 경로를 만든다. 산출물: 정상/실패 expected/actual·raw 결과.
- **W7.3 · 영상·SA 보충 실습 — 관측·Docker·Kubernetes·CI/CD·복구 (8h)**
  - 선행: W7.2.
  - 수용 기준: 승인 영상 배정 4.5h + 연결 실습 3.5h. Dockerfile·Compose, 로컬 Kubernetes 설정/배포 기록, CI workflow, 구조화 로그·트레이스, 백업/복구 runbook. 같은 버전으로 재현 기동하고 readiness/liveness를 구분한다. 로컬 배포·롤백·상태 확인과 DB 백업 복원 증거가 있으며 비밀 값이 Git/로그에 없다.
- **W7.4 · 퀴즈·본인 설명·증거·다음 주 준비 검토 (2h)**
  - 선행: W7.3.
  - 수용 기준: 퀴즈 3개를 자신의 말로 설명하고 정상/실패 증거와 다음 주 선행 조건을 검토한다.

## 7. 공식 문서와 증거

- [Docker Compose](https://docs.docker.com/compose/) — 현재 API·설치·보안 설정을 확인한다.
- [Kubernetes 로컬 기초](https://kubernetes.io/docs/tutorials/kubernetes-basics/) — 현재 API·설치·보안 설정을 확인한다.
- [Kubernetes probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) — 현재 API·설치·보안 설정을 확인한다.
- [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) — 현재 API·설치·보안 설정을 확인한다.
- [GitHub Actions CI](https://docs.github.com/en/actions/get-started/continuous-integration) — 현재 API·설치·보안 설정을 확인한다.
- [OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/) — 현재 API·설치·보안 설정을 확인한다.

[책 공식 소개](https://www.hanbit.co.kr/books/ai-에이전트-엔지니어링?code=B1562725816) · [저자 예제 코드](https://github.com/michaelalbada/BuildingApplicationsWithAIAgents) · [승인 영상과 선정 근거](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/video-resources.md) · [13장 목차](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-toc.md) · [SA 보완 영역](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-gap-map.md) · [영어·한글 용어 사전](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/glossary-ko-en.md)

읽은 절·자신의 설명·실습 명령·환경/패키지/데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 계획과 실행, fixture와 실제 모델/검색/DB 실행, 목표와 실측을 구분한다. 자료 갱신만으로 학습 또는 구현을 Done 처리하지 않는다.
