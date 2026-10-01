"""W1: 입력 계약을 검증하는 CPU/표준 라이브러리 실습."""
def normalize_text(value: object, max_length: int = 2000) -> str:
    """공백을 제거하고 입력 계약을 검사한다.

    Args:
        value: 호출자가 전달한 원본 값.
        max_length: 허용할 정규화 문자열의 최대 문자 수.
    Returns:
        앞뒤 공백이 제거된 비어 있지 않은 문자열.
    Raises:
        TypeError: 문자열이 아닌 입력인 경우.
        ValueError: 길이 한도가 양수가 아니거나 입력 길이가 범위 밖인 경우.
    """
    if max_length < 1:
        raise ValueError("max_length must be positive")
    if not isinstance(value, str):
        raise TypeError("text must be a string")
    normalized = value.strip()  # 정규화 후 검사해야 공백만 있는 입력도 거부한다.
    if not 1 <= len(normalized) <= max_length:
        raise ValueError("invalid text length")
    return normalized

assert normalize_text("  환불 규정  ") == "환불 규정"
for invalid in ["   ", None]:
    try:
        normalize_text(invalid)
    except (TypeError, ValueError):
        pass
    else:
        raise AssertionError("invalid input accepted")
print("W1 input contract: passed")
