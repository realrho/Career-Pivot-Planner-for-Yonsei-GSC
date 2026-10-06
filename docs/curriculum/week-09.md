# W9 제작 — MVP 통합 — 근거 응답(grounded response)·영속 상태(persistent state)·권한(permissions) 있는 검토

**주교재:** 『AI 에이전트 엔지니어링』 · **책 범위:** W1–W8 자산 재사용

**일정:** 2026-11-27–2026-12-03 (Asia/Seoul) · **총 계획:** 22h

[Notion 주차](https://app.notion.com/p/3ecc6f4a2c7e812189a5fad40b9b3f33) · [GitHub #9](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/9)

## 1. 이번 주 목표와 책 읽기

『AI 에이전트 엔지니어링』2·4·5·6·8·12·13장의 설계·도구·지식·상태·보안(security)·협업을 W1–W8 자산으로 적용한다.

**필수 실습:** W8준비gate를먼저확인하고입력→권한(permissions)→검색→생성→검증→분기→저장→조회/검토의통합경로를완성한다.

**재사용 산출물(deliverables):** 통합API·지속DB·근거/보류/검토3경로와 회귀검증(regression testing)

**완료 기준:** 정상 근거 응답(grounded response)·근거 없는 보류·고위험 검토가 실제 검색/모델/DB 경로에서 동작하고 재시작 후 조회된다. viewer와 다른 tenant의 검토를 거부한다.

## 2. 책·영상·실습을 연결한 22h 실행 순서

| 순서 | 활동 | 계획 시간 | 결과/목적 |
|---|---|---|---|
| 1 | 범위·계약·환경 동결과 통합 입력 준비 | 5h | W8 준비 gate 증거 확인. 모델/벡터backend/코퍼스/권한(permissions)/상태/API계약을 동결하고 새 환경 기동한다. |
| 2 | tenant·버전 검색과 실제 모델 근거 응답(grounded response) 통합 | 6h | 인용ID·의미평가·근거 없는 보류·교차tenant거부를 실제 경로로 검증한다. |
| 3 | 영속 상태(persistent state)·검토 권한·감사(audit) 원자성(atomicity) 통합 | 6h | case/review/audit를 PostgreSQL로 저장. 동시/중복검토·권한거부·재시작조회·rollback을 검증한다. |
| 4 | 정상·보류·검토 통합 회귀와 장애 처리 | 5h | 세 종단경로의 expected/actual 결과, 모델 timeout·형식 오류·DB실패 처리와 실행 증거를 남긴다. |

영상 배정은 주간 시간 안에 포함된 선택 시청·메모 시간이다. 제작 주차는 아래 주차 체크리스트 네 작업의 5h·6h·6h·5h로 시간을 집계한다. 새 강의를 추가하지 않고 앞 주차 실습 자산을 연결한다.

## 3. 이번 주에 볼 한국어 영상과 연결 실습

새 강의는 추가하지 않는다. W1–W8의 선택 영상·완료한 실습 기록을 필요한 문제에만 다시 참조한다.

## 4. 통합·검증 진행 방식

W8 준비 자산을 확인한 뒤 입력→검증된 신원→활성 정책 검색→모델→형식/근거 검증(grounding validation)→응답/보류/검토→원자적 저장→조회 경로를 연결한다. timeout·잘못된 인용·권한(permissions) 위반·동시 검토를 주입한다.

## 5. 주차 체크리스트·수용 기준(acceptance criteria, AC)

- **W9.1 · 범위·계약·환경 동결과 통합 입력 준비 (5h)**
  - 선행: W8.
  - 수용 기준: W8 준비 gate 증거 확인. 모델/벡터backend/코퍼스/권한(permissions)/상태/API계약을 동결하고 새 환경 기동한다.
- **W9.2 · tenant·버전 검색과 실제 모델 근거 응답(grounded response) 통합 (6h)**
  - 선행: W9.1.
  - 수용 기준: 인용ID·의미평가·근거 없는 보류·교차tenant거부를 실제 경로로 검증한다.
- **W9.3 · 영속 상태(persistent state)·검토 권한·감사(audit) 원자성(atomicity) 통합 (6h)**
  - 선행: W9.2.
  - 수용 기준: case/review/audit를 PostgreSQL로 저장. 동시/중복검토·권한거부·재시작조회·rollback을 검증한다.
- **W9.4 · 정상·보류·검토 통합 회귀와 장애 처리 (5h)**
  - 선행: W9.3.
  - 수용 기준: 세 종단경로의 expected/actual 결과, 모델 timeout·형식 오류·DB실패 처리와 실행 증거를 남긴다.

## 6. 공식 문서와 증거



[책 공식 소개](https://www.hanbit.co.kr/books/ai-에이전트-엔지니어링?code=B1562725816) · [저자 예제 코드](https://github.com/michaelalbada/BuildingApplicationsWithAIAgents) · [승인 영상과 선정 근거](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/video-resources.md) · [13장 목차](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-toc.md) · [SA 보완 영역](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-gap-map.md) · [영어·한글 용어 사전](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/glossary-ko-en.md)

읽은 절·자신의 설명·실습 명령·환경/패키지/데이터/모델/프롬프트(prompt)/인덱스(index) 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 계획과 실행, fixture와 실제 모델/검색/DB 실행, 목표와 실측을 구분한다. 자료 갱신만으로 학습 또는 구현을 Done 처리하지 않는다.
