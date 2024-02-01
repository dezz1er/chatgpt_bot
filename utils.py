import openai
import logging
import g4f
from temp_storage import conversation_history, trim_history


async def generate_text(prompt, user_id) -> dict:
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id] = trim_history(conversation_history[user_id])

    chat_history = conversation_history[user_id]

    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=chat_history,
            provider=g4f.Provider.GeekGpt,
        )
        chat_gpt_response = response
    except Exception as e:
        print(f"{g4f.Provider.GeekGpt.__name__}:", e)
        chat_gpt_response = "Извините, произошла ошибка."

    conversation_history[user_id].append({"role": "assistant",
                                          "content": chat_gpt_response})
    logging.info(conversation_history)
    length = sum(len(message["content"]) for message in conversation_history[
        user_id])
    logging.info(length)
    return chat_gpt_response


async def generate_image(prompt, n=1, size="1024x1024") -> list[str]:
    try:
        response = await openai.Image.acreate(
            prompt=prompt,
            n=n,
            size=size
        )
        urls = []
        for i in response['data']:
            urls.append(i['url'])
    except Exception as e:
        logging.error(e)
        return []
    else:
        return urls
