
from main import mac

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
    ("정상 3x3", matrix_3, matrix_3, 5),
    ("3x3 vs 5x5", matrix_3, filter_5, None),
    ("행 개수 부족", matrix_3[:2], matrix_3, None),
    ("열 개수 부족", [[1, 0], [0, 1], [1, 0]], matrix_3, None),
    ("빈 배열", [], matrix_3, None)
]

print("=== STEP 9-4-2 MAC 검증 테스트 ===")

passed = 0

for name, matrix, filt, expected in tests:
    try:
        result = mac(matrix, filt)

        if expected is not None and result == expected:
            status = "PASS"
        else:
            status = "FAIL"

        print(f"{name}: MAC 결과={result}")

    except ValueError as error:
        status = "PASS" if expected is None else "FAIL"
        print(f"{name}: 오류 감지 - {error}")

    print(f"검증 결과: {status}\n")

    if status == "PASS":
        passed += 1

print(f"전체 결과: {passed}/{len(tests)} PASS")
