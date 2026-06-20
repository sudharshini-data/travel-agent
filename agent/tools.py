import requests
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def get_weather(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return f"Could not fetch weather for {city}."
    
    temp = data["main"]["temp"]
    condition = data["weather"][0]["description"]
    return f"The current weather in {city} is {condition} with a temperature of {temp}°C."

def search_attractions(query: str) -> str:
    client = TavilyClient(api_key=TAVILY_API_KEY)
    results = client.search(query, max_results=5)

    output = []
    for result in results["results"]:
        output.append(f"{result['title']}: {result['url']}")

    return "\n".join(output)

def get_hotels_and_flights(city: str) -> str:
    mock_data = {
        "tokyo": {
            "hotels": [
                {"name": "Shinjuku Granbell Hotel", "price": "$120/night", "rating": "4.2/5"},
                {"name": "Park Hotel Tokyo", "price": "$180/night", "rating": "4.5/5"},
                {"name": "Dormy Inn Asakusa", "price": "$85/night", "rating": "4.0/5"},
            ],
            "flights": [
                {"airline": "Singapore Airlines", "duration": "7h 30m", "price": "$650"},
                {"airline": "Japan Airlines", "duration": "7h 15m", "price": "$720"},
            ]
        },
        "paris": {
            "hotels": [
                {"name": "Hotel Le Marais", "price": "$150/night", "rating": "4.3/5"},
                {"name": "Citadines Apart'hotel", "price": "$130/night", "rating": "4.1/5"},
            ],
            "flights": [
                {"airline": "Air France", "duration": "13h 00m", "price": "$890"},
                {"airline": "Singapore Airlines", "duration": "12h 45m", "price": "$950"},
            ]
        }
    }

    city_data = mock_data.get(city.lower())
    if not city_data:
        return f"No hotel or flight data available for {city}."

    hotels = "\n".join([f"{h['name']} - {h['price']} - Rating: {h['rating']}" for h in city_data["hotels"]])
    flights = "\n".join([f"{f['airline']} - {f['duration']} - {f['price']}" for f in city_data["flights"]])

    return f"Hotels:\n{hotels}\n\nFlights from Singapore:\n{flights}"