# 영어·한글 기술 용어 사전

## 한국어·영어 실무 용어 읽는 법

한국어로 적힌 핵심 기술·실무 용어는 **한국어(현업 English 표현)**으로 읽는다. 같은 소절에서는 첫 등장에 영어를 병기하고 이후 반복은 간결하게 유지한다. 팀마다 한국어·음역·영어를 섞어 쓰므로 아래 표현은 공통 이해를 위한 대응표이며 모든 회사의 말투가 같다는 뜻은 아니다.

이미 영어로 쓰인 Docker, Kubernetes, FastAPI, tenant, role, workflow, run_id, readiness/liveness, dev20/holdout30 등은 원문 그대로 사용한다. 코드·명령·API 경로·설정 키·URL도 그대로 유지한다. 약어의 전체 이름과 뜻은 기존 사전에서 확인하고, 교재 목차와 책/영상의 공식 제목은 원문을 보존한다.

## 학습 표현 → 현업 표현 → 회의에서 쓰는 문장

| 한국어 학습 표현 | 현업 English 표현 | 말할 때 쓰는 표현·업무 예시 | 뜻·구분 |
|---|---|---|---|
| 요구사항 | requirements | 이 requirements를 고객과 확정하자. | 필요한 동작과 제약을 합의한다. |
| 비기능 요구사항 | non-functional requirements, NFR | NFR에 P95와 비용 상한을 넣자. | 성능·신뢰성·보안·운영 제약이다. |
| 수용 기준 | acceptance criteria, AC | 이 AC를 통과해야 작업을 완료한다. | 완료를 관찰·검증할 조건이다. |
| 설계 결정 기록 | architecture decision record, ADR | 이 선택의 이유를 ADR에 남기자. | 요구·대안·선택·결과를 기록한다. |
| 트레이드오프 | trade-off | 지연과 비용의 trade-off를 설명하자. | 하나의 이점을 얻으며 다른 제약을 감수한다. |
| 입력 검증 | input validation | input validation에서 잘못된 필드를 거부하자. | 입력 타입·형식·허용 범위를 확인한다. |
| 인증 | authentication, AuthN | 인증된 사용자 신원을 확인했나? | 누가 요청했는지 확인한다. |
| 인가·권한 판단 | authorization, AuthZ | 이 role이 승인할 수 있는지 인가하자. | 그 신원이 특정 행동을 해도 되는지 판단한다. |
| 조직 경계 | tenant boundary | 다른 tenant 데이터가 검색되면 안 된다. | 조직/고객별 데이터·권한 격리 경계다. |
| 최소 권한 | least privilege | 서비스 role을 least privilege로 줄이자. | 필요한 행동·자원만 허용한다. |
| 멱등성 | idempotency | 재시도해도 중복 승인되지 않게 idempotent하게 만들자. | 같은 요청 반복의 업무 효과가 중복되지 않는다. |
| 동시성 | concurrency | 두 검토자가 동시에 승인하는 concurrency 사례를 보자. | 작업이 겹쳐 진행될 때 상태 충돌을 고려한다. |
| 원자성 | atomicity | 상태 변경과 감사 저장을 atomic하게 처리하자. | 관련 변경이 모두 성공하거나 모두 실패한다. |
| 트랜잭션 | transaction | 이 두 DB 변경은 한 transaction이다. | 함께 처리할 데이터 변경의 경계다. |
| 영속성 | persistence | 재시작 후에도 상태가 남는 persistence를 검증하자. | 데이터를 프로세스 수명 밖에 저장한다. |
| 지속성 | durability | commit이 성공한 기록의 durability를 보자. | 완료된 트랜잭션의 변경이 보존되는 성질이다. |
| 롤백 | rollback | 새 버전 오류가 나면 rollback하자. | DB 롤백과 배포 버전 롤백은 대상과 절차가 다르다. |
| 비동기 처리 | async processing | 이 경로는 async로 처리한다. | 기다리는 동안 다른 작업이 진행될 수 있다. 병렬 실행·작업 내구성을 자동 보장하지 않는다. |
| 재시도·제한 시간 | retry / timeout | timeout과 retry 예산을 정하자. | 재실행과 대기/실행 종료 한도다. |
| 검색 증강 생성 | retrieval-augmented generation, RAG | RAG 검색에 tenant 필터를 적용하자. | 검색 근거를 모델 입력에 결합한다. |
| 임베딩·청크 | embedding / chunk | chunk별 embedding을 저장하자. | 의미의 벡터 표현 / 검색·인용용 문서 단위다. |
| 하이브리드 검색·순위 재정렬 | hybrid search / reranking | hybrid search 뒤에 reranking을 비교하자. | 검색 방식을 조합 / 후보의 순서를 다시 계산한다. |
| 답변 보류 | abstention / abstain | 근거가 부족하면 abstain한다. | 모델 장애와 업무상 답변 보류를 분리한다. |
| 사람 검토 | human review | 고위험 사례를 human review로 보내자. | 검토자는 서버에서 확인한 권한으로 결정한다. |
| 부하 시험·처리량 | load testing / throughput | load test로 throughput과 오류율을 보자. | 정해진 부하를 주고 단위 시간 처리량을 측정한다. |
| 지연 | latency | 검색과 모델 구간 latency를 분리하자. | 요청 처리의 지연을 조건·단위와 함께 측정한다. |
| 관측 가능성 | observability | logs, metrics, traces를 연결하자. | 내부 상태와 실패를 실행 신호로 설명할 수 있는 정도다. |
| 배포 | deployment | 이 이미지 버전으로 deployment하자. | 버전·설정을 환경에 배치하고 동작을 확인한다. |
| 준비·생존 상태 검사 | readiness probe / liveness probe | readiness 실패와 liveness 실패를 구분하자. | 요청 수신 가능 여부 / 재시작 판단이다. |
| 보안그룹·서브넷 | security group / subnet | DB security group에 API 경로만 허용하자. | 허용 트래픽 규칙 / 네트워크 주소 구획이다. |
| 백업·복원·복구 | backup / restore / recovery | backup에서 restore한 뒤 실제 조회까지 recovery를 확인하자. | 사본 생성 / 데이터 되돌림 / 서비스 정상화다. |
| 지속적 전달·지속적 배포 | continuous delivery / continuous deployment | CD가 승인 후 전달인지 자동 배포인지 명시하자. | 운영 반영 승인 방식에 따라 구분한다. |
| 총 소유 비용 | total cost of ownership, TCO | TCO에 운영과 검토 인력도 포함하자. | 도입·운영·전환에 드는 전체 비용이다. |

표현/의미 확인: [AWS 인증·인가](https://docs.aws.amazon.com/IAM/latest/UserGuide/intro-structure.html) · [PostgreSQL 트랜잭션](https://www.postgresql.org/docs/current/tutorial-transactions.html) · [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/) · [AWS security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html). 회의 문장은 이 프로젝트에 맞춰 작성한 예시다.


약어는 영어 확장·한글 의미·실제 역할로 읽는다. 제품 이름과 알고리즘 이름에 근거 없는 풀네임을 만들지 않는다. 축약 표기는 문맥에 따라 달라질 수 있다. 각 주차 강의에는 이 용어가 필요한 이유와 실패 예시를 넣었다. 기존 모델 용어는 참고로 보존하며 Python·HTTP·SQL 기초 학습 과제로 배정하지 않는다. 2026-10-06 『AI 에이전트 엔지니어링』 및 SA 보완 용어를 추가했다.

## 기초·모델

| 표기 | English | 한글 | 의미·주의점 |
|---|---|---|---|
| SA | Solution Architect | 솔루션 아키텍트 | 고객 요구와 제약을 기술 설계·검증·설명으로 연결하는 역할. |
| AI | Artificial Intelligence | 인공지능 | 인식·추론·생성 등을 수행하는 계산 시스템의 넓은 범주. |
| ML | Machine Learning | 머신러닝·기계 학습 | 데이터에서 패턴/파라미터를 학습하는 방법. |
| LLM | Large Language Model | 대규모 언어 모델 | 대량 텍스트로 학습해 언어 확률/생성을 다루는 모델. |
| sLLM | small Large Language Model / small language model | 소형 언어 모델 | 문맥에 따라 표기가 다른 소형 언어 모델 통칭; 절대 크기 표준이 아니다. |
| RNN | Recurrent Neural Network | 순환 신경망 | 이전 상태를 다음 시점에 전달해 순차 입력을 처리한다. |
| Transformer | Transformer (architecture name) | 트랜스포머 | 어텐션을 핵심으로 토큰 관계를 처리하는 아키텍처 이름. |
| GPT | Generative Pre-trained Transformer | 생성형 사전 학습 트랜스포머 | 대표적인 디코더 중심 언어 모델 계열. |
| BERT | Bidirectional Encoder Representations from Transformers | 트랜스포머의 양방향 인코더 표현 | 대표적인 인코더 중심 사전 학습 모델. |
| BART | Bidirectional and Auto-Regressive Transformers | 양방향 및 자기회귀 트랜스포머 | 잡음 제거 학습을 활용하는 인코더·디코더 모델. |
| T5 | Text-to-Text Transfer Transformer | 텍스트 대 텍스트 전이 트랜스포머 | 여러 과제를 텍스트 입력/출력으로 표현하는 모델. |
| Q / K / V | Query / Key / Value | 쿼리·키·값 | 어텐션에서 연관성 계산과 정보 집계에 사용하는 표현. |
| token | token | 토큰 | 토크나이저가 나눈 처리 단위; 문자나 단어와 일대일 대응하지 않는다. |
| embedding | embedding | 임베딩 | 입력을 벡터로 표현한 것. 차원·모델·정규화·거리 기준을 같이 기록한다. |
| RoPE | Rotary Positional Embedding | 회전 위치 임베딩 | 회전을 이용해 토큰 위치 정보를 반영하는 방법. |
| ALiBi | Attention with Linear Biases | 선형 편향을 적용한 어텐션 | 어텐션에 위치 관련 선형 편향을 넣는 방법. |
| CLIP | Contrastive Language-Image Pre-training | 대조적 언어·이미지 사전 학습 | 이미지와 텍스트 표현을 대응시키는 모델/학습 접근. |
| LLaVA | Large Language and Vision Assistant | 대규모 언어·시각 어시스턴트 | 시각 입력과 언어를 연결하는 모델 계열. |
| DALL-E | DALL-E (model name) | 달리 | 이미지 생성 모델의 고유 이름; 약어 풀네임을 임의로 만들지 않는다. |
| SSM | State Space Model | 상태 공간 모델 | 입력과 내부 상태의 변화로 순차 데이터를 표현한다. |
| S4 | Structured State Space Sequence Model | 구조화 상태 공간 시퀀스 모델 | 긴 시퀀스를 효율적으로 다루는 구조화 상태 공간 모델. |
| Mamba | Mamba (architecture name) | 맘바 | 선택적 상태 공간 메커니즘을 활용하는 아키텍처 이름. |

## 학습·하드웨어·서빙

| 표기 | English | 한글 | 의미·주의점 |
|---|---|---|---|
| SFT | Supervised Fine-Tuning | 지도 미세 조정 | 지시·정답 예시로 모델 파라미터를 조정한다. |
| RL | Reinforcement Learning | 강화 학습 | 보상으로 행동 정책을 개선하는 학습 접근. |
| RLHF | Reinforcement Learning from Human Feedback | 사람 피드백을 이용한 강화 학습 | 사람 선호 등의 피드백으로 보상/정책을 학습한다. |
| PPO | Proximal Policy Optimization | 근접 정책 최적화 | 급격한 정책 갱신을 제한하려는 강화 학습 알고리즘. |
| DPO | Direct Preference Optimization | 직접 선호 최적화 | 선호 응답 쌍을 이용해 정책을 직접 최적화한다. |
| PEFT | Parameter-Efficient Fine-Tuning | 파라미터 효율적 미세 조정 | 업데이트할 파라미터를 줄이는 기법군. |
| LoRA | Low-Rank Adaptation | 저랭크 적응 | 저랭크 행렬 업데이트를 학습한다. |
| QLoRA | Quantized Low-Rank Adaptation | 양자화 저랭크 적응 | 양자화 기반 모델과 저랭크 학습을 결합한다. |
| ZeRO | Zero Redundancy Optimizer | 중복 없는 최적화기 | 분산 학습의 중복 상태 저장을 줄이는 방법. |
| CPU | Central Processing Unit | 중앙 처리 장치 | 범용 명령을 실행한다. CPU fixture 검증은 GPU 학습/추론 성능 증거가 아니다. |
| GPU | Graphics Processing Unit | 그래픽 처리 장치 | 대량 수치 연산을 병렬로 처리한다. |
| VRAM | Video Random Access Memory | 그래픽 메모리 | GPU가 사용하는 메모리; 모델 외 활성값·상태·캐시도 필요하다. |
| FP16 / FP32 | 16-bit / 32-bit Floating Point | 16/32비트 부동소수점 | 수치 표현 형식; 정밀도와 메모리 비용이 다르다. |
| BF16 | Brain Floating Point 16 | 브레인 16비트 부동소수점 | FP16과 지수/유효숫자 구성이 다른 16비트 형식. |
| KV cache | Key-Value cache | 키·값 캐시 | 이전 토큰 어텐션 계산을 재사용한다. 서비스 응답 캐시와 다르다. |
| GPTQ | GPTQ (method name) | GPTQ 양자화 방법 | 후학습 가중치 양자화 방법의 이름. 정식 풀네임을 단정해 지어내지 않는다. |
| AWQ | Activation-aware Weight Quantization | 활성값을 고려한 가중치 양자화 | 활성값 정보를 고려하는 가중치 양자화 접근. |
| vLLM | vLLM (project name) | 브이엘엘엠 | LLM 추론·서빙 프로젝트 이름. 약어 확장을 임의로 붙이지 않는다. |
| TTFT | Time To First Token | 첫 토큰까지 시간 | 요청 후 첫 출력 토큰까지 걸리는 시간. |
| TPOT | Time Per Output Token | 출력 토큰당 시간 | 출력 생성 단계의 토큰당 시간 지표. |
| RPM / TPM | Requests / Tokens Per Minute | 분당 요청 수·분당 토큰 수 | 서로 다른 요청량 제한. TPM은 Time Per Minute가 아니다. |
| P50 / P95 | 50th / 95th percentile | 50·95백분위 | 지연 분포의 위치. 표본·계산 방법·조건을 같이 보고한다. |
| prefill / decode | prefill / decode | 입력 처리·출력 생성 | 프롬프트 처리와 다음 토큰 반복 생성 단계. |
| quantization | quantization | 양자화 | 수치 표현 비트 수 등을 줄여 저장·연산 비용을 바꾸는 방법. |
| distillation | knowledge distillation | 지식 증류 | 큰 모델 등의 행동을 더 작은 모델이 학습하도록 하는 접근. |

## 검색·데이터·평가

| 표기 | English | 한글 | 의미·주의점 |
|---|---|---|---|
| RAG | Retrieval-Augmented Generation | 검색 증강 생성 | 외부 검색 근거를 모델 입력에 통합한다. |
| SQL / Text2SQL | Structured Query Language / Text-to-SQL | 구조화 질의 언어·텍스트에서 SQL 생성 | DB 질의 언어와 자연어로 질의를 만드는 과제. 생성 SQL 실행 권한은 별도다. |
| DB | Database | 데이터베이스 | 데이터 저장·조회·제약을 제공하는 시스템. |
| TF-IDF | Term Frequency–Inverse Document Frequency | 용어 빈도·역문서 빈도 | 흔한 단어를 낮추고 문서별 특징 단어를 강조하는 표현. |
| BM25 | Best Matching 25 | 베스트 매칭25 | 키워드 기반 검색 점수 방식. |
| RRF | Reciprocal Rank Fusion | 역순위 융합 | 다른 검색기의 순위를 합치는 방법. |
| KNN / ANN | k-Nearest Neighbors / Approximate Nearest Neighbor | k-최근접 이웃·근사 최근접 이웃 | 정확/근사 거리 검색 접근. |
| NSW / HNSW | Navigable Small World / Hierarchical Navigable Small World | 탐색 가능한 작은 세계·계층형 탐색 가능한 작은 세계 | 그래프 기반 근사 검색과 계층형 인덱스. |
| MNR loss | Multiple Negatives Ranking loss | 다중 음성 순위 손실 | 정답 쌍을 가깝게, 다른 쌍을 상대적으로 멀게 학습하는 손실. 공식 클래스는 MultipleNegativesRankingLoss. |
| MRR | Mean Reciprocal Rank | 평균 역순위 | 질문별 첫 정답 순위 역수의 평균. |
| Recall@k | Recall at k | 상위 k 검색 재현율 | 정답 근거 중 상위 k에 검색된 비율. |
| bi-encoder / cross-encoder | bi-encoder / cross-encoder | 바이 인코더·교차 인코더 | 각 입력을 따로 표현 / 입력 쌍을 함께 읽어 점수화한다. |
| reranking | reranking | 순위 재정렬 | 검색 후보를 다시 평가해 순서를 바꾼다. |
| ACID | Atomicity, Consistency, Isolation, Durability | 원자성·일관성·격리성·지속성 | DB 트랜잭션의 성질. 외부 서비스 작업은 별도다. |
| JSON / JSONL | JavaScript Object Notation / JSON Lines | 자바스크립트 객체 표기법·줄 단위 JSON | 구조 데이터 표현 / 각 줄이 독립 JSON인 로그 형식. |
| TTL | Time To Live | 유효 수명 | 캐시 등에 부여하는 시간 제한; 즉시 정책 갱신 보장은 아니다. |
| holdout | holdout evaluation set | 동결 최종 평가 세트 | 선택·조정에서 분리한 최종 평가 데이터. |
| leakage | data leakage | 데이터 누수 | 학습/선택 과정에서 최종 평가 정보를 사용해 평가가 낙관적으로 되는 현상. |
| citation / abstention | citation / abstention | 근거 인용·답변 보류 | 출처 연결 / 근거 부족 등으로 답변을 만들지 않는 결정. |
| idempotency | idempotency | 멱등성 | 같은 작업을 반복해도 추가 부작용이 생기지 않는 성질. |
| ingestion / metadata | ingestion / metadata | 수집·적재·메타데이터 | 원본을 검색 가능하게 준비 / 출처·버전·권한 등의 부가 정보. |
| tenant | tenant | 테넌트·고객 조직 경계 | 같은 서비스를 사용하는 고객/조직의 격리 단위. |
| schema / transaction | schema / transaction | 스키마·트랜잭션 | 데이터 구조 규칙 / 관련 DB 변경을 함께 처리하는 단위. |

## API·네트워크·보안

| 표기 | English | 한글 | 의미·주의점 |
|---|---|---|---|
| API / SDK | Application Programming Interface / Software Development Kit | 애플리케이션 프로그래밍 인터페이스·소프트웨어 개발 키트 | 호출 규약 / 구현을 돕는 라이브러리·도구 묶음. |
| HTTP / HTTPS | Hypertext Transfer Protocol / HTTP over TLS | 하이퍼텍스트 전송 프로토콜·TLS를 사용하는 HTTP | 요청/응답 규칙 / 보호된 전송. |
| DNS / IP / TCP | Domain Name System / Internet Protocol / Transmission Control Protocol | 도메인 이름 시스템·인터넷 프로토콜·전송 제어 프로토콜 | 이름 해석 / 주소·전달 / 순서 있는 전송. |
| TLS | Transport Layer Security | 전송 계층 보안 | 전송 암호화와 인증서 기반 상대 신원 확인. |
| CORS | Cross-Origin Resource Sharing | 교차 출처 리소스 공유 | 브라우저 출처 접근 규칙. 사용자 인증/인가를 대신하지 않는다. |
| IAM | Identity and Access Management | 신원 및 접근 관리 | 주체의 신원과 자원 접근을 관리한다. |
| RBAC | Role-Based Access Control | 역할 기반 접근 제어 | 역할에 허용 동작을 배정한다. |
| JWT | JSON Web Token | JSON 웹 토큰 | 클레임 전달 형식. 검증 없이 읽은 내용은 신뢰할 수 없다. |
| OAuth 2.0 / OIDC | OAuth 2.0 / OpenID Connect | OAuth 2.0 접근 위임·오픈아이디 커넥트 | OAuth는 규약 이름 / OIDC는 OAuth 위의 신원 계층. OAuth의 임의 풀네임은 만들지 않는다. |
| PII | Personally Identifiable Information | 개인 식별 정보 | 개인을 식별·연결할 수 있는 정보. |
| HITL | Human-in-the-Loop | 사람 참여 검토 | 특정 단계/위험 결정을 사람이 확인한다. |
| OWASP | Open Worldwide Application Security Project | 오픈 월드와이드 애플리케이션 보안 프로젝트 | 애플리케이션 보안 자료·프로젝트 커뮤니티. |
| prompt injection | prompt injection | 프롬프트 주입 | 신뢰되지 않은 입력 지시가 시스템 의도/권한을 바꾸려는 공격. |
| timeout / retry | timeout / retry | 시간 제한·재시도 | 최대 대기 / 일시 실패에 대한 제한된 재요청. |
| checkpoint | checkpoint | 체크포인트·재개 상태 | 중단 후 재개를 위한 상태 기록. 재개 시 권한/버전도 확인한다. |

## 운영·설계·협업

| 표기 | English | 한글 | 의미·주의점 |
|---|---|---|---|
| AWS / VPC | Amazon Web Services / Virtual Private Cloud | 아마존 웹 서비스·가상 사설 클라우드 | 클라우드 서비스군 / 논리적으로 분리된 네트워크 공간. |
| EC2 / S3 / RDS | Elastic Compute Cloud / Simple Storage Service / Relational Database Service | 탄력적 컴퓨트 클라우드·단순 스토리지 서비스·관계형 DB 서비스 | AWS의 가상 서버 / 객체 저장 / 관리형 관계형 DB. |
| CI / CD | Continuous Integration / Continuous Delivery | 지속적 통합·지속적 전달 | 변경 자동검증 / 배포 준비. CD는 Continuous Deployment(지속적 배포)로 쓰이기도 하므로 문맥을 명시한다. |
| MLOps / LLMOps | Machine Learning Operations / Large Language Model Operations | 머신러닝 운영·대규모 언어 모델 운영 | 데이터/모델 수명주기 / 프롬프트·검색·도구까지 포함하는 운영. |
| OTel | OpenTelemetry | 오픈텔레메트리 | 로그/메트릭/트레이스 등 계측·전달 프로젝트. |
| SLI / SLO / SLA | Service Level Indicator / Objective / Agreement | 서비스 수준 지표·목표·계약 | 측정치 / 내부 목표 / 고객과의 합의. |
| RTO / RPO | Recovery Time Objective / Recovery Point Objective | 복구 시간 목표·복구 시점 목표 | 복구까지 허용 시간 / 허용 데이터 손실 구간. |
| HA | High Availability | 고가용성 | 장애 중에도 서비스 가용성을 유지하는 설계 성질. 실제 검증 없이 주장하지 않는다. |
| K8s | Kubernetes (numeronym) | 쿠버네티스 | K와s 사이8글자를 숫자로 표시한 이름. 컨테이너 운영 조정 플랫폼. |
| ADR | Architecture Decision Record | 아키텍처 결정 기록 | 맥락·선택·대안·결과·재검토 조건. |
| FR / NFR | Functional / Non-Functional Requirement | 기능·비기능 요구사항 | 행동 / 품질·운영 제약. |
| PoC / MVP | Proof of Concept / Minimum Viable Product | 개념 검증·최소 기능 제품 | 특정 가능성 확인 / 제한된 문제의 종단 사용 흐름. |
| TCO / FinOps | Total Cost of Ownership / Financial Operations | 총소유비용·재무 운영 | 사용료 외 개발/운영 비용 / 클라우드 비용·가치 관리 실천. |
| PR | Pull Request | 풀 리퀘스트·변경 병합 요청 | 변경 이유·검증·검토를 모으는 협업 단위. |
| KISS / DRY | Keep It Simple, Stupid / Don't Repeat Yourself | 단순하게 유지·중복을 반복하지 않기 | 작고 명확한 설계를 위한 원칙. |
| SOLID | Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion | 단일 책임·개방 폐쇄·리스코프 치환·인터페이스 분리·의존성 역전 | 유지보수 가능한 설계 원칙군. 작은 실습에 불필요한 추상화를 강제하지 않는다. |
| WSL2 | Windows Subsystem for Linux 2 | 윈도우용 리눅스 하위 시스템2 | Windows에서 Linux 환경을 사용하는 경로. GPU/서버 호환성은 개별 확인한다. |
| CLI / UI | Command-Line Interface / User Interface | 명령줄 인터페이스·사용자 인터페이스 | 명령으로 조작 / 사용자가 조작하는 화면·접점. |
| Git / GitHub / FastAPI | Git / GitHub / FastAPI (product names) | 깃·깃허브·패스트API | 버전관리 / 협업호스팅 / Python웹API프레임워크. 각각 고유 이름이다. |
| Docker / Compose / PostgreSQL | Docker / Docker Compose / PostgreSQL | 도커·도커컴포즈·포스트그레SQL | 컨테이너도구 / 복수서비스설정 / 관계형DB 제품 이름. |
| LlamaIndex / AutoGen / LangGraph | LlamaIndex / AutoGen / LangGraph | 라마인덱스·오토젠·랭그래프 | RAG/에이전트/워크플로 관련 제품 이름. 약어 풀네임을 만들지 않는다. |
| Pinecone / Milvus / Redis | Pinecone / Milvus / Redis | 파인콘·밀버스·레디스 | 벡터검색/데이터저장 관련 제품 이름. 본 계획에서는 사용 역할과 실제 검증 범위를 명시한다. |

[이전 교재 참고 정오표: TPM·RoPE 등](https://www.onlybook.co.kr/entry/llm-errata) · [LoRA 원 논문](https://arxiv.org/abs/2106.09685) · [S4 원 논문](https://arxiv.org/abs/2111.00396) · [Mamba 원 논문](https://arxiv.org/abs/2312.00752) · [MNR 공식 문서](https://www.sbert.net/docs/package_reference/sentence_transformer/losses.html). 기본 개념 정의와 프로젝트 예시는 독립적으로 작성한 학습 설명이다.

## 에이전트·플랫폼·SA 보완

| 표기 | English | 한글 | 의미·주의점 |
|---|---|---|---|
| A2A | Agent2Agent | 에이전트 간 통신 | 에이전트 상호운용 프로토콜 이름. MCP의 도구/컨텍스트 연결과 역할을 구분한다. |
| ReAct | Reasoning and Acting | 추론과 행동 | 다음 행동을 결정하며 도구 결과를 반영하는 패턴. 프런트엔드 React와 다르다. |
| RLVR | Reinforcement Learning with Verifiable Rewards | 검증 가능 보상을 이용한 강화 학습 | 정답 검사 등 검증 가능한 신호를 보상으로 사용. 업무의 모든 품질이 자동 검증되는 것은 아니다. |
| MAESTRO | Multi-Agent Environment, Security, Threat, Risk, and Outcome | 에이전트 환경·보안·위협·위험·결과 위협 모델 | CSA의 에이전틱 AI 위협 모델. 계층과 연결 경계를 확인한다. |
| IaC | Infrastructure as Code | 코드로 관리하는 인프라 | 변경 계획·상태·검증을 추적. Terraform은 제품 이름. |
| CI/CD | Continuous Integration / Continuous Delivery or Deployment | 지속적 통합 / 지속적 전달 또는 배포 | CD는 팀의 배포 승인 방식에 따라 의미가 달라진다. |
| OIDC | OpenID Connect | 오픈아이디 커넥트 | OAuth 2.0 위에 신원 계층을 더한 프로토콜. 서명/발급자/대상/만료를 검증한다. |
| SSO | Single Sign-On | 통합 로그인 | 한 로그인 경험으로 여러 서비스 접근. 권한과 tenant 통제를 대체하지 않는다. |
| OAuth 2.0 | OAuth 2.0 (authorization framework name) | 권한 위임 프레임워크 | 공식 명세 이름으로 쓰며 억지로 약어 확장을 만들지 않는다. 인증·인가 목적을 구분한다. |
| RTO | Recovery Time Objective | 목표 복구 시간 | 업무가 허용하는 복구 시간 목표. 실제 복구시간을 측정해 비교한다. |
| RPO | Recovery Point Objective | 목표 복구 시점 | 장애 시 허용할 데이터 손실 시간 범위. 백업 생성만으로 보장되지 않는다. |
| NFR | Non-Functional Requirement | 비기능 요구사항 | 성능·신뢰성·보안·비용·운영 제약을 측정 가능한 조건으로 정의한다. |
| TCO | Total Cost of Ownership | 총 소유 비용 | 컴퓨팅뿐 아니라 검색/저장·운영·검토·전환 비용을 포함한다. |
| ROI | Return on Investment | 투자 수익률 | 도입 효과와 총비용을 가정/기간/측정 기준과 함께 계산한다. |
| ELK | Elasticsearch, Logstash, Kibana | 로그 수집·저장·시각화 스택 | 제품 이름의 머리글자. 최신 스택 구성은 실제 선택에 따라 달라진다. |
| SLA | Service Level Agreement | 서비스 수준 협약 | 고객과 합의한 책임/조건. 내부 목표 SLO 및 실측 SLI와 구분한다. |
| P95 | 95th percentile | 95백분위 응답시간 | 관측 요청의 약 95%가 이 값 이하. 평균/최댓값과 다르다. |
| Idempotency | Idempotency | 멱등성 | 같은 작업을 반복 요청해도 업무 효과가 중복되지 않는 성질. 키 저장과 작업 결과의 원자성을 검증한다. |
| Outbox | Transactional outbox pattern | 트랜잭션 아웃박스 | 업무 변경과 발행 예정 이벤트를 원자적으로 저장. 재발행·소비 중복은 별도 처리한다. |
| Probe | Liveness / Readiness / Startup probe | 생존·준비·시작 상태 점검 | 재시작 조건·트래픽 수신 준비·느린 시작을 구분한다. |
| ConfigMap / Secret | Kubernetes ConfigMap / Secret | 일반 설정 / 민감 설정 객체 | Secret의 base64 인코딩은 암호화가 아니다. 접근 통제·저장 암호화·로그 보호가 필요하다. |
| Digest | Image content digest | 이미지 내용 식별값 | 변할 수 있는 tag와 구분해 검증된 이미지 내용을 식별한다. |
| GraphRAG | Graph-based Retrieval-Augmented Generation | 그래프 기반 검색 증강 생성 | 관계/연결 질문에 도움. 지식 그래프 구축·권한·오염 비용을 따진다. |
| Context Engineering | Context Engineering | 컨텍스트 엔지니어링 | 모델이 사용할 지침·도구·근거·메모리를 선택/구성/제한하는 과정. 프롬프트 한 문장만 다루지 않는다. |
| C4 | Context, Containers, Components, Code | 컨텍스트·컨테이너·컴포넌트·코드 설계도 | C4의 container는 실행/저장 단위이며 반드시 Docker 컨테이너를 뜻하지 않는다. |

[MAESTRO 공식 설명](https://labs.cloudsecurityalliance.org/maestro/) · [Kubernetes 공식 문서](https://kubernetes.io/docs/concepts/) · [추가 영상](video-resources.md)
