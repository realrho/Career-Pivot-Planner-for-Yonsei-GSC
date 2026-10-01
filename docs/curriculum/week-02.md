# W2 학습 · 학습 원리·GPU 효율과 SQL·평가 데이터 설계

**기간:** 2026-10-09–2026-10-15 (Asia/Seoul) · **계획:** 22h · [Notion](https://app.notion.com/p/3ebc6f4a2c7e819fae0cd5cb69a99181) · [Jira SCRUM-7](https://realrho-1790798942092.atlassian.net/browse/SCRUM-7) · [GitHub #2](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/2)

**이번 주 통과 조건:** 학습 데이터와 평가 정답이 섞이지 않았음을 ID로 확인한다. SQL 문자열 일치와 실행 결과 일치의 차이, LoRA가 줄이는 비용과 남는 비용을 설명한다.

[전체 학습표](README.md) · [책 목차 원문](../book-toc.md) · [용어 사전](../glossary-ko-en.md) · [책/보충 범위](../book-gap-map.md)

## 1. 책 읽기와 필수 실습

**배정:** 4장 말 잘 듣는 모델 만들기 · 5장 GPU 효율적인 학습 · 6장 sLLM 학습하기

4.1–4.3은 사전 학습·SFT·보상 모델·PPO/RLHF·기각 샘플링·DPO를 목적과 필요한 데이터로 비교한다. 5.1–5.5는 데이터 타입·양자화·메모리·누적·체크포인팅·ZeRO·LoRA·QLoRA를 '무엇을 저장/학습하는가'로 읽는다. 6.1–6.3은 Text2SQL 데이터 구축→기초 모델 평가→학습→동일 기준 비교 흐름을 따라간다.

**필수 실습:** 6장 학습/평가 코드의 입출력을 표로 만들고 작은 SQLite 연습 DB에서 정답 SQL과 틀린 SQL의 결과를 비교한다. GPU가 있으면 5장 LoRA와 6장 짧은 학습 한 경로만 실행하고 실행 시간을 제한한다. GPU가 없으면 설정·메모리 계산·데이터/평가 파이프라인까지 필수로 하며 학습 실행은 미실행으로 남긴다.

책 본문은 소유한 책에서 읽는다. [공식 코드](https://github.com/onlybooks/llm)·[정오표](https://www.onlybook.co.kr/entry/llm-errata)를 확인하고 환경/모델/패키지 버전을 기록한다. 선택 GPU/멀티모달 실습의 미실행은 필수 완료와 분리한다.

## 2. 실행 순서·시간·수용 기준

| 순서 | 작업 | 계획 시간 | 완료 기준 | Jira |
|---|---|---|---|---|
| 1 | 책 4·5·6장 읽기·개념 노트 | 6h | 배정된 모든 절을 읽고 개념 관계·비교·질문을 자신의 말로 기록한다. | [SCRUM-18](https://realrho-1790798942092.atlassian.net/browse/SCRUM-18) |
| 2 | 책 필수 실습·환경/결과 기록 | 6h | 6장 학습/평가 코드의 입출력을 표로 만들고 작은 SQLite 연습 DB에서 정답 SQL과 틀린 SQL의 결과를 비교한다. GPU가 있으면 5장 LoRA와 6장 짧은 학습 한 경로만 실행하고 실행 시간을 제한한다. GPU가 없으면 설정·메모리 계산·데이터/평가 파이프라인까지 필수로 하며 학습 실행은 미실행으로 남긴다. | [SCRUM-19](https://realrho-1790798942092.atlassian.net/browse/SCRUM-19) |
| 3 | SA 보충 강의·재사용 실습 자산 만들기 | 8h | 학습 데이터와 평가 정답이 섞이지 않았음을 ID로 확인한다. SQL 문자열 일치와 실행 결과 일치의 차이, LoRA가 줄이는 비용과 남는 비용을 설명한다. | [SCRUM-20](https://realrho-1790798942092.atlassian.net/browse/SCRUM-20) |
| 4 | 퀴즈·설명·증거·다음 주 준비 검토 | 2h | 3개 퀴즈를 해설 없이 설명하고 train/dev/holdout 분리 manifest, 읽기 전용 SQL 실습, 모델 선택 비교표를 버전/실행 상태와 함께 저장한다. | [SCRUM-21](https://realrho-1790798942092.atlassian.net/browse/SCRUM-21) |

## 3. SA 보충 강의 · 개념→이유→예제→실습

### 3.1 SQL·스키마·읽기 권한

SQL, Structured Query Language(구조화 질의 언어)는 관계형 DB, Database(데이터베이스)의 데이터를 다루는 언어다. table(테이블)은 행과 열의 집합이고 schema(스키마)는 이름·타입·제약을 정한다. primary key(기본 키)는 행을 식별하며 foreign key(외래 키)는 다른 행과의 관계를 제한한다. SELECT로 읽고 WHERE로 조건을 좁힌다. 파라미터 바인딩은 값과 SQL 구문을 분리하므로 사용자 입력을 문자열 덧붙이기로 쿼리에 삽입하는 위험을 줄인다. 모델이 생성한 SQL은 임의 명령을 실행할 수 있으므로 별도의 읽기 전용 계정·허용 테이블·실행 시간 제한이 필요하다.

**작동 예시/실패 경계:** SELECT count(*) FROM cases WHERE tenant_id = ?에 값을 바인딩한다. SQL에 SELECT라는 단어가 있다는 검사만으로 안전한 질의가 되지는 않는다. SQL 생성 프로젝트와 이번 정책 검색 MVP는 서로 다른 시나리오이므로 SQL 학습 결과를 모델 성능으로 혼동하지 않는다.

**직접 해 보기:** 작은 SQLite DB에 합성 사례 5개를 넣는다. 조회·필터·JOIN 하나를 직접 작성한다. 생성 SQL의 실제 실행은 격리된 연습 DB와 읽기 권한에서만 수행한다.

### 3.2 데이터 분리와 정답 기준

train(학습 세트)는 파라미터를 학습하는 자료, dev/validation(개발/검증 세트)는 선택을 조정하는 자료, holdout/test(최종 평가 세트)는 선택을 끝낸 후 사용하는 자료다. 같은 정책 문서에서 질문을 조금 바꿔 나눠도 정보가 새어 나가는 leakage(누수)가 생길 수 있다. source_id·document_version·question_id를 저장하고 문서/시나리오 단위로 분리하는 것이 더 엄격하다. gold label(사람이 정한 평가 정답)은 정답 근거와 허용 답변/거절 조건을 함께 담아야 한다. LLM judge(언어 모델 평가자)의 점수는 사람 정답을 완전히 대신하지 못한다.

**작동 예시/실패 경계:** train 60개, dev 20개, holdout 20개는 설명용 개수다. 이번 포트폴리오에서는 개발 질문 20개와 미리 동결한 최종 질문 30개로 50개 시작이 가능하다. 같은 질문을 반복 호출해도 서로 다른 50질문을 얻은 것은 아니다.

**직접 해 보기:** 각 질문에 split·source_id·answerable·gold_evidence_ids를 붙인다. ID 중복과 문서 그룹 겹침을 검사한다. holdout의 답을 보며 프롬프트를 조정했으면 새 holdout이 필요하다고 기록한다.

### 3.3 프롬프트·RAG·미세 조정 선택

SFT, Supervised Fine-Tuning(지도 미세 조정)은 지시-응답 예시로 모델 가중치를 조정한다. PEFT, Parameter-Efficient Fine-Tuning(파라미터 효율적 미세 조정)은 학습할 파라미터를 줄이는 방법들의 범주다. LoRA, Low-Rank Adaptation(저랭크 적응)은 저랭크 행렬 업데이트를 학습한다. QLoRA, Quantized Low-Rank Adaptation(양자화 저랭크 적응)은 양자화된 기반 모델과 저랭크 학습을 결합한다. 갱신되는 고객 정책 지식은 RAG로 외부 근거를 공급하는 것이 관리에 유리하고, 답변 형식이나 반복되는 업무 행동은 프롬프트/SFT가 도움이 될 수 있다. 어떤 방법도 권한 확인과 데이터 갱신을 대신하지 않는다.

**작동 예시/실패 경계:** 정책이 매주 바뀌면 매주 미세 조정하기 전에 검색 문서 버전을 바꾸는 경로를 검토한다. 형식 오류가 많으면 구조화 출력·검증·예시 프롬프트부터 비교한다. SFT 데이터가 부족하거나 평가 기준이 없으면 학습을 서두르지 않는다.

**직접 해 보기:** 모델 선택표에 문제 유형·데이터량·갱신 주기·보안 경계·비용·검증 기준을 쓴다. API 모델 1개와 자체 서빙 대안 1개의 장단점을 비교하되 이번 MVP는 한 경로만 선택한다.

### 3.4 GPU 메모리를 예산으로 읽기

GPU, Graphics Processing Unit(그래픽 처리 장치)는 많은 수치 연산을 병렬로 처리하는 장치다. VRAM, Video Random Access Memory(그래픽 메모리)에는 가중치뿐 아니라 activation(중간 활성값), gradient(기울기), optimizer state(최적화기 상태), 캐시 등이 저장된다. 7B 모델의 16비트 가중치는 단순 계산으로 약 14GB(decimal)지만 학습 총 메모리는 더 크다. 4비트 가중치의 단순 크기 약 3.5GB도 메타데이터·활성값·연산 버퍼를 포함하지 않는다. gradient accumulation(기울기 누적)은 여러 작은 배치의 기울기를 모으며 gradient checkpointing(기울기 체크포인팅)은 중간값을 덜 저장하고 다시 계산한다. 처리 시간과 메모리의 교환이다.

**작동 예시/실패 경계:** 마이크로 배치 2, 누적 8, 데이터 병렬 장치 1이면 실효 배치 16이다. 이를 실측 GPU 사용량이라고 쓰지 않는다. LoRA도 기반 모델의 forward/backward 경로와 활성값 메모리가 남는다.

**직접 해 보기:** 파라미터 수×비트/8을 계산하고 단위를 GB/GiB로 구분한다. 선택 GPU의 메모리 예산표에 미측정 항목을 남긴다. GPU 실습은 장치·정밀도·배치·토큰 길이·시간·메모리 peak를 기록한다.

## 4. 실행 가능한 기초 계약 실습

아래는 핵심 규칙을 작게 분리해 CPU에서 확인하는 접근이다. 라이브러리 설치나 실제 모델 호출 없이 개념을 검증한다. 프로젝트 통합 구현과 증거 수준을 구분한다.

실행: `python labs/week-02/contract_demo.py` (저장소 루트).

```python
"""W2: 평가 분리의 ID 계약을 검사한다. 모델 학습은 수행하지 않는다."""
def validate_splits(splits: dict[str, set[str]]) -> int:
    """세 데이터 분할에 중복 ID가 없는지 검사한다.

    Args:
        splits: train/dev/holdout 이름과 각 분할의 ID 집합.
    Returns:
        전체 고유 ID 개수.
    Raises:
        ValueError: 필수 분할이 없거나 비어 있거나 ID가 중복된 경우.
    """
    if set(splits) != {"train", "dev", "holdout"}:
        raise ValueError("three splits required")
    seen: set[str] = set()
    for name, identifiers in splits.items():
        if not identifiers or seen.intersection(identifiers):
            raise ValueError(f"empty or overlapping split: {name}")
        seen.update(identifiers)
    return len(seen)

assert validate_splits({"train": {"a"}, "dev": {"b"}, "holdout": {"c"}}) == 3
try:
    validate_splits({"train": {"a"}, "dev": {"a"}, "holdout": {"c"}})
except ValueError:
    pass
else:
    raise AssertionError("leakage accepted")
# ID 분리만으로 문서/시나리오 의미 중복까지 검증한 것은 아니다.
print("W2 split-ID contract: passed")
```

**복잡도/병목:** 전체 ID 수 n에 시간/공간 O(n). 문서 내용/의미 누수는 별도 확인해야 한다.

## 5. 학습 중 만들 재사용 자산 · 상세 작업

아래 app/data/deployment 파일은 **앞으로 작성할 예정 경로**다. 현재 구현된 것으로 읽지 않는다. 작은 계약 실습을 실제 저장소/모델 경로로 확장하는 작업이다.

### 5.1 학습·평가 manifest 작성

`docs/data-manifest.md` 또는 JSON에 question_id·source_id·split·expected_result를 넣는다. Text2SQL 연습 자료와 정책검색 포트폴리오 자료를 구분한다. ID와 문서 그룹의 겹침을 검사한다.

### 5.2 SQL 직접 실행해 정답 기준 이해

`labs/week-02/`에 작은 SQLite DB 생성·조회 코드를 둔다. SELECT·WHERE·JOIN을 직접 작성하고 같은 결과를 내는 서로 다른 SQL을 비교한다. 모델이 생성한 SQL을 실제 업무 DB에 바로 실행하지 않는다.

### 5.3 선택 GPU 학습을 별도 기록

GPU가 있으면 공식 5–6장의 한 경로를 작은 데이터로 실행한다. base model/revision·LoRA 설정·토큰 길이·배치·시간·peak 메모리·기초/학습 후 평가를 남긴다. 실행하지 않으면 GPU_NOT_RUN으로 기록한다.

### 5.4 모델 선택 표 초안

프롬프트·RAG·SFT가 각각 해결하는 문제와 갱신·권한 한계를 비교한다. MVP 모델은 한 경로만 우선 선택하고 호출 계약의 입력·출력·오류를 적는다.

### 5.5 다음 주로 넘길 자산

정답 manifest·SQL 결과·메모리 계산·모델 선택표를 저장한다. 학습 코드 읽기 완료와 실제 파라미터 학습 완료는 서로 다른 체크박스로 둔다.

**다음 통합에 넘길 것:** train/dev/holdout 분리 manifest, 읽기 전용 SQL 실습, 모델 선택 비교표

## 6. 이해 확인 · 해설을 보기 전에 설명하기

**Q1. 학습 정확도가 올랐으면 고객 문제를 해결했는가?**

<details>
<summary>해설</summary>

분리된 평가 데이터와 실제 업무 조건에서 품질·안전·비용을 확인해야 한다.

</details>

**Q2. 4비트 모델이 3.5GB면 4GB GPU에서 학습 가능한가?**

<details>
<summary>해설</summary>

가중치 외 메모리가 있어 단순 계산으로 판단할 수 없다. 지원 연산·활성값·최적화기와 실제 환경을 확인한다.

</details>

**Q3. LLM이 만든 SQL에 SELECT만 허용하면 충분한가?**

<details>
<summary>해설</summary>

읽기 전용 권한·허용 스키마·시간/행 제한·파라미터 처리 등 여러 경계가 필요하다.

</details>

## 7. 공식 자료 · 읽을 범위

- [SQL 트랜잭션](https://www.postgresql.org/docs/current/tutorial-transactions.html) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.
- [LoRA 원 논문](https://arxiv.org/abs/2106.09685) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.
- [Hugging Face PEFT](https://huggingface.co/docs/peft/index) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.

## 증거와 완료 상태

학습 노트에는 읽은 절·자신의 설명·실습 명령·Python/패키지/장치·데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 문서/fixture/실제DB·모델/클라우드·GPU의 수준을 구분한다. 자료 작성만으로 본인의 학습 또는 서비스 제작을 완료 처리하지 않는다. 막히면 증상·시도·다음 행동과 일정 영향을 남긴다.
