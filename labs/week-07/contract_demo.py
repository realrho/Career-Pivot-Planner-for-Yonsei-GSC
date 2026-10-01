"""W7: 에이전트 도구 호출을 제한하는 순수 함수 실습."""
def bounded_workflow(actions: list[str], max_steps: int = 3) -> str:
    """허용된 도구만 최대 단계 수 안에서 처리한다.

    Args:
        actions: 모델이 제안했다고 가정한 도구 이름의 fixture 목록.
        max_steps: 허용할 최대 도구 개수.
    Returns:
        완료 시 COMPLETED, review 요청 시 REVIEW_PENDING.
    Raises:
        ValueError: 최대 단계가 양수가 아니거나 횟수 초과인 경우.
        PermissionError: 허용 목록 밖의 도구인 경우.
    """
    if max_steps < 1 or len(actions) > max_steps:
        raise ValueError("step budget exceeded")
    for action in actions:
        if action not in {"retrieve", "validate", "request_review"}:
            raise PermissionError("tool not allowed")
        if action == "request_review":
            return "REVIEW_PENDING"  # 검토 요청은 자동 승인과 다르다.
    return "COMPLETED"

assert bounded_workflow(["retrieve", "validate", "request_review"]) == "REVIEW_PENDING"
for actions in [["approve"], ["retrieve"] * 4]:
    try:
        bounded_workflow(actions)
    except (PermissionError, ValueError):
        pass
    else:
        raise AssertionError("unbounded or unauthorized action")
print("W7 workflow fixture: passed; real agent/deployment not validated")
