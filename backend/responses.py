RESPONSE_TEMPLATES = {
    "Food Quality": {
        "negative": (
            "Thank you for your feedback. We’re sorry about the food quality issue. "
            "{issue}. We’ve shared this with our kitchen team for improvement."
        )
    },
    "Service / Staff": {
        "negative": (
            "Thank you for bringing this to our attention. "
            "{issue}. We’re addressing this with our team."
        )
    },
    "Ambience / Seating": {
        "negative": (
            "Thank you for your feedback. {issue}. "
            "We’ll work on improving this experience."
        )
    },
    "Pricing": {
        "negative": (
            "Thank you for sharing your concern. {issue}. "
            "We continuously review pricing to ensure value."
        )
    }
}

def generate_response(aspect, sentiment, issue):
    return RESPONSE_TEMPLATES.get(
        aspect, {}
    ).get(
        sentiment,
        "Thank you for your feedback. We appreciate your time."
    ).format(issue=issue)
