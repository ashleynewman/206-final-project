import json
import unittest
import os
import requests
import sqlite3

client_id = "m8K0vXjoUNXwMo4AfkpZnw"
API_KEY = "U-Y8QD3RL11wbcrmj9w3Yt3i_vFz97mdYqynngNtmGCFGZpmcdFRkGrMMztgvFwtvo7YR9JHpIkJk_pxr8qy9J9CGorVcWj0ac5poi4yMXWbliWoTxpgyIyIol-zX3Yx"
headers = {'Authorization': 'Bearer %s' % API_KEY}
base_url = "https://api.yelp.com/v3"

def create_connection(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return cur, conn

def city_restaurant_data(city_name, term_name, off):
    url = base_url + "/businesses/search"
    params = {'term': term_name, 'location': city_name, 'limit': 25, 'sort_by': 'rating', 'offset':off}
    req = requests.get(url, params=params, headers=headers, timeout=100)
    info = json.loads(req.text)
    return info
    
def table_set_up(data, city_name, cur, conn):
    cur.execute(f'CREATE TABLE IF NOT EXISTS {city_name} (id_num TEXT, name TEXT, food_type TEXT, rating INTEGER, longitude INTEGER, latitude INTEGER)')
    restaurant_list = data['businesses']
    for restaurant in restaurant_list:
        id_num = restaurant['id']
        name = restaurant['name']
        rating = restaurant['rating']
        longitude = restaurant['coordinates']['longitude']
        latitude = restaurant['coordinates']['latitude']
        type_of_food = restaurant['categories'][0]['title']
        cur.execute(f'INSERT INTO {city_name} (id_num, name, food_type, rating, longitude, latitude) VALUES (?,?,?,?,?,?)', (id_num, name, type_of_food, rating, longitude, latitude))
    conn.commit()

def top_cities():
    url = 'https://travel.usnews.com/rankings/best-foodie-destinations-in-the-usa/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    list_tags = soup.find_all("h3",{"class":"Heading__HeadingStyled-sc-1w5xk2o-0-h3 kuJtke Heading-sc-1w5xk2o-1 jFucEe"})
    d = []

    for tag in list_tags:
        a_tag = tag.find("a",{"class":"Anchor-byh49a-0 jHLCCZ"})
        name = a_tag.get('href').strip('/')
        city_name = name.split('_')
        city_string = ' '.join(city_name)
        d.append(city_string) 

    return d


def main():
    cur, conn = create_connection("db_test.db")

    i = 0
    while i < 76:
        rest_info = city_restaurant_data("New York City", "restaurant", i)
        table_set_up(rest_info, "New_York_City", cur, conn)
        i += 25

    ls = top_cities()
    print(ls)

if __name__ == "__main__":
    main()
    #unittest.main(verbosity=2)