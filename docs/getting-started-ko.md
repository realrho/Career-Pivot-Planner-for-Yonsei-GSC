# 시작하기 · 책·영상·실습을 연결하는 방법

주교재는 Michael Albada의 **『AI 에이전트 엔지니어링』(한빛미디어)**이다. 제공받은 13장 목차를 전부 읽되, 프로젝트에 필요한 지식·평가를 먼저 배워 적용하도록 장 순서를 바꿨다. 목차로 범위를 판단한 계획이며 책 본문을 검토한 품질 평가나 책 내용의 대체 요약은 아니다.

학습 8주(176h) + 제작 2주(44h), 총 10주. 기존 일정 2026-10-02–2026-12-10, 주 22h, Asia/Seoul을 유지한다. **2026-10-06 사용자 승인 영상 10묶음**을 각 주차의 읽기→영상→실습에 연결했다. Python·HTTP·SQL 기초 과정은 제외하고 API·입력 검증·트랜잭션·비동기 처리를 학습한다. 구현에 필요한 프레임워크와 영속 저장소 사용은 해당 실습에서 익힌다.

Docker와 Kubernetes는 로컬 실행 실습까지 필수다. 실제 클라우드 배포, 운영 Kubernetes HA, 추가 모델/검색 엔진, GPU 학습은 선택 심화다.

[책 공식 소개](https://www.hanbit.co.kr/books/ai-에이전트-엔지니어링?code=B1562725816) · [저자 예제 코드](https://github.com/michaelalbada/BuildingApplicationsWithAIAgents) · [승인 영상과 선정 근거](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/video-resources.md) · [13장 목차](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-toc.md) · [SA 보완 영역](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/book-gap-map.md) · [영어·한글 용어 사전](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/blob/main/docs/glossary-ko-en.md)

AWS 주교재는 [사용자 지정 시작 영상](https://www.youtube.com/watch?v=cBbHXCmoUTc&list=PLtUgHNmvcs6qr33RT-UiguSsCr_2Gq0S3&index=3)과 연결 재생목록으로 교체했다(2026-10-07). W5 EC2·보안그룹 → W6 비용/정리 → W7 기존 FastAPI/Compose 배포 개념 → W8 선택 ADR로 연결한다. IAM/VPC는 공식 문서로 보완한다. 실제 AWS 배포는 선택 심화이며 주 22h와 8+2주 일정은 유지한다.

## 매주 실제 진행 순서

1. 주차 교재에서 책의 장/절과 이번 주 문제·완료 기준을 확인한다.
2. 책 개념을 읽으며 용어를 **약어 → English full name → 자연스러운 한국어 뜻 → 프로젝트에서 하는 일**로 적는다.
3. W1 API는 [FastAPI 첫걸음 전체 재생목록](https://youtube.com/playlist?list=PL8kmk2VivDmQyPLmc4zF6yLEl-Rc6D9lg&si=iKuEUs7JNHJV-N7R)의 공개 기본편 6개를 모두 학습한다. 나머지 영상은 해당 주차에 지정한 편/부분을 본다. 영상 직후 예제 실행과 입력·실패·배포 실습을 한다.
4. 책 개념을 합성 정책 프로젝트에 적용하고 정상/실패 expected/actual을 비교한다.
5. 자기 설명·퀴즈·raw 결과·commit/run_id를 남기고 수용 기준을 만족했을 때 본인의 진행 상태를 바꾼다.

주차 강의는 책 본문의 발췌가 아니라 개념과 시스템 경계를 연결한 자체 설명이다. 이해가 막히면 책 해당 절→영상 해당 부분→현재 공식 문서 순서로 확인한다. 영상에 나온 오래된 API/설치/가격을 그대로 쓰지 않는다.

## 환경과 학습 범위

프로젝트 기존 FastAPI/Pydantic 환경을 이용한다. Python·HTTP·SQL 기초 과정은 배정하지 않는다. API·입력 검증·트랜잭션·비동기 실패 처리는 실제 실습으로 익힌다. 서로 다른 실험의 패키지/모델 환경은 분리하고 검증한 버전을 기록한다.

W1 Docker 이미지/컨테이너 입문 → W3 kind 또는 minikube 로컬 클러스터와 kubectl → W5 PostgreSQL 영속 상태 → W6 Terraform 로컬 plan/state → W7 Dockerfile/Compose + Kubernetes API 배포/probes/Secret/롤백 + Actions CI + 백업 복원으로 이어진다. Docker·Kubernetes는 개념 시청만으로 완료하지 않는다. GPU/실제 클라우드/운영 K8s HA는 선택 심화다.

실제 RAG 경로는 W2 한 검색 backend로 시작하고 W3 평가 세트로 확인한다. dev20과 최종 holdout30은 분리한다. 최종 질문으로 설정을 선택하지 않는다. 모델·DB·권한 통합이 없으면 fixture 실습만으로 W8 준비 gate를 통과했다고 기록하지 않는다.

## W9 제작 시작 조건

API 계약·실제 검색·영속 DB·권한/검토·재현 기동·평가 세트의 6자산을 W8까지 준비한다. 로컬 Kubernetes는 API 배포/롤백 학습 증거를 남기며 최종 데모의 기본 전체 스택은 Compose로 재현할 수 있다. 6자산이 없으면 2주 제작 추정을 다시 잡는다.

읽은 절·자신의 설명·실습 명령·환경/패키지/데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 계획과 실행, fixture와 실제 모델/검색/DB 실행, 목표와 실측을 구분한다. 자료 갱신만으로 학습 또는 구현을 Done 처리하지 않는다.

[10주 교재](curriculum/README.md) · [MVP 설계](project-blueprint.md) · [이전 교재 보관](curriculum/archive-book-v2/README.md)
