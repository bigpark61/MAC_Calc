
# Mission 3 - STEP 1 00
# 2차원 배열과 MAC 연산

# 십자가 필터
cross_filter = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

# X 필터
x_filter = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

# 입력 패턴: 십자가
pattern = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

def input_matrix(name):
    """3x3 배열을 사용자로부터 입력받는다."""

    matrix = []

    print(f"\n{name} 입력 (3행, 각 행에 숫자 3개)")

    for i in range(3):
        while True:
            try:
                line = input(f"{i + 1}행: ")
                row = [float(x) for x in line.split()]

                if len(row) != 3:
                    print("입력 오류: 숫자 3개를 입력하세요.")
                    continue

                matrix.append(row)
                break

            except ValueError:
                print("입력 오류: 숫자만 입력하세요.")

    return matrix


def mac(pattern, filter_matrix):
    """입력 패턴과 필터의 MAC 점수를 계산한다."""
    score = 0.0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_matrix[i][j]

    return score


def main():
    print("=== Mini NPU Simulator ===")

    filter_a = input_matrix("필터 A")

    print("\n입력된 필터 A:")
    for row in filter_a:
        print(row)


if __name__ == "__main__":
    main()

