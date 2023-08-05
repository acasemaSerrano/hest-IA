import json
import os
from datetime import datetime, timedelta
from funtions.Weather import InterpreteWeather, DefinicionWeather

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

DTLimiteDinamico = datetime.now()


async def get_answer(question, nick, nombre = ""):
    global DTLimiteDinamico
    global MetaMessages
    global HestiaThinking

## config["chatGPT"]["msgErrorAPI"]

    tmp = DTLimiteDinamico + timedelta(minutes=config["chatGPT"]["TCEstatico"])
    
    if tmp < datetime.now():
        reset()
    if nombre == "":
        MetaMessages.append({"role": "user", "content": nick + ": " + question})
    else:
        MetaMessages.append({"role": "function", "content": question, "name": nombre})


    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=MetaMessages,
        functions=GetFunction(),
        function_call="auto"
    )
    
    message = request["choices"][0]["message"]

    print(request)
    if message.get("function_call"):
        return await get_answer(json.dumps(InterpreteDeFunciones(message["function_call"])), nick, message["function_call"]["name"])

    MetaMessages.append({"role": "assistant", "content": message['content']})
    
    DTLimiteDinamico = datetime.now() + timedelta(seconds=config["chatGPT"]["TCDinamico"]) * request["usage"]["completion_tokens"]
    

    return message['content']


def GetFunction():
    obj = []

    obj.extend(DefinicionWeather())


    return obj
        

def InterpreteDeFunciones(function):
    value = function["name"].split("-")[0]
    if value == "Weather":
        return InterpreteWeather(function)
    else:
        return "No Se pudo hacer"