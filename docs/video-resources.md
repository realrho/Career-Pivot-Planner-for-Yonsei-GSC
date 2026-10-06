# 승인한 한국어 영상 · 10개 학습 묶음

사용자 승인: 2026-10-06. W1 API는 사용자가 지정한 공개 재생목록 6개를 모두 학습한다. 나머지 영상은 각 주차의 책 개념 뒤에 배정된 부분을 시청하고 해당 실습을 바로 한다. 모든 주차의 실제 URL·선택 편·보는 시점·산출물은 주차 교재에도 들어 있다. 계획 배정 총 12.5h는 시청/메모를 포함하며 영상 재생시간과 다르다.

평점이 있는 유료 전체 강좌의 리뷰를 개별 유튜브 영상 평점으로 표시하지 않았다. 공개 자료의 강사·소속·공개 실습 자료·내용 적합성을 바탕으로 선정했다. 개인 채널 영상은 공식 제품 문서와 함께 검증한다. 영상의 오래된 API·설치·가격은 현재 기준으로 확인한다.

## 1. API 전체 수업·입력 검증

**배치 주차:** W1 · **언어:** 한국어

- [FastAPI 첫걸음 — API 전체 재생목록(공개 기본편 6개)](https://youtube.com/playlist?list=PL8kmk2VivDmQyPLmc4zF6yLEl-Rc6D9lg&si=iKuEUs7JNHJV-N7R) — hatemogi.

**선정 근거·검증 한계:** 사용자가 지정한 재생목록으로 교체했다. 2026-10-06 공개 목록에서 기본편 6개와 무료 공개 안내를 확인했다. 약 65분이며 유료 심화 강좌는 포함하지 않는다. 오래된 예제는 현재 FastAPI·Pydantic 공식 문서와 비교한다.

**W1 학습 범위:** ‘FastAPI 첫걸음’ 재생목록의 공개 기본편 6개를 목록 순서대로 모두 학습한다(약 65분). API 소개 → uv 환경 준비 → API 서버 만들기 → 경로 데코레이터·경로 함수 → Pydantic 입력 검증 → CRUD. 재생목록에 있는 환경 준비도 함께 따라 하되 별도의 Python·HTTP·SQL 기초 과정은 추가하지 않는다.

**W1 연결 실습:** 각 영상의 예제를 직접 실행한 뒤 정책 질문 API로 바꿔 본다. 요청·응답 계약과 생성·조회·수정·삭제 경로를 정리하고, 정상 입력 1개와 공백·잘못된 타입·길이 초과·허용하지 않은 필드의 실패 4개를 검증한다. REST, Representational State Transfer(자원 표현을 통한 상태 전달), CRUD, Create·Read·Update·Delete(생성·조회·수정·삭제), JSON, JavaScript Object Notation(데이터 교환 형식)의 뜻을 자신의 말로 설명한다.

**완료 기록:** 공개 영상 6개 모두 시청·예제 실행을 체크한다. API 전체 수업과 Docker 입문 시청·메모는 W1의 2h, 코드 따라 하기와 계약·검증 실습은 SA 보충 6h에 포함한다.

## 2. 트랜잭션·ACID

**배치 주차:** W5 · **언어:** 한국어

- [BJ.42 데이터베이스 트랜잭션과 ACID](https://www.youtube.com/watch?v=sLJ8ypeHGlM) — 쉬운코드, 약 25분.

**선정 근거·검증 한계:** 개념 설명이 중심이라 SQL 기초를 다시 학습하지 않고 원자성·동시성 실습에 연결할 수 있다.

**W5 선택 범위:** 트랜잭션·ACID 개념(약 25분). SQL 문법과 Java/Spring 문법 학습은 제외한다.

**W5 연결 실습:** 승인 상태 변경과 감사 기록을 같은 트랜잭션으로 묶고 감사 실패를 주입한다. 모두 롤백되는지, 중복/동시 승인에 충돌 처리가 있는지 확인한다.

## 3. 비동기 처리·취소·타임아웃

**배치 주차:** W4 · **언어:** 한국어

- [Real-world asyncio - 김준기 - PyCon.KR 2019](https://www.youtube.com/watch?v=QaiczQzJAmA) — PyCon Korea. [발표 슬라이드](https://speakerdeck.com/achimnol/pycon-kr-2019-real-world-asyncio).

**선정 근거·검증 한계:** PyCon Korea 발표이며 발표자 공개 슬라이드에 실서비스 경험이 설명되어 있다. 2019 발표이므로 예제 API를 현재 문서와 비교한다.

**W4 선택 범위:** 발표 슬라이드와 함께 이벤트 루프·blocking 호출·취소·타임아웃 관련 부분을 본다. 2019 코드/API는 현재 공식 문서와 비교한다.

**W4 연결 실습:** 느린 도구·예외·취소를 주입해 종료 한도, 자원 정리, 중복 실행 여부를 검증한다.

## 4. Docker·Dockerfile·Compose

**배치 주차:** W1, W7 · **언어:** 한국어

- [생활코딩 Docker 입구 수업](https://www.youtube.com/playlist?list=PLuHgQVnccGMDeMJsGq2O-55Ymtx0IdKWf) — 생활코딩, 약 42분.
- [도커: 이미지 만드는 법 - Dockerfile & build](https://www.youtube.com/watch?v=0kQC19w0gTI) — 생활코딩, 약 18분.
- [Docker Compose](https://www.youtube.com/watch?v=EK6iYRCIjYs) — 생활코딩, 약 16분.

**선정 근거·검증 한계:** 생활코딩의 공개 강좌와 교안. 입구 강좌에 Lablup 리뷰 참여가 표기되어 있고 짧은 단위로 실행할 수 있다.

**W1 선택 범위:** Docker 입구 수업 8편(약 42분): 이미지/컨테이너·명령·네트워크·마운트.

**W1 연결 실습:** 같은 이미지로 컨테이너를 재생성하고 포트·볼륨을 확인한다. 이미지 제작과 Compose는 W7에서 이어간다.

**W7 선택 범위:** W1에 이어 Dockerfile/build 약 18분 + Compose 약 16분. 같은 입문 목록 전체를 반복하지 않는다.

**W7 연결 실습:** API 이미지, DB 볼륨, healthcheck, 설정/비밀 분리를 구현하고 Compose 재기동 및 DB 복원을 확인한다.

## 5. Kubernetes 로컬 배포

**배치 주차:** W3, W7 · **언어:** 한국어

- [[따배쿠] 쿠버네티스 시리즈](https://www.youtube.com/playlist?list=PLApuRlvrZKohaBHvXAOhUD-RxD0uQ3z0c) — TTABAE-LEARN. [공개 실습 자료](https://github.com/237summit/Getting-Start-Kubernetes).

**선정 근거·검증 한계:** 공개 시리즈와 실습 GitHub 저장소가 있어 아키텍처와 실제 kubectl/배포를 연결할 수 있다. 예전 클러스터 설치/Ingress 절차는 현재 공식 문서로 대체한다.

**W3 선택 범위:** 따배쿠 1편 소개, 3-2 kubectl, 4-1 아키텍처/Pod를 골라 본다. 오래된 설치 절차는 현재 공식 로컬 가이드로 대체한다.

**W3 연결 실습:** kind 또는 minikube 중 하나로 로컬 클러스터를 만들고 kubectl get/describe/logs와 샘플 Pod 상태를 확인한다. W7 Deployment 실습의 선행 준비다.

**W7 선택 범위:** 5-2 probes, 5-6 자원, 6-3 Deployment, 7-1 Service, 10 ConfigMap, 11 Secret을 선택한다. 실행에 필요한 예제부터 보고 남는 심화는 추가 시간에 본다.

**W7 연결 실습:** W3 로컬 클러스터에 API를 Deployment/Service로 배포한다. readiness/liveness·requests/limits·ConfigMap/Secret·로그·롤백을 실제 확인한다. Secret의 base64는 암호화가 아니다.

## 6. AWS 네트워크·권한

**배치 주차:** W5 · **언어:** 한국어

- [(리뉴얼) 쉽게 설명하는 AWS 기초강의 29. VPC와 서브넷](https://www.youtube.com/watch?v=azd_k4bOXqw) — AWS 강의실, 약 23분.
- [(리뉴얼) 쉽게 설명하는 AWS 기초강의 9. IAM 기초](https://www.youtube.com/watch?v=HKIg04dDS8A) — AWS 강의실, 약 11분.

**선정 근거·검증 한계:** 같은 강사의 Inflearn 전체 강좌는 조회 시점 평점 4.9/후기 170개였다. 이는 연결된 전체 강좌 평가이며 두 유튜브 영상의 개별 평점이 아니다. 채널은 독립 강사 운영이다.

[전체 강좌 후기 출처](https://www.inflearn.com/course/%EC%89%BD%EA%B2%8C-%EC%84%A4%EB%AA%85%ED%95%98%EB%8A%94-aws-%EA%B8%B0%EC%B4%88?cid=333984)

**W5 선택 범위:** VPC·서브넷 약 23분 + IAM 기초 약 11분. 독립 강사 채널이며 AWS 공식 채널과 구분한다.

**W5 연결 실습:** 공개 API/비공개 DB 네트워크와 신원→role→tenant 권한표를 그린다. IAM 정책·비밀 관리·저장소/컴퓨팅 선택 이유를 적는다.

## 7. CI/CD·GitHub Actions

**배치 주차:** W7 · **언어:** 한국어

- [[10분 테코톡] 도비의 CI/CD와 Github Action](https://www.youtube.com/watch?v=SKILL1pT6f4) — 우아한테크.

**선정 근거·검증 한계:** 우아한테크의 공개 학습자 발표로 개념을 빠르게 익히고 공식 Actions 문서로 실제 workflow를 작성한다.

**W7 선택 범위:** CI/CD와 GitHub Actions 개념을 보고 공식 문서로 프로젝트용 최소 workflow를 만든다.

**W7 연결 실습:** 검증→테스트→이미지 빌드 단계와 실패 차단을 확인한다. 자동 운영 배포 권한은 설계에서 검토한다.

## 8. IaC·Terraform

**배치 주차:** W6 · **언어:** 한국어

- [Terraform·IaC 기초 소개](https://www.youtube.com/watch?v=3qSpwqckvXQ) — 데브아트 DevArt, 약 15분.

**선정 근거·검증 한계:** 현업 DevOps 관점의 공개 입문 영상이다. 전체 실습 강좌로 보지 않고 init/plan/state는 공식 문서로 보충한다.

**W6 선택 범위:** Terraform·IaC 소개 약 15분 후 공식 CLI 문서의 init/validate/plan/state를 읽는다.

**W6 연결 실습:** 로컬 파일 리소스로 상태/변경 계획을 확인한다. 클라우드 적용은 필수가 아니며 state와 비밀을 저장소에 커밋하지 않는다.

## 9. 부하 시험·k6

**배치 주차:** W3 · **언어:** 한국어

- [[인프런] 대규모 트래픽 처리를 위한 부하 테스트 입문/실전 — 공개 영상](https://www.youtube.com/playlist?list=PLtUgHNmvcs6qAqWz-UhH-_ploSbK2eHwG) — JSCODE.

**선정 근거·검증 한계:** 2026년 공개 영상 목록과 선택 가능한 부하/병목 강의가 있다. 연결된 전체 강좌는 별도 유료이며 필수 과제는 공개 부분과 로컬 API로 수행한다.

**W3 선택 범위:** 공개 목록 1.3 처리량, 1.4 k6 선택, 1.7 테스트 실습, 2.1·2.2 병목 분석. 서버 준비는 기존 로컬 API로 대체한다.

**W3 연결 실습:** k6로 기존 /health와 유효 접수 경로를 측정한다. 입력·동시성·시간을 고정하고 P50/P95·오류율을 기록한다. AI 분석 지연으로 오인하지 않는다.

## 10. SA 설계 리뷰·비용

**배치 주차:** W6, W8 · **언어:** 한국어

- [당신의 아키텍처는 Well-Architected 한가요?](https://www.youtube.com/watch?v=VpSNzSI0pk8) — Amazon Web Services Korea, 약 26분.
- [비용 최적화를 통해 AWS 비용 알뜰하게 관리하기](https://www.youtube.com/watch?v=IqD_8q0TaC0) — Amazon Web Services Korea, 약 25분.

**선정 근거·검증 한계:** Amazon Web Services Korea 공식 세션으로 고객 설계 검토와 비용 최적화 관점을 배운다. 현재 가격을 제공하는 자료로 사용하지 않는다.

**W6 선택 범위:** AWS 비용 최적화 소개 약 25분. 영상의 과거 가격은 현재 단가로 쓰지 않는다.

**W6 연결 실습:** 월 요청수·토큰·검색/DB·저장·운영 인건비·검토 비율을 변수로 TCO 및 성공 요청당 비용을 산정한다.

**W8 선택 범위:** Well-Architected 소개 약 26분. W6 비용표와 W7 운영 결과를 가져와 설계 리뷰를 한다.

**W8 연결 실습:** 6개 관점(운영 우수성·보안·신뢰성·성능 효율·비용 최적화·지속 가능성)으로 ADR과 고객 제안서를 리뷰한다. 미검증 항목과 선택 이유를 표시한다.

## 현재 기준 확인용 공식 문서

- [API·입력 검증](https://fastapi.tiangolo.com/tutorial/body/)
- [Pydantic v2](https://docs.pydantic.dev/latest/concepts/models/)
- [비동기](https://fastapi.tiangolo.com/ko/async/)
- [트랜잭션](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [Docker Compose](https://docs.docker.com/compose/)
- [Kubernetes 로컬 기초](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- [Kubernetes probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/)
- [GitHub Actions CI](https://docs.github.com/en/actions/get-started/continuous-integration)
- [Terraform 실행](https://developer.hashicorp.com/terraform/cli/run)
- [Terraform local provider](https://registry.terraform.io/providers/hashicorp/local/latest/docs/resources/file)
- [k6](https://grafana.com/docs/k6/latest/)
- [AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [MAESTRO](https://labs.cloudsecurityalliance.org/maestro/)
- [OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/)
