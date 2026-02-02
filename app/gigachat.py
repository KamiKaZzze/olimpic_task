import httpx
from app.config import GIGACHAT_MODEL
from app.gigachat_auth import get_access_token

CHAT_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

async def call_gigachat(messages, extra=None):
    token = await get_access_token()

    payload = {
        "model": GIGACHAT_MODEL,
        "messages": messages
    }
    if extra:
        payload.update(extra)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60, verify=False) as client:
        r = await client.post(CHAT_URL, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()
