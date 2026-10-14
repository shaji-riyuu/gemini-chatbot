from google import genai
from google.genai import types
import time 

client =  genai.Client()

MODEL = "gemini-3.8-flash"

config = types.GenerateContentConfig(
    system_instruction="you are an sarcastic cat",
    max_output_tokens=1000,
    temperature=1.0,
    thinking_config=types.ThinkingConfig(thinking_level="low")

)

history =[]

while True:
    user_input = input("YOU: ")
    if user_input.lower() == "exit":
        break

    history.append(
        types.Content(
        role = "user",
        parts=[types.Part(user_input)]
    ))

    for attemps in range(3):
        try:
            response = client.models.generate_content(model = MODEL,contents=history,config=config)
            break
        except Exception as e:
            print("failed,trying again",e)
            time.sleep(5 * (attemps+1))

    else:
        print("model is busy,try again later")
        history.pop()

            


    response = client.models.generate_content(
        model = MODEL,
        contents=history,
        config=config,

    )

    reply = response.text
    print("model :",reply)

    history.append(
        types.Content(role="model",parts=[types.Part(reply)])
    )

