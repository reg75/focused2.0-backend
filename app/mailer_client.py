import os
import requests

def notify_observation(payload: dict) -> None:
    print("[mailer] task started") # Debug
    MAILER_URL = os.getenv("MAILER_URL", "http://127.0.0.1:8001")
    MAILER_API_KEY = os.getenv("MAILER_API_KEY", "")

    if not MAILER_API_KEY:
        print("[mailer] WARNING: MAILER_API_KEY is empty despite .env loading")
    try:
        url = f"{MAILER_URL.rstrip('/')}/mail/observation"
        headers = {
            "X-API-KEY": MAILER_API_KEY, 
            "Content-Type": "application/json",
        }
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"[mailer] POST {url} status={r.status_code} body={r.text[:200]}")
    
    except Exception as e:
        print(f"[mailer] EXCEPTION {e}")