# CookBot

한이음·캡스톤디자인에서 진행한 양팔 요리 로봇 프로젝트의 MuJoCo 시뮬레이션 및 데이터 수집 코드입니다.

## 주요 기능

- OpenManipulator-X 양팔 MuJoCo 환경 구성
- 손목 카메라를 포함한 멀티뷰 렌더링
- 양팔 수동 조작 및 joint state 발행
- ROS 2 bag(db3) 기반 동작 데이터 저장
- db3 데이터를 ACT 및 HDF5 형식으로 변환
- 저장된 동작 데이터를 MuJoCo에서 재생

## 디렉터리 구성

- `Mujoco/legacy/`: 초기 단일·양팔 로봇 및 손목 카메라 시뮬레이션
- `Mujoco/`: 팀 프로젝트에서 발전시킨 멀티뷰 데이터 수집·변환·재생 파이프라인
- `Mujoco/assets/`: 초기·후기 시뮬레이션이 함께 사용하는 3D mesh
- `Mujoco/data_set_*/`: 동작 재생 및 변환 검증용 샘플 데이터

## 나의 담당

- 프로젝트 팀장
- 실제 로봇 URDF를 활용한 MuJoCo 양팔 가상환경 구현
- 카메라 시점 구성과 동작·데이터 수집 파이프라인 사전 검증
- 텔레오퍼레이션 기반 학습 데이터 구축 및 검증

## 출처

이 저장소는 공동 프로젝트 결과물과 개인 개발 내용을 함께 정리한 저장소입니다. 통합한 팀 저장소의 원본은 [IAMJP520/CookingBot](https://github.com/IAMJP520/CookingBot)에서 확인할 수 있습니다.

## License

MuJoCo 관련 코드는 각 디렉터리에 포함된 Apache License 2.0을 따릅니다.
