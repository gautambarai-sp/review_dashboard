def rating_to_sentiment(rating: int) -> str:
    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    return "negative"


POSITIVE_WORDS = [
    "good", "great", "amazing", "love", "tasty",
    "quick", "friendly", "excellent", "perfect"
]

NEGATIVE_WORDS = [
    "bad", "worst", "cold", "late", "delay",
    "rude", "slow", "terrible", "oily"
]


def text_to_sentiment(text: str) -> str:
    pos = sum(w in text for w in POSITIVE_WORDS)
    neg = sum(w in text for w in NEGATIVE_WORDS)
    if pos > neg:
        return "positive"
    elif neg > pos:
        return "negative"
    return "neutral"


def final_text_sentiment(clean_text, rule_sentiment, ml_sentiment):
    if ml_sentiment in ["positive", "negative"]:
        return ml_sentiment
    return rule_sentiment


def hybrid_sentiment(rating_sentiment, text_sentiment):
    if rating_sentiment == text_sentiment:
        return rating_sentiment
    if text_sentiment != "neutral":
        return text_sentiment
    return rating_sentiment


def confidence_score(review_text, verified, rating_sentiment, text_sentiment):
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
