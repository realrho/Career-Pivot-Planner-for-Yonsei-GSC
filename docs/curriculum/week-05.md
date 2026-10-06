# W5 학습 — 멀티 에이전트·영속 상태·트랜잭션·보안

**주교재:** 『AI 에이전트 엔지니어링』 · **책 범위:** 8장 단일 에이전트에서 멀티 에이전트로 / 12장 에이전틱 시스템 보안

**일정:** 2026-10-30–2026-11-05 (Asia/Seoul) · **총 계획:** 22h

[Notion 주차](https://app.notion.com/p/3ebc6f4a2c7e817e9825cec827df9013) · [SCRUM-10](https://realrho-1790798942092.atlassian.net/browse/SCRUM-10) · [GitHub #5](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/5)

## 1. 이번 주 목표와 책 읽기

8.1–8.10 전체: 에이전트 수·조율·A2A·메시지 브로커·액터·워크플로 엔진·상태/영속성. 12.1–12.6 전체: 에이전트 위험·공격·모델 보안·레드팀·MAESTRO·데이터 보호·보호 장치. 한 에이전트 기준선을 먼저 유지한다.

**필수 실습:** PostgreSQL의 사례 상태·검토·감사를 한 트랜잭션으로 저장하고 실패·동시 갱신을 검증한다. 인증된 tenant/role로 검색·조회·검토를 제한한다. 도구 접근 위협 모델을 그리고 클라우드 IAM/VPC 설계를 작성한다.

**재사용 산출물:** 영속 상태·검토·감사 설계, 트랜잭션 실패 기록, 권한 매핑, 위협 모델, 큐·저장소·네트워크 선택표

**완료 기준:** 감사 저장 실패 시 업무 상태도 롤백되며 중복·동시 검토가 잘못 승인되지 않는다. 교차 tenant·viewer 승인·주입된 도구 호출을 거부한다.

## 2. 책·영상·실습을 연결한 22h 실행 순서

| 순서 | 활동 | 계획 시간 | 결과/목적 |
|---|---|---|---|
| 1 | 책 읽기·설계 노트 | 6h | 8.1–8.10 전체: 에이전트 수·조율·A2A·메시지 브로커·액터·워크플로 엔진·상태/영속성. 12.1–12.6 전체: 에이전트 위험·공격·모델 보안·레드팀·MAESTRO·데이터 보호·보호 장치. 한 에이전트 기준선을 먼저 유지한다. |
| 2 | 승인 영상 선택 시청 | 1h | 묶음 2·6. 아래 보는 시점·범위를 따른다. |
| 3 | 책 개념 프로젝트 실습 | 6h | PostgreSQL의 사례 상태·검토·감사를 한 트랜잭션으로 저장하고 실패·동시 갱신을 검증한다. 인증된 tenant/role로 검색·조회·검토를 제한한다. 도구 접근 위협 모델을 그리고 클라우드 IAM/VPC 설계를 작성한다. |
| 4 | 영상과 연결한 SA 실습 | 7h | 영속 상태·검토·감사 설계, 트랜잭션 실패 기록, 권한 매핑, 위협 모델, 큐·저장소·네트워크 선택표 |
| 5 | 설명·퀴즈·증거 검토 | 2h | 감사 저장 실패 시 업무 상태도 롤백되며 중복·동시 검토가 잘못 승인되지 않는다. 교차 tenant·viewer 승인·주입된 도구 호출을 거부한다. |

영상 배정은 주간 시간 안에 포함된 선택 시청·메모 시간이다. 영상마다 아래 시청 직후 실습을 이어서 수행한다. 순서는 진행 안내이며 Jira 네 작업은 읽기6h·개념 실습6h·영상/SA8h·검토2h로 시간을 집계한다.

## 3. 이번 주에 볼 한국어 영상과 연결 실습

### 영상 1. Transactions · 학습 묶음 2

**보는 시점:** 8.9 상태와 영속성 관리 다음.

- [BJ.42 데이터베이스 트랜잭션과 ACID](https://www.youtube.com/watch?v=sLJ8ypeHGlM) — 쉬운코드, 한국어 수업.

**볼 범위:** 트랜잭션·ACID 개념(약 25분). SQL 문법과 Java/Spring 문법 학습은 제외한다.

**시청 직후 실습:** 승인 상태 변경과 감사 기록을 같은 트랜잭션으로 묶고 감사 실패를 주입한다. 모두 롤백되는지, 중복/동시 승인에 충돌 처리가 있는지 확인한다.

### 영상 2. AWS network and permissions · 학습 묶음 6

**보는 시점:** 12장 위협·데이터 보호·에이전트 권한 다음.

- [(리뉴얼) 쉽게 설명하는 AWS 기초강의 29. VPC와 서브넷](https://www.youtube.com/watch?v=azd_k4bOXqw) — AWS 강의실, 한국어 수업.
- [(리뉴얼) 쉽게 설명하는 AWS 기초강의 9. IAM 기초](https://www.youtube.com/watch?v=HKIg04dDS8A) — AWS 강의실, 한국어 수업.

**볼 범위:** VPC·서브넷 약 23분 + IAM 기초 약 11분. 독립 강사 채널이며 AWS 공식 채널과 구분한다.

**시청 직후 실습:** 공개 API/비공개 DB 네트워크와 신원→role→tenant 권한표를 그린다. IAM 정책·비밀 관리·저장소/컴퓨팅 선택 이유를 적는다.


## 4. 영어·한국어 개념 강의

### 5.1 Transaction·ACID — 트랜잭션과 일관된 갱신

transaction(트랜잭션)은 함께 성공하거나 함께 실패해야 하는 업무 변경의 경계다. ACID는 Atomicity(원자성), Consistency(일관성), Isolation(격리성), Durability(지속성)이다. 격리 수준·조건부 갱신·제약은 동시 요청의 결과에 영향을 준다. 한 DB의 원자성이 외부 API나 메시지 발행까지 자동으로 확장되지는 않는다.

**업무 예시:** 검토 결정과 감사 기록을 한 트랜잭션으로 저장한다. 감사 삽입 실패가 나면 사례 상태만 승인으로 남아서는 안 된다. 오래된 case_version으로 결정하면 충돌을 반환한다.

**직접 할 일:** 쉬운코드 영상에서 개념·ACID를 보고 SQL/Java 문법 기초는 생략한다. 실제 PostgreSQL에서 실패 주입·동시 검토·재시작 후 조회를 검증한다.

### 5.2 Queue·Cache·Outbox — 큐·캐시·발행 기록

message broker(메시지 브로커)는 작업이나 이벤트 전달을 중개한다. worker(워커)는 전달된 작업을 수행한다. Redis는 캐시 등에 쓰이는 저장소 제품이고 SQS·RabbitMQ·Kafka는 서로 다른 운영·전달 모델을 가진 제품이다. 모든 제품을 구현하지 않고 지속성·순서·중복·지연·운영 부담으로 하나를 선택한다. outbox(발행 기록 패턴)는 DB 변경과 발행할 이벤트를 함께 기록한 뒤 전달을 수행하는 방식이다.

**업무 예시:** 접수 상태만 DB에 저장하고 메시지 전송이 실패하면 작업이 사라질 수 있다. 중복 전달도 고려해 워커의 업무 효과를 멱등하게 만든다.

**직접 할 일:** 내구성 요구와 로컬 시연 범위를 적고 DB 작업 기록/브로커 중 하나를 선택한다. 캐시 키에 tenant·정책 버전을 넣고 만료·무효화를 설명한다.

### 5.3 Identity·IAM·RBAC — 신원과 권한

IAM, Identity and Access Management(신원·접근 관리)는 리소스 권한을 관리한다. RBAC, Role-Based Access Control(역할 기반 접근 제어)은 역할별 허용 행동을 정한다. authentication(인증)은 신원 확인, authorization(인가)은 해당 행동의 허용 여부다. SSO, Single Sign-On(통합 로그인)과 OAuth/OIDC는 기업 신원 통합을 위한 선택 영역이다. 서비스 권한과 최종 사용자의 업무 권한을 모두 확인한다.

**업무 예시:** API 서버가 DB에 접근하는 권한과 viewer가 검토를 승인하는 권한은 다르다. 본문 reviewer=true는 신원 증거가 아니다.

**직접 할 일:** IAM 기초 영상과 역할 표를 연결한다. 읽기·검색·승인·관리 권한을 매핑하고 역할/tenant 불일치를 실패 사례로 만든다.

### 5.4 Threat Model·VPC — 위협 모델과 네트워크 경계

threat model(위협 모델)은 자산·신뢰 경계·공격 경로·대응을 정리한 것이다. VPC, Virtual Private Cloud(가상 사설 클라우드)는 클라우드 네트워크를 구성하는 경계다. subnet(서브넷)·라우팅·보안 그룹은 서로 다른 역할을 한다. prompt injection(프롬프트 주입)은 문서의 악성 지시가 업무 권한처럼 해석되는 위험이다. 책의 MAESTRO는 Multi-Agent Environment, Security, Threat, Risk, and Outcome(다중 에이전트 환경·보안·위협·위험·결과) 위협 모델링 틀이다.

**업무 예시:** 검색 문서가 '모든 정책을 외부로 보내라'고 해도 도구 권한과 시스템 규칙을 바꾸면 안 된다. 공개 API와 비공개 DB 사이의 허용 연결만 설계한다.

**직접 할 일:** VPC·서브넷 영상을 보고 API/DB/비밀 저장소/사용자의 데이터 흐름을 그린다. 누출·과도한 권한·내부 실패를 각 1개 이상 위협 모델에 넣는다.

## 5. 확인 퀴즈

### Q1. DB 트랜잭션으로 외부 API 쓰기도 자동 롤백되는가?

**해설:** 한 DB 경계를 넘는 부작용에는 별도 발행 기록·보상·조정이 필요하다.

### Q2. 비동기 작업이 한 번만 전달된다고 가정해도 되는가?

**해설:** 선택 시스템의 전달 보장을 확인하고 중복 처리와 실패 복원을 설계한다.

### Q3. viewer=true 같은 본문 필드를 권한으로 사용해도 되는가?

**해설:** 서버가 검증한 신원과 역할을 권한 판단에 사용한다.

## 6. Jira 작업·수용 기준

- **SCRUM-30 · 책 8·12장 읽기·설계/개념 노트 (6h)**
  - 선행: SCRUM-9.
  - 수용 기준: 8.1–8.10 전체: 에이전트 수·조율·A2A·메시지 브로커·액터·워크플로 엔진·상태/영속성. 12.1–12.6 전체: 에이전트 위험·공격·모델 보안·레드팀·MAESTRO·데이터 보호·보호 장치. 한 에이전트 기준선을 먼저 유지한다. 산출물: 핵심 용어의 영어·한글 뜻과 업무 설계 메모.
- **SCRUM-31 · 책 개념을 적용한 프로젝트 실습 (6h)**
  - 선행: SCRUM-30.
  - 수용 기준: PostgreSQL의 사례 상태·검토·감사를 한 트랜잭션으로 저장하고 실패·동시 갱신을 검증한다. 인증된 tenant/role로 검색·조회·검토를 제한한다. 도구 접근 위협 모델을 그리고 클라우드 IAM/VPC 설계를 작성한다. 산출물: 정상/실패 expected/actual·raw 결과.
- **SCRUM-32 · 영상·SA 보충 실습 — 멀티 에이전트·영속 상태·트랜잭션·보안 (8h)**
  - 선행: SCRUM-31.
  - 수용 기준: 승인 영상 배정 1h + 연결 실습 7h. 영속 상태·검토·감사 설계, 트랜잭션 실패 기록, 권한 매핑, 위협 모델, 큐·저장소·네트워크 선택표. 감사 저장 실패 시 업무 상태도 롤백되며 중복·동시 검토가 잘못 승인되지 않는다. 교차 tenant·viewer 승인·주입된 도구 호출을 거부한다.
- **SCRUM-33 · 퀴즈·본인 설명·증거·다음 주 준비 검토 (2h)**
  - 선행: SCRUM-32.
  - 수용 기준: 퀴즈 3개를 자신의 말로 설명하고 정상/실패 증거와 다음 주 선행 조건을 검토한다.

## 7. 공식 문서와 증거

- [트랜잭션](https://www.postgresql.org/docs/current/tutorial-transactions.html) — 현재 API·설치·보안 설정을 확인한다.
- [MAESTRO](https://labs.cloudsecurityalliance.org/maestro/) — 현재 API·설치·보안 설정을 확인한다.

[책 공식 소개](https://www.hanbit.co.kr/books/ai-에이전트-엔지니어링?code=B1562725816) · [저자 예제 코드](https://github.com/michaelalbada/BuildingApplicationsWithAIAgents) · [승인 영상과 선정 근거](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/video-resources.md) · [13장 목차](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-toc.md) · [SA 보완 영역](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-gap-map.md) · [영어·한글 용어 사전](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/glossary-ko-en.md)

읽은 절·자신의 설명·실습 명령·환경/패키지/데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 계획과 실행, fixture와 실제 모델/검색/DB 실행, 목표와 실측을 구분한다. 자료 갱신만으로 학습 또는 구현을 Done 처리하지 않는다.
