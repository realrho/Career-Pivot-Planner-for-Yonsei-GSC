# W9 제작 · MVP 통합 — 근거 응답·영속 상태·권한 있는 검토

**기간:** 2026-11-27–2026-12-03 (Asia/Seoul) · **계획:** 22h · [Notion](https://app.notion.com/p/3ecc6f4a2c7e812189a5fad40b9b3f33) · [Jira SCRUM-47](https://realrho-1790798942092.atlassian.net/browse/SCRUM-47) · [GitHub #9](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/9)

**이번 주 통과 조건:** 정상 근거 응답·근거 없는 보류·고위험 검토가 실제 검색/모델/DB 경로에서 동작하고 재시작 후 조회된다. viewer와 다른 tenant의 검토를 거부한다.

[전체 학습표](README.md) · [책 목차 원문](../book-toc.md) · [용어 사전](../glossary-ko-en.md) · [책/보충 범위](../book-gap-map.md)

## 1. 책 읽기와 필수 실습

**배정:** 이전 8주 자산 재사용

책 9–13·15장의 필요한 절과 W1–W8 실습 자산을 참조한다. 새 강의를 몰아넣지 않고 이미 검증한 경로를 연결한다.

**필수 실습:** W8준비gate를먼저확인하고입력→권한→검색→생성→검증→분기→저장→조회/검토의통합경로를완성한다.

책 본문은 소유한 책에서 읽는다. [공식 코드](https://github.com/onlybooks/llm)·[정오표](https://www.onlybook.co.kr/entry/llm-errata)를 확인하고 환경/모델/패키지 버전을 기록한다. 선택 GPU/멀티모달 실습의 미실행은 필수 완료와 분리한다.

## 2. 실행 순서·시간·수용 기준

| 순서 | 작업 | 계획 시간 | 완료 기준 | Jira |
|---|---|---|---|---|
| 1 | 범위·계약·환경 동결과 통합 입력 준비 | 5h | W8 준비 gate 증거 확인. 모델/벡터backend/코퍼스/권한/상태/API계약을 동결하고 새 환경 기동한다. | [SCRUM-49](https://realrho-1790798942092.atlassian.net/browse/SCRUM-49) |
| 2 | tenant·버전 검색과 실제 모델 근거 응답 통합 | 6h | 인용ID·의미평가·근거 없는 보류·교차tenant거부를 실제 경로로 검증한다. | [SCRUM-50](https://realrho-1790798942092.atlassian.net/browse/SCRUM-50) |
| 3 | 영속 상태·검토 권한·감사 원자성 통합 | 6h | case/review/audit를 PostgreSQL로 저장. 동시/중복검토·권한거부·재시작조회·rollback을 검증한다. | [SCRUM-51](https://realrho-1790798942092.atlassian.net/browse/SCRUM-51) |
| 4 | 정상·보류·검토 통합 회귀와 장애 처리 | 5h | 세 종단경로의 expected/actual 결과, 모델 timeout·형식 오류·DB실패 처리와 실행 증거를 남긴다. | [SCRUM-52](https://realrho-1790798942092.atlassian.net/browse/SCRUM-52) |

## 3. 상세 빌드 레시피 · 파일·입력·실패·검증

### 1. 범위·설정·통합 입력 동결 (5h)

W8의 6가지 필수 준비 항목을 실제 증거로 확인한다. corpus12–24개·tenant2개·활성정책·모델1경로·벡터backend1개·schema/prompt/index버전을 고정한다. 기존 API 계약 변경이 필요하면 먼저 ADR/테스트를 수정한다. 합성 정상/근거없음/고위험 사례 각각 하나를 저장한다. 준비 미완료면 날짜/범위를 조정한다.

### 2. 검색→생성→근거 검증 연결 (6h)

예정 app/services/analyze.py에서 서버 신원 컨텍스트를 받는다. retrieval adapter가 tenant/활성version 조건을 적용하고 evidence ID를 반환한다. model adapter는 동일 근거로 구조화 결과를 생성한다. output validator가 필드·인용 소속·허용결정을 검사한다. 근거 없음은 ABSTAIN, 기술 오류는 FAILED로 구분한다. 의미 일치는 평가 rubric으로 확인한다.

### 3. 저장→조회→검토 연결 (6h)

PostgreSQL repository에 case/status/run/version을 저장하고 동일 tenant 조회만 허용한다. POST review는 reviewer/tenant/상태/expected_version을 확인하고 상태·review·audit를 원자적으로 갱신한다. viewer/다른tenant/중복최종검토/동시검토를 거부한다. API 재시작 후 case와 검토 대기가 유지되는지 실제 DB에서 확인한다.

### 4. 실패를 포함한 종단 회귀 (5h)

정상근거응답·근거없는보류·고위험검토 3경로와 모델timeout/형식오류/DB감사실패를 검증한다. 비동기 접수202를 유지한다면 지속 작업과 재개가 존재하는지 확인한다. 모델 호환성이나 새 큐 프레임워크를 이번 주 새로 확장하지 않는다. raw 입력/expected/actual·버전·run_id를 남긴다.

## 4. 이 주차에서 새로 확장하지 않을 범위

GPU미세조정·멀티모달·다중에이전트·두번째DB/모델·KubernetesHA는 추가 과정이다. 필수 Compose와 실제 모델/검색/DB 경로를 먼저 검증한다. 기존 준비 자산이 없으면 예상44시간을 다시 산정한다.

[공통 MVP 설계/계약](../project-blueprint.md) · [환경/학습법](../getting-started-ko.md)

## 증거와 완료 상태

학습 노트에는 읽은 절·자신의 설명·실습 명령·Python/패키지/장치·데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 문서/fixture/실제DB·모델/클라우드·GPU의 수준을 구분한다. 자료 작성만으로 본인의 학습 또는 서비스 제작을 완료 처리하지 않는다. 막히면 증상·시도·다음 행동과 일정 영향을 남긴다.
