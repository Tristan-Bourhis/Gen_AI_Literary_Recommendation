import csv
from datetime import datetime

from app.core.config import USER_RESPONSES_DIR
from app.core.utils import write_json


def save_responses(payload, prefix="responses"):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    USER_RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    json_path = USER_RESPONSES_DIR / f"{prefix}_{timestamp}.json"
    write_json(json_path, payload)
    return json_path


def save_responses_csv(payload, prefix="responses"):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    USER_RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = USER_RESPONSES_DIR / f"{prefix}_{timestamp}.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        for key, value in payload.items():
            writer.writerow([key, value])
    return csv_path
