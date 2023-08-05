import requests
import os
import json

with open(f"{os.path.realpath(os.path.dirname(__file__))}/../config.json") as file:
    config = json.load(file)


def get(city):
    key = config["Weather_key"]
    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={key}&q={city}&aqi=no")
    if response.status_code == 200:
        print("Todo bien! Respuesta:")
        print(response.json())
        result = {}
        result["temperatura"] = str(response.json()["current"]["temp_c"]) + " grados celsius"
        result["condicion"] = response.json()["current"]["condition"]["text"]
        result["HoraLocal"] = response.json()["location"]["localtime"]
        return result
        #return response.json()
    else:
        print(f"Oops, algo salió mal al llamar al API del clima. Codigo fue: {response.status_code}")


def getForecast(city, day):
    key = config["Weather_key"]
    response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={city}&days={day}&aqi=no&alerts=no")
    if response.status_code == 200:
        print("Todo bien! Respuesta:")
        print(response.json())
        result = {}
        result["dia"] = response.json()["forecast"]["forecastday"][day - 1]["date"]
        result["TemperaturaMaximas"] = str(response.json()["forecast"]["forecastday"][day - 1]["day"]["maxtemp_c"]) + " grados celsius"
        result["TemperaturaMinimas"] = str(response.json()["forecast"]["forecastday"][day - 1]["day"]["mintemp_c"]) + " grados celsius"
        result["condicion"] = response.json()["forecast"]["forecastday"][day - 1]["day"]["condition"]["text"]
        return result
        #return response.json()
    else:
        print(f"Oops, algo salió mal al llamar al API del clima. Codigo fue: {response.status_code}")

print(getForecast("Málaga", 1))

def InterpreteWeather(info):
    value = info["name"].split("-")[1]
    argumentos = json.loads(info["arguments"])
    
    if value == "get":
        return get(argumentos["ubicacion"])
    
    elif value == "getForecast":
        return getForecast(argumentos["ubicacion"], argumentos["DiaRelativo"])
    else:
        return "No Se pudo hacer"

def DefinicionWeather():
    return [
            {
                "name": "Weather-get",
                "description": "Obtener el clima actual y la hora local",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ubicacion": {
                            "type": "string",
                            "description": "La ubicación, debe ser una ciudad",
                        }
                    },
                    "required": ["ubicacion"]
                }
            },
                        {
                "name": "Weather-getForecast",
                "description": "Obtener el clima en el futuro",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ubicacion": {
                            "type": "string",
                            "description": "La ubicación, debe ser una ciudad",
                        },
                        "DiaRelativo": {
                            "type": "integer",
                            "description": "El dia relatibo a hoy, hoy siendo 0, tiene que ser de 1 a 10",
                        }
                    },
                    "required": ["ubicacion", "DiaRelativo"]
                }
            }
        ]
