import requests
import json
from typing import Dict, Optional


class WeatherService:
    def __init__(self):
        self.base_url = "https://wttr.in"

    def get_weather(self, city: str) -> Optional[Dict]:
        """Gets a weather for certain city."""
        try:
            url = f"{self.base_url}/{city}?format=j1"
            response = requests.get(url)
            response.raise_for_status()

            weather_data = response.json()

            current = weather_data.get('current_condition', [{}])[0]
            weather = weather_data.get('weather', [{}])[0]

            return {
                'temperature': {
                    'celsius': current.get('temp_C'),
                    'fahrenheit': current.get('temp_F')
                },
                'feels_like': {
                    'celsius': current.get('FeelsLikeC'),
                    'fahrenheit': current.get('FeelsLikeF')
                },
                'description': current.get('weatherDesc', [{}])[0].get('value'),
                'humidity': current.get('humidity'),
                'wind_speed': {
                    'kmh': current.get('windspeedKmph'),
                    'mph': current.get('windspeedMiles')
                },
                'pressure': {
                    'mb': current.get('pressure'),
                    'inches': current.get('pressureInches')
                },
                'visibility': {
                    'km': current.get('visibility'),
                    'miles': current.get('visibilityMiles')
                },
                'uv_index': current.get('uvIndex'),
                'location': {
                    'city': weather_data.get('nearest_area', [{}])[0].get('areaName', [{}])[0].get('value'),
                    'country': weather_data.get('nearest_area', [{}])[0].get('country', [{}])[0].get('value'),
                    'region': weather_data.get('nearest_area', [{}])[0].get('region', [{}])[0].get('value')
                }
            }

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while retrieving weather data: {e}")
            return None
        except (KeyError, IndexError) as e:
            print(f"Error occurred while processing weather data: {e}")
            return None

    def get_weather_text(self, city: str) -> str:
        """Gets the weather in text format."""
        try:
            url = f"{self.base_url}/{city}"
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error while getting text weather data: {e}")
            return ""

    def close(self):
        print("[WeatherService] Closing service...")
        if hasattr(self, 'session') and self.session:
            self.session.close()
            print("[WeatherService] HTTP session closed")
        else:
            print("[WeatherService] No session to close")


if __name__ == "__main__":
    weather_service = WeatherService()

    weather_data = weather_service.get_weather("Poltava")
    if weather_data:
        print("\nWeather data in JSON format:")
        print(json.dumps(weather_data, indent=2, ensure_ascii=False))

    weather_text = weather_service.get_weather_text("Poltava")
    if weather_text:
        print("\nWeather data in text format:")
        print(weather_text)