from google.genai import types
from google import genai

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


claci_tool = types.Tool(
    function_declarations=[
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