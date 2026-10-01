# 책 내용과 SA 보충 범위

이 분석은 **사용자가 제공한 목차**를 기준으로 한다. 본문 전체를 읽지 않고 '책에 전혀 없다'고 단정하지 않는다. 책 본문은 소유한 책에서 읽고, 여기서는 프로젝트에 필요한 운영·통합 경계를 보충한다.

| 분야 | 목차에서 확인한 범위 | 보충할 실무 경계 | 주차 |
|---|---|---|---|
| LLM 기초·학습·GPU | 1–8장: Transformer/HF/SFT/LoRA/양자화/vLLM | 모델 선택의 업무·비용·데이터 조건, 실제 실행과 계산 구분 | W1–3 |
| RAG·캐시·검증·로그 | 9장에 이미 존재 | 요청 계약·tenant/버전 캐시·비밀/원문 로깅 경계 | W1/3/4/6 |
| 검색·embedding·hybrid·reranker | 10–11장에 이미 존재 | gold 근거·동결 평가·권한 필터·같은 조건 비교 | W4–5 |
| 벡터 DB·HNSW·Pinecone | 12장에 이미 존재 | 관계형 업무 상태·원자적 검토·멱등 적재·활성 버전 | W5 |
| MLOps/LLMOps·RAG 평가 | 13장에 이미 존재 | 권한/주입/보류/검토 평가, 실행 버전·실패 비용 | W6–7 |
| 멀티모달·AutoGen 에이전트 | 14–15장에 이미 존재 | 허용 도구·최대 단계·재개·검토 승인 경계 | W7 |
| 새로운 아키텍처 | 16장: SSM/S4/Mamba | 고객 조건·호환성·측정 증거로 선택하는 ADR | W8 |
| Python/Git/API 기초 | 목차에 독립적인 기초 과정은 보이지 않음 | 환경·함수/예외·변경 이력·HTTP/JSON/FastAPI 계약 | W1 |
| SQL·데이터 무결성 | 6장 Text2SQL은 생성 과제 | 직접 SQL·키/제약·읽기 권한·ACID·동시성 | W2/5 |
| 네트워크·클라우드·권한 | 목차에 독립적인 전체 과정은 보이지 않음 | DNS/TLS·VPC/subnet·IAM/RBAC·비밀 | W3/6 |
| 배포·운영·복구 | 서빙/운영 주제는 있으나 세부 통합 경계를 추가 | Docker/Compose·readiness·CI/CD·관측·백업/RTO/RPO | W7 |
| SA 고객 설계·전달 | 별도 전담 장은 보이지 않음 | discovery·FR/NFR·PoC/MVP·ADR·TCO·영어 데모 | W8–10 |

필수 스택은 Python/FastAPI, SQL/PostgreSQL, RAG+한 벡터 backend, 모델 한 경로, 서버 권한/검토, Docker Compose, 평가/로그/CI다. 책의 LlamaIndex/Pinecone/AutoGen을 읽고, 프로젝트에서는 이미 검증한 한 경로를 선택한다. Milvus·LangGraph·Redis를 동시에 새 필수로 얹지 않는다. AWS는 IAM/VPC/배포 설계 필수, 실제 리소스 배포 선택. Kubernetes는 개념·선택 기준 필수, 클러스터 운영은 추가 과정이다.

GPU 학습·전체 멀티모달 생성·두 번째 DB/모델·분산 학습·K8s 고가용성은 선택 심화다. 책의 모든 장을 읽는 것과 모든 고비용 실습을 실행하는 것은 다르다. 선택 미실행은 기록하고, 핵심 실제 검색/DB/모델 경로가 막히면 최종 통합 gate는 미완료로 둔다.

[책 원문 목차](book-toc.md) · [주차별 학습표](curriculum/README.md) · [용어 사전](glossary-ko-en.md)
