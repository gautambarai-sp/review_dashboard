ASPECT_KEYWORDS = {
    "Food Quality": ["food", "taste", "cold", "oily", "portion", "quality"],
    "Service / Staff": ["staff", "service", "slow", "rude", "waiter"],
    "Ambience / Seating": ["ambience", "seating", "space", "crowded", "clean"],
    "Pricing": ["price", "pricing", "expensive", "overpriced", "value"]
}

def detect_aspects(text: str):
    aspects = []
    for aspect, words in ASPECT_KEYWORDS.items():
        if any(w in text for w in words):
            aspects.append(aspect)
    return aspects


def extract_issue(aspect: str, text: str):
    if aspect == "Food Quality":
        if "cold" in text:
            return "Food served cold"
        if "oily" in text:
            return "Food too oily"
        return "Food quality issue"

    if aspect == "Service / Staff":
        if "slow" in text:
            return "Slow service"
        if "rude" in text:
            return "Staff behavior issue"
        return "Service issue"

    if aspect == "Ambience / Seating":
        if "space" in text or "crowded" in text:
            return "Seating space issue"
        return "Ambience issue"

    if aspect == "Pricing":
        if "expensive" in text or "overpriced" in text:
            return "Pricing feels expensive"
        return "Pricing concern"

    return "General issue"
