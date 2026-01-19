import datetime
import pandas as pd
import hopsworks

# aqicn api doc: https://aqicn.org/json-api/doc/
aqicn_url = "https://api.waqi.info/feed/@10009"
country = "Sweden"
city = "Stockholm"
street = "Hornsgatan 108 Gata"
latitude = 59.3172224331124
longitude = 18.0486603472042
today = datetime.date.today()

import requests 

def get_pm25():
    url = aqicn_url
    import os
    params = {"token": os.getenv("AQICN_API_KEY")}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame()
    df['pm25'] = [data['data']['iaqi']['pm25']['v']]
    df['pm25'] = df['pm25'].astype('float32')

    df['country'] = country
    df['city'] = city
    df['street'] = street
    df['date'] = today
    df['date'] = pd.to_datetime(df['date'])
    df['url'] = url

    return df

aq_today_df = get_pm25()
print(aq_today_df)
print(aq_today_df.info())

def get_hourly_weather_forecast():
    # API doc: https://open-meteo.com/en/docs?longitude=18.0687&latitude=59.3294&timezone=auto
    url = "https://api.open-meteo.com/v1/ecmwf"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "precipitation", "wind_speed_10m", "wind_direction_10m"],
        "timezone": "auto",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    hourly = data['hourly']

    time_index = pd.to_datetime(hourly['time'])
    interval = time_index[1] - time_index[0]

    hourly_data = {
        "date": pd.date_range(
            start=time_index[0],
            end=time_index[-1] + interval,
            freq=interval,
            inclusive="left",
        )
    }

    hourly_data["temperature_2m_mean"] = hourly["temperature_2m"]
    hourly_data["precipitation_sum"] = hourly["precipitation"]
    hourly_data["wind_speed_10m_max"] = hourly["wind_speed_10m"]
    hourly_data["wind_direction_10m_dominant"] = hourly["wind_direction_10m"]

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    hourly_dataframe = hourly_dataframe.dropna()

    return hourly_dataframe



hourly_df = get_hourly_weather_forecast()
hourly_df = hourly_df.set_index('date')
daily_df = hourly_df.between_time('11:59', '12:01')
daily_df = daily_df.reset_index()
daily_df['date'] = pd.to_datetime(daily_df['date']).dt.date
daily_df['date'] = pd.to_datetime(daily_df['date'])
daily_df['city'] = city
print(daily_df)
print(daily_df.info())


project = hopsworks.login()
fs = project.get_feature_store()

air_quality_fg = fs.get_feature_group(name='air_quality', version=1)
weather_fg = fs.get_feature_group(name='weather', version=1)

air_quality_fg.insert(aq_today_df)
weather_fg.insert(daily_df, wait=True)
