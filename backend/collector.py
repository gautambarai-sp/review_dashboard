import pandas as pd
from datetime import datetime
import uuid
import os

FILE = "data/collected_reviews.csv"

def save_review(restaurant_name, rating, review_text, verified):
    row = {
        "review_id": str(uuid.uuid4()),
        "restaurant_name": restaurant_name,
        "rating": rating,
        "review_text": review_text,
        "review_date": datetime.utcnow().date().isoformat(),
        "platform": "Internal",
        "verified_visit": verified
    }

    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(FILE, index=False)
