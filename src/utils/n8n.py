"""Simple n8n integration helpers."""

import os
import requests

N8N_WEBHOOK_URL = os.environ.get('N8N_WEBHOOK_URL')


def send_event(event: str, payload: dict) -> None:
    """Send event data to n8n if webhook url configured."""
    if not N8N_WEBHOOK_URL:
        return
    try:
        requests.post(N8N_WEBHOOK_URL, json={"event": event, "data": payload}, timeout=5)
    except requests.RequestException:
        pass
