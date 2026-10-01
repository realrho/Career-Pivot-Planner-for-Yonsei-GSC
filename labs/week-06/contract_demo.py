"""W6: 신뢰된 신원이라는 전제에서 권한/상태 전이를 검사한다."""
def approve_review(role: str, actor_tenant: str, case_tenant: str, status: str) -> str:
    """검토자 역할과 tenant 및 상태 조건을 검사한다.

    Args:
        role: 서버가 검증한 주체의 역할.
        actor_tenant: 서버가 검증한 주체의 tenant.
        case_tenant: DB에 저장된 사례의 tenant.
        status: 저장된 현재 상태.
    Returns:
        허용된 경우 APPROVED 문자열.
    Raises:
        PermissionError: 역할 또는 tenant 경계가 맞지 않는 경우.
        ValueError: 검토 대기 상태가 아닌 경우.
    """
    if role != "reviewer" or actor_tenant != case_tenant:
        raise PermissionError("review not authorized")
    if status != "REVIEW_PENDING":
        raise ValueError("invalid transition")
    return "APPROVED"

assert approve_review("reviewer", "A", "A", "REVIEW_PENDING") == "APPROVED"
for role, tenant, status in [("viewer", "A", "REVIEW_PENDING"),
                             ("reviewer", "B", "REVIEW_PENDING"),
                             ("reviewer", "A", "APPROVED")]:
    try:
        approve_review(role, tenant, "A", status)
    except (PermissionError, ValueError):
        pass
    else:
        raise AssertionError("unsafe approval")
# 실제 인증, DB 저장, 동시 갱신은 이 순수 함수 실습의 검증 범위 밖이다.
print("W6 permission/state predicate: passed")
