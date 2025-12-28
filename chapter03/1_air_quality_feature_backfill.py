# Download air quality historical data from: https://aqicn.org/city/sweden/stockholm-hornsgatan-108-gata/
# Read your CSV file into a DataFrame
import pandas as pd

csv_file = "air-quality-data.csv"
df = pd.read_csv(csv_file, parse_dates=["date"], skipinitialspace=True)

# Data cleaning
df_aq = df[["date", "pm25"]].copy()
df_aq["pm25"] = df_aq["pm25"].astype("float32")
# Drop any rows with missing data
df_aq.dropna(inplace=True)

# aqicn api doc: https://aqicn.org/json-api/doc/
aqicn_url = "https://api.waqi.info/feed/@10009"
country = "Sweden"
city = "Stockholm"
street = "Hornsgatan 108 Gata"

df_aq["country"] = country
df_aq["city"] = city
df_aq["street"] = street
df_aq["url"] = aqicn_url

import hopsworks

project = hopsworks.login()
fs = project.get_feature_store()

import great_expectations as ge

aq_expectation_suite = ge.core.ExpectationSuite(
    expectation_suite_name="aq_expectation_suite"
)

aq_expectation_suite.add_expectation(
    ge.core.expectation_configuration.ExpectationConfiguration(
        expectation_type="expect_column_min_to_be_between",
        kwargs={
            "column": "pm25",
            "min_value": -0.1,
            "max_value": 500.0,
            "strict_min": True,
        },
    )
)

air_quality_fg = fs.get_or_create_feature_group(
    name="air_quality",
    description="Air Quality characteristics of each day",
    version=1,
    primary_key=["country", "city", "street"],
    event_time="date",
    expectation_suite=aq_expectation_suite,
)

print(df_aq)
air_quality_fg.insert(df_aq, wait=True)
air_quality_fg.update_feature_description("date", "Date of measurement of air quality")
air_quality_fg.update_feature_description(
    "country",
    "Country where the air quality was measured (sometimes a city in acqcn.org)",
)
air_quality_fg.update_feature_description(
    "city", "City where the air quality was measured"
)
air_quality_fg.update_feature_description(
    "street", "Street in the city where the air quality was measured"
)
air_quality_fg.update_feature_description(
    "pm25",
    "Particles less than 2.5 micrometers in diameter (fine particles) pose health risk",
)


import requests


def get_sensor_geo():
    import os

    params = {"token": os.getenv("AQICN_API_KEY")}
    response = requests.get(aqicn_url, params=params)
    response.raise_for_status()
    data = response.json()
    return data['data']['city']['geo']


def get_historical_weather(start_date, end_date, latitude, longitude):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "temperature_2m_mean",
            "precipitation_sum",
            "wind_speed_10m_max",
            "wind_direction_10m_dominant",
        ],
        "timezone": "GMT",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    daily = data["daily"]

    df = pd.DataFrame(
        {
            "date": pd.to_datetime(daily["time"]),
            "temperature_2m_mean": daily["temperature_2m_mean"],
            "precipitation_sum": daily["precipitation_sum"],
            "wind_speed_10m_max": daily["wind_speed_10m_max"],
            "wind_direction_10m_dominant": daily["wind_direction_10m_dominant"],
        }
    )

    return df


weather_expectation_suite = ge.core.ExpectationSuite(
    expectation_suite_name="weather_expectation_suite"
)


def expect_greater_than_zero(col):
    weather_expectation_suite.add_expectation(
        ge.core.expectation_configuration.ExpectationConfiguration(
            expectation_type="expect_column_min_to_be_between",
            kwargs={
                "column": col,
                "min_value": -0.1,
                "max_value": 1000.0,
                "strict_min": True,
            },
        )
    )


expect_greater_than_zero("precipitation_sum")
expect_greater_than_zero("wind_speed_10m_max")

weather_fg = fs.get_or_create_feature_group(
    name="weather",
    description="Weather characteristics of each day",
    version=1,
    primary_key=["city"],
    event_time="date",
    expectation_suite=weather_expectation_suite,
)
start_date = pd.Series.min(df_aq["date"])
start_date = start_date.strftime("%Y-%m-%d")
import datetime

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
end_date = yesterday.strftime("%Y-%m-%d")
geo = get_sensor_geo()
weather_df = get_historical_weather(start_date, end_date, geo[0], geo[1])
weather_df['city'] = city
print(weather_df)
weather_fg.insert(weather_df, wait=True)

weather_fg.update_feature_description("date", "Date of measurement of weather")
weather_fg.update_feature_description(
    "city", "City where weather is measured/forecast for"
)
weather_fg.update_feature_description("temperature_2m_mean", "Temperature in Celsius")
weather_fg.update_feature_description(
    "precipitation_sum", "Precipitation (rain/snow) in mm"
)
weather_fg.update_feature_description(
    "wind_speed_10m_max", "Wind speed at 10m abouve ground"
)
weather_fg.update_feature_description(
    "wind_direction_10m_dominant", "Dominant Wind direction over the dayd"
)
