from app.llm_limiter import gigachat_semaphore
from app.gigachat import call_gigachat

async def call_gigachat_limited(*args, **kwargs):
    async with gigachat_semaphore:
        return await call_gigachat(*args, **kwargs)
