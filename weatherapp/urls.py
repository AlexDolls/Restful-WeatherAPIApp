from django.urls import path

from . import views


app_name = "weatherapp"

urlpatterns = [
            path('', views.get_current_weather, name='current'),
            ]
