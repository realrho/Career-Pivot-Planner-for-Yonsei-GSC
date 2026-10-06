# W3 학습 — 평가 세트(evaluation set)·근거 검증(grounding validation)·부하 시험(load testing)

**주교재:** 『AI 에이전트 엔지니어링』 · **책 범위:** 9장 검증 및 측정

**일정:** 2026-10-16–2026-10-22 (Asia/Seoul) · **총 계획:** 22h

[Notion 주차](https://app.notion.com/p/3ebc6f4a2c7e8116b6d0e972f595de78) · [GitHub #3](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/3)

## 1. 이번 주 목표와 책 읽기

9.1–9.5 전체: 개발 생명주기 평가(evaluation), 평가 세트(evaluation set), 도구·계획·메모리·학습의 컴포넌트(component) 평가, 엔드투엔드 평가, 환각(hallucination)·예기치 않은 입력, 배포(deployment) 준비. 2.9 평가 전략도 다시 읽는다.

**필수 실습:** dev20과 최종 holdout30을 분리한다. 검색 성공·근거 일치·답변 가능 여부·보류·검토·권한(permissions)을 평가 rubric(evaluation rubric)으로 작성하고 원시 결과를 남긴다. 기준선의 품질·지연(latency)·비용을 별도 측정한다.

**재사용 산출물(deliverables):** 평가 rubric, dev20/holdout30 manifest, 평가 실행 포맷, 지연/오류 기준선, 부하 시험(load testing) 시나리오

**완료 기준:** 평가 설정과 원시 결과가 추적되며 품질·응답시간(response time)·오류율(error rate)을 분리해 보고한다. 최종 질문은 설정 선택에서 제외한다.

## 2. 책·영상·실습을 연결한 22h 실행 순서

| 순서 | 활동 | 계획 시간 | 결과/목적 |
|---|---|---|---|
| 1 | 책 읽기·설계 노트 | 6h | 9.1–9.5 전체: 개발 생명주기 평가(evaluation), 평가 세트(evaluation set), 도구·계획·메모리·학습의 컴포넌트(component) 평가, 엔드투엔드 평가, 환각(hallucination)·예기치 않은 입력, 배포(deployment) 준비. 2.9 평가 전략도 다시 읽는다. |
| 2 | 승인 영상 선택 시청 | 2.5h | 묶음 9·5. 아래 보는 시점·범위를 따른다. |
| 3 | 책 개념 프로젝트 실습 | 6h | dev20과 최종 holdout30을 분리한다. 검색 성공·근거 일치·답변 가능 여부·보류·검토·권한(permissions)을 평가 rubric(evaluation rubric)으로 작성하고 원시 결과를 남긴다. 기준선의 품질·지연(latency)·비용을 별도 측정한다. |
| 4 | 영상과 연결한 SA 실습 | 5.5h | 평가 rubric, dev20/holdout30 manifest, 평가 실행 포맷, 지연/오류 기준선, 부하 시험(load testing) 시나리오 |
| 5 | 설명·퀴즈·증거 검토 | 2h | 평가 설정과 원시 결과가 추적되며 품질·응답시간(response time)·오류율(error rate)을 분리해 보고한다. 최종 질문은 설정 선택에서 제외한다. |

영상 배정은 주간 시간 안에 포함된 선택 시청·메모 시간이다. 영상마다 아래 시청 직후 실습을 이어서 수행한다. 순서는 진행 안내이며 주차 체크리스트 네 작업은 읽기6h·개념 실습6h·영상/SA8h·검토2h로 시간을 집계한다.

## 3. 이번 주에 볼 한국어 영상과 연결 실습

### 영상 1. Load testing k6 · 학습 묶음 9

**보는 시점:** 9장 컴포넌트(component)/E2E 평가(evaluation)와 평가 세트(evaluation set) 분리 다음.

- [[인프런] 대규모 트래픽 처리를 위한 부하 테스트 입문/실전 — 공개 영상](https://www.youtube.com/playlist?list=PLtUgHNmvcs6qAqWz-UhH-_ploSbK2eHwG) — JSCODE, 한국어 수업.

**볼 범위:** 공개 목록 1.3 처리량(throughput), 1.4 k6 선택, 1.7 테스트 실습, 2.1·2.2 병목(bottleneck) 분석. 서버 준비는 기존 로컬 API로 대체한다.

**시청 직후 실습:** k6로 기존 /health와 유효 접수 경로를 측정한다. 입력·동시성(concurrency)·시간을 고정하고 P50/P95·오류율(error rate)을 기록한다. AI 분석 지연(latency)으로 오인하지 않는다.

### 영상 2. Kubernetes · 학습 묶음 5

**보는 시점:** 성능 측정에서 실행 환경을 기록하는 이유 다음.

- [[따배쿠] 쿠버네티스 시리즈](https://www.youtube.com/playlist?list=PLApuRlvrZKohaBHvXAOhUD-RxD0uQ3z0c) — TTABAE-LEARN, 한국어 수업.

**볼 범위:** 따배쿠 1편 소개, 3-2 kubectl, 4-1 아키텍처/Pod를 골라 본다. 오래된 설치 절차는 현재 공식 로컬 가이드로 대체한다.

**시청 직후 실습:** kind 또는 minikube 중 하나로 로컬 클러스터를 만들고 kubectl get/describe/logs와 샘플 Pod 상태를 확인한다. W7 Deployment 실습의 선행 준비다.


## 4. 영어·한국어 개념 강의

### 3.1 Evaluation Dataset — 평가 세트(evaluation set)와 누수 방지

evaluation(평가)은 원하는 행동을 대표 사례와 기준으로 확인하는 과정이다. dev set(개발 세트)은 설정 선택에 쓰고 holdout set(보류 평가 세트)은 최종 결과를 확인할 때 사용한다. ID만 달라도 같은 문서나 사실상 같은 질문이면 leakage(평가 누수)가 생길 수 있다. 데이터·정답 근거·평가(evaluation) 설정의 버전을 같이 고정한다.

**업무 예시:** dev20으로 문서 분할을 골랐다면 최종30은 별도로 보관한다. 50개 전체 점수로 개발과 최종 결과를 섞어 보여 주지 않는다.

**직접 할 일:** 질문 ID·문서 출처·의미 중복을 검사한다. 정답 근거와 답변 가능 여부를 함께 기록하고 holdout manifest를 동결한다.

### 3.2 Retrieval·Answer Quality — 검색과 답변 품질

Recall@k(상위 k개 검색의 정답 근거 포함률)는 검색 단계, MRR, Mean Reciprocal Rank(평균 역순위)는 첫 정답 근거의 순위를 평가(evaluation)한다. 인용 ID가 존재하는지는 구조 검사이며 근거가 답을 뒷받침하는지는 의미 검사다. LLM-as-a-judge(모델을 이용한 평가)는 보조 수단이고 사람의 rubric·불일치 검토가 필요하다.

**업무 예시:** 없는 근거 ID, 맞는 ID로 잘못 설명한 답, 근거 없는 질문의 답변 보류(abstention)를 서로 다른 실패로 분류한다.

**직접 할 일:** 검색·형식·근거 의미·보류/검토 항목을 분리한 평가표와 5개 실패 사례를 만든다.

### 3.3 Load Test·Latency — 부하 시험(load testing)과 응답시간(response time)

load test(부하 시험)는 요청량과 동시성(concurrency)이 늘 때 품질·오류·지연(latency)이 어떻게 변하는지 확인한다. throughput(처리량)과 latency(지연시간)는 다른 지표다. P95는 95백분위 응답시간이며 평균만 보면 느린 요청을 놓칠 수 있다. k6는 부하 생성 도구 이름이다. 실제 모델 호출 비용과 외부 서비스 제한도 시험 조건에 포함한다.

**업무 예시:** 동시성을 높여도 성공 요청이 늘지 않고 오류만 증가하면 서버 수 추가만으로 해결되지 않을 수 있다. timeout을 성공한 보류로 세지 않는다.

**직접 할 일:** 영상 9의 처리량(throughput)·지연·병목(bottleneck)·시험 흐름 편을 보고 로컬 API 기준선을 측정한다. 고비용 모델은 낮은 부하·고정 예산으로 별도 측정한다.

### 3.4 Kubernetes Architecture — 클러스터와 선언된 상태

K8s는 Kubernetes의 K와 s 사이 8글자를 숫자로 표시한 이름이다. control plane(제어 영역)은 원하는 상태를 관리하고 node(노드)는 Pod를 실행한다. Pod는 컨테이너(container) 실행의 기본 단위이며 Deployment는 복제 수와 업데이트를 관리한다. YAML은 설정 표현 형식이지 서버에 실제 배포(deployment)된 상태의 증거는 아니다.

**업무 예시:** 'replicas: 2' 파일을 쓴 것과 Ready Pod가 2개 실행된 것은 다르다. 실제 클러스터 상태와 설정을 비교한다.

**직접 할 일:** 따배쿠 1·3-2·4-1을 먼저 본다. 최신 공식 로컬 환경 안내로 kubectl 조회·Pod 상태를 확인하고 W7 배포 전에 구조를 설명한다.

## 5. 확인 퀴즈

### Q1. 모든 50문제로 설정을 고르고 같은 점수를 최종 평가(evaluation)로 보고해도 되는가?

**해설:** 개발/최종 세트를 나누고 최종 세트는 선택에 쓰지 않는다. 중복과 누수도 검사한다.

### Q2. 올바른 인용 ID가 있으면 근거 검증(grounding validation)이 끝나는가?

**해설:** ID 검사와 답의 의미가 근거와 일치하는지 검사는 별도다.

### Q3. 평균 응답시간(response time)만 비교하면 충분한가?

**해설:** P95·오류율(error rate)·성공률·동시성(concurrency)·요청 구성·비용을 함께 봐야 한다.

## 6. 주차 체크리스트·수용 기준(acceptance criteria, AC)

- **W3.1 · 책 9장 읽기·설계/개념 노트 (6h)**
  - 선행: W2.
  - 수용 기준: 9.1–9.5 전체: 개발 생명주기 평가(evaluation), 평가 세트(evaluation set), 도구·계획·메모리·학습의 컴포넌트(component) 평가, 엔드투엔드 평가, 환각(hallucination)·예기치 않은 입력, 배포(deployment) 준비. 2.9 평가 전략도 다시 읽는다. 산출물(deliverables): 핵심 용어의 영어·한글 뜻과 업무 설계 메모.
- **W3.2 · 책 개념을 적용한 프로젝트 실습 (6h)**
  - 선행: W3.1.
  - 수용 기준: dev20과 최종 holdout30을 분리한다. 검색 성공·근거 일치·답변 가능 여부·보류·검토·권한(permissions)을 평가 rubric(evaluation rubric)으로 작성하고 원시 결과를 남긴다. 기준선의 품질·지연(latency)·비용을 별도 측정한다. 산출물: 정상/실패 expected/actual·raw 결과.
- **W3.3 · 영상·SA 보충 실습 — 평가 세트·근거 검증(grounding validation)·부하 시험(load testing) (8h)**
  - 선행: W3.2.
  - 수용 기준: 승인 영상 배정 2.5h + 연결 실습 5.5h. 평가 rubric, dev20/holdout30 manifest, 평가 실행 포맷, 지연/오류 기준선, 부하 시험 시나리오. 평가 설정과 원시 결과가 추적되며 품질·응답시간(response time)·오류율(error rate)을 분리해 보고한다. 최종 질문은 설정 선택에서 제외한다.
- **W3.4 · 퀴즈·본인 설명·증거·다음 주 준비 검토 (2h)**
  - 선행: W3.3.
  - 수용 기준: 퀴즈 3개를 자신의 말로 설명하고 정상/실패 증거와 다음 주 선행 조건을 검토한다.

## 7. 공식 문서와 증거

- [Kubernetes 로컬 기초](https://kubernetes.io/docs/tutorials/kubernetes-basics/) — 현재 API·설치·보안(security) 설정을 확인한다.
- [k6](https://grafana.com/docs/k6/latest/) — 현재 API·설치·보안 설정을 확인한다.

[책 공식 소개](https://www.hanbit.co.kr/books/ai-에이전트-엔지니어링?code=B1562725816) · [저자 예제 코드](https://github.com/michaelalbada/BuildingApplicationsWithAIAgents) · [승인 영상과 선정 근거](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/video-resources.md) · [13장 목차](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-toc.md) · [SA 보완 영역](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-gap-map.md) · [영어·한글 용어 사전](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/glossary-ko-en.md)

읽은 절·자신의 설명·실습 명령·환경/패키지/데이터/모델/프롬프트(prompt)/인덱스(index) 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 계획과 실행, fixture와 실제 모델/검색/DB 실행, 목표와 실측을 구분한다. 자료 갱신만으로 학습 또는 구현을 Done 처리하지 않는다.
