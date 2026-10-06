# W2 학습 — 지식·메모리·RAG와 정책·권한 필터

**주교재:** 『AI 에이전트 엔지니어링』 · **책 범위:** 6장 지식과 메모리

**일정:** 2026-10-09–2026-10-15 (Asia/Seoul) · **총 계획:** 22h

[Notion 주차](https://app.notion.com/p/3ebc6f4a2c7e819fae0cd5cb69a99181) · [SCRUM-7](https://realrho-1790798942092.atlassian.net/browse/SCRUM-7) · [GitHub #2](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/2)

## 1. 이번 주 목표와 책 읽기

6.1–6.4 전체: 컨텍스트 윈도·전체 텍스트 검색, 시맨틱 검색·벡터 스토어·RAG·경험 메모리, 지식 그래프·GraphRAG·노트 작성. GraphRAG 구축은 개념과 선택 기준을 읽고 고급 구현은 선택한다.

**필수 실습:** 합성 정책 12–24개를 준비해 source_id·tenant_id·policy_version·allowed_roles를 붙인다. 한 임베딩 모델과 검색 backend로 분할→인덱싱→검색 한 경로를 실행한다. 질문 20개와 정답 근거를 개발 세트로 만든다.

**재사용 산출물:** 문서/청크 manifest, 실제 검색 경로, 정책·권한 필터, dev20 질문과 근거, 검색 실패 사례

**완료 기준:** 다른 tenant·비활성 버전·권한 밖 근거가 검색 결과와 응답에 섞이지 않는다. 문서·청크·인덱스 버전과 근거 ID가 연결된다.

## 2. 책·영상·실습을 연결한 22h 실행 순서

| 순서 | 활동 | 계획 시간 | 결과/목적 |
|---|---|---|---|
| 1 | 책 읽기·설계 노트 | 6h | 6.1–6.4 전체: 컨텍스트 윈도·전체 텍스트 검색, 시맨틱 검색·벡터 스토어·RAG·경험 메모리, 지식 그래프·GraphRAG·노트 작성. GraphRAG 구축은 개념과 선택 기준을 읽고 고급 구현은 선택한다. |
| 2 | 승인 영상 선택 시청 | 0h | 배정 0h. 책 실습에 집중. |
| 3 | 책 개념 프로젝트 실습 | 6h | 합성 정책 12–24개를 준비해 source_id·tenant_id·policy_version·allowed_roles를 붙인다. 한 임베딩 모델과 검색 backend로 분할→인덱싱→검색 한 경로를 실행한다. 질문 20개와 정답 근거를 개발 세트로 만든다. |
| 4 | 영상과 연결한 SA 실습 | 8h | 문서/청크 manifest, 실제 검색 경로, 정책·권한 필터, dev20 질문과 근거, 검색 실패 사례 |
| 5 | 설명·퀴즈·증거 검토 | 2h | 다른 tenant·비활성 버전·권한 밖 근거가 검색 결과와 응답에 섞이지 않는다. 문서·청크·인덱스 버전과 근거 ID가 연결된다. |

영상 배정은 주간 시간 안에 포함된 선택 시청·메모 시간이다. 영상마다 아래 시청 직후 실습을 이어서 수행한다. 순서는 진행 안내이며 Jira 네 작업은 읽기6h·개념 실습6h·영상/SA8h·검토2h로 시간을 집계한다.

## 3. 이번 주에 볼 한국어 영상과 연결 실습

이 주는 책 실습에 집중한다. 새 영상 묶음을 추가하지 않고 앞 주에서 확인한 개념을 실제 검색 경로에 적용한다.

## 4. 영어·한국어 개념 강의

### 2.1 RAG·Chunking — 검색 증강 생성과 문서 분할

RAG, Retrieval-Augmented Generation(검색 증강 생성)은 모델에 검색한 근거를 제공해 답하도록 하는 방식이다. chunking(문서 분할)은 검색 단위를 만드는 작업이다. 너무 작으면 예외 조항이 떨어지고 너무 크면 불필요한 내용과 비용이 늘어난다. overlap(겹침)은 경계의 문맥을 일부 보존하지만 문서 구조와 표·절 제목을 대신하지 못한다.

**업무 예시:** 환불 원칙과 예외를 서로 다른 청크에 넣으면 원칙만 검색해 잘못 답할 수 있다. 문서 제목·절·버전·청크 위치를 함께 보관한다.

**직접 할 일:** 두 분할 설정을 dev20으로 비교하고 근거 누락 사례를 기록한다. 최종 holdout 정답으로 설정을 고르지 않는다.

### 2.2 Embedding·Hybrid Search — 임베딩·하이브리드 검색

embedding(임베딩)은 텍스트를 비교 가능한 숫자 벡터로 나타낸 것이다. semantic search(의미 검색)는 벡터 유사성을 사용하고 lexical search(어휘 검색)는 단어·코드 일치를 찾는다. hybrid search(하이브리드 검색)는 두 경로를 결합한다. 비슷한 문장이 검색돼도 실제 정책의 적용 대상·날짜·예외가 맞는지는 따로 검사해야 한다.

**업무 예시:** 'P-103 환불'처럼 정확한 정책 번호는 어휘 검색이 유리할 수 있다. embedding 점수는 답이 참일 확률이 아니다.

**직접 할 일:** 한 backend에서 의미/어휘 검색 결과를 비교한다. 재정렬 추가는 기준선보다 이득이 있는 경우에만 선택한다.

### 2.3 Tenant·Version Filter — 고객사·정책 버전·권한 경계

tenant(테넌트)는 고객사처럼 데이터를 격리할 단위다. metadata filter(메타데이터 필터)는 tenant·활성 버전·사용자 역할 조건을 검색에 적용한다. 검색 뒤 화면에서만 숨기면 모델에 이미 다른 고객사의 근거가 전달될 수 있다. 인덱싱과 검색 단계 모두 권한 경계를 설계하고 최종 결과를 다시 확인한다.

**업무 예시:** tenant-a의 질문이 tenant-b 문서를 받아오거나 이전 환불 버전으로 답하면 유사도가 높아도 실패다. 요청 본문의 tenant 값을 신뢰하지 않는다.

**직접 할 일:** 교차 tenant·이전 버전·권한 없는 문서 사례를 만들고 retrieval 결과와 모델 입력에서 모두 제외됨을 확인한다.

### 2.4 Memory·GraphRAG — 메모리와 지식 그래프 선택

context window(컨텍스트 윈도)는 한 호출에서 모델이 참고할 입력 범위다. short-term memory(단기 메모리)는 현재 작업 상태, long-term memory(장기 메모리)는 작업 간 저장된 정보를 뜻한다. GraphRAG는 graph(그래프)의 관계 정보를 검색에 활용하는 방식이며 단순 벡터 검색보다 항상 좋지는 않다. 관계 구축·최신화·권한 검사와 운영 비용을 함께 고려한다.

**업무 예시:** 고객별 메모리가 섞이면 이후 대화까지 다른 고객사의 정보를 노출할 수 있다. '최근 요약'에는 원문 출처·버전과 만료 조건이 필요하다.

**직접 할 일:** 단기 상태/장기 지식/감사 기록을 다른 저장 목적에 배정한다. GraphRAG 도입 여부를 데이터 관계와 평가 이득으로 설명한다.

## 5. 확인 퀴즈

### Q1. 벡터 유사도가 높으면 정책 답변도 맞는가?

**해설:** 정책 버전·적용 대상·예외·권한과 답변의 의미 일치를 별도로 확인한다.

### Q2. 권한 필터는 응답 화면에서만 적용해도 되는가?

**해설:** 검색과 모델 입력 이전에 적용하고 최종 결과에서도 검사해야 한다.

### Q3. GraphRAG가 기본 필수 구현인가?

**해설:** 관계 기반 질의에 실제 이득이 있고 구축·운영 비용을 감당할 때 선택한다. 이번 과정에서는 모든 절을 읽되 구축은 선택이다.

## 6. Jira 작업·수용 기준

- **SCRUM-18 · 책 6장 읽기·설계/개념 노트 (6h)**
  - 선행: SCRUM-6.
  - 수용 기준: 6.1–6.4 전체: 컨텍스트 윈도·전체 텍스트 검색, 시맨틱 검색·벡터 스토어·RAG·경험 메모리, 지식 그래프·GraphRAG·노트 작성. GraphRAG 구축은 개념과 선택 기준을 읽고 고급 구현은 선택한다. 산출물: 핵심 용어의 영어·한글 뜻과 업무 설계 메모.
- **SCRUM-19 · 책 개념을 적용한 프로젝트 실습 (6h)**
  - 선행: SCRUM-18.
  - 수용 기준: 합성 정책 12–24개를 준비해 source_id·tenant_id·policy_version·allowed_roles를 붙인다. 한 임베딩 모델과 검색 backend로 분할→인덱싱→검색 한 경로를 실행한다. 질문 20개와 정답 근거를 개발 세트로 만든다. 산출물: 정상/실패 expected/actual·raw 결과.
- **SCRUM-20 · 영상·SA 보충 실습 — 지식·메모리·RAG와 정책·권한 필터 (8h)**
  - 선행: SCRUM-19.
  - 수용 기준: 승인 영상 배정 0h + 연결 실습 8h. 문서/청크 manifest, 실제 검색 경로, 정책·권한 필터, dev20 질문과 근거, 검색 실패 사례. 다른 tenant·비활성 버전·권한 밖 근거가 검색 결과와 응답에 섞이지 않는다. 문서·청크·인덱스 버전과 근거 ID가 연결된다.
- **SCRUM-21 · 퀴즈·본인 설명·증거·다음 주 준비 검토 (2h)**
  - 선행: SCRUM-20.
  - 수용 기준: 퀴즈 3개를 자신의 말로 설명하고 정상/실패 증거와 다음 주 선행 조건을 검토한다.

## 7. 공식 문서와 증거

- [OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/) — 현재 API·설치·보안 설정을 확인한다.

[책 공식 소개](https://www.hanbit.co.kr/books/ai-에이전트-엔지니어링?code=B1562725816) · [저자 예제 코드](https://github.com/michaelalbada/BuildingApplicationsWithAIAgents) · [승인 영상과 선정 근거](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/video-resources.md) · [13장 목차](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-toc.md) · [SA 보완 영역](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-gap-map.md) · [영어·한글 용어 사전](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/glossary-ko-en.md)

읽은 절·자신의 설명·실습 명령·환경/패키지/데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 계획과 실행, fixture와 실제 모델/검색/DB 실행, 목표와 실측을 구분한다. 자료 갱신만으로 학습 또는 구현을 Done 처리하지 않는다.
