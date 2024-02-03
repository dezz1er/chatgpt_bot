import openai


openai.api_key = 'sk-2AAszqIqRyl6KXxmC908BfB27fFb45C89714Ed8f0e22386a'
openai.api_base = "https://neuroapi.host/v1"


def ask(messages: list) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    print(response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']


messages = []
while True:
    question = input()
    messages.append({"role": "user", "content": question})
    answer = ask(messages=messages)
    messages.append({"role": "assistant", "content": answer})
