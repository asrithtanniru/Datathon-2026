def is_duplicate_score(similarity_score: float, threshold: float = 0.92) -> bool:
    return similarity_score > threshold
