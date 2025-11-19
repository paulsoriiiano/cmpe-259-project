"""
API calls to OpenMeteo.
"""


import openmeteo_requests
import requests_cache

from geopy.geocoders import Nominatim
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
_cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
_retry_session = retry(_cache_session, retries = 5, backoff_factor = 0.2)

# Setup OpenMeteo Client
_openmeteo = openmeteo_requests.Client(session = _retry_session)


def get_weather(location: str, days: int = 0):
  """ Uses OpenMeteo API for fetch weather data for a given location. """
  try:
    # 1. Get location latitude and longitude
    geolocator = Nominatim(user_agent="ca_parks_va_agent")
    loc = geolocator.geocode(f"{location}, California", timeout=10)
    if not loc:
      return f"Sorry, {location} could not be found. Please try again."

    latitude, longitude = loc.latitude, loc.longitude

    # 2. Fetch weather data
    # 2.1 Weather codes (from OpenMeteo docs)
    weather_code_map = {
      0: "clear sky",
      1: "mainly clear", 2: "partly cloudy", 3: "overcast",
      45: "foggy", 48: "rime fog",
      51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle",
      61: "light rain", 63: "moderate rain", 65: "heavy rain",
      71: "light snow", 73: "moderate snow", 75: "heavy snow",
      95: "slight to moderate thunderstorms",
      80: "rain showers"
    }

    # 2.2 Call client
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
      "latitude": latitude,
      "longitude": longitude,
      "current": ["temperature_2m", "relative_humidity_2m", "weather_code", "precipitation",
                  "rain", "showers", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
      "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"],
      "wind_speed_unit": "mph",
      "temperature_unit": "fahrenheit",
      "precipitation_unit": "inch",
      "forecast_days": days + 1 # +1 to include today's forecast if days > 0
    }

    responses = _openmeteo.weather_api(url, params=params)

    # 3. Parse data
    response = responses[0]

    if days == 0 or response.Daily() is None: # For current weather or if daily forecast is not available
        current = response.Current()
        temperature = int(current.Variables(0).Value())
        humidity = int(current.Variables(1).Value())
        precipitation = current.Variables(3).Value()
        rain = current.Variables(4).Value()
        showers = current.Variables(5).Value()
        wind = int(current.Variables(6).Value())
        wind_direction = current.Variables(7).Value() # Corrected from Variable to Variables
        wind_gusts = int(current.Variables(8).Value())  # Corrected from Variable to Variables

        code = current.Variables(2).Value()
        condition = weather_code_map.get(code, "Unknown conditions")

        return (
            f"Current weather in {location}: {condition}.\n"
            f"- Temperature: {temperature}°F, Humidity: {humidity}%\n"
            f"- Wind: {wind} mph (gusts up to {wind_gusts} mph) from {wind_direction}°\n"
            f"- Precipitation: {precipitation} inches (Rain: {rain} inches, Showers: {showers} inches)"
        )
    else:
        daily = response.Daily()
        daily_weather_code = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(3).ValuesAsNumpy()
        daily_wind_speed_10m_max = daily.Variables(4).ValuesAsNumpy()

        forecast_lines = [f"{days}-day forecast for {location}:"]
        for i in range(min(days, len(daily_weather_code))):
            condition = weather_code_map.get(daily_weather_code[i], "Unknown conditions")
            max_temp = daily_temperature_2m_max[i]
            min_temp = daily_temperature_2m_min[i]
            precipitation = daily_precipitation_sum[i]
            max_wind = daily_wind_speed_10m_max[i]

            forecast_lines.append(
                f"Day {i+1}: {condition}\n" 
                f"- Temp: {min_temp:.1f} — {max_temp:.1f}°F\n"
                f"- Precipitation: {precipitation:.2f} inches\n"
                f"- Max Wind: {max_wind:.1f} mph"
            )
        return "\n\n".join(forecast_lines)

  except Exception as e:
    return f"Error retrieving data: {e}"
