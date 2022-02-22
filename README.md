<h1 align="center">Restful WeatherAPIApp</h1>
<p align = "center">
<a href = "https://github.com/django/django"><img src = "https://img.shields.io/badge/Django-4.0.2-green"></img></a>
<a href ="https://www.python.org/downloads/release/python-397/"><img src = "https://img.shields.io/badge/Python-3.9.7-green"></img></a>
<a href = "https://www.django-rest-framework.org/"><img src = "https://img.shields.io/badge/DRF-3.13.1-red"></img></a>
<a href = "https://reactjs.org/"><img src = "https://img.shields.io/badge/React-17.0.2-blue"></img></a>
</p>
<p align = center>
<img src = "https://imgur.com/4uewx6i.jpeg"><img>
<h2 align = "center"><strong><a href = "http://vps-39294.vps-default-host.net/weatherapp/">Try it in Live Version</a></strong></h2>
</p>

<h2>Technologies used in project</h2>
<ol>
<li><strong>Python3</strong></li>
<li><strong>Django4</strong></li>
<li><strong>PostgreSQL</strong> - <i>As production and dev DB</i></li>
<li><strong>ReactJS</strong> - <i>Froent-end UI elements</i></li>
<li><strong>DRF (Django Rest Framework)</strong> - <i>Using it to follow the <strong>REST</strong> methodology</i></li>
<li><strong>Nginx</strong> - <i>As proxy server</i></li>
<li><strong>Docker</strong> - <i>project deploying (dev and prod deploying versions)</i></li>
</ol>

<h2>Description</h2>
<h3>Index page</h3>
<hr>
<img src = "https://github.com/AlexDolls/WeatherAPIApp/blob/master/screenshots_readme/index_page_country.png">
  The WeatherApp index page represented by ReactJS elements. First what you seee - select box with countries.
  To see how WeatherApp is giving weather info just do steps:
  <strong>
  <ol>
  <li> Choose country you want from first select</li>
  <br>
  <img src = "https://github.com/AlexDolls/WeatherAPIApp/blob/master/screenshots_readme/index_page_pop_list.png">
  <br>
  <li> After this you'll see select with cities - choose city you want</li>
  <li> When city choosed, the result with weather info will displayed down with grid displaying system</li>
  <br>
  <img src = "https://github.com/AlexDolls/WeatherAPIApp/blob/master/screenshots_readme/index_page_weather_info.png">  
  </ol>
  Countries and cities names in JSON format i took from this github repository - https://github.com/dr5hn/countries-states-cities-database.
  </strong>
  <br>
   Based on them i build files that contains only necessary info for app, files placed in weatherapp/static/weatherapp/files/json/:
  <ul>
  <li>countries_cities.json</li>
  <li>countries.json</li>
  </ul>
 
<h3>Tech features</h3>
<ol>
<li><strong>Restful</strong></li>
  <ul>
    <li>Client-server</li>
    <li>Stateless</li>
    <i>No request's data storage in DB or any other storage</i>
    <li>Cacheability</li>
    <i>Caching all server's responses for save time when client asks same info.
    Represented in project by Cache class.</i>
    <li>Uniform interface</li>
    <i>Giving neccessary info about content types and another actions that client can do with the asked resourse by using Django REST Framework.</i>
  </ul>
<li><strong>Business logic in Classes</strong></li>
<i>All business logic and necessary functionality represented in Classes. Using that architecture make able easily expanding existing functions
by inheritance BaseAPI Abstract class and definition methods for new API calls. It also easier to auto-test it </i>
</ol>
<br>
<strong>That also make able to make your views look like short calling the object's methods</strong>
https://github.com/AlexDolls/WeatherAPIApp/blob/master/weatherapp/views.py

```Python
@api_view(['GET'])
@parser_classes([JSONParser])   
def get_current_weather(request):
    city = request.GET.get("city", "Kiev")
    country_code = request.GET.get("countrycode", "")
    
    weather_api_object = CurrentWeather(GeoCording(city, country_code))
    
    weather_info = weather_api_object.send()
  
    return Response(weather_info)
```


<br>
<h2>Installation</h2>
<h3>Basic requirements</h3>
Install <a href = "https://docs.docker.com/get-docker/"><strong>Docker Engine</strong></a> and <a href = "https://docs.docker.com/compose/install/"><strong>Docker Compose</strong></a> on your PC.
<h3>Development</h3>

1. Rename *.env.dev-sample* to *.env.dev*.
1. Update the environment variables in the *docker-compose.yml* and *.env.dev* files.
1. Build the images and run the containers:

    ```bash
    $ docker-compose up -d --build
    ```
1. Don't forget to create superuser (needs to get access to admin panel)

    ```bash
    $ docker-compose exec web python3 manage.py createsuperuser
    ```

 Test it out at [http://localhost:8000](http://localhost:8000)(http://127.0.0.1:8000).
<h3>Production</h3>
Uses daphne + nginx.

1. Rename *.env.prod-sample* to *.env.prod* and *.env.prod.db-sample* to *.env.prod.db*. Update the environment variables as you need.
1. Build the images and run the containers:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```
1. Make migartions to DB

    ```sh
    $ docker-compose -f docker-compose.prod.yml exec web python3 manage.py makemigrations
    $ docker-compose -f docker-compose.prod.yml exec web python3 manage.py migrate
    ```
   
1. Collect staticfiles
   
    ```sh
    $ docker-compose -f docker-compose.prod.yml exec web python3 manage.py collectstatic
    ```
1. Don't forget to create superuser (needs to get access to admin panel)

    ```bash
    $ docker-compose exec web python3 manage.py createsuperuser
    ```
Test it out at [http://localhost:1337](http://localhost:1337)(http://127.0.0.1:1337). To apply changes, the image must be re-built.
