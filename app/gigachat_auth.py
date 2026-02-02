import base64
import uuid
import time
import httpx
from app.config import GIGACHAT_API_KEY

TOKEN_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

_token_cache = {
    "token": None,
    "expires_at": 0
}

async def get_access_token():
    now = int(time.time())
    if _token_cache["token"] and _token_cache["expires_at"] > now + 60:
        return _token_cache["token"]



    headers = {
        "Authorization": f"Basic {GIGACHAT_API_KEY}",
        "Content-Type": "application/x-www-form-urlencoded",
        "RqUID": str(uuid.uuid4())
    }

    data = {"scope": "GIGACHAT_API_PERS"}

    async with httpx.AsyncClient(timeout=20, verify=False) as client:
        r = await client.post(TOKEN_URL, data=data, headers=headers)
        r.raise_for_status()
        payload = r.json()

    _token_cache["token"] = payload["access_token"]
    _token_cache["expires_at"] = payload["expires_at"]

    return _token_cache["token"]
