from datetime import datetime


def log_event(event, payload=None):
    timestamp = datetime.utcnow().isoformat()
    return {"timestamp": timestamp, "event": event, "payload": payload or {}}
