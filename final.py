import json
import unittest
import os
import requests
import sqlite3
from bs4 import BeautifulSoup
import matplotlib
import matplotlib.pyplot as plt

# client_id = "m8K0vXjoUNXwMo4AfkpZnw"
# API_KEY = "U-Y8QD3RL11wbcrmj9w3Yt3i_vFz97mdYqynngNtmGCFGZpmcdFRkGrMMztgvFwtvo7YR9JHpIkJk_pxr8qy9J9CGorVcWj0ac5poi4yMXWbliWoTxpgyIyIol-zX3Yx"
# headers = {'Authorization': 'Bearer %s' % API_KEY}
# base_url = "https://api.yelp.com/v3"

#api_key = "3b22c3c6736254515a21e9f73410387b"
#base_url = "https://history.openweathermap.org/data/2.5/aggregated/month?"

location_lat_long_api_key = "MQosMrFCrMn14jS6h32hinuTQWrHDd5q"
weather_api_key = "IYyo8JaZe0W8MznnblAr2cRPpDeeTQGa"


def create_connection(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return cur, conn

def get_url(city_name, month, state_abbr):
    # url = base_url + "q=" + city_name + ",US-" + state_abbr + "&month=" + month + "&appid=" + api_key
    
    #below, the lat_long_info is a json object with the lat and long coordinates inside
    #the only thing with the url that needs to change is the "location" parameter I guess
    #to whatever city name we pass in
    #otherwise i wouldn't change this url
    
    mapquest_url = f"http://open.mapquestapi.com/geocoding/v1/address?key={location_lat_long_api_key}&location=Boston, MA"
    req2 = requests.get(mapquest_url)
    lat_long_info = json.loads(req2.text)
    print("LAT LONG API RESULT: \n\n\n")
    print(json.dumps(lat_long_info, indent=4))
    print("DATA:\n")
    #below gets dictionary of just the lat and long for the city
    results = lat_long_info['results'][0]['locations'][0]['latLng']
    #below are the lat and long strings, gotta keep them as strings so we can pass them
    #into the api for weather data
    lat_str = results['lat']
    long_str = results['lng']
    print(results)


    #the "weather_info" json object should return monthly weather data in celcius 
    #given the lat and long as imputs
    #otherwise I don't think we need to change anything else about this

    #key = month, val = temp in celcius
    weather_data = {}
    
    url_weather = f"https://api.meteostat.net/v2/point/climate?lat={lat_str}&lon={long_str}&alt=58&x-api-key={weather_api_key}"
    req = requests.get(url_weather)
    weather_info = json.loads(req.text)

    data_json = weather_info['data']
    for month in data_json:
        #gets month of interest, 1 = Jan, 2 = Feb, 3 = March, etc.
        month_num_string = month['month']
        #gets average of month in celcius
        temp_string_celcius = month['tavg']
        weather_data[month_num_string] = temp_string_celcius
    print("Weather API RESULT: \n\n\n")
    #print(json.dumps(weather_info, indent=4))

    
    #Not sure what this should return, maybe make 
    #2 functions, 1 for each api request?
    return info
    

def get_weather_data(data, cur, conn, table_name, month):
    mean_temp = data["result"]["temp"]["mean"]
    mean_humidity = data["result"]["humidity"]["mean"]
    mean_rain = data["result"]["precipitation"]["mean"]
    mean_clouds = data["result"]["clouds"]["mean"]
    sunshine_hours = data["result"]["sunshine_hours"]

    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (month INTEGER, temp INTEGER, humidity INTEGER, precipitation INTEGER, clouds INTEGER, sunshine INTEGER')
    cur.execute(f'INSERT INTO {table_name} (month, temp, humidity, precipitation, clouds, sunshine)  VALUES (?,?,?,?,?,?)', (month, mean_temp, mean_humidity, mean_rain, mean_clouds, sunshine_hours))
    print(month, mean_temp, mean_humidity, mean_rain, mean_clouds, sunshine_hours)
    conn.commit()

def get_website_data():
    url = 'https://wallethub.com/edu/happiest-places-to-live/32619'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table",{"class":"cardhub-edu-table center-aligned sortable"})

    headers = []
    head = table.find("thead")
    tr = head.find("tr")
    head_tags = tr.find_all("th")
    for tag in head_tags:
        headers.append(tag.text.strip())
    
    state_ids = []
    data = []
    body = table.find("tbody")
    row_tags = body.find_all("tr")
    for tr_tag in row_tags:
        td_tags = tr_tag.find_all("td")
        overall_rank = int(td_tags[0].text.strip())
        city_name = td_tags[1].text.strip()
        #---------
        temp = city_name.split(",")
        state_ids.append((temp[0], temp[1]))
        #--------
        total_score = float(td_tags[2].text.strip())
        emotional_and_pysical_score = int(td_tags[3].text.strip())
        income_and_employment_score = int(td_tags[4].text.strip())
        community_and_enviornment_score = int(td_tags[5].text.strip())
        row = [overall_rank, city_name, total_score, emotional_and_pysical_score, income_and_employment_score, community_and_enviornment_score]
        data.append(row)
    return data, state_ids

def make_website_table(data, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS HappyData (overall_rank INTEGER, city TEXT, total_score INTEGER, well_being_rank INTEGER, income_employment_rank INTEGER, community_environment_rank INTEGER)')
    for i in data:
        cur.execute('INSERT INTO HappyData (overall_rank, city, total_score, well_being_rank, income_employment_rank, community_environment_rank)  VALUES (?,?,?,?,?,?)', (i[0], i[1], i[2], i[3], i[4], i[5]))
    conn.commit()

def process_data():
    pass

def visualization_1():
    pass

def visualization_2():
    pass

# def city_restaurant_data(city_name, term_name, off):
#     url = base_url + "/businesses/search"
#     params = {'term': term_name, 'location': city_name, 'limit': 25, 'sort_by': 'rating', 'offset':off}
#     req = requests.get(url, params=params, headers=headers, timeout=100)
#     info = json.loads(req.text)
#     return info
    
# def table_set_up(data, city_name, cur, conn):
#     cur.execute(f'CREATE TABLE IF NOT EXISTS {city_name} (id_num TEXT, name TEXT, food_type TEXT, rating INTEGER, longitude INTEGER, latitude INTEGER)')
#     restaurant_list = data['businesses']
#     for restaurant in restaurant_list:
#         id_num = restaurant['id']
#         name = restaurant['name']
#         rating = restaurant['rating']
#         longitude = restaurant['coordinates']['longitude']
#         latitude = restaurant['coordinates']['latitude']
#         type_of_food = restaurant['categories'][0]['title']
#         cur.execute(f'INSERT INTO {city_name} (id_num, name, food_type, rating, longitude, latitude) VALUES (?,?,?,?,?,?)', (id_num, name, type_of_food, rating, longitude, latitude))
#     conn.commit()

# def top_cities():
#     url = 'https://travel.usnews.com/rankings/best-foodie-destinations-in-the-usa/'
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}

#     r = requests.get(url, headers=headers)
#     soup = BeautifulSoup(r.text, "html.parser")

#     list_tags = soup.find_all("h3",{"class":"Heading__HeadingStyled-sc-1w5xk2o-0-h3 kuJtke Heading-sc-1w5xk2o-1 jFucEe"})
#     d = []

#     for tag in list_tags:
#         a_tag = tag.find("a",{"class":"Anchor-byh49a-0 jHLCCZ"})
#         name = a_tag.get('href').strip('/')
#         city_name = name.split('_')
#         city_string = ' '.join(city_name)
#         d.append(city_string) 

#     return d


def main():
    cur, conn = create_connection("db_test.db")
    web_data, state_ids = get_website_data()
    make_website_table(web_data, cur, conn)

    i = 1
    while i < 13:
        for j in state_ids:
            x = get_url(j[0], str(i), j[1])
            get_weather_data(x, cur, conn, "Monthly Weather Averages", i)
        i += 1

    # i = 0
    # while i < 76:
    #     rest_info = city_restaurant_data("New York City", "restaurant", i)
    #     table_set_up(rest_info, "New_York_City", cur, conn)
    #     i += 25

    # ls = top_cities()
    # print(ls)

if __name__ == "__main__":
    main()
    #unittest.main(verbosity=2)