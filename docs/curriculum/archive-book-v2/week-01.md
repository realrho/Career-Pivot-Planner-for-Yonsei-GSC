# W1 학습 · LLM 기초를 이해하고 Python·Git·API 계약 세우기

**기간:** 2026-10-02–2026-10-08 (Asia/Seoul) · **계획:** 22h · [Notion](https://app.notion.com/p/3ebc6f4a2c7e817e9b59e2ed884085ed) · [GitHub #1](https://github.com/realrho/Enterprise-AI-Knowledge-Risk-Copilot/issues/1)

**이번 주 통과 조건:** 빈 입력·공백 입력을 거부하고 정상 입력을 동일하게 정규화한다. 타입 힌트와 실제 검증의 차이를 설명하며 202 접수와 분석 완료를 구분한다.

[전체 학습표](README.md) · [책 목차 원문](../book-toc.md) · [용어 사전](../glossary-ko-en.md) · [책/보충 범위](../book-gap-map.md)

## 1. 책 읽기와 필수 실습

**배정:** 1장 LLM 지도 · 2장 트랜스포머 아키텍처 · 3장 허깅페이스 트랜스포머

1.1–1.4로 임베딩·언어 모델·sLLM·RAG의 관계를 그린다. 2.1–2.8은 토큰→임베딩→위치 정보→Q/K/V 어텐션→출력 순으로 설명한다. 인코더·디코더·인과적/마스크 학습을 구분한다. 3.1–3.5에서 모델/토크나이저/데이터셋의 역할과 학습/추론 경로를 따라간다. 부록 A.1–A.3은 토큰 발급과 비밀 관리까지 함께 읽는다.

**필수 실습:** 공식 3장 노트북에서 토크나이저 예제와 작은 모델의 추론 한 경로를 실행한다. 문장 3개의 토큰 ID·길이·모델 revision을 저장한다. torch 학습 코드는 forward→loss→backward→optimizer 순서를 주석으로 설명한다. 전체 모델 학습·공개 업로드는 선택이다.

책 본문은 소유한 책에서 읽는다. [공식 코드](https://github.com/onlybooks/llm)·[정오표](https://www.onlybook.co.kr/entry/llm-errata)를 확인하고 환경/모델/패키지 버전을 기록한다. 선택 GPU/멀티모달 실습의 미실행은 필수 완료와 분리한다.

## 2. 실행 순서·시간·수용 기준

| 순서 | 작업 | 계획 시간 | 완료 기준 | 작업 ID |
|---|---|---|---|---|
| 1 | 책 1·2·3장 읽기·개념 노트 | 6h | 배정된 모든 절을 읽고 개념 관계·비교·질문을 자신의 말로 기록한다. | W1.1 |
| 2 | 책 필수 실습·환경/결과 기록 | 6h | 공식 3장 노트북에서 토크나이저 예제와 작은 모델의 추론 한 경로를 실행한다. 문장 3개의 토큰 ID·길이·모델 revision을 저장한다. torch 학습 코드는 forward→loss→backward→optimizer 순서를 주석으로 설명한다. 전체 모델 학습·공개 업로드는 선택이다. | W1.2 |
| 3 | SA 보충 강의·재사용 실습 자산 만들기 | 8h | 빈 입력·공백 입력을 거부하고 정상 입력을 동일하게 정규화한다. 타입 힌트와 실제 검증의 차이를 설명하며 202 접수와 분석 완료를 구분한다. | W1.3 |
| 4 | 퀴즈·설명·증거·다음 주 준비 검토 | 2h | 3개 퀴즈를 해설 없이 설명하고 정규화/입력 검증 함수, 요청·응답 계약표, 오류 사례, 환경 잠금 기록를 버전/실행 상태와 함께 저장한다. | W1.4 |

## 3. SA 보충 강의 · 개념→이유→예제→실습

### 3.1 Python 실행 환경과 데이터 흐름

Python(파이썬)은 프로그램을 실행하는 언어이고, interpreter(인터프리터)는 소스의 동작을 실행하는 런타임이다. virtual environment(가상 환경)는 프로젝트별 설치 패키지 공간이다. 같은 파일이라도 다른 python.exe로 실행하면 import 결과가 달라질 수 있다. 설치 명령을 현재 인터프리터의 `python -m pip`로 실행하고 Python·패키지 버전을 기록하는 이유다. 리스트는 순서 있는 여러 값, 딕셔너리는 키로 값을 찾는 구조다. 함수는 입력을 받아 결과를 반환하는 단위이며 예외는 정상 처리와 실패를 구분하는 경로다. 파일→문자열→검증된 객체→서비스 함수→JSON 응답으로 값이 바뀌는 위치를 그려 보자.

**작동 예시/실패 경계:** 문자열 '  환불 규정  '을 strip 후 처리한다. None·공백·너무 긴 문자열은 각각 오류로 분류한다. `text: str`라는 주석만으로 None 입력이 자동 거부되지 않는다. 프레임워크의 검증 또는 명시적인 함수 검사가 필요하다.

**직접 해 보기:** 실행 Python 경로·버전 출력→가상 환경 생성→같은 Python으로 패키지 설치→정규화 함수를 직접 호출→정상/실패 입력을 기록한다.

### 3.2 Git으로 변경의 근거 남기기

Git(깃)은 파일 변경 이력을 저장하는 버전 관리 도구다. working tree(작업 디렉터리)에서 수정하고 staging area(스테이징 영역)에 커밋할 변경을 고른 뒤 commit(커밋)으로 스냅샷을 만든다. branch(브랜치)는 커밋을 가리키는 이동 가능한 이름이다. GitHub(깃허브)는 원격 저장소와 협업 서비스를 제공한다. PR, Pull Request(풀 리퀘스트, 변경 병합 요청)는 변경 이유·검증·검토를 한곳에 모으는 절차다. 실행한 노트북에 비밀 토큰이나 사용자 데이터가 남으면 이력에도 들어갈 수 있으므로 커밋 전 diff(변경 비교)를 읽는다.

**작동 예시/실패 경계:** 좋은 커밋은 '입력 공백 제거 후 길이 검증'처럼 한 목적을 표현한다. requirements의 범위만 저장하면 다음 설치가 같다고 보장하지 못하므로 검증한 정확 버전 또는 lockfile(의존성 잠금 파일)도 남긴다.

**직접 해 보기:** `git status`→작은 수정→`git diff`→테스트→`git add`→`git commit`의 순서를 설명한다. 실습 브랜치는 codex/w01-api-contract로 만들고 다른 저장소의 이력을 섞지 않는다.

### 3.3 HTTP·API·JSON과 FastAPI 경계

API, Application Programming Interface(애플리케이션 프로그래밍 인터페이스)는 프로그램 간 사용 규약이다. HTTP, Hypertext Transfer Protocol(하이퍼텍스트 전송 프로토콜)은 요청·응답 메시지 규칙이다. method(메서드)는 동작, path(경로)는 대상, headers(헤더)는 메타데이터, body(본문)는 입력을 담는다. JSON, JavaScript Object Notation(자바스크립트 객체 표기법)은 텍스트 데이터 형식이다. FastAPI(패스트API)는 Python 웹 API 프레임워크라는 제품 이름이다. 입력·출력 schema(스키마, 데이터 구조 규칙)를 명시하면 호출자가 내부 구현을 몰라도 사용할 수 있다. 200은 요청 성공, 202는 접수, 404는 대상 없음, 422는 입력 계약 위반에 쓴다. 202 이후 실제 작업을 수행하고 상태를 갱신하는 경로가 없으면 분석은 끝나지 않는다.

**작동 예시/실패 경계:** POST /cases/analyze가 case_id와 received를 반환해도 evidence나 decision이 없으면 AI 분석 성공이라는 표현을 쓰지 않는다. GET /health는 프로세스 응답 여부이며 데이터베이스 준비까지 증명하지 않는다.

**직접 해 보기:** 기존 app/main.py와 tests/test_health.py를 읽고 경로·본문·응답·오류 표를 작성한다. 정상 요청 1개와 실패 요청 3개를 직접 검증한다. 기존 네 개 테스트를 실행한 환경도 기록한다.

### 3.4 계약·의존성·테스트의 역할

contract(계약)는 입력, 출력, 오류, 부작용에 관한 합의다. dependency(의존성)는 함수가 필요로 하는 외부 자원이다. API 계층은 HTTP 변환, service(서비스) 계층은 업무 규칙, adapter(어댑터)는 모델/DB 제품 호출을 맡으면 교체 이유가 선명해진다. KISS, Keep It Simple, Stupid(가능한 단순하게 유지), DRY, Don't Repeat Yourself(중복을 반복하지 않기)는 작고 명확한 설계를 위한 원칙이다. 테스트는 구현을 다시 적기보다 깨지면 고객 행동이 달라지는 경계를 확인해야 한다. 이번 범위에서는 입력 검증, 오류 응답, 상태 의미가 핵심이다.

**작동 예시/실패 경계:** 모델을 바꿔도 AnalyzeResult의 필드와 실패 의미가 유지되어야 한다. 어댑터를 여럿 만들기 전에 한 모델 경로로 계약을 검증하고 두 번째 공급자는 필요할 때 추가한다.

**직접 해 보기:** docs/contracts.md의 향후 계약에 tenant가 본문에서 권한으로 신뢰되지 않는다는 조건을 쓴다. 요청/결과 예제와 실패 이유를 짝지어 저장한다.

## 4. 실행 가능한 기초 계약 실습

아래는 핵심 규칙을 작게 분리해 CPU에서 확인하는 접근이다. 라이브러리 설치나 실제 모델 호출 없이 개념을 검증한다. 프로젝트 통합 구현과 증거 수준을 구분한다.

실행: `python labs/week-01/contract_demo.py` (저장소 루트).

```python
"""W1: 입력 계약을 검증하는 CPU/표준 라이브러리 실습."""
def normalize_text(value: object, max_length: int = 2000) -> str:
    """공백을 제거하고 입력 계약을 검사한다.

    Args:
        value: 호출자가 전달한 원본 값.
        max_length: 허용할 정규화 문자열의 최대 문자 수.
    Returns:
        앞뒤 공백이 제거된 비어 있지 않은 문자열.
    Raises:
        TypeError: 문자열이 아닌 입력인 경우.
        ValueError: 길이 한도가 양수가 아니거나 입력 길이가 범위 밖인 경우.
    """
    if max_length < 1:
        raise ValueError("max_length must be positive")
    if not isinstance(value, str):
        raise TypeError("text must be a string")
    normalized = value.strip()  # 정규화 후 검사해야 공백만 있는 입력도 거부한다.
    if not 1 <= len(normalized) <= max_length:
        raise ValueError("invalid text length")
    return normalized

assert normalize_text("  환불 규정  ") == "환불 규정"
for invalid in ["   ", None]:
    try:
        normalize_text(invalid)
    except (TypeError, ValueError):
        pass
    else:
        raise AssertionError("invalid input accepted")
print("W1 input contract: passed")
```

**복잡도/병목:** 길이 n 입력의 시간/공간 O(n). 웹 프레임워크·HTTP 동작은 별도 실습이다.

## 5. 학습 중 만들 재사용 자산 · 상세 작업

아래 app/data/deployment 파일은 **앞으로 작성할 예정 경로**다. 현재 구현된 것으로 읽지 않는다. 작은 계약 실습을 실제 저장소/모델 경로로 확장하는 작업이다.

### 5.1 환경을 분리하고 첫 실행 확인

책 노트북은 공식 저장소의 환경·정오표 기준으로 별도 실행한다. 프로젝트는 별도 .venv에서 기존 API의 네 테스트를 실행한다. 책 의존성과 최신 프로젝트 의존성을 한 환경에서 무조건 합치지 않는다. 버전·장치·명령·실패 메시지를 `docs/study/week-01-evidence.md`에 남긴다.

### 5.2 입력 모델과 API 표 작성

예정 `app/schemas.py`에 text 길이·공백·선택 필드를 정의하고 `docs/contracts.md`에 접수·조회·오류 응답을 쓴다. 기존 경로를 바꾸기 전 계약을 고정한다. case_id·request_id·status를 서로 다른 값으로 설명한다.

### 5.3 서비스 경계를 작은 함수로 분리

정규화→검증→서비스 호출→HTTP 변환 순으로 추적한다. 예정 `app/services/cases.py`는 업무 행동, API route는 HTTP 변환을 맡는다. 현재 딕셔너리 저장을 PostgreSQL 구현 완료로 표시하지 않는다.

### 5.4 실패와 결과 확인

정상 문장·공백·None·길이 초과·없는 ID를 각각 검증한다. 202 접수와 실제 처리 완료의 차이를 적고 /health와 미래 readiness의 경계를 남긴다.

### 5.5 재사용 결과 정리

정규화 함수와 요청·응답 예제를 `labs/week-01/`에 보관한다. 계약·환경·실제 테스트 결과가 W9 통합의 입력이다. 제공된 표준 라이브러리 코드는 별도의 CPU 계약 연습이다.

**다음 통합에 넘길 것:** 정규화/입력 검증 함수, 요청·응답 계약표, 오류 사례, 환경 잠금 기록

## 6. 이해 확인 · 해설을 보기 전에 설명하기

**Q1. 타입 힌트가 API 입력을 자동 검증하는가?**

<details>
<summary>해설</summary>

일반 Python 타입 힌트는 강제 검증이 아니다. 명시적 검사나 FastAPI/Pydantic 검증 경로가 필요하다.

</details>

**Q2. 202와 received를 분석 완료로 보고할 수 있는가?**

<details>
<summary>해설</summary>

접수 증거다. 실제 분석 결과와 완료 상태를 따로 확인해야 한다.

</details>

**Q3. 모델과 토크나이저를 임의로 다른 revision으로 섞어도 되는가?**

<details>
<summary>해설</summary>

토큰 ID의 의미와 모델 입력 계약이 달라질 수 있으므로 호환 모델·토크나이저 revision을 기록한다.

</details>

## 7. 공식 자료 · 읽을 범위

- [Python 튜토리얼: 함수·자료구조·예외](https://docs.python.org/3/tutorial/) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.
- [Pro Git: status/diff/commit/branch](https://git-scm.com/book/en/v2) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.
- [FastAPI: body/errors/testing](https://fastapi.tiangolo.com/tutorial/) — 해당 강의에 필요한 절과 예제만 읽고 자신의 합성 자료/계약에 적용한다.

## 증거와 완료 상태

학습 노트에는 읽은 절·자신의 설명·실습 명령·Python/패키지/장치·데이터/모델/프롬프트/인덱스 버전·expected/actual·raw 결과·commit/run_id·한계를 기록한다. 문서/fixture/실제DB·모델/클라우드·GPU의 수준을 구분한다. 자료 작성만으로 본인의 학습 또는 서비스 제작을 완료 처리하지 않는다. 막히면 증상·시도·다음 행동과 일정 영향을 남긴다.
