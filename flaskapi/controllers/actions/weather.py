import requests

import constants
from controllers.actions.base import BaseAction
from utils.utils import extract_location_from_question


WEATHER_API_URL = "http://api.weatherapi.com/v1/forecast.json?key={access_key}&q={query}&days=1&aqi=no&alerts=no"
RESPONSE = "The weather in {location} today is expected to be {text} with temperature between {lowtemp} and {maxtemp} degrees Celsius."

DEFAULT_LOCATION = "Krems"
UNKNOWN_LOCATION_ERROR = "Sorry, I don't know the weather for that location."


class WeatherAction(BaseAction):
    def __init__(self):
        super().__init__()
        self._endpoint = WEATHER_API_URL.replace("{access_key}", self._conf.get("WeatherAPI-Key"))

    def perform(self, question):
        """Perform action - Acquire weather data from API."""
        result_str = None
        
        location = extract_location_from_question(question)
        if location is None:
            location = DEFAULT_LOCATION
        
        endpoint = self._endpoint.replace("{type}", "forecast")\
                                 .replace("{query}", location)
        response = requests.get(endpoint)
        print(response.status_code)
        if response.status_code == 200:
            day = response.json().get('forecast').get("forecastday")[0].get("day")
            maxtemp=str(day.get("maxtemp_c"))
            lowtemp=str(day.get("mintemp_c"))
            text=str(day.get("condition").get("text"))
            result_str = RESPONSE.replace("{location}", location) \
                                            .replace("{text}", text) \
                                            .replace("{maxtemp}", maxtemp) \
                                            .replace("{lowtemp}", lowtemp)
            print(result_str)
        else:
            if response.status_code == 400:
                if response.json().get("error").get("code") == 1006:
                    result_str = UNKNOWN_LOCATION_ERROR
        return result_str