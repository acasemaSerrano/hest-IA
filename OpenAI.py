import json
import os
from datetime import datetime, timedelta

import openai

with open(f"{os.path.realpath(os.path.dirname(__file__))}/./config.json") as file:
    config = json.load(file)

openai.api_key = config["OpenAI_key"]
file_path = os.path.join(os.path.realpath(
    os.path.dirname(__file__)), 'OpenAI.prompt.txt')


MetaMessages = []

def reset():
    global MetaMessages

    with open(file_path, encoding="utf-8") as file:
        MetaMessages = [
            {"role": "system",
             "content": file.read()}]

reset()

DateTimeUltimoMessage = datetime.now()


async def get_answer(question):
    global DateTimeUltimoMessage
    global MetaMessages

    tmp = DateTimeUltimoMessage + timedelta(minutes=1)
    if tmp < datetime.now():
        reset()
    
    DateTimeUltimoMessage = datetime.now()

    MetaMessages.append({"role": "user", "content": question})

    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=MetaMessages
    )
    output = request['choices'][0]['message']['content']
    MetaMessages.append({"role": "assistant", "content": output})
    return output



