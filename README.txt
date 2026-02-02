Виртуальное окружение

python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

Установка зависимостей

pip install -r requirements.txt

Конфигурация окружения

Создай файл .env в корне проекта:

# GigaChat
GIGACHAT_API_KEY=your_api_key
GIGACHAT_MODEL=GigaChat-2

# FastAPI
HOST=0.0.0.0
PORT=8000

tokens_used.txt - счетчик токенов

для получения GIGACHAT_API_KEY залогиниться в личный кабинет https://developers.sber.ru/studio/registration , и получить ключ