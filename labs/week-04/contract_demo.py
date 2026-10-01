"""W4: 다중 정답 검색의 Recall@k와 첫 정답 역순위를 계산한다."""
def retrieval_metrics(ranked_ids: list[str], gold_ids: set[str], k: int) -> tuple[float, float]:
    """하나의 질문에 대한 검색 지표를 계산한다.

    Args:
        ranked_ids: 높은 순위부터 나열한 중복 없는 검색 ID.
        gold_ids: 사람이 정한 정답 근거 ID 집합.
        k: 평가할 상위 검색 개수.
    Returns:
        (Recall@k, 상위 k 안 첫 정답의 역순위). 정답 미검색이면 역순위 0.
    Raises:
        ValueError: k가 양수가 아니거나 gold가 없거나 검색 ID가 중복된 경우.
    """
    if k < 1 or not gold_ids or len(set(ranked_ids)) != len(ranked_ids):
        raise ValueError("invalid metric input")
    top_ids = ranked_ids[:k]
    recall = len(set(top_ids) & gold_ids) / len(gold_ids)
    # 질문별 역순위의 평균을 내면 MRR@k가 된다.
    reciprocal_rank = next((1 / rank for rank, item in enumerate(top_ids, 1)
                            if item in gold_ids), 0.0)
    return recall, reciprocal_rank

assert retrieval_metrics(["x", "a", "y"], {"a", "b"}, 3) == (0.5, 0.5)
assert retrieval_metrics(["x"], {"a"}, 1) == (0.0, 0.0)
print("W4 retrieval arithmetic: passed")
