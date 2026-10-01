"""W8: 실제 증거 유무를 직접 입력받는 제작 준비 체크 실습."""
REQUIRED_ASSETS = frozenset({"api_contract", "real_retrieval", "persistent_db",
                             "authorization_review", "reproducible_start", "evaluation_set"})

def missing_assets(evidence: dict[str, bool]) -> list[str]:
    """필수 준비 항목 중 실행 증거가 없는 항목을 찾는다.

    Args:
        evidence: 실제 기록을 확인한 뒤 입력하는 자산별 준비 여부.
    Returns:
        누락된 항목의 정렬된 이름 목록.
    Raises:
        TypeError: 준비 여부가 bool이 아닌 경우.
    """
    if any(not isinstance(value, bool) for value in evidence.values()):
        raise TypeError("evidence flags must be boolean")
    # 자동 실행 검증기가 아니다. True를 쓰기 전에 연결된 실제 증거를 읽어야 한다.
    return sorted(asset for asset in REQUIRED_ASSETS if evidence.get(asset) is not True)

assert len(missing_assets({})) == 6
assert missing_assets({asset: True for asset in REQUIRED_ASSETS}) == []
print("W8 readiness predicate: passed; actual project readiness not asserted")
