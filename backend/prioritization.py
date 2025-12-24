def compute_priority_scores(df):
    df = df.copy()
    df["severity"] = 1
    df["week"] = df["review_date"].dt.to_period("W").astype(str)

    summary = (
        df.groupby(["aspects", "issue"])
        .agg(
            frequency=("issue", "count"),
            avg_confidence=("confidence_score", "mean")
        )
        .reset_index()
    )

    summary["priority_score"] = (
        summary["frequency"] * 0.4 +
        summary["avg_confidence"] * 0.3
    )

    return summary.sort_values("priority_score", ascending=False)
