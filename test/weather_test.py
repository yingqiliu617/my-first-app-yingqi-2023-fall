# this is the "test/weather_test.py" file...

from app.weather import display_forecast


def test_weather_app():

    # Test with a valid US zip code
    assert display_forecast("06070") == True
