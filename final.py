import json
import os
import requests
import sqlite3
from bs4 import BeautifulSoup
import calcs_vis

location_lat_long_api_key = "MQosMrFCrMn14jS6h32hinuTQWrHDd5q"
weather_api_key = "IYyo8JaZe0W8MznnblAr2cRPpDeeTQGa"


def create_connection(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return cur, conn

def lat_long_table(cur, conn, lat, long, place):
    cur.execute('CREATE TABLE IF NOT EXISTS LatLongData (id INTEGER, latitude INTEGER, longitude INTEGER)')
    cur.execute('INSERT INTO LatLongData (id, latitude, longitude) VALUES (?,?,?)', (place, lat, long))

def get_weather_data(cur, conn, location):
  
    #below, the lat_long_info is a json object with the lat and long coordinates inside
    #the only thing with the url that needs to change is the "location" parameter I guess
    #to whatever city name we pass in
    #otherwise i wouldn't change this url
    
    mapquest_url = f"http://open.mapquestapi.com/geocoding/v1/address?key={location_lat_long_api_key}&location={location}" #&location=Boston, MA
    req2 = requests.get(mapquest_url)
    lat_long_info = json.loads(req2.text)
   
    #below gets dictionary of just the lat and long for the city
    results = lat_long_info['results'][0]['locations'][0]['latLng']
    #below are the lat and long strings, gotta keep them as strings so we can pass them
    #into the api for weather data
    lat_str = results['lat']
    long_str = results['lng']
    lat_long_table(cur, conn, lat_str, long_str, location)
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
        percip = month['prcp']
  
        weather_data[month_num_string] = (temp_string_celcius, percip) #, pressure, sunshine
  
    
    return weather_data
    

def weather_table(data, cur, conn, location, temp_list):
    cur.execute(f'CREATE TABLE IF NOT EXISTS WeatherData (location INTEGER, average_temp_id INTEGER, average_precipitation_id INTEGER)') #, avg_pressure INTEGER, avg_hours_sunshine INTEGER
    temp = 0
    percip = 0
  
    for key in data:
        temp += int(data[key][0])
        percip += int(data[key][1])
 
    avg_temp = temp / 12
    avg_percip = percip / 12

    final_temp = 0
    if (avg_temp in temp_list) == False:
        temp_list.append(avg_temp)
        final_temp = temp_list.index(avg_temp)
        cur.execute('INSERT INTO Temperatures (temperature, id) VALUES (?,?)', (avg_temp, final_temp))
    else:
        final_temp = temp_list.index(avg_temp)

 
    cur.execute(f'INSERT INTO WeatherData (location, average_temp_id, average_precipitation_id) VALUES (?,?,?)', (location, final_temp, avg_percip)) #, avg_pressure, avg_sunshine
    conn.commit()

def website_prep():
    url = 'https://wallethub.com/edu/happiest-places-to-live/32619'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table",{"class":"cardhub-edu-table center-aligned sortable"})

    body = table.find("tbody")
    row_tags = body.find_all("tr")
    return row_tags


def get_website_data(i, row_tags):
    tr_tag = row_tags[i]
    td_tags = tr_tag.find_all("td")
    overall_rank = int(td_tags[0].text.strip())
    city_name = td_tags[1].text.strip()

    total_score = float(td_tags[2].text.strip())
    emotional_and_pysical_score = int(td_tags[3].text.strip())
    income_and_employment_score = int(td_tags[4].text.strip())
    community_and_enviornment_score = int(td_tags[5].text.strip())
    row = [overall_rank, city_name, total_score, emotional_and_pysical_score, income_and_employment_score, community_and_enviornment_score]
    return row
    

def website_table(data, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS HappyData (overall_rank INTEGER, city TEXT, total_score INTEGER, well_being_rank INTEGER, income_employment_rank INTEGER, community_environment_rank INTEGER)')
    cur.execute('INSERT INTO HappyData (overall_rank, city, total_score, well_being_rank, income_employment_rank, community_environment_rank)  VALUES (?,?,?,?,?,?)', (data[0], data[1], data[2], data[3], data[4], data[5]))
    conn.commit()

def get_start_index(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS HappyData (overall_rank INTEGER, city TEXT, total_score INTEGER, well_being_rank INTEGER, income_employment_rank INTEGER, community_environment_rank INTEGER)')
    cur.execute('SELECT city FROM HappyData')
    x = cur.fetchall()
    if len(x) >= 1 and len(x) < 182:
        return len(x)
    elif len(x) > 181: #181 is last
        return -1
    else:
        return 0
    

def get_temp_lists(cur):
    cur.execute('CREATE TABLE IF NOT EXISTS Temperatures (temperature INTEGER, id INTEGER)')
    cur.execute('SELECT temperature FROM Temperatures')
    x = cur.fetchall()
    t = []
    for i in x:
        t.append(i)
    return t

def main():
    cur, conn = create_connection("finalData1.db")

    start = 1
    stop = 25
    row_tags = website_prep()
    temp_list = get_temp_lists(cur)

    while start < stop:
        current_index = get_start_index(cur, conn)
        if current_index == -1:
            calcs_vis.main()
            break

        location = get_website_data(current_index, row_tags) #list of current location's data from website table
        weather_data = get_weather_data(cur, conn, location[1])
        weather_table(weather_data, cur, conn, location[1], temp_list)
        website_table(location, cur, conn) #maybe make location the current_index here to reduce database duplicate data
        # location_table(cur, conn, location[1], current_index)

        start += 1


if __name__ == "__main__":
    main()