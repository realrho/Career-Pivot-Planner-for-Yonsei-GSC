# AWS 영상 학습 · EC2 배포(deployment)를 SA 설계로 연결하기

**주교재:** [사용자가 지정한 시작 영상](https://www.youtube.com/watch?v=cBbHXCmoUTc&list=PLtUgHNmvcs6qr33RT-UiguSsCr_2Gq0S3&index=3) · [재생목록: 비전공자도 이해할 수 있는 AWS 입문/실전](https://www.youtube.com/playlist?list=PLtUgHNmvcs6qr33RT-UiguSsCr_2Gq0S3) — JSCODE 박재성.
**수업 자료:** [강사 공개 교안](https://jscode.notion.site/2a38dc67ca1448f7ab350e40b89abd5a). 2026-10-07 교체 반영.

강사 교안에서 EC2 서버 배포·보안그룹(security group)·IP/Port·스토리지(storage)·탄력적 IP·비용 정리·Route 53을 확인했다. 개별 시작 영상의 제목·전체 자막·공개 재생목록 전체 편수/총 재생시간은 확인하지 못했으므로 편 번호나 타임스탬프를 지정하지 않는다. 아래 순서는 프로젝트용 학습 배정이다. 공개 영상에서 해당 주제를 찾아 보고, 없는 주제는 교안과 AWS 공식 문서로 보완한다. 유료 전체 강좌 수강이나 도메인(domain) 구매는 필수가 아니다.

## 어느 주차에 무엇을 할까?

| 주차 | 시청·복습 범위 | 바로 할 일 | 남길 증거 |
|---|---|---|---|
| W5 · 네트워크(network)/권한(permissions) | 지정 영상부터 EC2·리전(region)·보안그룹(security group)·IP/Port 부분 선택 | 공개 API/비공개 DB 그림, 포트(port)/접근 주체 표, IAM 역할과 업무 role/tenant 권한표 | 네트워크 도식 1개·허용/거부 연결표·권한 실패 사례 |
| W6 · 비용/IaC | W5 노트와 비용 정리 교안 복습 | 컴퓨팅(compute)·디스크(disk)·공인 IPv4(public IPv4)·도메인(domain) 관련 자원을 비용표에 넣고 정리 순서 작성 | 현재 단가 출처/확인일·사용량 가정·정리 체크리스트 |
| W7 · 배포(deployment)/복구(recovery) | 서버 접속·배포 교안을 W7 컨테이너(container) 실습에 적용 | Express/Spring 예제의 서버·포트·프로세스 개념을 기존 FastAPI/Compose로 바꾸어 로컬 재기동·로그·복원(restore) 확인 | 명령·환경·expected/actual·재시작/복원 기록 |
| W8 · 고객 설계 | Route 53/DNS 개념과 네트워크/비용 노트 검토 | EC2/Compose와 관리형 플랫폼 대안, 도메인/TLS 필요성·운영 책임을 ADR로 비교 | 선택 이유·대안·미검증 항목·TCO 시나리오 |

W5 영상 1h 중 트랜잭션(transaction) 약 25분 + AWS 선택 시청/메모 35분을 배정한다. 전체 AWS 재생목록 완강은 이 35분의 완료 조건이 아니다. 부족한 부분은 7h 연결 실습 안에서 교안/공식 문서를 참고한다. W6–W8은 기존 실습 시간에 노트를 재사용하며 새 필수 영상 시간을 더하지 않는다. 8주 학습+2주 제작, 주 22h와 총 영상 배정 12.5h를 유지한다. 실제 AWS 자원 생성/배포는 선택 심화이며 기본 완료 증거는 로컬 실행과 설계 기록이다.

## 개념을 차례로 이해하기

### 1. 컴퓨터를 빌리는 것과 서비스를 배포(deployment)하는 것
AWS는 Amazon Web Services(아마존 웹 서비스), EC2는 Elastic Compute Cloud(탄력적 클라우드 컴퓨팅)다. EC2는 서버 자원을 제공하고, 앱 프로세스·라이브러리·설정·업데이트는 사용자가 관리한다. deployment(배포)는 실행할 버전과 설정을 특정 환경에 배치해 사용할 수 있게 하는 과정이다. 서버 생성만으로 API가 실행되지는 않는다.

Region(리전)은 지리적 서비스 영역, AZ는 Availability Zone(가용 영역)이다. 리전(region) 선택은 데이터 위치·지연(latency)·서비스 지원·비용에 영향을 준다. 가용 영역(availability zone, AZ) 여러 개를 쓰는 것만으로 앱의 복구(recovery)와 데이터 일관성(consistency)이 자동 보장되지는 않는다. [AWS 리전/가용 영역](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html).

### 2. 어디로 가는가와 누가 접속하는가
IP는 Internet Protocol(인터넷 프로토콜), port(포트)는 같은 호스트의 서비스 접속 지점을 구분한다. DNS는 Domain Name System(도메인 이름 시스템), Route 53은 AWS의 DNS 서비스 제품명이다. DNS가 주소를 연결하는 것과 TLS, Transport Layer Security(전송 계층 보안)가 통신을 보호하는 것은 별개다.

VPC는 Virtual Private Cloud(가상 사설 클라우드), subnet(서브넷)은 그 안의 주소 범위를 나눈 네트워크(network)다. route table(라우팅 테이블)은 트래픽의 목적지에 따른 경로를 정하고, security group(보안그룹)은 리소스의 허용 트래픽을 정한다. 보안그룹(security group)은 stateful(상태 추적형)이며 허용된 연결의 응답 트래픽을 추적한다. [AWS 보안그룹](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html).

**프로젝트 적용:** 외부 사용자→API, API→DB만 필요한 연결로 그린다. DB의 5432 포트(port)를 인터넷 전체에 열지 않는다. 로컬의 127.0.0.1 바인딩은 원격 접속용 인터페이스(interface)와 다르다. 실제 공개 배포(deployment)를 고르면 앱 인증(authentication)·TLS·방화벽을 함께 검증한다.

### 3. 네트워크(network) 접근 허용과 업무 권한(permissions)
IAM은 Identity and Access Management(신원·접근 관리)다. AWS 리소스 작업에는 역할·정책을, 앱의 검토 승인에는 RBAC, Role-Based Access Control(역할 기반 접근 제어)과 tenant(조직 경계)를 적용한다. 포트(port)가 열려 있거나 서버 IAM 역할이 있다고 사용자가 사례를 승인할 수 있는 것은 아니다.

**프로젝트 적용:** API 서비스 역할에는 필요한 리소스 작업만 허용한다. 워크로드는 가능한 경우 역할의 임시 자격 증명(temporary credentials)을 사용한다. 사용자 역할·조직은 서버가 검증하고 viewer 승인과 교차 tenant 요청을 거부한다. 이 부분은 새 영상의 포함 범위를 가정하지 않고 [AWS IAM 모범 사례](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)와 W5 실습으로 보완한다.

### 4. 저장·비용·정리
EBS는 Elastic Block Store(탄력적 블록 스토리지), EIP는 Elastic IP address(탄력적 IP 주소)다. 디스크(disk) 유지·서버 종료·주소 해제는 서로 다른 작업이다. 공인 IPv4(public IPv4)는 요금이 발생할 수 있으므로 무료라고 가정하지 않는다. 서버를 멈췄다는 사실만으로 모든 비용이 끝났다고 기록하지 않는다. [AWS 탄력적 IP](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html).

**프로젝트 적용:** 실행 시간·디스크·주소·전송량을 비용표 변수로 적는다. 실제 AWS 실습을 선택하면 실습용 자원 목록과 정리 후 남은 자원을 확인한다. 백업(backup)/필요 데이터 확인→실습 서버 종료→잔여 디스크·주소·도메인(domain) 관련 자원 확인 순서로 기록한다. 이 문서는 기존 업무 자원 삭제 명령을 제공하지 않는다.

## FastAPI 프로젝트에 옮기는 순서

1. W1 API 계약(API contract)을 유지하고 기존 FastAPI 앱의 실행 명령·포트(port)·환경 변수를 적는다. 영상의 Express/Spring은 예시 프레임워크이므로 다른 언어로 다시 만들 필요가 없다.
2. W5에서 서버·네트워크(network)·보안그룹(security group)·IAM과 앱 role/tenant를 분리해 도식화한다. 허용 주체·목적지·포트·이유와 거부 사례를 적는다.
3. W7의 Dockerfile/Compose로 같은 이미지 버전의 API/DB를 로컬 기동한다. DB는 외부 공개 없이 연결하고 로그·재기동·권한(permissions) 실패를 확인한다. 현재 메모리 API의 재시작 데이터 소실을 지속 DB 성공으로 표시하지 않는다.
4. 실제 AWS 배포(deployment)를 선택하는 경우에만 EC2 접속·이미지 실행·인증(authentication)/TLS·로그·자원 정리(resource cleanup)를 수행한다. 로컬 증거와 AWS 실행 증거를 별도로 기록한다.
5. W8 ADR, Architecture Decision Record(아키텍처 결정 기록)에 요구→대안→선택→비용→운영 책임을 연결한다. TCO, Total Cost of Ownership(총 소유 비용)에 운영/검토 인력까지 포함한다.

## 완료 체크

- [ ] 각 시청 기록에 영상 URL·실제로 본 범위·자기 설명·다음 실습을 남겼다.
- [ ] EC2/VPC/보안그룹(security group)/IAM과 앱 RBAC/tenant의 역할 차이를 설명했다.
- [ ] API/DB 연결표와 허용/거부 사례를 작성하고 W5 앱 권한(permissions) 실패를 확인했다.
- [ ] W6 비용표와 자원 정리(resource cleanup) 계획, W7 로컬 실행/복원(restore) 증거, W8 선택 ADR을 연결했다.
- [ ] 계획/실행, 로컬/AWS, 접수 API/실제 AI 분석을 구분해 결과를 기록했다.

[주차 영상 목록](video-resources.md) · [W5 교재](curriculum/week-05.md) · [MVP 설계](project-blueprint.md)
