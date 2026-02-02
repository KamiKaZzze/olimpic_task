from fastapi import APIRouter
from app.schemas import ChatRequest
from app.gigachat import call_gigachat
from app.prompts import (
    SYSTEM_PROMPT_PHARMACIST,
    SYSTEM_PROMPT_SUGGESTIONS,
)
from app.tokens import tokens_from_usage, estimate_tokens
from app.token_store import add_tokens
from app.gigachat_limited import call_gigachat_limited

router = APIRouter()


@router.post("/chat")
async def chat(req: ChatRequest):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_PHARMACIST},
        *req.chat_history,
        {"role": "user", "content": req.user_input},
    ]

    resp = await call_gigachat_limited(messages)
    answer = resp["choices"][0]["message"]["content"].strip()

    # 1) точный подсчёт
    tokens = tokens_from_usage(resp)

    # 2) fallback, если usage не пришёл
    if tokens <= 0:
        tokens = estimate_tokens(messages, answer)

    total = add_tokens(tokens)

    return {
        "answer": answer,
        "tokens_used": tokens,
        "total_tokens": total,
    }


@router.post("/suggestions")
async def suggestions(req: ChatRequest):
    last_assistant_message = None
    if req.chat_history:
        for msg in reversed(req.chat_history):
            if msg.get("role") == "assistant":
                last_assistant_message = msg.get("content")
                break

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_SUGGESTIONS},
        {
            "role": "assistant",
            "content": (
                "System prompt основного ассистента для анализа:\n\n"
                + SYSTEM_PROMPT_PHARMACIST
            )
        }
    ]

    if last_assistant_message:
        messages.append({
            "role": "assistant",
            "content": "Последний ответ ассистента:\n\n" + last_assistant_message
        })

    messages.append({"role": "user", "content": req.user_input})

    resp = await call_gigachat_limited(messages, extra={"temperature": 1.0})
    raw = resp["choices"][0]["message"]["content"]

    options = [
        line.strip("-• ").strip()
        for line in raw.split("\n")
        if line.strip()
    ][:3]

    # 1) точный подсчёт
    tokens = tokens_from_usage(resp)

    # 2) fallback
    if tokens <= 0:
        tokens = estimate_tokens(messages, raw)

    total = add_tokens(tokens)

    return {
        "options": options,
        "tokens_used": tokens,
        "total_tokens": total,
    }
