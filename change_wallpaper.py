import requests
import random, os
import ctypes
import tkinter as tk
from tkinter import *
import json
import time

def get_wallpaper_id(config)-> int:

    def get_data(query) -> dict:
        print(query)
        response = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key=2f035cc83f954aae86b20901242904&q={query}&days=1&aqi=no&alerts=no')
        data = response.json()
        conditions = {}
        def convert_time(time) -> int:
            time_str = time.lower()
            pm = False
            if 'pm' in time_str:
                pm = True
            time_str = time_str.removesuffix('am').removesuffix('pm')
            time_str = time_str.replace(':', '')
            time = int(time_str)
            if pm:
                time += 1200
            elif time >= 1200:
                time -= 1200
            return time

        time = int(''.join(data['location']['localtime'].split(' ')[1].split(':')))
        conditions['time'] = time
        conditions['sunrise-time'] = convert_time(data['forecast']['forecastday'][0]['astro']['sunrise'])
        conditions['sunset-time'] = convert_time(data['forecast']['forecastday'][0]['astro']['sunset'])
        hour = (time - time%100)//100

        hour_data = data['forecast']['forecastday'][0]['hour'][hour]
        conditions['coverage'] = hour_data['cloud']
        conditions['temp'] = hour_data['temp_f']
        conditions['precip'] = (hour_data['precip_mm'])

        return conditions

    def group(config):
        query = config['location']

        groups = config['levels']
        print(groups)
        conditions = get_data(query)
        print(conditions)
        time_groups = {
            "Night": (conditions['sunset-time'] + 75, conditions['sunrise-time'] - 75),
            "Sunrise": (conditions['sunrise-time'] - 75, conditions['sunrise-time'] + 75),
            "Sunset": (conditions['sunset-time'] - 75, conditions['sunset-time'] + 75),
            "Midday": (conditions['sunrise-time'] + 75, conditions['sunset-time'] - 75)
        }

        
        
        
        coverage_groups = groups['coverage_groups']
        precip_groups = groups['precip_groups']
        temp_groups = groups['temp_groups']

        
        time = conditions['time']
        temp = conditions['temp']
        coverage = conditions['coverage']
        precip = conditions['precip']
        grouped_conditions = {}

        if time >= time_groups['Night'][0] or time <= time_groups['Night'][1]:
            grouped_conditions['time'] = 'Night'
        elif time >= time_groups['Sunrise'][0] and time <= time_groups['Sunrise'][1]:
            grouped_conditions['time'] = 'Sunrise'
        elif time >= time_groups['Sunset'][0] and time <= time_groups['Sunset'][1]:
            grouped_conditions['time'] = 'Sunrise'
        elif time >= time_groups['Midday'][0] and time <= time_groups['Midday'][1]:
            grouped_conditions['time'] = 'Midday'
        


        if coverage >= coverage_groups['partial_max']:
            grouped_conditions['coverage'] = 'Cloudy'
        elif coverage >= coverage_groups['clear_max']:
            grouped_conditions['coverage'] = 'Partial'
        else:
            grouped_conditions['coverage'] = 'Clear'
        

        if precip >= precip_groups["some_max"]:
            grouped_conditions['precip'] = "Rainy"
        elif precip >= precip_groups["mild_max"]:
            grouped_conditions['precip'] = "Some"
        elif precip >= precip_groups["none_max"]:
            grouped_conditions["precip"] = "Mild"
        else:
            grouped_conditions["precip"] = "None"


        if temp <= temp_groups['snowy_max']:
            grouped_conditions['temp'] = 'Snowy'
        elif temp <= temp_groups["chilly_max"]:
            grouped_conditions['temp'] = 'Chilly'
        elif temp <= temp_groups["mild_max"]:
            grouped_conditions['temp'] = 'Mild'
        else:
            grouped_conditions['temp'] = 'Warm'

        temp_class = grouped_conditions['temp']
        precip_class = grouped_conditions['precip']
        cloud_class = grouped_conditions['coverage']
        time_class = grouped_conditions['time']

        return (time_class+temp_class+cloud_class+precip_class)

    return group(config)

def change_wallpaper(config, key)-> None:
    appdata_path = f"{os.getenv('APPDATA')}\\QL_Desktop_Changer"

    image_number = random.choice(config['wallpaper'][key])
    image_name = f"{str('0'*(4-len(str(image_number))))+str(image_number)}.jpg"
    wallpaper_path = os.path.join(appdata_path, "images", image_name)
    wallpaper_style = 6
    SPI_SETDESKWALLPAPER = 20
    image = ctypes.c_wchar_p(wallpaper_path)
    print(wallpaper_path)
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image, wallpaper_style)
    pass

def open_config():
    config_path = os.path.join(f"{os.getenv('APPDATA')}\\QL_Desktop_Changer", "config.json")
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

def main():
    config = open_config()

    
    while True:
        try:
            key = get_wallpaper_id(config)
            change_wallpaper(config,key)
            time.sleep(config['interval'])
        except:
            time.sleep(60)
main()
