
import json
from pathlib import Path

# data.json 파일 경로
file_path = Path(__file__).with_name("data.json")

print("=== data.json 구조 확인 ===")

if not file_path.exists():
    print("오류: data.json 파일이 없습니다.")

else:
    try:
        with file_path.open(
            "r", encoding="utf-8-sig"
        ) as file:
            data = json.load(file)

        print("\n[최상위 데이터 타입]")
        print(type(data).__name__)

        if isinstance(data, dict):
            print("\n[최상위 키]")
            print(list(data.keys()))

            # 필터 정보
            filters = data.get("filters", {})

            print("\n[필터 정보]")
            if isinstance(filters, dict):
                for key, value in filters.items():
                    print(
                        f"{key}: "
                        f"{type(value).__name__}"
                    )
                    if isinstance(value, dict):
                        print("  하위 키:", list(value.keys()))
            else:
                print("filters 타입:", type(filters).__name__)

            # 패턴 정보
            patterns = data.get("patterns", [])

            print("\n[패턴 정보]")
            print("타입:", type(patterns).__name__)

            if isinstance(patterns, list):
                print("패턴 개수:", len(patterns))

                for i, pattern in enumerate(patterns):
                    if isinstance(pattern, dict):
                        print(
                            f"{i + 1}. "
                            f"N={pattern.get('N')}, "
                            f"expected={pattern.get('expected')}, "
                            f"keys={list(pattern.keys())}"
                        )
            elif isinstance(patterns, dict):
                print("패턴 키:", list(patterns.keys()))

        else:
            print("최상위 구조가 객체(dict)가 아닙니다.")

    except json.JSONDecodeError as error:
        print("JSON 형식 오류:", error)

    except OSError as error:
        print("파일 읽기 오류:", error)

print("\n=== 패턴 상세 구조 ===")

for name, pattern in data["patterns"].items():
    print(f"\n패턴명: {name}")

    if isinstance(pattern, dict):
        for key, value in pattern.items():
            if isinstance(value, list):
                print(f"  {key}: 리스트, 길이={len(value)}")
                if value and isinstance(value[0], list):
                    print(f"  열 개수: {len(value[0])}")
            else:
                print(f"  {key}: {value}")