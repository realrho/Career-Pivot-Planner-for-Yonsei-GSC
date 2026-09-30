# 프로젝트 설계서 · 고객·범위·계약·아키텍처

> **프로젝트:** Enterprise AI Knowledge & Risk Copilot. 두 가상 SaaS 사업부의 합성 정책·사례로 ‘근거 검색→분석→불확실/고위험 검토’ 업무를 구현한다. 이 고객 시나리오는 기존 프로젝트를 구체화한 학습 가정이다.

## 고객·문제·가치

지원 담당자는 여러 버전의 정책에서 조건을 찾기 어렵고, 위험한 예외는 검토자에게 넘겨야 한다. 고객 목표는 출처를 확인할 수 있는 분석 초안과 검토 이유를 제공하는 것이다. 실제 고객 시간 절감/채용 성과는 측정하지 않았다. 합성 corpus의 제품 행동과 기술 품질부터 검증한다.

**사용자:** support analyst, reviewer, system operator. **입력:** 합성 사례 텍스트·신뢰된 tenant/user 컨텍스트. **출력:** status·decision·rationale·evidence IDs/sections·policy version·review reason·trace ID.

## 3개 최종 데모

1. 정상: 정책 근거가 있는 사례→최신 허용 문서→근거 포함 구조화된 답변.
2. 근거 부족: corpus 밖 질문→INSUFFICIENT_EVIDENCE→추측 결론 없음.
3. 고위험: 충분한 근거가 있어도 HUMAN_REVIEW→권한 있는 승인/수정→재개→audit. 재시작·중복 승인을 검증한다.

## 범위와 성공 기준

필수는 API·문서 ingestion·Milvus 검색·citation RAG·bounded graph·HITL·guardrail·평가·모델/비용 비교·로컬 배포·데모다. 선택 심화는 reranker·query rewrite·실제 cloud·local K8s·GPU/vLLM/LoRA다. 선택 과정으로 핵심 gate를 대신하지 않는다.

| 요구사항 | 설계/검증 |
|---|---|
| 문서·사례 수집 | 24개 합성 정책·manifest·안정 ID·version·중복 방지 |
| 근거 검색 | trusted tenant/활성 version 필터를 모든 검색 경로에 강제 |
| 답변·보류 | 허용 context citation·schema·조건 검증 / 근거 부족 종료 |
| 에이전트 | read-only tool 3개·최대 호출/retry/deadline·trace |
| 사람 검토 | durable pause/resume·reviewer 권한·중복 승인·audit |
| 평가 | W3 50개/W5 200개 synthetic·family split·원본 결과 |
| 성능 목표 | 자동응답 경로 P95 5초 목표. 실제 환경·concurrency·표본과 분리 |
| 보안 gate | 시험 범위에서 cross-tenant leak/무권한 변경/위조 citation 0 |
| 재현 | 고정 버전·clean setup·full stack·restart/restore |
| 비용 | 실usage·단가 출처/날짜·per 1K attempts/success·budget cap |



품질 수치는 기준선과 개선을 비교하고 subset·표본을 공개한다. 목표를 못 맞췄으면 root cause·trade-off·다음 실험을 쓰며 달성한 것처럼 표시하지 않는다.

## 목표 아키텍처: 현재 구현과 구분

~~~mermaid
flowchart TD
    U["사용자 / Demo"] --> API["FastAPI: schema + trusted scope"]
    API --> S["Case service / bounded workflow"]
    S --> R["Retriever: tenant + active version"]
    R --> V["Milvus + synthetic policies"]
    S --> G["LLM adapter / read-only tools"]
    G --> O["Output + citation + risk gate"]
    O --> A["Answer / insufficient evidence"]
    O --> H["HITL review + durable resume"]
    S --> P["PostgreSQL cases / reviews / audit / checkpoint"]
    R --> C["Redis scoped/versioned cache"]
    S --> T["Trace / metrics / eval reports"]
~~~

**현재 원격 코드 확인:** app/main.py는 GET /health·POST /cases/analyze·GET /cases/{case_id} 뼈대이고, in-memory ID/status만 저장한다. 기존 테스트 4개다. 실제 AI 분석·영속성·Milvus·LangGraph·HITL·Redis·배포는 앞으로 구현/검증할 범위다. 위 그림은 목표 구조다.

## 단계별 계약

**cases:** case_id, request_id, trusted tenant, text/redaction strategy, status, proposed decision, created_at, revision. **reviews:** review_id, case_id, assigned scope, reason, decision, reviewer, timestamp, revision. **evidence:** chunk_id, policy_id/version, section_id, tenant_id, source/provenance, effective_at, hash, embedding/index version.

목표 endpoint는 /search, /cases/analyze, /cases/{case_id}, /reviews/{review_id}/decision, /health/live, /health/ready다. 현재 endpoint와 신규 endpoint를 docs/contracts.md에 나눠 쓴다. W1 상태/API 계약→W2 검색 계약→W3 생성 schema→W4 graph/tool 계약→W5 승인 계약 순서로 고정한다.

## 선택과 대가

| 선택 | 이유 | 대가·재검토 |
|---|---|---|
| FastAPI | 타입 계약·API 통합·테스트 | CPU/장기 작업은 worker 경로 재검토 |
| RAG | 정책 갱신·근거 추적 | 검색 누락·권한/버전 관리 필요 |
| Milvus | 기존 계획의 vector DB 실습 | Windows/리소스 제약. small-scale 대안 비교 |
| LangGraph 제한 흐름 | 복잡한 업무·HITL 상태 추적 | durable state·retry 부작용 관리 |
| PostgreSQL | 사례/승인 일관성·공유 상태 | migration/transaction/backup 필요 |
| Redis | 반복 검색/답변 지연 감소 | tenant/version key·invalidations·PII 검토 |
| API 모델 2개 | GPU 없이 실품질/비용 비교 | rate limit·data transfer·usage 요금 의존 |
| 로컬 Compose | 재현/장애 연습 | HA/cloud 운영 성과와 구분 |



## 상태·운영·데이터 경계

RECEIVED → PROCESSING → COMPLETED / INSUFFICIENT_EVIDENCE / HUMAN_REVIEW / FAILED. HTTP 202는 접수이며 업무 완료가 아니다. HUMAN_REVIEW는 검토자 승인까지 대기하고 재시작/중복에서 같은 상태를 유지해야 한다.

공개 또는 직접 작성한 synthetic data만 사용한다. 회사 정책·스크린샷·실사용자 개인정보·내부 지표를 corpus에 넣지 않는다. 공개 자료는 링크/라이선스/사용 범위를 확인하고 필요한 발췌만 사용한다. 모델로 보낼 데이터와 logs/cache/audit 보존 항목을 따로 정의한다.

## 증거·출시 한계

교육용 단가·fixture·설계 문서는 실제 고객 성능/비용/운영 결과가 아니다. 실클라우드·GPU는 별도 접근/예산/실행 검증이 필요하다. 이 포트폴리오를 production-ready라고 단정하지 않고 검증 환경과 남은 gaps를 전달한다.

공식 근거: [AWS GenAI lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html), [Milvus Windows/환경](https://milvus.io/docs/prerequisite-docker.md), [LangGraph workflow](https://docs.langchain.com/oss/python/langgraph/workflows-agents), [interrupt](https://docs.langchain.com/oss/python/langgraph/interrupts), [OWASP 위험 분류](https://owasp.org/projects/top-10-for-large-language-model-applications).