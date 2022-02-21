'use strict';


const host = window.location
const d = React.createElement;
const countries_api_url = host + "countries/"
const cities_api_url = host + "cities/"
const get_current_weather_api_url = host + "current_weather/"
const get_weather_icon_url = "http://openweathermap.org/img/wn/"

String.prototype.firstLetterCaps = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

class PopCountryList extends React.Component {
  constructor(props) {
    super(props);
    this.state = { error: null, isLoaded: false, countries: [], cities: [], country: null, country_code: null};
    this.handleChange = this.handleChange.bind(this);
  }


  componentDidMount(){
	  fetch(countries_api_url)
	    .then(res => res.json())
	    .then(
		    (result) => {
			    this.setState({
				isLoaded: true,
				countries: result
			    });
		    },

		    (error) => {
			    this.setState({
				    isLoaded: true,
				    error
			    });
		    }
	    )
  }

  render(){
	const {error, isLoaded, countries} = this.state;
	console.log("Current country" + this.state.country)
	if (error) {
		return d(
			"div",
			{},
			"Error occured!"
		);
	} else if (!isLoaded){
		return d(
			"div",
			{},
			"Loading..."
		);
	} else {
		return React.createElement(
			"div",
			null,
			React.createElement(
			'select',
                        {
				className: "form-select",
				onChange: this.handleChange,
			},
                        countries.map(country => (
                        React.createElement(
                                "option",
                                {
                                        key: country.id,
					value: `{"name":"${country.name}", "country_code":"${country.id}"}`,
                                },
                                country.name
                        	)
                        ))

			),
			d("p",null),

			React.createElement(
				PopCitiesList, 
				{
					country: this.state.country,
					country_code: this.state.country_code,
				},
			)
		
		);

	}

  }
	handleChange(e) {
	const new_country = e.target.options[e.target.selectedIndex].value;
	const json_new_country = JSON.parse(new_country)
	this.setState({country: json_new_country.name, country_code: json_new_country.country_code})
  }

   

}


class PopCitiesList extends React.Component {

  constructor(props) {
    super(props);
    this.state = { error: null, isLoaded: false, cities: [], last_country: null, cached_countries:[], load_on_cache:false, city: null};
    this.handleChange = this.handleChange.bind(this);
  }

  get_cities(){
	  if (this.props.country){
	  fetch(cities_api_url + "?country=" + this.props.country)
            .then(res => res.json())
            .then(
                    (result) => {
			    console.log(result)
			    this.state.cities = []
                            this.setState({
                                    cities: this.state.cities.concat(result),
				    last_country: this.props.country,
				    cached_countries: this.state.cached_countries.concat(
					    {
					    "name":this.props.country,
					    "cities":result,
					    }
				    ),
				    load_on_cache: false,
				    isLoaded: true
                            });
                    },

                    (error) => {
                            this.setState({
                                    isLoaded: true,
                                    error
                            });
                    }
            )
	} else {
		console.log("Wait for not null country")
	}
  }

  check_cache(element){
	var cache = this.state.cached_countries
	for (var i = 0; i < cache.length; i++){
		if (cache[i].name === element){
			return cache[i].cities;
		}
	}
	return false;
  }

  render(){
	if (this.state.last_country != this.props.country){
		const cached_item = this.check_cache(this.props.country)
		if (cached_item === false){
			this.get_cities()
		}else if ((cached_item != false)&&(!this.state.load_on_cache)){
			this.setState({cities: cached_item, load_on_cache: true})
		}
	}
	if (this.props.country){
        const {error, isLoaded, cities} = this.state;
        if (error) {
                return d(
                        "div",
                        {},
                        "Error occured!"
                );
        } else if (!isLoaded){
                return d(
                        "div",
                        {},
                        "Loading..."
                );
        } else {
		return d(
			"div",
			null,
			d(
        		'select',
        		{
				className: "form-select",
				onChange: this.handleChange,
			},
        		this.state.cities.map(function (item) {
			return React.createElement(
				'option',
				{
					key:item.id, 
					value:item.name,
				},
				item.name
			);
			})
		),
			d("p", null),
			d(
				WeatherInfoList,
				{
					city: this.state.city,
					country_code: this.props.country_code,
				}
			)
		);

	}
	
	} else {
		return "Choose country"
	}

  }

  handleChange(e) {
        const new_city = "" + e.target.options[e.target.selectedIndex].value;
        this.setState({city: new_city})
  }


}

class WeatherInfoList extends React.Component {
  constructor(props) {
    super(props);
    this.state = { error: null, isLoaded: false, weather_info: [], last_city: null, error_with: null};
  }


  get_weather(){
	  if (this.props.city){
          fetch(get_current_weather_api_url + "?city=" + this.props.city + "&countrycode=" + this.props.country_code)
            .then(res => res.json())
            .then(
                    (result) => {
			    console.log(result)
                            this.setState({
				last_city: this.props.city,
                                isLoaded: true,
                                weather_info: result,
				error: null,
                            });
                    },

                    (error) => {
                            this.setState({
                                    isLoaded: true,
                                    error,
				    error_with: this.props.city,
                            });
                    }
            )
  } else {
	  console.error("Wait for not null city value...")
  }
}

render(){
	if ((this.props.city != this.state.last_city) && (this.props.city != this.state.error_with)){
		this.get_weather()
	}
        if ((this.props.city) && (this.props.city != this.state.error_with)){
        const {error, isLoaded} = this.state;
	const weather_info = this.state.weather_info
	console.log("Error status = " + error)
        if (error) {
                return d(
                        "div",
                        {},
                        "Error occured!"
                );
        } else if (!isLoaded){
                return d(
                        "div",
                        {},
                        "Loading..."
                );
        } else {
		return d(
			"div",
			null,
			d("div", {className: "container"}, 
				d("div", {className: "row", style:{textAlign: "center"}},
					d("div", {className: "col"}, 
						d("img", {src:get_weather_icon_url + weather_info.weather[0].icon + "@2x.png"}),
						d("strong", null, weather_info.main.temp + "℃")
					)
				),
				d("div", {className: "row", style:{textAlign: "center"}},
					d(
						"div", 
						{className:"col"},
						"Feels like ",
						d(
							"strong",
							null,
							`${weather_info.main.feels_like}℃ `,
							d(
								"p", 
								null,
								`${weather_info.weather[0].description.firstLetterCaps()}`
							)
						)
					)
				),
				d("hr", null),
				d("div", {className: "row"},
                                        d("div", {className: "col", style: {textAlign: "left"}},
						"Humitidy: ",
                                                d("strong", null, weather_info.main.humidity + "%")
					),
					d("div", {className: "col", style:{textAlign: "right"}},
                                                "Visibility: ",
                                                d("strong", null, (parseFloat(weather_info.visibility)/1000).toFixed(1)),
						"km"
                                        )
                                ),
				d("p", null),
				d("div", {className: "row"},
                                        d("div", {className: "col", style:{textAlign: "center"}},
                                                "Pressure: ",
                                                d("strong", null, weather_info.main.pressure),
						"hPa",
						d("p", null, "Wind: ",
                                                d("strong", null, weather_info.wind.speed),
						"m/s"
						)
                                        )
                                )

			)
		);

        }
	
        }else {
                return "Choose city"
        }
}

}




const domContainerPopList = document.querySelector('#poplist_country');
ReactDOM.render(d(PopCountryList), domContainerPopList);

