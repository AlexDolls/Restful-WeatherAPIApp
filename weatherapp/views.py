from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

import requests

from abc import ABC, abstractmethod
import datetime
import json

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
                ):

        self.geocording = geocording
        self.cache = cache

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
 

class AllCountriesAPI(BaseAPI):
    
    __countries_cities_dict = {}
    __countries = {}

    @classmethod
    def send(cls):
        if not cls.__countries_cities_dict:
            with open("weatherapp/countries_cities.json") as f:
                cls.__countries_cities_dict = json.load(f)
        if not cls.__countries:
            with open("weatherapp/countries.json") as f:
                cls.__countries = json.load(f)

    @classmethod
    def get_cities(cls, country: str):
        cls.send()
        return cls.__countries_cities_dict.get(country, "Can't find country: {}".format(country))

    @classmethod
    def get_countries(cls):
        cls.send()
        return cls.__countries



        
@api_view(['GET'])
@parser_classes([JSONParser])   
def get_current_weather(request):
    city = request.GET.get("city", "Kiev")
    country_code = request.GET.get("countrycode", "")
    
    weather_api_object = CurrentWeather(GeoCording(city, country_code))
    
    weather_info = weather_api_object.send()
  
    return Response(weather_info)


@api_view(['GET'])
def get_countries(request):

    return Response(AllCountriesAPI.get_countries())


@api_view(['GET'])
def get_cities(request):
    country = request.GET.get("country")

    return Response(AllCountriesAPI.get_cities(country))


def index(request):
    return render(request, "weatherapp/index.html", {"weather_action_title":"Current Weather"})
