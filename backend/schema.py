# ----------------------------
# Rating-based sentiment
# ----------------------------
def rating_to_sentiment(rating: int) -> str:
    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    else:
        return "negative"


# ----------------------------
# Text-based sentiment (rule-based MVP)
# ----------------------------
POSITIVE_WORDS = [
    "good", "great", "amazing", "love", "tasty",
    "quick", "friendly", "excellent", "perfect"
]

NEGATIVE_WORDS = [
    "bad", "worst", "cold", "late", "delay",
    "rude", "slow", "terrible", "oily"
]


def text_to_sentiment(text: str) -> str:
    pos = sum(word in text for word in POSITIVE_WORDS)
    neg = sum(word in text for word in NEGATIVE_WORDS)

    if pos > neg:
        return "positive"
    elif neg > pos:
        return "negative"
    else:
        return "neutral"


# ----------------------------
# Hybrid sentiment resolver
# ----------------------------
def hybrid_sentiment(rating_sentiment: str, text_sentiment: str) -> str:
    if rating_sentiment == text_sentiment:
        return rating_sentiment

    # Trust text more if it's clearly positive/negative
    if text_sentiment != "neutral":
        return text_sentiment

    return rating_sentiment


# ----------------------------
# Confidence score engine
# ----------------------------
def confidence_score(
    review_text: str,
    verified: bool,
    rating_sentiment: str,
    text_sentiment: str
) -> int:

    score = 50
    words = review_text.split()

    if verified:
        score += 20

    if len(words) > 20:
        score += 10
    elif len(words) < 5:
        score -= 20

    if rating_sentiment == text_sentiment:
        score += 10
    else:
        score -= 10

    return max(0, min(100, score))
