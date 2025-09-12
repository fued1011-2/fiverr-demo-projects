import requests
import pandas as pd

def fetch_weather(latitude=52.52, longitude=13.41, output_file="weather.csv"):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "forecast_days": 1
    }
    response = requests.get(url, params=params, timeout=60)
    data = response.json()

    times = data['hourly']['time']
    temps = data['hourly']['temperature_2m']

    df = pd.DataFrame({"time": times, "temperature_C": temps})
    df.to_csv(output_file, index=False)
    print(f"Saved weather data to {output_file}")

if __name__ == "__main__":
    fetch_weather()
