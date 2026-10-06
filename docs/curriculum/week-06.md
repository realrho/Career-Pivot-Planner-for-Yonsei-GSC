# W6 학습 — 학습·개선 루프·실험·비용·인프라 코드

**주교재:** 『AI 에이전트 엔지니어링』 · **책 범위:** 7장 에이전틱 시스템의 학습 / 11장 개선 루프

**일정:** 2026-11-06–2026-11-12 (Asia/Seoul) · **총 계획:** 22h

[Notion 주차](https://app.notion.com/p/3ebc6f4a2c7e8156b65ddfe5240f458e) · [SCRUM-11](https://realrho-1790798942092.atlassian.net/browse/SCRUM-11) · [GitHub #6](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/6)

## 1. 이번 주 목표와 책 읽기

7.1–7.3 전체: 비모수적 예시·Reflexion·경험 학습, 파인튜닝·소형 모델·SFT·DPO·RLVR. 11.1–11.4 전체: 피드백 파이프라인·사람 리뷰·프롬프트/도구 개선·실험·지속 학습. 2.3·2.7의 모델 선택과 비용도 복습한다.

**필수 실습:** dev 세트에서 프롬프트/검색/도구 중 변수 하나를 바꾸고 기준선과 비교한다. 개선 후보는 버전·품질·지연·실패·비용을 기록한다. 가상의 비용 모델과 실제 사용량을 분리한다. Terraform은 로컬 파일 리소스로 plan/state 차이를 확인한다.

**재사용 산출물:** 실험 기록, 피드백 우선순위, 모델/운영 비용표, Terraform 계획·상태 기록, 개선 승인 조건

**완료 기준:** 최종 holdout을 튜닝에 사용하지 않으며 개선 이득과 추가 비용을 함께 설명한다. 파인튜닝 읽기와 실제 학습 실행을 구분한다.

## 2. 책·영상·실습을 연결한 22h 실행 순서

| 순서 | 활동 | 계획 시간 | 결과/목적 |
|---|---|---|---|
| 1 | 책 읽기·설계 노트 | 6h | 7.1–7.3 전체: 비모수적 예시·Reflexion·경험 학습, 파인튜닝·소형 모델·SFT·DPO·RLVR. 11.1–11.4 전체: 피드백 파이프라인·사람 리뷰·프롬프트/도구 개선·실험·지속 학습. 2.3·2.7의 모델 선택과 비용도 복습한다. |
| 2 | 승인 영상 선택 시청 | 1h | 묶음 8·10. 아래 보는 시점·범위를 따른다. |
| 3 | 책 개념 프로젝트 실습 | 6h | dev 세트에서 프롬프트/검색/도구 중 변수 하나를 바꾸고 기준선과 비교한다. 개선 후보는 버전·품질·지연·실패·비용을 기록한다. 가상의 비용 모델과 실제 사용량을 분리한다. Terraform은 로컬 파일 리소스로 plan/state 차이를 확인한다. |
| 4 | 영상과 연결한 SA 실습 | 7h | 실험 기록, 피드백 우선순위, 모델/운영 비용표, Terraform 계획·상태 기록, 개선 승인 조건 |
| 5 | 설명·퀴즈·증거 검토 | 2h | 최종 holdout을 튜닝에 사용하지 않으며 개선 이득과 추가 비용을 함께 설명한다. 파인튜닝 읽기와 실제 학습 실행을 구분한다. |

영상 배정은 주간 시간 안에 포함된 선택 시청·메모 시간이다. 영상마다 아래 시청 직후 실습을 이어서 수행한다. 순서는 진행 안내이며 Jira 네 작업은 읽기6h·개념 실습6h·영상/SA8h·검토2h로 시간을 집계한다.

## 3. 이번 주에 볼 한국어 영상과 연결 실습

### 영상 1. IaC Terraform · 학습 묶음 8

**보는 시점:** 11장 개선·변경 관리와 비용 계획 다음.

- [Terraform/IaC introductory guide](https://www.youtube.com/watch?v=3qSpwqckvXQ) — 데브아트 DevArt, 한국어 수업.

**볼 범위:** Terraform·IaC 소개 약 15분 후 공식 CLI 문서의 init/validate/plan/state를 읽는다.

**시청 직후 실습:** 로컬 파일 리소스로 상태/변경 계획을 확인한다. 클라우드 적용은 필수가 아니며 state와 비밀을 저장소에 커밋하지 않는다.

### 영상 2. SA design review and cost · 학습 묶음 10

**보는 시점:** 2.7 비용 트레이드오프 재독·11장 실험 다음.

- [비용 최적화를 통해 AWS 비용 알뜰하게 관리하기](https://www.youtube.com/watch?v=IqD_8q0TaC0) — Amazon Web Services Korea, 한국어 수업.

**볼 범위:** AWS 비용 최적화 소개 약 25분. 영상의 과거 가격은 현재 단가로 쓰지 않는다.

**시청 직후 실습:** 월 요청수·토큰·검색/DB·저장·운영 인건비·검토 비율을 변수로 TCO 및 성공 요청당 비용을 산정한다.


## 4. 영어·한국어 개념 강의

### 6.1 SFT·DPO·RLVR — 학습 선택의 목적

SFT, Supervised Fine-Tuning(지도 파인튜닝)은 예시 입력과 원하는 출력으로 모델을 조정한다. DPO, Direct Preference Optimization(직접 선호 최적화)은 선호된/비선호된 응답 쌍을 사용한다. RLVR, Reinforcement Learning with Verifiable Rewards(검증 가능한 보상을 이용한 강화학습)는 검사 가능한 결과에 보상을 준다. in-context learning(문맥 내 학습)은 호출에 예시를 넣는 방식이며 모델 가중치를 바꾸지 않는다.

**업무 예시:** 현재 정책 버전이 자주 바뀌는 지식 문제는 검색 개선이 먼저일 수 있다. 출력 스타일 문제와 정보 부족을 같은 파인튜닝 과제로 묶지 않는다.

**직접 할 일:** 문제 유형·데이터·평가·예산·운영 부담으로 네 접근을 비교한다. 고비용 학습은 선택이며 실행하지 않은 결과는 미실행으로 기록한다.

### 6.2 Feedback·Experiment — 피드백과 통제된 실험

feedback pipeline(피드백 파이프라인)은 실패·사용자 수정·검토 결과를 개선 후보로 연결한다. A/B test(A/B 시험)는 다른 조건을 비교하지만 요청 구성·사용자 차이·표본 크기를 고려해야 한다. shadow mode(그림자 실행)는 실제 결정에 영향을 주지 않도록 새 경로를 비교한다. 한 번에 여러 변수를 바꾸면 개선 원인을 설명하기 어렵다.

**업무 예시:** 답변 오류를 모두 프롬프트 탓으로 돌리지 않고 검색 누락·버전·권한·도구 실패·모델 해석으로 분류한다.

**직접 할 일:** 기준선과 한 변수만 바꾼 실험을 dev20에서 실행한다. 개선·회귀·비용을 적고 적용/보류 이유를 남긴다.

### 6.3 TCO·Unit Cost — 총비용과 업무 효과

TCO, Total Cost of Ownership(총소유비용)는 모델 호출뿐 아니라 컴퓨팅·저장소·네트워크·관측·운영 인력·사람 검토 비용을 포함한다. unit cost(단위 비용)는 성공 요청 또는 완료 업무당 비용처럼 분모를 명확히 정한다. ROI, Return on Investment(투자수익률)는 비용과 편익을 가정·기간과 함께 비교한다. 이론 요금 계산과 실제 청구/측정은 구분한다.

**업무 예시:** 싼 모델이 검토 요청을 많이 만들어 전체 운영비가 커질 수 있다. timeout·재시도·실패 호출의 비용도 포함한다.

**직접 할 일:** 영상 10의 비용 세션을 보고 요청량·토큰·재시도·검토율을 바꾼 3개 시나리오를 계산한다. 요금은 사용 시점의 공식 가격을 확인한다.

### 6.4 IaC·Terraform State — 인프라 코드와 상태

IaC, Infrastructure as Code(코드로 관리하는 인프라)는 설정과 변경을 재현·검토할 수 있게 표현한다. Terraform은 이 작업을 수행하는 제품 이름이다. configuration(설정), plan(변경 계획), state(관리 상태)는 서로 다른 자료다. state에 비밀 값이 남을 수 있으므로 저장 위치·접근 권한·잠금·백업을 설계한다. plan만 만들었다고 인프라가 배포된 것은 아니다.

**업무 예시:** 로컬 파일 리소스로 init→plan→apply 후 다시 plan을 실행해 변경이 없음을 확인할 수 있다. 실제 AWS 생성은 비용·권한 조건이 있는 별도 선택 실습이다.

**직접 할 일:** 영상 8과 공식 문서로 로컬 예제를 실행한다. 변경 전후 계획·상태·재현 결과를 저장하되 민감 값은 기록에서 제외한다.

## 5. 확인 퀴즈

### Q1. RAG와 파인튜닝은 같은 문제를 해결하는가?

**해설:** 변하는 지식 검색과 모델 행동 조정은 목적이 다르다. 문제·평가·데이터로 선택한다.

### Q2. 호출당 요금만으로 가장 경제적인 모델을 선택할 수 있는가?

**해설:** 성공률·재시도·검토율·인프라·운영 인력을 포함한 업무당 총비용을 비교한다.

### Q3. Terraform plan 결과는 배포 증거인가?

**해설:** 예정 변경의 설명이다. apply 후 실제 상태와 결과를 별도로 확인한다.

## 6. Jira 작업·수용 기준

- **SCRUM-34 · 책 7·11장 읽기·설계/개념 노트 (6h)**
  - 선행: SCRUM-10.
  - 수용 기준: 7.1–7.3 전체: 비모수적 예시·Reflexion·경험 학습, 파인튜닝·소형 모델·SFT·DPO·RLVR. 11.1–11.4 전체: 피드백 파이프라인·사람 리뷰·프롬프트/도구 개선·실험·지속 학습. 2.3·2.7의 모델 선택과 비용도 복습한다. 산출물: 핵심 용어의 영어·한글 뜻과 업무 설계 메모.
- **SCRUM-35 · 책 개념을 적용한 프로젝트 실습 (6h)**
  - 선행: SCRUM-34.
  - 수용 기준: dev 세트에서 프롬프트/검색/도구 중 변수 하나를 바꾸고 기준선과 비교한다. 개선 후보는 버전·품질·지연·실패·비용을 기록한다. 가상의 비용 모델과 실제 사용량을 분리한다. Terraform은 로컬 파일 리소스로 plan/state 차이를 확인한다. 산출물: 정상/실패 expected/actual·raw 결과.
- **SCRUM-36 · 영상·SA 보충 실습 — 학습·개선 루프·실험·비용·인프라 코드 (8h)**
  - 선행: SCRUM-35.
  - 수용 기준: 승인 영상 배정 1h + 연결 실습 7h. 실험 기록, 피드백 우선순위, 모델/운영 비용표, Terraform 계획·상태 기록, 개선 승인 조건. 최종 holdout을 튜닝에 사용하지 않으며 개선 이득과 추가 비용을 함께 설명한다. 파인튜닝 읽기와 실제 학습 실행을 구분한다.
- **SCRUM-37 · 퀴즈·본인 설명·증거·다음 주 준비 검토 (2h)**
  - 선행: SCRUM-36.
  - 수용 기준: 퀴즈 3개를 자신의 말로 설명하고 정상/실패 증거와 다음 주 선행 조건을 검토한다.

## 7. 공식 문서와 증거

- [Terraform 실행](https://developer.hashicorp.com/terraform/cli/run) — 현재 API·설치·보안 설정을 확인한다.
- [Terraform local provider](https://registry.terraform.io/providers/hashicorp/local/latest/docs/resources/file) — 현재 API·설치·보안 설정을 확인한다.
- [AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) — 현재 API·설치·보안 설정을 확인한다.

[책 공식 소개](https://www.hanbit.co.kr/books/ai-에이전트-엔지니어링?code=B1562725816) · [저자 예제 코드](https://github.com/michaelalbada/BuildingApplicationsWithAIAgents) · [승인 영상과 선정 근거](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/video-resources.md) · [13장 목차](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-toc.md) · [SA 보완 영역](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-gap-map.md) · [영어·한글 용어 사전](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/glossary-ko-en.md)

읽은 절·자신의 설명·실습 명령·환경/패키지/데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 계획과 실행, fixture와 실제 모델/검색/DB 실행, 목표와 실측을 구분한다. 자료 갱신만으로 학습 또는 구현을 Done 처리하지 않는다.
