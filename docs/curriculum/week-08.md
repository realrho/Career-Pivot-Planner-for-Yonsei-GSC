# W8. 설계 판단을 증거와 영어 데모로 전달하기

> 고객 문제에서 설계 선택·측정·한계까지 10분 안에 설명하는 포트폴리오로 완성한다.

2026-11-19 → 2026-11-25 · 총 22h (주당 계획 가정)

[Jira SCRUM-13](https://realrho-1790798942092.atlassian.net/browse/SCRUM-13) · [GitHub #8](https://github.com/realrho/test/issues/8) · [W7 선행 과정](https://app.notion.com/p/3ebc6f4a2c7e81909714e0d4739b893f)

## 학습 목표와 시작 조건

**기술:** Customer narrative · Architecture trade-offs · Evidence audit · Demo · Interview · Internal transfer

**시작 조건:** W1~W7 증거·ADR·평가·benchmark·운영 검증. 완료하지 못한 항목은 계획/제약으로 표시하고 포장으로 숨기지 않는다.

이 페이지는 학습 교재와 앞으로 구현할 작업이다. 문서가 작성된 것을 서비스 구현/평가 완료로 표시하지 않는다. 학습은 아래 4개 강의→손 실습→코드 실습→빌드→퀴즈→증거 제출 순서로 진행한다.

## 이번 주 시간표

- D1 3h: claim-evidence audit·미완료 정리
- D2 3h: 영문 README·architecture/ADR 연결
- D3 3h: 평가/비용/안전 보고서 일관성
- D4 3h: 10-slide outline·영어 script
- D5 4h: fresh setup·3흐름·5분 데모 측정
- D6 4h: 모의면접·3분 pitch·정리
- D7 2h: 내부 이동 자료/skill gap·버퍼

## 개념 강의

### 1. SA의 설명은 기술 목록보다 고객의 의사결정에 맞춰야 한다

대상 청중을 고객 의사결정자·개발자·면접관으로 나눈다. 고객은 업무 변화·위험·비용을, 개발자는 계약·실행·장애 처리를, 면접관은 선택 이유·대안·기여를 확인한다. 하나의 10분 설명 안에서도 문제→요구사항→선택→측정→추천의 순서를 유지한다.

예: ‘LangGraph·Milvus·Redis를 사용했다’보다 ‘정책 변경과 출처 확인이 필요해 RAG를 선택하고, 복잡한 사례에만 제한 도구 흐름을 쓰며, 고위험은 사람이 검토하게 했다’가 판단을 보여 준다. 각 기술 선택 뒤에 이점뿐 아니라 비용·제약·언제 바꿀지를 한 문장으로 설명한다.

8주 목표는 모든 SA 역량 완성이 아니라 end-to-end 설계·구현·평가 판단의 증거를 만드는 것이다. 실제 BytePlus 업무·면접 기대는 현직자 피드백으로 갱신한다. 자신의 TikTok Trust & Safety 업무 배경과 AI/ML 공부를 고객 문제 이해·risk design 역량으로 연결하되 회사 내부 자료를 쓰지 않는다.

### 2. Evidence audit: 숫자·주장·파일을 1대1로 연결한다

각 claim에 artifact path·commit SHA·run_id·dataset/model/prompt/index version·환경·날짜를 연결한다. 예: ‘P95 개선’에는 baseline/variant raw result와 같은 조건을, ‘HITL 복구’에는 restart/resume 테스트·audit를 연결한다. 목표·교육용 가정·fixture·real measurement·미실행을 표시한다.

주차 체크박스를 문서를 썼다는 이유로 닫지 않는다. 서비스 구현/시험 완료는 해당 AC 증거가 있어야 Done이다. 기능별 현재 상태 표에는 Implemented/Fixture-validated/Real-validated/Planned/Blocked와 근거를 쓴다. 실모델을 쓰지 않은 stub은 contract validation까지만 주장한다.

핵심 7개 산출물은 실행 가능한 bounded copilot, 고객 요구사항, 아키텍처/ADR, 평가 보고서, 모델·비용 benchmark, guardrail/실패 분석, 5분 영어 데모다. runbook·data card·영문 README가 재현을 돕는다. 문서 분량보다 다른 사람이 주장과 실행을 검증할 수 있는지가 우선이다.

### 3. Demo: 정상만 보여 주면 설계 역량이 드러나지 않는다

5분 데모는 0:00~0:40 고객 문제/제약, 0:40~1:20 구조/선택, 1:20~2:20 정상 답변+source/version, 2:20~3:00 근거 부족, 3:00~4:00 고위험→review→권한 승인, 4:00~4:40 품질/latency/cost, 4:40~5:00 한계와 다음 단계로 구성한다.

데모 데이터와 환경을 고정하고 real model/network 장애가 나면 어떻게 보여 줄지 준비한다. 저장된 영상/trace를 fallback으로 사용하면 녹화·fixture·이전 실행임을 명확히 표시한다. 실패를 성공 화면처럼 바꾸지 않는다. 새 checkout에서 README만 보고 실행하는 사람 관점으로 재현한다.

영어는 유창한 기술 용어보다 짧은 판단 문장부터 연습한다. ‘I chose retrieval because the policy changes frequently and reviewers need evidence.’ ‘This benchmark uses synthetic cases, so I would validate customer traffic before rollout.’ 같은 문장으로 이유·범위를 분리한다. 읽는 스크립트와 실제 실행 시간을 따로 확인한다.

### 4. Interview·handoff: 반론에 대답할 수 있어야 한다

면접 답변은 상황→요구사항→선택지→결정→근거→한계→재검토 조건 순서다. ‘왜 fine-tuning이 아닌 RAG?’, ‘왜 agent가 필요한가?’, ‘tenant leak은 어디서 막는가?’, ‘Redis가 죽으면?’, ‘P95가 10초면?’, ‘10배 트래픽이면?’에 현재 증거와 다음 실험을 연결한다.

고객이 데이터 외부 전송을 허용하지 않으면 provider 선택과 region·self-hosted cost를 다시 검토한다. 작은 corpus면 더 단순한 DB 검색이 충분할 수 있다. traffic이 늘면 worker queue·capacity·index·rate limit을 측정하며, 언제나 Kubernetes가 첫 답은 아니다. 자신의 선택을 절대 규칙처럼 말하지 않는다.

내부 이동 활동은 개인 계획 트랙이다. 현직자에게 물을 질문·리뷰 요청 초안·받은 피드백·반영한 ADR를 남긴다. 연락 대상과 메시지 전송은 사용자가 직접 수행한다. 포트폴리오 완성과 내부 이동/면접 확정은 서로 다른 상태다. 마지막 페이지에 향후 4주 skill gap과 priority를 기록한다.



## 따라 하는 실습과 예상 결과

fresh checkout로 설치→unit/contract→fixture integration→real integration(접근 가능할 때)→3개 데모→restart 검증을 따라간다. claim-evidence matrix에 모든 숫자를 넣고 링크가 실제 파일/실행에 연결되는지 확인한다. 미완료 항목을 삭제하지 말고 제한/추가 단계로 남긴다.

10-slide outline: 1 고객 문제, 2 FR/NFR, 3 architecture, 4 RAG/version/access, 5 bounded agent/tools, 6 HITL/guardrails, 7 evaluation/failure, 8 latency/cost, 9 deployment/runbook, 10 recommendation/limits. 슬라이드 제작은 이번 학습 산출물이며 지금 계획 정리로 deck/녹화가 완성됐다고 표시하지 않는다.

모의면접 10질문에 60~90초 답하고 자신이 결정한 trade-off 3개를 영어 3분 pitch로 녹음한다. 설명 시간·어려웠던 질문·증거 부족을 기록한 후 마지막 정리를 한다.

## 코드로 확인하는 핵심 원리

포트폴리오 claim 점검을 작은 함수로 연습한다. 링크가 있다는 것과 실제 증거라는 것은 다르므로 내용 확인을 추가한다.

```python
def missing_evidence(claims: dict[str, str | None]) -> list[str]:
    """아직 증거 링크가 없는 claim 이름을 반환한다.

    Args:
        claims: 주장 이름과 증거 경로/URL 매핑.
    Returns:
        빈 evidence 값을 가진 주장 이름 목록.
    Raises:
        없음. URL 접근 가능성/실행 진위는 별도 검증한다.
    """
    # 경로 문자열 존재만 검사한다. 실제 증거 내용은 사람이 확인한다.
    return [claim for claim, evidence in claims.items()
            if not evidence or not evidence.strip()]

assert missing_evidence({'fixture tests': 'reports/run.json',
                         'real GPU benchmark': None}) == ['real GPU benchmark']
```

**복잡도와 병목:** n개 claim에 시간 O(n+문자열 총 길이), 출력 공간 O(m). 포트폴리오 병목은 코드 계산보다 접근 가능한 real 실행 증거·재현 환경·설명 품질이다.

## 프로젝트에서 빌드할 부분

### W8.1 7개 산출물 claim-evidence audit·미완료 정리 · 5h

**왜 필요한가:** 다음 구현을 판단할 계약·데이터·환경을 먼저 확정한다.

**수정/작성 위치:** docs/portfolio/evidence-matrix.md, docs/evidence/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W7 완료 gate가 선행한다.

**완료 조건:** 각 주장에 path/commit/run/config·실제/fixture/목표·한계를 연결하고 증거 없는 항목은 Planned/Blocked로 표시한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W8.2 영문 README·architecture·평가/비용/안전 문서 정리 · 6h

**왜 필요한가:** 개념을 실제 핵심 경로에 연결해 다음 검증의 기준선을 만든다.

**수정/작성 위치:** README.md, docs/architecture.md, docs/evaluation.md, docs/benchmark.md

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W8.1의 산출물이 선행한다.

**완료 조건:** fresh setup 명령·현재 기능·설계 trade-off·측정/가정을 일관되게 설명하고 모든 참조 링크를 검증한다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W8.3 10-slide 자료·영어 5분 데모·재현 검증 · 6h

**왜 필요한가:** 실패·권한·복구 경계를 구현해 정상 시연만으로 놓치는 문제를 찾는다.

**수정/작성 위치:** docs/portfolio/deck-outline.md, docs/portfolio/demo-script.md, reports/w08/

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W8.2의 산출물이 선행한다.

**완료 조건:** 정상/근거부족/HITL 3흐름과 실제 5분 시연·fallback 표시·fresh checkout 결과를 남긴다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.

### W8.4 면접 Q&A·3분 pitch·이동 준비·다음 skill gap · 5h

**왜 필요한가:** 검증 결과를 설계 결정과 다른 사람이 확인할 증거로 바꾼다.

**수정/작성 위치:** docs/portfolio/interview.md, docs/portfolio/transfer.md

**작업 순서:** 계약/예상 결과 작성 → 최소 구현 → 정상과 실패 경로 실행 → actual 결과 저장 → 문서/ADR 연결. W8.3의 산출물이 선행한다.

**완료 조건:** 10질문 답변·trade-off 3개·3분 설명·현직자 feedback 반영·후속 skill gap을 정리한다. 이동/채용 확정은 별도 상태로 둔다.

**제출 증거:** PR/commit URL, run ID와 config, 기대/실제 결과, 실패/한계. 근거가 없으면 해당 구현은 Planned/Blocked로 둔다.



## 주차 완료 기준

- [ ] 실행 copilot와 7개 핵심 산출물에 실제 증거 연결
- [ ] fresh setup·3흐름 데모·실제 영어 5분 시연 결과
- [ ] README/Notion/Jira/GitHub의 완료 상태·수치가 일치
- [ ] 10분 설계 설명·3분 pitch·10개 면접 Q&A·후속 gap 정리

## 이해 확인 퀴즈

**Q1. 학습 문서가 완성됐으면 8주 구현 이슈를 Done으로 바꿀까?**

<details>
<summary>해설 확인</summary>

아니다. 이슈별 실제 구현/측정 AC와 evidence를 충족해야 한다.

</details>

**Q2. 가장 높은 정확도 모델을 항상 추천해야 하나?**

<details>
<summary>해설 확인</summary>

품질 하한·지연·비용·privacy·운영 조건을 함께 보며 실제 비교 결과로 추천한다.

</details>

**Q3. 데모 네트워크 장애 때 녹화본을 live라고 보여 줘도 되나?**

<details>
<summary>해설 확인</summary>

녹화/fixture/이전 실행임을 표시하고 live 실패와 fallback을 구분한다.

</details>



## 면접에서 설명할 한 문장

“이번 주에는 고객 문제에서 설계 선택·측정·한계까지 10분 안에 설명하는 포트폴리오로 완성한다. 이를 확인한 증거는 ___이며, 아직 확인하지 못한 범위는 ___입니다.”

기술 이름을 외우기보다 선택 이유·실패 경우·측정 조건·대안을 자기 말로 설명한다.

## 공식 자료: 읽을 범위와 사용법

- [AWS GenAI 검토 질문](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [GitHub Actions/검증](https://docs.github.com/en/actions/get-started/understand-github-actions) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.
- [Git 변경·증거 관리](https://git-scm.com/book/en/v2) — 해당 주차 강의와 대응하는 절만 읽고, 예제를 자기 corpus/API에 적용한다.

문서 URL은 2026-10-01 확인. 설치/API 세부는 실습 시 사용 버전의 공식 문서를 다시 확인한다. 본 강의 설명·실습·프로젝트 판단 기준은 이 포트폴리오를 위해 작성한 교육 내용이다.

## 선택 심화·환경이 막힐 때

더 긴 영문 기술 보고서·추가 cloud/GPU 실험은 후속 4주 과정. 증거가 없는 기능을 새로 붙이는 것보다 기존 결과 설명과 재현을 우선한다.

핵심 gate가 안 되면 Jira에 실패 증상·환경·시도·다음 행동을 기록한다. fixture로 계약 학습을 이어 갈 수 있지만 real DB/model/cloud/GPU 완료로 바꾸지 않는다.


## Jira 실행 작업 바로가기

| 순서 | 작업·시간 | 선행 |
|---|---|---|
| 8.1 | [SCRUM-42](https://realrho-1790798942092.atlassian.net/browse/SCRUM-42) · 7개 산출물 claim-evidence audit·미완료 정리 · 5h | SCRUM-12 |
| 8.2 | [SCRUM-43](https://realrho-1790798942092.atlassian.net/browse/SCRUM-43) · 영문 README·architecture·평가/비용/안전 문서 정리 · 6h | SCRUM-42 |
| 8.3 | [SCRUM-44](https://realrho-1790798942092.atlassian.net/browse/SCRUM-44) · 10-slide 자료·영어 5분 데모·재현 검증 · 6h | SCRUM-43 |
| 8.4 | [SCRUM-45](https://realrho-1790798942092.atlassian.net/browse/SCRUM-45) · 면접 Q&A·3분 pitch·이동 준비·다음 skill gap · 5h | SCRUM-44 |

## 구현 레시피 · 주장과 근거를 묶는 포트폴리오

### Claim-evidence matrix

| 주장 | 필요한 증거 | 없는 경우 |
|---|---|---|
| 검색 개선 | 같은 split/config의 raw retrieval 결과·실패 분석 | 가설/다음 실험 |
| 안전한 검토 | 무권한/중복/restart/resume 테스트 | gap/Blocked |
| P95 개선 | 동일 환경·표본·concurrency·cold/warm 결과 | 목표/가정 |
| 비용 절감 | 실제 usage·단가 출처/날짜·실패/검토량 | 예시 계산 |
| 운영 가능 | clean setup·장애/restore·runbook | local 범위만 표시 |

1. 모든 주차 Evidence를 모아 각 AC가 어떤 commit/run을 참조하는지 확인한다.
2. 영어 README에 고객 문제·current behavior·실행 명령·target architecture·results/limits를 순서대로 쓴다.
3. architecture 문서의 current/target 그림과 상태를 비교하고 stale diagram을 고친다.
4. 평가·benchmark·guardrail 보고서의 dataset/model/index version을 일치시킨다.
5. 10-slide와 demo는 같은 실제 3개 시나리오·측정 조건을 사용한다.
6. fresh checkout에서 다른 사람 관점으로 실행하고 실제 발표 시간을 기록한다.
7. fixture/녹화 fallback을 표시하고 10개 반론 질문에 근거와 한계로 답한다.
8. 기존 Internal Transfer 기록에 ‘받은 조언→바꾼 결정→증거’를 남긴다.

### 영어 답변 틀

“I chose ___ because the customer requires ___. Compared with ___, this improves ___ but adds ___. I verified it using ___ under ___. I have not yet validated ___. I would revisit this choice when ___.”

3분 pitch는 고객 문제 30초·구조 60초·결과 60초·한계/다음 단계 30초로 연습한다. 대답할 수 없는 질문은 그럴듯한 숫자로 채우지 말고 추가 검증 계획을 제시한다.
