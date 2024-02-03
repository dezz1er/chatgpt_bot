import logging
import g4f
from bot import redis
import json

import openai


openai.api_key = 'sk-2AAszqIqRyl6KXxmC908BfB27fFb45C89714Ed8f0e22386a'
openai.api_base = "https://neuroapi.host/v1"


async def get_chat_history(user_id: str) -> list:
    history = await redis.get(user_id)
    if history:
        return json.loads(history)
    return []


# Сохраняем историю на 1 час
async def save_chat_history(user_id: str, chat_history: list):
    await redis.set(user_id, json.dumps(chat_history), ex=3600)


async def generate_text(prompt, user_id: str) -> str:
    chat_history = await get_chat_history(user_id)

    chat_history.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt
        )
        chat_gpt_response = response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(e)
        chat_gpt_response = "Извините, произошла ошибка."

    chat_history.append({"role": "assistant", "content": chat_gpt_response})
    await save_chat_history(user_id, chat_history)

    logging.info(chat_history)
    return chat_gpt_response


async def generate_image(prompt, n=1, size="1024x1024") -> list:
    try:
        response = await openai.Image.create(
            prompt=prompt,
            n=n,
            size=size
        )
        urls = [image['url'] for image in response['data']]
    except Exception as e:
        logging.error(e)
        return []
    return urls
