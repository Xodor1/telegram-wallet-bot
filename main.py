import os
from wallet_bot import start_bot

if __name__ == '__main__':
    # Получаем токен из переменных окружения или вставь вручную (не рекомендуется)
    token = os.environ.get("TELEGRAM_BOT_TOKEN")

    # Получаем путь для webhook (например: "webhook")
    webhook_path = os.environ.get("WEBHOOK_PATH") or "webhook"

    # Внешний URL проекта на Render (без / в конце)
    render_url = os.environ.get("RENDER_EXTERNAL_URL")

    # Проверка на наличие обязательных значений
    if not token:
        raise Exception("TELEGRAM_BOT_TOKEN is not set")
    if not render_url:
        raise Exception("RENDER_EXTERNAL_URL is not set")

    # Финальный URL вебхука
    webhook_url = f"{render_url}/{webhook_path}"

    # Запуск бота
    start_bot(token, webhook_url)
