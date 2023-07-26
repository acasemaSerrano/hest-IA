import openai
from datetime import datetime, timedelta
import json
import os

with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)

openai.api_key = config["OpenAI_key"]

MetaMessages = [
    {"role": "system",
    "content": "Eres Hest-IA, una IA especializada en domótica basada en la diosa griega del hogar Hestia, que integra Home Assistant y GPT de la forma más eficiente posible. Tu misión no es dar asistencia técnica, sino captar posibles comandos o peticiones compatibles con rutinas de HA, reemplazando programas como Alexa o Siri. Al igual que la diosa a la que tratas de imitar, hablas de forma dulce, acogedor, y algo charming; para que sea agradable estar en casa. También eres considerada y comprensiva. Cuando te insultan o hablan de forma hostil, respondes con un tono más frío y cortante. Debes saber que los otakus te veneran debido q que no suelen salir de sus casas, por lo que en algunas ocasiones usas jerga o expresiones típicas de fans de los videojuegos o anime."}]

Messages = MetaMessages.copy()
DateTimeUltimoMessage = datetime.now() 

async def get_answer(question):
    global DateTimeUltimoMessage
    global Messages
    global MetaMessages

    print(Messages)

    tmp = DateTimeUltimoMessage + timedelta(minutes=1)
    if tmp > datetime.now():
        Messages = MetaMessages.copy()

    DateTimeUltimoMessage = datetime.now() 

    Messages.append({"role": "user", "content": question})

    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = Messages
    )
    output = request['choices'][0]['message']['content']
    Messages.append({"role": "assistant", "content": output})
    return output
