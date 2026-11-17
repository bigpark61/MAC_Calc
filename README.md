# Mini NPU Simulator

2차원 입력 패턴과 필터의 MAC (Multiply-Accumulate) 연산 점수를 계산하는 간단한 Python 예제입니다.

## 실행 방법

Python 3가 설치되어 있어야 합니다. 프로젝트 폴더에서 다음 명령을 실행하세요.

```powershell
python main.py
```

## 동작 내용

- 십자가 입력 패턴에 십자가 필터와 X 필터를 각각 적용합니다.
- 각 위치의 입력값과 필터값을 곱해 모두 더한 점수를 출력합니다.

예상 출력:

```text
=== Mini NPU Simulator ===
Cross 점수: 5.0
X 점수: 1.0
```
