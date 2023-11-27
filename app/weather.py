# Import necessary modules
from IPython.display import Image, display  # Used for displaying images in IPython environment
from pgeocode import Nominatim  # Used for querying location details from a given postal code
import requests  # Used for making HTTP requests
import json  # Used for working with JSON data

# Unicode representation of the degree sign
DEGREE_SIGN = u"\N{DEGREE SIGN}"

# Function to display a seven-day weather forecast for a given zip code
def display_forecast(zip_code, country_code="US"):
    """
    Displays a seven-day weather forecast for the provided zip code.

    Params:

        country_code (str): a valid country code (see supported country codes list). Default is "US".

        zip_code (str): a valid US zip code, like "20057" or "06510".
    """

    # Use Nominatim to get the geographical coordinates (latitude and longitude) for the given zip code
    nomi = Nominatim(country_code)
    geo = nomi.query_postal_code(zip_code)
    latitude = geo["latitude"]
    longitude = geo["longitude"]

    # Construct the URL to get information about the weather forecast for the specified location
    request_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)

    # Extract the forecast URL from the response
    forecast_url = parsed_response["properties"]["forecast"]
    forecast_response = requests.get(forecast_url)
    parsed_forecast_response = json.loads(forecast_response.text)

    # Extract and filter the daytime periods from the forecast data
    periods = parsed_forecast_response["properties"]["periods"]
    daytime_periods = [period for period in periods if period["isDaytime"] == True]

    # Display relevant information for each daytime period
    for period in daytime_periods:
        print("-------------")
        print(period["name"], period["startTime"][0:7])
        print(period["shortForecast"], f"{period['temperature']} {DEGREE_SIGN}{period['temperatureUnit']}")
        display(Image(url=period["icon"]))

    return True

# The following block is executed only if the script is run from the command line
if __name__ == "__main__":
    # Prompt the user to input a zip code
    zip_code = input("Please input a zip code (e.g., '06510'): ")

    # Call the display_forecast function with the provided zip code
    display_forecast(zip_code)
