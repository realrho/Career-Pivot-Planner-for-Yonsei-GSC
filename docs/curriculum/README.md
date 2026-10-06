# 『AI 에이전트 엔지니어링』 · SA 학습 8주 + MVP 제작 2주

주교재는 Michael Albada의 **『AI 에이전트 엔지니어링』(한빛미디어)**이다. 제공받은 13장 목차를 전부 읽되, 프로젝트에 필요한 지식·평가를 먼저 배워 적용하도록 장 순서를 바꿨다. 목차로 범위를 판단한 계획이며 책 본문을 검토한 품질 평가나 책 내용의 대체 요약은 아니다.

학습 8주(176h) + 제작 2주(44h), 총 10주. 기존 일정 2026-10-02–2026-12-10, 주 22h, Asia/Seoul을 유지한다. **2026-10-06 사용자 승인 영상 10묶음**을 각 주차의 읽기→영상→실습에 연결했다. Python·HTTP·SQL 기초 과정은 제외하고 API·입력 검증·트랜잭션·비동기 처리를 학습한다. 구현에 필요한 프레임워크와 영속 저장소 사용은 해당 실습에서 익힌다.

Docker와 Kubernetes는 로컬 실행 실습까지 필수다. 실제 클라우드 배포, 운영 Kubernetes HA, 추가 모델/검색 엔진, GPU 학습은 선택 심화다.

[책 공식 소개](https://www.hanbit.co.kr/books/ai-에이전트-엔지니어링?code=B1562725816) · [저자 예제 코드](https://github.com/michaelalbada/BuildingApplicationsWithAIAgents) · [승인 영상과 선정 근거](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/video-resources.md) · [13장 목차](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-toc.md) · [SA 보완 영역](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-gap-map.md) · [영어·한글 용어 사전](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/glossary-ko-en.md)

## 주차별 책·영상·실습 연결

| 주차·기존 일정 | 책과 학습 주제 | 영상 배정 | 교재·진행 |
|---|---|---|---|
| W1 · 2026-10-02–2026-10-08 | 1·2·3장 · 에이전트 설계·UX와 API 계약·입력 검증 | 묶음 1·4 / 2h | [주차 교재](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/curriculum/week-01.md) · [SCRUM-6](https://realrho-1790798942092.atlassian.net/browse/SCRUM-6) |
| W2 · 2026-10-09–2026-10-15 | 6장 · 지식·메모리·RAG와 정책·권한 필터 | 실습 집중 | [주차 교재](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/curriculum/week-02.md) · [SCRUM-7](https://realrho-1790798942092.atlassian.net/browse/SCRUM-7) |
| W3 · 2026-10-16–2026-10-22 | 9장 · 평가 세트·근거 검증·부하 시험 | 묶음 9·5 / 2.5h | [주차 교재](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/curriculum/week-03.md) · [SCRUM-8](https://realrho-1790798942092.atlassian.net/browse/SCRUM-8) |
| W4 · 2026-10-23–2026-10-29 | 4·5장 · 도구·오케스트레이션·비동기 처리 | 묶음 3 / 1h | [주차 교재](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/curriculum/week-04.md) · [SCRUM-9](https://realrho-1790798942092.atlassian.net/browse/SCRUM-9) |
| W5 · 2026-10-30–2026-11-05 | 8·12장 · 멀티 에이전트·영속 상태·트랜잭션·보안 | 묶음 2·6 / 1h | [주차 교재](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/curriculum/week-05.md) · [SCRUM-10](https://realrho-1790798942092.atlassian.net/browse/SCRUM-10) |
| W6 · 2026-11-06–2026-11-12 | 7·11장 · 학습·개선 루프·실험·비용·인프라 코드 | 묶음 8·10 / 1h | [주차 교재](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/curriculum/week-06.md) · [SCRUM-11](https://realrho-1790798942092.atlassian.net/browse/SCRUM-11) |
| W7 · 2026-11-13–2026-11-19 | 10장 · 관측·Docker·Kubernetes·CI/CD·복구 | 묶음 4·5·7 / 4.5h | [주차 교재](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/curriculum/week-07.md) · [SCRUM-12](https://realrho-1790798942092.atlassian.net/browse/SCRUM-12) |
| W8 · 2026-11-20–2026-11-26 | 13장 · 인간 협업·거버넌스·고객 제안·제작 준비 | 묶음 10 / 0.5h | [주차 교재](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/curriculum/week-08.md) · [SCRUM-13](https://realrho-1790798942092.atlassian.net/browse/SCRUM-13) |
| W9 · 2026-11-27–2026-12-03 | 제작 · MVP 통합 — 근거 응답·영속 상태·권한 있는 검토 | 실습 집중 | [주차 교재](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/curriculum/week-09.md) · [SCRUM-47](https://realrho-1790798942092.atlassian.net/browse/SCRUM-47) |
| W10 · 2026-12-04–2026-12-10 | 제작 · MVP 검증 — 최종 평가·복구·포트폴리오 시연 | 실습 집중 | [주차 교재](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/curriculum/week-10.md) · [SCRUM-48](https://realrho-1790798942092.atlassian.net/browse/SCRUM-48) |

## 주 22h 학습 방법

W1–W8은 책 읽기 6h, 책 개념 프로젝트 실습 6h, 승인 영상과 SA 실습 8h, 본인 설명/증거 검토 2h다. 영상 시간은 실제 재생시간의 합이 아니라 선택 편 시청·멈춤·메모를 포함한 계획 배정이다. 총 영상 배정 12.5h는 176h 학습 시간에 포함된다. 전체 재생목록 완강은 요구하지 않는다. W2는 새 영상 없이 RAG 실습에 집중한다. W9–W10은 새 학습보다 준비한 자산의 통합·검증에 44h를 쓴다.

책 읽기에서 문제와 용어를 적고 → 주차에서 지정한 영상 부분을 보며 기술 사용법을 연결하고 → 책 개념 실습 → 영상 직후 SA 실습 → 퀴즈와 실행 증거 검토 순서로 진행한다. 책의 모든 장 읽기와 고비용 예제 전부 실행은 구분한다. 입력부터 검색·평가를 먼저 배워서 도구 자율성을 늘리기 전에 실패를 측정할 수 있게 한다.

## 재사용 자산과 제작 시작 조건

W8까지 API 계약·실제 검색·PostgreSQL 영속 상태·권한/검토·재현 기동·평가 세트를 준비한다. Docker Compose와 로컬 Kubernetes API 배포·롤백을 확인하고 운영 규모에 맞는 플랫폼 선택 ADR을 남긴다. 미완료 선행 자산이 있으면 W9 시작/범위를 조정한다. 2주 제작은 준비 자산 재사용을 전제로 한 추정이다.

읽은 절·자신의 설명·실습 명령·환경/패키지/데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 계획과 실행, fixture와 실제 모델/검색/DB 실행, 목표와 실측을 구분한다. 자료 갱신만으로 학습 또는 구현을 Done 처리하지 않는다.

## 이전 자료

[이전 교재 16장 계획 보관](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/curriculum/archive-book-v2/README.md)과 기존 v1 보관본은 참고 자료다. labs/week-01..08의 예제는 이전 교재용 소형 계약 실습이며 새 주차의 학습 완료를 대신하지 않는다. 현재 API는 접수/조회 뼈대이며 실제 AI·검색·DB 통합은 학습 후 제작 과제다.
