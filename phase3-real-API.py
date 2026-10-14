import requests
def get_weather(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"
    response = requests.get(url,params={"name":city,"count":1})

    data = response.json()
    if "results" not in data:
        return "city not founded"
        
    
    lon= data["results"][0]["longitude"]
    lat = data["results"][0]["latitude"]
     # print(lon,lat)

    url2 = "https://api.open-meteo.com/v1/forecast"
    response2 = requests.get(url2,params={"longitude": lon,"latitude":lat,"timezone":"auto","current":"temperature_2m"})

    data2 = response2.json()
    current_temp = data2["current"]["temperature_2m"]
    return f"{current_temp}°C"

print(get_weather("mumbai"))