import asyncio

# Максимум 10 параллельных запросов к GigaChat
gigachat_semaphore = asyncio.Semaphore(10)
