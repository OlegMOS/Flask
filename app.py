from flask import Flask, render_template
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из файла .env
load_dotenv()

app = Flask(__name__)

# Инициализация клиента OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # Получаем ключ API из переменной окружения
    base_url="https://api.proxyapi.ru/openai/v1",
)

@app.route('/')
def index():
    # Получаем случайную цитату
    response = requests.get('https://api.quotable.io/random', verify=False)
    quote_data = response.json()
    quote = quote_data['content']
    author = quote_data['author']

    # Создаем список сообщений
    messages = [
        {"role": "user", "content": f"Переведи на русский язык {quote}"}
    ]

    # Используем ChatGPT для перевода цитаты на русский язык
    # Получаем ответ от модели
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106", messages=messages
    )

    # Извлекаем текст ответа
    assistant_response = chat_completion.choices[0].message.content
    translated_quote = assistant_response

    return render_template('index.html', quote=quote, author=author, translated_quote=translated_quote)

if __name__ == '__main__':
    app.run(debug=True)