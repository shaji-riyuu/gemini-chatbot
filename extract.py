from google import genai 
from google.genai import types
import time
import json

def clean(res):

    start = res.find("{")
    end = res.rfind("}")
    if start == -1 or end == -1:
        return None
    else:
   
        clean_json=res[start:end+1]
        return clean_json

client = genai.Client() 

MODEL = "gemini-3.8-flash"


config = types.GenerateContentConfig(
    system_instruction="you are an helpfull assistent",
    max_output_tokens=1000,
    thinking_config=types.ThinkingConfig(thinking_level="low"),
    temperature=1.0,
    response_mime_type="application/json",
)

message = "bhai kal 5th oct ko 2500 rupees de dena, Rahul ko, tuition fees wala"
prompt = f"Extract name, date and amount from this message. Return only JSON, nothing else.\n\nMessage: {message}"

for attemp in range(3):
    try:
        response = client.models.generate_content(model=MODEL,config=config,contents=prompt)  
        break
    except Exception as e:
        print("failed.Retrying---",e)
        time.sleep(5*(attemp+1))  
else:
    print("model is busy.try againg later.")
    exit()



# clean_json = clean(response.text)
# if clean_json == "None":
#     print("no json is find in :",response.text)
# try:
#     final_clean=json.loads(clean_json)
# except json.JSONDecodeError:
#     print("Bad json.get:",clean_json)

# print(final_clean[int("amount")])
# print(type(final_clean[int("amount")]))
# print(final_clean)
reply = response.text
print(reply)
print(reply["name"])


