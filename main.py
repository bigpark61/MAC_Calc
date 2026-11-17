

# Mission E3 - Mini NPU Simulator
# STEP 6: 사용자 입력 모드 구현

EPSILON = 1e-9


# 1. 3x3 배열 입력
def input_matrix(name):
    matrix = []

    print(f"\n[{name} 입력]")
    print("각 행에 숫자 3개를 공백으로 구분하여 입력하세요.")

    for i in range(3):
        while True:
            try:
                values = input(f"{i + 1}행 입력: ").split()

                if len(values) != 3:
                    print("오류: 숫자 3개를 입력하세요.")
                    continue

                row = [int(value) for value in values]
                matrix.append(row)
                break

            except ValueError:
                print("오류: 정수만 입력할 수 있습니다.")

    return matrix


# 2. 배열 출력
def print_matrix(matrix, name):
    print(f"\n[{name}]")
    for row in matrix:
        print(" ".join(map(str, row)))


# 3. 배열 크기 검증
def validate_matrix(matrix, size=3):
    if len(matrix) != size:
        return False

    for row in matrix:
        if len(row) != size:
            return False

        for value in row:
            if type(value) not in (int, float):
                return False

    return True


# 4. MAC 연산
def mac(matrix, filter_matrix):
    total = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            total += matrix[i][j] * filter_matrix[i][j]

    return total


# 5. 두 MAC 점수 비교
def compare_scores(score_a, score_b):
    if abs(score_a - score_b) <= EPSILON:
        return "UNDECIDED"

    elif score_a > score_b:
        return "A"

    else:
        return "B"


# 6. 사용자 입력 모드
def user_input_mode():
    print("\n=== 사용자 입력 모드 (3x3) ===")

    # 배열 A, B 입력
    matrix_a = input_matrix("배열 A")
    matrix_b = input_matrix("배열 B")

    # 필터 입력
    filter_matrix = input_matrix("필터 F")

    # 입력 검증
    if not all(validate_matrix(m) for m in
               [matrix_a, matrix_b, filter_matrix]):
        print("배열 크기 또는 데이터 오류")
        return

    # 입력 데이터 출력
    print_matrix(matrix_a, "배열 A")
    print_matrix(matrix_b, "배열 B")
    print_matrix(filter_matrix, "필터 F")

    # MAC 계산
    score_a = mac(matrix_a, filter_matrix)
    score_b = mac(matrix_b, filter_matrix)

    # 점수 비교
    result = compare_scores(score_a, score_b)

    # 결과 출력
    print("\n=== MAC 연산 결과 ===")
    print("A 점수:", score_a)
    print("B 점수:", score_b)
    print("판정:", result)


# 7. 메인 메뉴
def main():
    print("\n=== Mini NPU Simulator ===")

    print("\n[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    choice = input("선택: ").strip()

    if choice == "1":
        user_input_mode()

    elif choice == "2":
        print("\ndata.json 분석은 STEP 7에서 구현합니다.")

    else:
        print("잘못된 메뉴 선택입니다.")


if __name__ == "__main__":
    main()
