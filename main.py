
# Mission E3 - Mini NPU Simulator
# STEP 3: 2차원 배열 입력, 출력 및 검증


# 1. 3x3 배열 입력 함수
def input_matrix(name):
    matrix = []

    print(f"\n[{name} 입력]")
    print("각 행에 숫자 3개를 공백으로 구분하여 입력하세요.")

    for i in range(3):
        while True:
            try:
                values = input(f"{i + 1}행 입력: ").split()

                # 숫자 개수 검증
                if len(values) != 3:
                    print("오류: 숫자 3개를 입력해야 합니다.")
                    continue

                # 문자열을 정수로 변환
                row = [int(value) for value in values]

                matrix.append(row)
                break

            except ValueError:
                print("오류: 정수만 입력할 수 있습니다.")

    return matrix


# 2. 배열 출력 함수
def print_matrix(matrix, name):
    print(f"\n[{name} 출력]")

    for row in matrix:
        print(" ".join(map(str, row)))


# 3. 배열 검증 함수
def validate_matrix(matrix):
    # 행 개수 확인
    if len(matrix) != 3:
        return False

    for row in matrix:
        # 열 개수 확인
        if len(row) != 3:
            return False

        # 숫자 자료형 확인
        for value in row:
            if type(value) not in (int, float):
                return False

    return True

# 4. MAC 연산 함수
def mac(matrix, filter_matrix):
    total = 0

    for i in range(3):
        for j in range(3):
            total += matrix[i][j] * filter_matrix[i][j]

    return total

# 5. 패턴 필터 정의
FILTER_CROSS = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

FILTER_X = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

EPSILON = 1e-9

# 6. 패턴 판정 함수
def classify_pattern(matrix):
    # Cross 필터 MAC 점수
    score_cross = mac(matrix, FILTER_CROSS)

    # X 필터 MAC 점수
    score_x = mac(matrix, FILTER_X)

    # 점수 차이
    difference = abs(score_cross - score_x)

    # 판정
    if difference <= EPSILON:
        result = "UNDECIDED"
    elif score_cross > score_x:
        result = "Cross"
    else:
        result = "X"

    return score_cross, score_x, result

# 4. 메인 프로그램
def main():
    print("=== Mini NPU Simulator ===")
    print("STEP 3: 2차원 배열 구현")

    # 배열 A 입력
    matrix_a = input_matrix("배열 A")

    # 배열 B 입력
    matrix_b = input_matrix("배열 B")

    # 배열 출력
    print_matrix(matrix_a, "배열 A")
    print_matrix(matrix_b, "배열 B")

    # 배열 검증
    print("\n[배열 검증 결과]")
    print("배열 A:", validate_matrix(matrix_a))
    print("배열 B:", validate_matrix(matrix_b))


    # MAC 연산 수행
    score_a = mac(matrix_a, FILTER_CROSS)
    score_b = mac(matrix_b, FILTER_CROSS)

    print("\n[MAC 연산 결과]")
    print("배열 A 점수:", score_a)
    print("배열 B 점수:", score_b)

    # STEP 5: 패턴 판정
    print("\n[패턴 판정 결과]")

    score_cross_a, score_x_a, result_a = classify_pattern(matrix_a)
    score_cross_b, score_x_b, result_b = classify_pattern(matrix_b)

    print("\n배열 A")
    print("Cross 점수:", score_cross_a)
    print("X 점수:", score_x_a)
    print("최종 판정:", result_a)

    print("\n배열 B")
    print("Cross 점수:", score_cross_b)
    print("X 점수:", score_x_b)
    print("최종 판정:", result_b)

if __name__ == "__main__":
    main()
