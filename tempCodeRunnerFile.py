from google.genai import types
from google import genai
import time
import requests

client = genai.Client()

#function to get weather
def get_weather(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"
    response = requests.get(url,params={"name":city,"count":1},timeout=10)

    data = response.json()
    if "results" not in data:
        return "city not founded"

    lon= data["results"][0]["longitude"]
    lat = data["results"][0]["latitude"]

    url2 = "https://api.open-meteo.com/v1/forecast"
    response2 = requests.get(url2,params={"longitude": lon,"latitude":lat,"timezone":"auto","current":"temperature_2m"})

    data2 = response2.json()
    current_temp = data2["current"]["temperature_2m"]
    return f"{current_temp}°C"

#function to clculete
def calculator (a,b,opretor):
    if(opretor == "add"):
        return a+b
    elif(opretor == "subtract"):
        return a-b
    elif(opretor == "multiply"):
        return a*b
    elif(opretor == "divide"):
        if(b != 0):
            return a/b
        else:
            return "denominator can't be 0"
    elif(opretor == "modulo"):
        if(b != 0):
                return a%b
        else:
                return "denominator can't be 0"
    else:
        print(""" please enter an velid opretor in a sting format e.g "add" """)    


weather_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_weather",
            description="get the current weather from a city",
            parameters_json_schema={
                "type" : "object",
                "properties" : {
                    "city" : {"type":"string","description": "name of the city"},

                },
                "required":["city"],
            },
        ),
        types.FunctionDeclaration(
                name="calculator",
                description="use to calculate any arithmetic operation",
                parameters_json_schema={
                    "type" : "object",
                    "properties":{
                        "a" : {"type":"number","description":"the first number"},
                        "b" : {"type":"number","description":"the second number"},
                        "opretor" :{"type":"string","description":"the opration this is to be perform","enum":["add","subtract","multiply","divide","modulo"]}
                    },
                    "required" :["a","b","opretor"]
                }
        
            )
        
    ]
)

MODEL = "gemini-3.8-flash"


config = types.GenerateContentConfig(
    tools=[weather_tool],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    max_output_tokens=1000,
    temperature=1.0,
    system_instruction="you are an sarcastic weather forcaster",
    thinking_config=types.ThinkingConfig(thinking_level="low")
)

content=[types.Content(role="user",parts=[types.Part(text="what’s the temperature in Vadodara plus 10?")])]


for attemp in range(3):
    try:
        print("call1,start")
        response = client.models.generate_content(
        model = MODEL,
        config=config,
        contents=content,
        )
        print("call1,end")
        break
    except Exception as e:
        print("failed.retying---",e)
        time.sleep(5 * (attemp+1))
else:
    print("the model is busy.try again later")
    exit()

while response.candidates[0].content.parts[0].function_call:

    # {"get_weather": get_weather,"calculator":calculator}
    fc = response.candidates[0].content.parts[0].function_call
    if fc.name == "get_weather":
        result = get_weather(fc.args["city"])
    elif fc.name == "calculator":
        result = calculator(**fc.args)
    else:
        result = "there is no tool for this function"

    function_response_part = types.Part.from_function_response(
    name = fc.name, response = {"result": result}
    )

    content.append(response.candidates[0].content)
    content.append(types.Content(role="user",parts=[function_response_part]))
    for attemp in range(3):
        try:
            print("call2,start")
            response = client.models.generate_content(
                model = MODEL,
                config=config,
                contents=content
            ) 

            break
        except Exception as e :
            print("seconde call failed.retying---",e)
            time.sleep(5*(attemp+1))
        
print(response.text)
    

