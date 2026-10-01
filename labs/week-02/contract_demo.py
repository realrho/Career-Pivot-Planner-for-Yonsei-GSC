"""W2: 평가 분리의 ID 계약을 검사한다. 모델 학습은 수행하지 않는다."""
def validate_splits(splits: dict[str, set[str]]) -> int:
    """세 데이터 분할에 중복 ID가 없는지 검사한다.

    Args:
        splits: train/dev/holdout 이름과 각 분할의 ID 집합.
    Returns:
        전체 고유 ID 개수.
    Raises:
        ValueError: 필수 분할이 없거나 비어 있거나 ID가 중복된 경우.
    """
    if set(splits) != {"train", "dev", "holdout"}:
        raise ValueError("three splits required")
    seen: set[str] = set()
    for name, identifiers in splits.items():
        if not identifiers or seen.intersection(identifiers):
            raise ValueError(f"empty or overlapping split: {name}")
        seen.update(identifiers)
    return len(seen)

assert validate_splits({"train": {"a"}, "dev": {"b"}, "holdout": {"c"}}) == 3
try:
    validate_splits({"train": {"a"}, "dev": {"a"}, "holdout": {"c"}})
except ValueError:
    pass
else:
    raise AssertionError("leakage accepted")
# ID 분리만으로 문서/시나리오 의미 중복까지 검증한 것은 아니다.
print("W2 split-ID contract: passed")
