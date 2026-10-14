from google import genai
from pydantic import BaseModel,Field
from typing import List,Optional
from google.genai import types
import time

class Payment(BaseModel):
    name : str = Field(description="name of the person")
    date : str = Field(description="date of the payment")
    amount : int = Field(description="amount in rupees only as a number")

client = genai.Client()
message = "bhai kal 5th oct ko do hazar rupees de dena, Rahul ko, tuition fees wala"
prompt= f"Extract the name, date and amount from this message.\n\nMessage: {message}"

MODEL= "gemini-3.8-flash"
Config=types.GenerateContentConfig(
    response_mime_type="application/json",
    response_json_schema=Payment.model_json_schema()
)
for attemp in range(5):
    try:
        response = client.models.generate_content(model=MODEL,contents=prompt,config=Config)
        break
    except Exception as e:
        print("failed.retrying---",e)
        time.sleep(5 * (attemp+1))
else:
 print("model is busy.try againg later")
 exit()   
        


payment = Payment.model_validate_json(response.text)

print(payment)
print(payment.name)
print(payment.amount)
print(type(payment.amount))
