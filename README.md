# Mission E3 — Mini NPU Simulator

> Windows + Visual Studio Code 환경에서 Python으로 구현한 2차원 배열 기반 MAC(Multiply–Accumulate) 연산 및 패턴 분석 시뮬레이터

## 1. 프로젝트 개요

본 프로젝트는 2차원 배열에 대한 **원소별 곱셈 및 누산(MAC)** 연산을 Python으로 직접 구현하고, 입력 배열과 필터의 점수를 비교하여 패턴을 판정하는 학습용 Mini NPU 시뮬레이터입니다. 사용자 입력 모드와 `data.json` 분석 모드를 제공하며, 입력 검증·예외 처리·성능 측정·자동 테스트를 수행합니다.

### 주요 기능

- 3×3 배열 A, B 및 필터 F를 사용자가 직접 입력
- MAC 연산을 이용한 점수 계산과 A/B 비교
- Cross 및 X 필터 기반 JSON 패턴 분석
- 점수 차이가 `epsilon` 이하인 경우 `UNDECIDED` 판정
- JSON 예상 판정과 실제 판정의 PASS/FAIL 집계
- 배열 크기 검증 및 파일·메뉴 입력 오류 처리
- 3×3, 5×5, 13×13, 25×25 배열의 연산 횟수와 실행시간 측정

## 2. 개발 및 실행 환경

| 구분 | 환경 |
|---|---|
| 운영체제 | Windows |
| 개발 도구 | Visual Studio Code (VS Code) |
| 언어 | Python 3 |
| 터미널 | PowerShell |
| 작업 경로(개발 예시) | `C:\Temp\E3_Mini_NPU` |
| 데이터 형식 | JSON |

본 프로젝트는 **WSL/Ubuntu 없이 Windows 환경에서 실행**합니다. 표준 라이브러리를 이용한 구현을 기준으로 하며, 별도의 패키지 설치가 필요한 경우 실제 `main.py`의 import 문을 확인해 추가해야 합니다.

## 3. 프로젝트 파일 구성

```text
E3_Mini_NPU/
├── main.py               # 메뉴, MAC 연산, JSON 분석, 성능 측정
├── data.json             # 필터와 패턴 데이터
├── test_dimensions.py    # 배열·필터 크기 검증
├── test_mac.py           # MAC 정상/오류 입력 테스트
├── test_final.py         # 최종 자동 통합 테스트
└── README.md             # 프로젝트 설명서
```

개발 중 생성한 `data_backup.json`, `data_temp.json` 등 백업·임시 파일은 제출 대상에서 제외할 수 있습니다.

## 4. 실행 방법

1. VS Code에서 프로젝트 폴더를 엽니다.
2. **Terminal → New Terminal**을 선택하여 PowerShell을 실행합니다.
3. 다음 명령을 입력합니다.

```powershell
cd C:\Temp\E3_Mini_NPU
python --version
python main.py
```

실행 메뉴:

```text
=== Mini NPU Simulator ===

[모드 선택]
1. 사용자 입력 (3x3)
2. data.json 분석
0. 종료
선택:
```

- **1:** 배열 A, 배열 B, 필터 F를 3행씩 입력하고 MAC 점수와 최종 판정을 확인합니다.
- **2:** `data.json`을 읽어 패턴별 MAC 판정·예상값 비교·성능 분석을 실행합니다.
- **0:** 프로그램을 종료합니다.

메뉴에서 잘못된 값(`3`, `abc`, 빈 입력, `-1` 등)을 입력하면 오류를 안내하고 메뉴로 돌아옵니다.

### 사용자 입력 모드 예시

배열 A (X 패턴):

```text
1 0 1
0 1 0
1 0 1
```

배열 B (Cross 패턴):

```text
0 1 0
1 1 1
0 1 0
```

필터 F (Cross 패턴):

```text
0 1 0
1 1 1
0 1 0
```

실행 결과:

```text
=== MAC 연산 결과 ===
A 점수: 1
B 점수: 5
판정: B
```

## 5. MAC 연산 알고리즘

MAC(Multiply–Accumulate)은 배열과 필터의 같은 위치 원소를 곱한 후 결과를 모두 더하는 연산입니다.

수학적으로 N×N 배열 A와 필터 F에 대해 다음과 같이 정의합니다.

\[
\operatorname{MAC}(A,F)=\sum_{i=0}^{N-1}\sum_{j=0}^{N-1} A_{ij}F_{ij}
\]

핵심 구현 구조:

```python
def mac(matrix, filter_matrix):
    validate_mac_dimensions(matrix, filter_matrix)
    total = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            total += matrix[i][j] * filter_matrix[i][j]
    return total
```

이 함수는 입력 배열과 필터의 크기를 검증한 후 MAC을 수행합니다. 3×3 입력 배열과 5×5 필터처럼 크기가 불일치하면 `ValueError`를 발생시켜 연산을 차단합니다.

## 6. epsilon 판정 및 UNDECIDED

두 MAC 점수의 차이가 매우 작을 때 무리하게 한쪽을 선택하지 않도록 `epsilon` 임계값을 적용합니다.

- `|score_cross - score_x| <= epsilon`: `UNDECIDED`
- `score_cross > score_x`이고 차이가 임계값보다 큼: `Cross`
- `score_x > score_cross`이고 차이가 임계값보다 큼: `X`

`epsilon`의 실제 설정값은 제출 시 `main.py`의 값을 기준으로 확인합니다. 이 판정 방식은 동점 또는 근소한 점수 차이를 보류하는 의도적인 규칙입니다.

## 7. data.json 분석 결과

`data.json`은 최상위에 `meta`, `filters`, `patterns`를 포함합니다. 분석 대상 패턴은 총 6개입니다.

| 패턴 | 예상 판정 | 실제 판정 | 결과 |
|---|---|---|---|
| `size_5_1` | X | UNDECIDED | FAIL |
| `size_5_2` | Cross | Cross | PASS |
| `size_13_1` | X | X | PASS |
| `size_13_2` | Cross | UNDECIDED | FAIL |
| `size_25_1` | X | UNDECIDED | FAIL |
| `size_25_2` | Cross | Cross | PASS |

```text
=== 전체 테스트 결과 요약 ===
총 테스트: 6
PASS: 3
FAIL: 3
```

### 실패 원인 분석

`size_5_1`, `size_13_2`, `size_25_1`은 JSON에 지정된 예상값이 X 또는 Cross이지만, **원래 MAC 점수와 epsilon 판정 기준**을 적용하면 `UNDECIDED`가 나옵니다. 즉, 해당 3건은 예상 라벨과 실제 판정이 일치하지 않습니다.

이 결과를 감추거나 정답에 맞추기 위해 알고리즘을 임의 변경하지 않았습니다. 향후 개선 시에는 `epsilon` 값의 타당성, 패턴 데이터의 구분력, 필터 설계 및 기대 라벨의 적절성을 별도로 검토할 수 있습니다.

> **주의:** 위의 JSON 패턴 판정 3 PASS / 3 FAIL은 아래의 프로그램 기능 자동 통합 테스트 9 PASS / 0 FAIL과 서로 다른 검증 결과입니다.

## 8. 성능 측정 및 시간복잡도

Python의 `time.perf_counter()`를 이용하여 MAC 연산을 반복 측정하고 평균 실행시간을 계산했습니다. 아래 시간은 STEP 9-5-1에서 확인한 실행 예시이며, PC 상태와 실행 시점에 따라 변동됩니다.

| 배열 크기 | 평균 실행시간(ms) | 원소별 곱셈 횟수 |
|---|---:|---:|
| 3×3 | 0.003310 | 9 |
| 5×5 | 0.006960 | 25 |
| 13×13 | 0.035900 | 169 |
| 25×25 | 0.124990 | 625 |

N×N 배열에 대해 모든 원소를 한 번씩 방문하므로 곱셈 횟수는 **N²**이며, 이중 반복문의 이론적 시간복잡도는 **O(N²)**입니다. 예를 들어 5×5에서 25×25로 커지면 한 변의 길이는 5배, 곱셈 횟수는 25배가 됩니다.

`mac()` 함수에 배열 크기 검증이 추가된 이후의 측정시간에는 **검증 수행시간도 포함**됩니다. 따라서 위 수치를 순수 MAC 연산만의 시간으로 해석해서는 안 됩니다.

## 9. 예외 처리 및 기능 검증

| 검증 영역 | 내용 |
|---|---|
| 메뉴 입력 | 잘못된 숫자·문자·빈 입력·음수 처리, 메뉴 재출력, 정상 종료 |
| 배열 입력 | 숫자 부족·초과, 문자·소수 입력 오류 처리 |
| JSON 파일 | 파일 없음, 문법 오류, 필수 키 누락 처리 |
| 배열/필터 | 정사각형 여부, 크기 일치 여부, 빈 배열 검사 |
| 회귀 테스트 | 기존 JSON 6개 패턴 결과 유지 |
| 성능 | 3×3, 5×5, 13×13, 25×25 실행시간 및 연산 횟수 출력 |

배열 크기 검증과 MAC 함수 테스트는 각각 5건 모두 통과했습니다.

## 10. 최종 자동 통합 테스트

다음 명령으로 최종 테스트를 실행합니다.

```powershell
python test_dimensions.py
python test_mac.py
python test_final.py
```

`test_final.py`의 검증 결과:

```text
=== Mission E3 최종 통합 테스트 ===
[PASS] 3x3 MAC 연산
[PASS] 정상 배열 크기 검증
[PASS] 크기 불일치 오류 처리
[PASS] Cross 라벨 정규화
[PASS] X 라벨 정규화
[PASS] UNDECIDED 판정
[PASS] JSON 데이터 구조
[PASS] JSON 패턴 6개
[PASS] MAC 성능 측정

=== 최종 통합 테스트 결과 ===
총 테스트: 9
PASS: 9
FAIL: 0
최종 통합 테스트 성공
```

**최종 결과: 자동 통합 테스트 9/9 PASS.** 이 결과는 프로그램의 핵심 기능과 예외 처리 일부가 정상 동작함을 보여줍니다. 모든 가능한 입력을 검증했다는 뜻은 아닙니다.

## 11. 구현 성과 및 개선 방향

**구현 성과**

- Python으로 2차원 배열과 MAC 연산을 직접 구현
- 입력 배열·필터 크기 검증과 사용자 오류 처리 구현
- JSON 패턴 분석 및 예상 라벨 비교 자동화
- epsilon을 이용한 보류 판정(`UNDECIDED`) 구현
- 배열 크기에 따른 연산 횟수와 실행시간 측정
- 최종 자동 통합 테스트 9/9 PASS 달성

**향후 개선 방향**

- 반복 횟수를 늘려 성능 측정 편차 완화
- 배열 검증시간과 순수 MAC 계산시간 분리
- epsilon 값과 필터 설계의 영향 분석
- 테스트 케이스 확장 및 자동화

---

**Mission E3 — Mini NPU Simulator**  
실행 환경: Windows / VS Code / Python
