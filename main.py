
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


def mac(pattern, filter_matrix):
    """입력 패턴과 필터의 MAC 점수를 계산한다."""
    score = 0.0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_matrix[i][j]

    return score


def main():
    cross_score = mac(pattern, cross_filter)
    x_score = mac(pattern, x_filter)

    print("=== Mini NPU Simulator ===")
    print(f"Cross 점수: {cross_score}")
    print(f"X 점수: {x_score}")


if __name__ == "__main__":
    main()
