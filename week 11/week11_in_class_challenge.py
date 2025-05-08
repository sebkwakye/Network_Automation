'''
Python program that retrieves the current weather for a given city using the OpenWeatherMap API.

API: OpenWeatherMap (https://openweathermap.org/api)
https://home.openweathermap.org/users/sign_up
'''

import requests

# Define API key 
API_KEY = "128502ffd60981675a141af6c34e6cf2"

# Prompt user for a city name
city = input("Enter a city name for its current weather: ")

# Build API request URL; using metric units for Celsius
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

# Make request to the OpenWeatherMap API and store response variable
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON data from the response

    print(data)

    # Extract data from the JSON response
    main = data.get('main', {})
    weather = data.get('weather', [{}])[0]

    # Get temperature in Celsius and calculate Fahrenheit
    temp_c = main.get('temp')
    temp_f = temp_c * 9/5 + 32 if temp_c is not None else None

    # Get humidity and weather description
    humidity = main.get('humidity')
    description = weather.get('description')
    icon_code = weather.get('icon')

    # Print the collected weather information
    print(f"Current weather in {city}:")
    if temp_c is not None and temp_f is not None:
        print(f"Temperature: {temp_c:.2f}°C / {temp_f:.2f}°F")
    else:
        print("Temperature data not available.")

    if humidity is not None:
        print(f"Humidity: {humidity}%")
    else:
        print("Humidity data not available.")

    if description:
        print(f"Description: {description.capitalize()}")
    else:
        print("Weather description not available.")

    # Display the weather icon URL
    if icon_code:
        print(f"Weather Icon URL: http://openweathermap.org/img/wn/{icon_code}.png")
    else:
        print("Weather icon not available.")

else:
    print("Error fetching weather data. Please check your API key and city name.")
