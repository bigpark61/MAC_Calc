
from main import validate_mac_dimensions

# 정상 3x3 배열
matrix_3 = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

# 정상 5x5 필터
filter_5 = [
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
]

# 테스트 케이스
tests = [
    ("정상 3x3", matrix_3, matrix_3, True),
    ("3x3 vs 5x5", matrix_3, filter_5, False),
    ("행 개수 부족", matrix_3[:2], matrix_3, False),
    ("열 개수 부족", [[1, 0], [0, 1], [1, 0]], matrix_3, False),
    ("빈 배열", [], matrix_3, False)
]

print("=== STEP 9-4 배열 크기 검증 테스트 ===")

passed = 0

for name, matrix, filt, expected in tests:
    try:
        result = validate_mac_dimensions(matrix, filt)
    except ValueError as error:
        result = False
        print(f"{name}: 오류 감지 - {error}")

    status = "PASS" if result == expected else "FAIL"

    if status == "PASS":
        passed += 1

    print(f"검증 결과: {status}\n")

print(f"전체 결과: {passed}/{len(tests)} PASS")
