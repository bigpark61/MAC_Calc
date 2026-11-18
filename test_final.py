
# STEP 9-5-5: Mission E3 최종 자동 테스트

import json
import main
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from main import (
    mac,
    validate_mac_dimensions,
    normalize_label,
    normalize_filter_keys,
    classify_json_pattern,
    measure_mac_time,
    user_input_mode,
)

passed = 0
failed = 0


def check(name, condition):
    global passed, failed

    if condition:
        passed += 1
        print(f"[PASS] {name}")
    else:
        failed += 1
        print(f"[FAIL] {name}")


print("=== Mission E3 최종 통합 테스트 ===")

# 1. 정상 MAC 연산
matrix = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0],
]

check("3x3 MAC 연산", mac(matrix, matrix) == 5)

# 2. 배열 크기 검증
check(
    "정상 배열 크기 검증",
    validate_mac_dimensions(matrix, matrix) is True
)

# 3. 크기 불일치 오류
try:
    mac(matrix, [[1, 0], [0, 1]])
    check("크기 불일치 오류 처리", False)
except ValueError:
    check("크기 불일치 오류 처리", True)

# 4. 라벨 정규화
check("Cross 라벨 정규화", normalize_label("+") == "Cross")
check("X 라벨 정규화", normalize_label("x") == "X")

normalized_filters = normalize_filter_keys({
    "size_3": {"+": matrix, " X ": matrix}
})
check(
    "필터 키 별칭 정규화",
    normalized_filters == {"size_3": {"cross": matrix, "x": matrix}},
)

try:
    normalize_filter_keys({"size_3": {"cross": matrix, "+": matrix}})
    check("중복 필터 키 거부", False)
except ValueError:
    check("중복 필터 키 거부", True)

# 5. epsilon 판정
tie_matrix = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
_, _, result = classify_json_pattern(
    tie_matrix, matrix, matrix
)
check("UNDECIDED 판정", result == "UNDECIDED")

# 6. JSON 파일 로드 및 구조 확인
path = Path(__file__).resolve().parent / "data.json"

try:
    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    valid_json = (
        isinstance(data, dict)
        and isinstance(data.get("filters"), dict)
        and isinstance(data.get("patterns"), dict)
    )

    check("JSON 데이터 구조", valid_json)

    if valid_json:
        check("JSON 패턴 6개", len(data["patterns"]) == 6)
    else:
        check("JSON 패턴 6개", False)

except (OSError, json.JSONDecodeError) as e:
    print(f"JSON 오류: {e}")
    check("JSON 데이터 구조", False)
    check("JSON 패턴 6개", False)

# 7. 성능 측정
avg_ms, operations = measure_mac_time(
    matrix, matrix, repeat=10
)

check(
    "MAC 성능 측정",
    avg_ms >= 0 and operations == 9
)

# 8. 사용자 모드의 순수 MAC 시간 측정
input_rows = [
    "0 1 0", "1 1 1", "0 1 0",
    "0 1 0", "1 1 1", "0 1 0",
    "0 1 0", "1 1 1", "0 1 0",
]
timer_calls = []
validation_calls = []
output = StringIO()
original_validate = main.validate_mac_dimensions


def track_validation(matrix, filter_matrix):
    validation_calls.append(len(timer_calls))
    return original_validate(matrix, filter_matrix)


def fake_perf_counter():
    timer_calls.append(None)
    return 1 + (len(timer_calls) - 1) * 0.001


with patch("builtins.input", side_effect=input_rows), \
        patch("main.validate_mac_dimensions", side_effect=track_validation), \
        patch("main.time.perf_counter", side_effect=fake_perf_counter), \
        redirect_stdout(output):
    user_input_mode()

check(
    "사용자 모드 측정에서 검증 제외",
    validation_calls == [0, 0]
    and len(timer_calls) == 2
    and "연산 시간: 1.000000 ms" in output.getvalue(),
)

# 9. 최종 결과
print("\n=== 최종 통합 테스트 결과 ===")
print("총 테스트:", passed + failed)
print("PASS:", passed)
print("FAIL:", failed)

if failed == 0:
    print("최종 통합 테스트 성공")
else:
    print("최종 통합 테스트 실패")
