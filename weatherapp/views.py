from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests

from abc import ABC, abstractmethod
import datetime

from . import tmp_key_file
# Create your views here.

APIkey = tmp_key_file.APIkey


class BaseAPI(ABC):

    @abstractmethod
    def send(self, **querystring):
        pass


class Cache:
    
    def __init__(self, expire_time: int):
        self._cache_dict = {}
        self._expire_time = expire_time
    
    def add(self, key: str, value: dict):
        self._cache_dict[key] = value
        self._cache_dict[key]["income-date"] = datetime.datetime.now()

    def get(self, key:str, request_date: datetime.datetime):
        if item := self._cache_dict.get(key, False):

            if (request_date - item["income-date"]).seconds < self._expire_time:
                return item

            else:
                self._cache_dict.pop(key)

        return False
    
    def remove(self, key: str):
        self._cache_dict.pop(key)

    def get_full_cache(self):
        return self._cache_dict


class WeatherCache(Cache):
    pass
                

class DictFormatting(ABC):

    @abstractmethod
    def __init__(self, entrypoint_keys: dict = {"main: Main"}):
        self._entrypoint_keys = entrypoint_keys
        self._match_names = {
                          "temp":"Temperature",
                          "feels_like":"Feels like",
                          "temp_min": "Temp min",
                          "temp_max": "Temp max",
                          "pressure": "Pressure",
                          "humidity": "Humidity"
                        }

    def execute(self, collection: dict):
        res = ""

        for entrypoint in self._entrypoint_keys:
            entrypoint_value = collection.get(entrypoint, False)

            if entrypoint_value:
                try:
                    if entrypoint_value.keys():
                        for subkey in entrypoint_value.keys():
                            matched = self._match_names.get(subkey, False)
                            if matched:
                                res += "{0}:{1}\n".format(matched, entrypoint_value.get(subkey))

                    if not entrypoint_value.keys():
                        res += "{0}:{1}\n".format(self._entrypoint_keys[entrypoint], entrypoint_value)

                except AttributeError:
                    res += "{0}:{1}\n".format(self._entrypoint_keys[entrypoint], entrypoint_value)
        return res


class CurrentWeatherDict(DictFormatting):

    def __init__(self):
        self._entrypoint_keys = {
                                    "main":"Main",
                                 }
        self._match_names = {
                          "temp":"Temperature",
                          "feels_like":"Feels like",
                          "temp_min": "Temp min",
                          "temp_max": "Temp max",
                          "pressure": "Pressure",
                          "humidity": "Humidity",
                        }

    
class GeoCording(BaseAPI):

    def __init__(self, city: str, country_code: str = ""):
        self.city = city
        self.country_code = country_code

    def send(self):
        url = "http://api.openweathermap.org/geo/1.0/direct?q={0},{1}&limit=1&appid={2}".format(self.city, self.country_code, APIkey)

        r = requests.get(url)

        return r.json()[0]


class CurrentWeather(BaseAPI):

    def __init__(
                    self, 
                    geocording: GeoCording,
                    cache: Cache = WeatherCache(3600),
                    response_formatter: DictFormatting = CurrentWeatherDict()
                ):

        self.geocording = geocording
        self.cache = cache
        self.response_formatter = response_formatter

    def send(self):
        coords = self.geocording.send()

        try:
            lon = coords.get("lon", "0")
            lat = coords.get("lat", "0")
        except AttributeError:
            print("Failed lon/lat finding...")

        result = self.get_from_cache("{}-{}".format(lon, lat), datetime.datetime.now())

        if result == False:
            url = "http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&units=metric&appid={2}".format(lat, lon, APIkey)
            r = requests.get(url)
            self.add_to_cache("{}-{}".format(lon, lat), r.json())
            result = r.json()

        return result
        
    def get_from_cache(self, key: str, request_date: datetime.datetime):
        return self.cache.get(key, request_date)

    def add_to_cache(self, key: str, value: dict):
        self.cache.add(key, value)

    def fancy_view(self):
        collection = self.send()
        return self.response_formatter.execute(collection)
        
@api_view()
def get_current_weather(request):
    city = request.GET.get("city", "Kiev")
    country_code = request.GET.get("countrycode", "804")
    
    weather_api_object = CurrentWeather(GeoCording(city, country_code))
    
    weather_info = weather_api_object.send()
  
    return Response(weather_info)


