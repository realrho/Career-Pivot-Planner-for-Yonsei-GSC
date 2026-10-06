# 책 중심 학습 시작하기

확정한 구조는 **학습 8주 + 제작 2주, 총 10주**다. 기존 주 22시간을 계획 가정으로 유지한다. 학습 176시간 + 제작 44시간이다. 날짜는 2026-10-02를 새 시작일로 가정해 12-10까지 배치했다. 실제 시작일/주당 시간이 다르면 주차 순서를 유지하며 날짜를 옮긴다.

## 매주 같은 순서로 공부하기

1. **읽기 6h:** 배정한 모든 절을 읽는다. '무엇인가→어디에 쓰나→어떤 비용/한계가 있나'를 3문장으로 적는다.
2. **책 실습 6h:** 주차의 필수 경로를 실행한다. 공식 노트북·정오표를 사용하고 버전/명령/입출력을 남긴다. GPU가 필요한 선택 실습은 따로 표시한다.
3. **SA 보충 8h:** 주차의 네 강의를 읽고 계약 실습과 프로젝트용 작은 자산을 만든다. 계산 fixture에서 끝난 항목과 실제 DB/모델 항목을 구분한다.
4. **설명·증거 검토 2h:** 퀴즈 3개를 해설 없이 답한다. 실행 결과와 남은 질문을 Notion/GitHub에 기록한다.

각 주차의 **통과 조건**을 충족해야 다음 의존 작업이 준비된다. 책 읽기만 끝났다면 읽기 완료로, 실행 못한 실습은 미실행으로 남긴다. 기간은 목표이지 학습 능력을 판단하는 점수가 아니다.

## 책 환경과 프로젝트 환경 분리

책은 2024년 예제를 포함한다. 모델 이름·공급자 기능·SDK가 달라질 수 있으므로 [공식 코드](https://github.com/onlybooks/llm)와 [정오표](https://www.onlybook.co.kr/entry/llm-errata)를 먼저 확인한다. 오래된 노트북 설치를 최신 API 코드와 무조건 섞지 않는다. book environment와 project environment의 Python·패키지 버전·모델 revision을 각각 남긴다. 인증 토큰은 환경/비밀 관리 경로에 두며 노트북 출력·Git·로그에 넣지 않는다.

프로젝트의 기존 API는 Python 3.11+이다. 아래는 현재 뼈대 설치/검증 명령이며 정확 버전 잠금은 W7의 실습으로 정리한다. PowerShell에서 저장소 루트 기준:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e '.[dev]'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

`-m`은 해당 Python의 모듈을 실행한다. `-e`는 작업 중인 프로젝트를 편집 가능한 형태로 설치하며 `[dev]`는 테스트 의존성을 포함한다. `app.main:app`은 모듈과 FastAPI 객체 경로다. `--reload`는 개발 중 변경 반영용이다. 현재 /health·접수·메모리 조회만 있고 실제 분석/검색/영속DB는 아직 구현되지 않았다.

새로 제공한 `labs/week-01..08/contract_demo.py`는 표준 라이브러리 CPU 실습이다. 예: `python labs/week-01/contract_demo.py`. 이 예제의 통과는 웹API·모델·PostgreSQL·GPU 실행 검증과 다르다.

## 필수 / 선택 / 막혔을 때

기초가 어려우면 추가 GPU/멀티모달 실습부터 줄이고 입력/DB/검색/권한 필수 자산을 우선한다. GPU 없이 학습 코드 흐름·메모리·평가 설계를 이해할 수 있지만 실제 학습했다고 쓰지는 않는다. 모델 키/예산이 없으면 retrieval과 fixture를 진행하고 최종 실제 모델 gate를 미완료로 둔다. 환경 실패는 Python경로→패키지→버전/하드웨어 지원→요청/데이터 계약 순으로 확인한다.

W8 준비 gate: API 계약, 실제 검색, 영속 DB, 권한/검토, 재현 가능한 기동, 평가 세트. 이 자산이 없으면 2주 제작 추정을 다시 잡는다.

[목차](book-toc.md) · [SA 보충 범위](book-gap-map.md) · [영어·한글 용어](glossary-ko-en.md) · [10주 교재](curriculum/README.md) · [MVP 설계](project-blueprint.md)
