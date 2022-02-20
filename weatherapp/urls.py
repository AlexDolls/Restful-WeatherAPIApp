from django.urls import path

from . import views


app_name = "weatherapp"

urlpatterns = [
            path('', views.index, name='index'),
            path('cities/', views.get_cities, name='get_cities'),
            path('countries/', views.get_countries, name='get_countries'),
            path('current_weather/', views.get_current_weather, name = "get_current_weather"),
            ]
