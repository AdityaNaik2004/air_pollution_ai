import requests
import pandas as pd
import datetime

def get_realtime_aqi(city="Delhi"):
    url = f"https://api.openaq.org/v2/latest?city={city}"
    r = requests.get(url).json()

    pm25 = None
    for m in r["results"][0]["measurements"]:
        if m["parameter"] == "pm25":
            pm25 = m["value"]

    date = datetime.datetime.now().strftime("%Y-%m-%d")

    return {"date": date, "pm25": pm25}

if __name__ == "__main__":
    print(get_realtime_aqi())