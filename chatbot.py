from google import genai 
from google.genai import types
import time

client = genai.Client() 

MODEL = "gemini-3.8-flash"


config = types.GenerateContentConfig(
    system_instruction="you are an helpfull assistent",
    max_output_tokens=1000,
    thinking_config=types.ThinkingConfig(thinking_level="low"),
    temperature=1.0
)

history = []

while True:
    user_text = input("You: ")
    if user_text.lower() == "exit":
        break
   
    history.append(
        types.Content(role = "user",parts=[types.Part(text=user_text)])
    )
    
    for attempt in range(3):
        try:
            response = client.models.generate_content( model=MODEL,contents=history,config=config )
            break
        except Exception as e:
            print("failed,retrying:",e)
            time.sleep(5*(attempt+1))
    else:
        print("gemini is busy,try againg later.")
        history.pop()
        continue

    replay = response.text
    print("gemini : ",replay)
    history.append(
        types.Content(role="model",parts=[types.Part(text=replay)])
    )
