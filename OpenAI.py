import openai
from datetime import datetime, timedelta
import json
import os

with open(f"{os.path.realpath(os.path.dirname(__file__))}/./config.json") as file:
        config = json.load(file)

openai.api_key = config["OpenAI_key"]

MetaMessages = [
    {"role": "system",
    "content": ""}]

DateTimeUltimoMessage = datetime.now() 

async def get_answer(question):
    global DateTimeUltimoMessage
    global MetaMessages

    
    print(MetaMessages)

    tmp = DateTimeUltimoMessage + timedelta(minutes=1)
    if tmp > datetime.now():
        reset()

    DateTimeUltimoMessage = datetime.now() 

    MetaMessages.append({"role": "user", "content": question})

    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = MetaMessages
    )
    output = request['choices'][0]['message']['content']
    MetaMessages.append({"role": "assistant", "content": output})
    return output


def reset():
    with  open('/../OpenAI.pront.txt','r', encoding="utf-8") as file:
        MetaMessages = [
            {"role": "system",
            "content": file.read()}]