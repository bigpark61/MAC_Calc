

# Mission E3 - Mini NPU Simulator
# STEP 6: 사용자 입력 모드 구현
import time
import json
from pathlib import Path


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


# STEP 8: MAC 연산시간 측정
def measure_mac_time(matrix, filter_matrix, repeat=10):

    # 배열 크기
    n = len(matrix)

    # 크기 검증
    if not validate_matrix(matrix, n):
        raise ValueError("입력 배열 크기 오류")

    if not validate_matrix(filter_matrix, n):
        raise ValueError("필터 크기 오류")

    # 사전 실행: 초기 실행 영향 완화
    mac(matrix, filter_matrix)

    elapsed_times = []

    # MAC 연산 반복 측정
    for _ in range(repeat):

        start_time = time.perf_counter()

        mac(matrix, filter_matrix)

        end_time = time.perf_counter()

        elapsed_ms = (end_time - start_time) * 1000

        elapsed_times.append(elapsed_ms)

    # 평균 시간
    average_ms = sum(elapsed_times) / repeat

    # 원소별 곱셈 횟수
    operation_count = n * n

    return average_ms, operation_count

# 5. 두 MAC 점수 비교
def compare_scores(score_a, score_b):
    if abs(score_a - score_b) <= EPSILON:
        return "UNDECIDED"

    elif score_a > score_b:
        return "A"

    else:
        return "B"


# STEP 7-2: JSON 데이터 로드
def load_json_data():
    file_path = Path(__file__).with_name("data.json")

    try:
        with file_path.open(
            "r", encoding="utf-8-sig"
        ) as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print("오류: JSON 최상위 구조가 올바르지 않습니다.")
            return None

        if not isinstance(data.get("filters"), dict):
            print("오류: filters 구조가 올바르지 않습니다.")
            return None

        if not isinstance(data.get("patterns"), dict):
            print("오류: patterns 구조가 올바르지 않습니다.")
            return None

        print("\n[data.json 로드 성공]")
        print("필터 크기:", list(data["filters"].keys()))
        print("패턴 개수:", len(data["patterns"]))

        return data

    except FileNotFoundError:
        print("오류: data.json 파일을 찾을 수 없습니다.")
    except json.JSONDecodeError as error:
        print("JSON 형식 오류:", error)
    except OSError as error:
        print("파일 읽기 오류:", error)

    return None

# STEP 7-4: JSON 패턴 판정
def classify_json_pattern(matrix, filter_cross, filter_x):

    score_cross = mac(matrix, filter_cross)
    score_x = mac(matrix, filter_x)

    if abs(score_cross - score_x) <= EPSILON:
        result = "UNDECIDED"
    elif score_cross > score_x:
        result = "Cross"
    else:
        result = "X"

    return score_cross, score_x, result

# STEP 7-5: 판정 라벨 정규화
def normalize_label(label):
    label = str(label).strip().lower()

    if label in ("+", "cross"):
        return "Cross"

    elif label == "x":
        return "X"

    elif label == "undecided":
        return "UNDECIDED"

    return "UNKNOWN"

# STEP 7-3: JSON 패턴 및 필터 추출
def extract_json_patterns(data):
    total_count = 0
    pass_count = 0
    fail_count = 0
    failed_cases = []

    filters = data["filters"]
    patterns = data["patterns"]

    print("\n=== JSON 패턴 및 필터 추출 ===")

    for pattern_name, pattern in patterns.items():

        # 패턴 입력 배열과 정답
        matrix = pattern["input"]
        expected = pattern["expected"]

        # 배열 크기
        n = len(matrix)
        size_key = f"size_{n}"

        # 크기에 맞는 필터 선택
        filter_cross = filters[size_key]["cross"]
        filter_x = filters[size_key]["x"]

        # 배열 검증
        valid_input = validate_matrix(matrix, n)
        valid_cross = validate_matrix(filter_cross, n)
        valid_x = validate_matrix(filter_x, n)

        print(f"\n[패턴: {pattern_name}]")
        print(f"배열 크기: {n}x{n}")
        print(f"예상 판정: {expected}")
        print(f"입력 배열 검증: {valid_input}")
        print(f"Cross 필터 검증: {valid_cross}")
        print(f"X 필터 검증: {valid_x}")

        # 배열 검증 실패 시 연산하지 않음
        if not (valid_input and valid_cross and valid_x):
            print("오류: 배열 또는 필터 크기 불일치")
            continue


        # MAC 연산 및 판정
        score_cross, score_x, result = classify_json_pattern(
            matrix, filter_cross, filter_x
        )

        print("\n[MAC 분석 결과]")
        print("Cross 점수:", score_cross)
        print("X 점수:", score_x)
        print("최종 판정:", result)

        # STEP 7-5: 예상 판정과 실제 판정 비교
        expected_label = normalize_label(expected)

        if result == expected_label:
            status = "PASS"
        else:
            status = "FAIL"

        print("\n[판정 검증]")
        print("예상 판정:", expected_label)
        print("실제 판정:", result)
        print("검증 결과:", status)

        total_count += 1

        if status == "PASS":
            pass_count += 1
        else:
            fail_count += 1
            failed_cases.append({
                "name": pattern_name,
                "expected": expected_label,
                "actual": result,
                "cross": score_cross,
                "x": score_x
            })

    print("\n=== 전체 테스트 결과 요약 ===")
    print("총 테스트:", total_count)
    print("PASS:", pass_count)
    print("FAIL:", fail_count)

    if failed_cases:
        print("\n[실패 케이스]")

        for case in failed_cases:
            print(
                f"{case['name']}: "
                f"예상={case['expected']}, "
                f"실제={case['actual']}"
            )


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

# STEP 8: 배열 크기별 성능 분석
def analyze_mac_performance(data):

    print("\n=== MAC 성능 분석 ===")
    print("크기       평균 시간(ms)     연산 횟수")
    print("-" * 43)

    # 3x3 테스트 배열
    matrix_3 = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]

    filter_3 = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]

    # 3x3 측정
    avg_ms, operations = measure_mac_time(
        matrix_3, filter_3, repeat=10
    )

    print(f"{'3x3':<10} {avg_ms:<17.6f} {operations}")

    # JSON의 크기별 필터 활용
    for n in [5, 13, 25]:

        size_key = f"size_{n}"

        filter_cross = data["filters"][size_key]["cross"]

        # 필터 자체를 입력 배열로 사용하여
        # 크기별 MAC 성능 측정
        avg_ms, operations = measure_mac_time(
            filter_cross, filter_cross, repeat=10
        )

        print(
            f"{n}x{n:<7} "
            f"{avg_ms:<17.6f} "
            f"{operations}"
        )

    print("\n시간복잡도: O(N^2)")

# STEP 7-2: JSON 분석 모드
def json_analysis_mode():
    data = load_json_data()

    if data is None:
        return

    print("\n[JSON 분석 준비 완료]")
    print("필터:", len(data["filters"]), "종류")
    print("패턴:", len(data["patterns"]), "개")

    # STEP 7-3
    extract_json_patterns(data)
    # STEP 8: MAC 성능 측정
    analyze_mac_performance(data)

# 7. 메인 메뉴

# STEP 9-1: 메뉴 입력 예외 처리
def main():

    while True:
        print("\n=== Mini NPU Simulator ===")

        print("\n[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("0. 종료")

        try:
            choice = input("선택: ").strip()

        except (EOFError, KeyboardInterrupt):
            print("\n프로그램을 종료합니다.")
            break

        if choice == "1":
            user_input_mode()

        elif choice == "2":
            json_analysis_mode()

        elif choice == "0":
            print("\n프로그램을 종료합니다.")
            break

        else:
            print("\n[입력 오류]")
            print("0, 1, 2 중 하나를 선택하세요.")



if __name__ == "__main__":
    main()
