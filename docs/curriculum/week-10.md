# W10 제작 — MVP 검증 — 최종 평가·복구·포트폴리오 시연

**주교재:** 『AI 에이전트 엔지니어링』 · **책 범위:** W1–W8 자산 재사용

**일정:** 2026-12-04–2026-12-10 (Asia/Seoul) · **총 계획:** 22h

[Notion 주차](https://app.notion.com/p/3ecc6f4a2c7e819b9b43f0b0f71f1323) · [GitHub #10](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/10)

## 1. 이번 주 목표와 책 읽기

『AI 에이전트 엔지니어링』9·10·11·13장의 평가·관측·개선·고객 설명을 적용한다.

**필수 실습:** 개발20+동결 holdout30질문을구분해실제 모델평가를수행한다. 깨끗한환경기동·재시작·백업 복원을검증하고코드/보고서/시연을연결한다.

**재사용 산출물:** 평가raw결과·benchmark표·복구기록·README/아키텍처·5분데모

**완료 기준:** 재현 명령·버전·예산·측정 조건과 실패 사례가 합성 자료의 실행 증거로 추적된다. 안전 gate 통과 여부와 품질 목표 달성을 분리해 보고한다.

## 2. 책·영상·실습을 연결한 22h 실행 순서

| 순서 | 활동 | 계획 시간 | 결과/목적 |
|---|---|---|---|
| 1 | 50질문 평가·실패 분석·지연/비용 측정 | 5h | dev20/holdout30을 분리 보고하고 raw결과·측정조건·실제 공급자가격·재시도를 기록한다. |
| 2 | Compose·로컬 Kubernetes 기동·롤백·DB 복원·CI 검증 | 6h | 새 환경 기동, DB복원 후 사례/감사 조회, 권한/필터/전이 회귀를 통과하고 복구시간을 기록한다. W7에서 준비한 로컬 Kubernetes API 배포/롤백 증거를 재확인한다. 운영 HA 구축은 추가 과정이다. |
| 3 | README·ADR·아키텍처·평가 보고서 정리 | 6h | 필수/선택범위와 구현/미구현·목표/실측을 구분. commit/run_id로 모든 핵심주장을 연결한다. |
| 4 | 5분 데모·영어 설명·최종 수용 기준 확인 | 5h | 정상근거/보류/검토3경로를 시연하고 SA90초영어설명·한계/대안·재현명령을 검토한다. |

영상 배정은 주간 시간 안에 포함된 선택 시청·메모 시간이다. 제작 주차는 아래 주차 체크리스트 네 작업의 5h·6h·6h·5h로 시간을 집계한다. 새 강의를 추가하지 않고 앞 주차 실습 자산을 연결한다.

## 3. 이번 주에 볼 한국어 영상과 연결 실습

새 강의는 추가하지 않는다. W1–W8의 선택 영상·완료한 실습 기록을 필요한 문제에만 다시 참조한다.

## 4. 통합·검증 진행 방식

dev20과 동결 holdout30을 각각 보고한다. 지연·비용·오류율을 실행 환경과 함께 기록한다. Compose 새 기동, W7 로컬 Kubernetes 배포/롤백, DB 백업 복원, CI 실패 차단을 확인하고 5분 시연을 준비한다.

## 5. 주차 체크리스트·수용 기준

- **W10.1 · 50질문 평가·실패 분석·지연/비용 측정 (5h)**
  - 선행: W9.
  - 수용 기준: dev20/holdout30을 분리 보고하고 raw결과·측정조건·실제 공급자가격·재시도를 기록한다.
- **W10.2 · Compose·로컬 Kubernetes 기동·롤백·DB 복원·CI 검증 (6h)**
  - 선행: W10.1.
  - 수용 기준: 새 환경 기동, DB복원 후 사례/감사 조회, 권한/필터/전이 회귀를 통과하고 복구시간을 기록한다. W7에서 준비한 로컬 Kubernetes API 배포/롤백 증거를 재확인한다. 운영 HA 구축은 추가 과정이다.
- **W10.3 · README·ADR·아키텍처·평가 보고서 정리 (6h)**
  - 선행: W10.2.
  - 수용 기준: 필수/선택범위와 구현/미구현·목표/실측을 구분. commit/run_id로 모든 핵심주장을 연결한다.
- **W10.4 · 5분 데모·영어 설명·최종 수용 기준 확인 (5h)**
  - 선행: W10.3.
  - 수용 기준: 정상근거/보류/검토3경로를 시연하고 SA90초영어설명·한계/대안·재현명령을 검토한다.

## 6. 공식 문서와 증거



[책 공식 소개](https://www.hanbit.co.kr/books/ai-에이전트-엔지니어링?code=B1562725816) · [저자 예제 코드](https://github.com/michaelalbada/BuildingApplicationsWithAIAgents) · [승인 영상과 선정 근거](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/video-resources.md) · [13장 목차](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-toc.md) · [SA 보완 영역](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-gap-map.md) · [영어·한글 용어 사전](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/glossary-ko-en.md)

읽은 절·자신의 설명·실습 명령·환경/패키지/데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 계획과 실행, fixture와 실제 모델/검색/DB 실행, 목표와 실측을 구분한다. 자료 갱신만으로 학습 또는 구현을 Done 처리하지 않는다.
