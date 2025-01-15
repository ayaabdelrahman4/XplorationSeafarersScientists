import requests

# API keys
API_KEY_WEATHER = "de26752686c975de6a1c38a998f50fec"
API_KEY_AIR_POLLUTION = "de26752686c975de6a1c38a998f50fec"
BASE_URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather?"
BASE_URL_AIR_POLLUTION = "http://api.openweathermap.org/data/2.5/air_pollution?"

# Function to get current weather data
def get_current_weather(lat, lon):
    url = f"{BASE_URL_WEATHER}lat={lat}&lon={lon}&appid={API_KEY_WEATHER}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            if "weather" in data and len(data["weather"]) > 0:
                weather = {
                    "main": data["weather"]["main"],  # Weather condition (Rain, Clear, etc.)
                    "temp": data["main"]["temp"],  # Current temperature in °C
                    "description": data["weather"][0]["description"],  # Description of weather
                    "wind_speed": data["wind"]["speed"],  # Wind speed
                }
                return weather
            else:
                print("Weather data is missing or in an unexpected format.")
                return None
        except (KeyError, IndexError) as e:
            print(f"Error parsing weather data: {e}")
            return None
    else:
        print(f"Failed to fetch weather data. Status code: {response.status_code}")
        return None

# Function to get air pollution data
def get_air_pollution(lat, lon):
    url = f"{BASE_URL_AIR_POLLUTION}lat={lat}&lon={lon}&appid={API_KEY_AIR_POLLUTION}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            if "list" in data:
                air_quality = data["list"][0]["main"]["aqi"]
                co = data["list"][0]["components"]["co"]
                return {
                    "aqi": air_quality,
                    "co": co
                }
            else:
                return None
        except KeyError as e:
            print(f"Error parsing air pollution data: {e}")
            return None
    else:
        print(f"Failed to fetch air pollution data. Status code: {response.status_code}")
        return None
