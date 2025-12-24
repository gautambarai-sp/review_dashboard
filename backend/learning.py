import pandas as pd
from datetime import datetime
import os

FILE = "data/response_feedback.csv"

def log_response_feedback(review_id, aspect, issue, response_text, action):
    row = {
        "review_id": review_id,
        "aspect": aspect,
        "issue": issue,
        "response_text": response_text,
        "action": action,
        "timestamp": datetime.utcnow().isoformat()
    }

    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(FILE, index=False)
