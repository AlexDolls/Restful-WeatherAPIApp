from django.urls import path

from . import views


app_name = "weatherapp"

urlpatterns = [
            path('', views.get_current_weather, name='current'),
            path('cities/', views.get_cities, name='get_cities'),
            path('countries/', views.get_countries, name='get_countries'),
            ]
