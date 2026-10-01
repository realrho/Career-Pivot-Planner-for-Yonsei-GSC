"""W3: 가상 단가로 토큰 비용을 계산한다. 실제 청구/성능 결과가 아니다."""
from decimal import Decimal

def token_cost(input_tokens: int, output_tokens: int,
               input_per_million: Decimal, output_per_million: Decimal) -> Decimal:
    """입력/출력 토큰의 가상 사용료 합계를 계산한다.

    Args:
        input_tokens: 입력 토큰 개수.
        output_tokens: 출력 토큰 개수.
        input_per_million: 입력 백만 토큰당 가상 단가.
        output_per_million: 출력 백만 토큰당 가상 단가.
    Returns:
        같은 통화 단위의 비용. 검색/재시도/저장 비용은 제외한다.
    Raises:
        ValueError: 개수 또는 단가가 음수인 경우.
    """
    if min(input_tokens, output_tokens, input_per_million, output_per_million) < 0:
        raise ValueError("negative usage or price")
    # 이진 부동소수점 반올림 영향을 줄이기 위해 Decimal로 계산한다.
    million = Decimal(1_000_000)
    return (Decimal(input_tokens) * input_per_million
            + Decimal(output_tokens) * output_per_million) / million

assert token_cost(2000, 300, Decimal("1"), Decimal("4")) == Decimal("0.0032")
print("W3 fictional token cost:", token_cost(2000, 300, Decimal("1"), Decimal("4")))
