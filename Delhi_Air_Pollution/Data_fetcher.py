import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import csv

DELHI_LATITUDE = 28.6139
DELHI_LONGITUDE = 77.2090

# loading the API key from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')


def unix_to_date(unix):
    """Converts unix timestamp to date in the format of DD-MM-YYYY"""
    return datetime.fromtimestamp(unix).strftime('%d-%m-%Y')


def get_pollution_data():
    base_url = 'http://api.openweathermap.org/data/2.5/air_pollution/history?'
    url = base_url + f'lat={DELHI_LATITUDE}&lon={DELHI_LONGITUDE}&start=1420072200&end=1700697952&appid=' + API_KEY
    response = requests.get(url).json()
    unique_dates = []
    pollution_data = []
    for item in response['list']:
        date = unix_to_date(item['dt'])
        if date not in unique_dates:
            unique_dates.append(date)
            pollution_data.append({
                'city': 'Delhi',
                'date': date,
                'aqi': item['main']['aqi'],
                'co': item['components']['co'],
                'no': item['components']['no'],
                'no2': item['components']['no2'],
                'o3': item['components']['o3'],
                'so2': item['components']['so2'],
                'pm2_5': item['components']['pm2_5'],
                'pm10': item['components']['pm10'],
                'nh3': item['components']['nh3']

            })
    return pollution_data


# Writing data into a CSV file
file_path = 'Data/delhi_air_pollution_data.csv'
os.makedirs(os.path.dirname(file_path), exist_ok=True)
with open(file_path, 'w', newline='') as file:
    headers = ['city', 'date', 'aqi', 'co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for val in get_pollution_data():
        writer.writerow(val)

########################################
# The OpenWeather API only gives data of the last 3 years i.e.,2021,2022,2022, so we will be
# using kaggle dataset: https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india
# which contains data from 2015 to 2020
#######################################
