import unittest
import sqlite3
import json
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def visualization_1(cur):
    avg1 = []
    avg1_5 = []
    avg2 = []
    avg2_5 = []
    avg3 = []
    cur.execute('SELECT city, total_score FROM HappyData JOIN WeatherData WHERE HappyData.overall_rank = WeatherData.location + 1 AND WeatherData.avg_temp < 10')
    temp_ones = cur.fetchall()
    for i in temp_ones:
        if i[1] < 50:
            avg1.append(i[0])
        elif i[1] > 70:
            avg2.append(i[0])
        else:
            avg1_5.append(i[0])
    cur.execute('SELECT city, total_score FROM HappyData JOIN WeatherData WHERE HappyData.overall_rank = WeatherData.location + 1 AND WeatherData.avg_temp >= 10 AND WeatherData.avg_temp <= 21')
    temp_twos = cur.fetchall()
    for i in temp_twos:
        if i[1] < 50:
            avg1_5.append(i[0])
        elif i[1] > 70:
            avg2_5.append(i[0])
        else:
            avg2.append(i[0]) 
    cur.execute('SELECT city, total_score FROM HappyData JOIN WeatherData WHERE HappyData.overall_rank = WeatherData.location + 1 AND WeatherData.avg_temp > 21')
    temp_threes = cur.fetchall()
    for i in temp_threes:
        if i[1] < 50:
            avg2.append(i[0])
        elif i[1] > 70:
            avg3.append(i[0])
        else:
            avg2_5.append(i[0])
    x_city = []
    y_rank = []
    for i in avg1:
        x_city.append(i)
        y_rank.append("1")
    for i in avg1_5:
        x_city.append(i)
        y_rank.append("1.5")
    for i in avg2:
        x_city.append(i)
        y_rank.append("2")
    for i in avg2_5:
        x_city.append(i)
        y_rank.append("2.5")
    for i in avg3:
        x_city.append(i)
        y_rank.append("3")
    fig, ax = plt.subplots()
    ax.bar(x_city, y_rank)
    ax.set_xlabel('city')
    ax.set_ylabel('rank')
    ax.set_title('Bargraph of the Average Temperature to Total Happiness Score Ranking Per City')
    fig.savefig('test1.png')
    plt.show()

def visualization_2(cur):
    avg1 = []
    avg1_5 = []
    avg2 = []
    avg2_5 = []
    avg3 = []
    cur.execute('SELECT city, avg_precipitation FROM HappyData, WeatherData WHERE HappyData.overall_rank = WeatherData.location + 1 AND WeatherData.avg_temp < 10')
    temp_ones = cur.fetchall()
    for i in temp_ones:
        if i[1] > 900:
            avg1.append(i[0])
        elif i[1] < 170:
            avg2.append(i[0])
        else:
            avg1_5.append(i[0])
    cur.execute('SELECT city, avg_precipitation FROM HappyData, WeatherData WHERE HappyData.overall_rank = WeatherData.location + 1 AND WeatherData.avg_temp >= 10 AND WeatherData.avg_temp <= 21')
    temp_twos = cur.fetchall()
    for i in temp_twos:
        if i[1] > 900:
            avg1_5.append(i[0])
        elif i[1] < 170:
            avg2_5.append(i[0])
        else:
            avg2.append(i[0]) 
    cur.execute('SELECT city, avg_precipitation FROM HappyData, WeatherData WHERE HappyData.overall_rank = WeatherData.location + 1 AND WeatherData.avg_temp > 21')
    temp_threes = cur.fetchall()
    for i in temp_threes:
        if i[1] > 900:
            avg2.append(i[0])
        elif i[1] < 170:
            avg3.append(i[0])
        else:
            avg2_5.append(i[0])
    x_city = []
    y_rank = []
    for i in avg1:
        x_city.append(i)
        y_rank.append("1")
    for i in avg1_5:
        x_city.append(i)
        y_rank.append("1.5")
    for i in avg2:
        x_city.append(i)
        y_rank.append("2")
    for i in avg2_5:
        x_city.append(i)
        y_rank.append("2.5")
    for i in avg3:
        x_city.append(i)
        y_rank.append("3")
    fig, ax = plt.subplots()
    ax.bar(x_city, y_rank)
    ax.set_xlabel('city')
    ax.set_ylabel('rank')
    ax.set_title('Bargraph of the Average Temperature to Average Precipitation Ranking Per City')
    fig.savefig('test2.png')
    plt.show()

def visualization_3(cur):
    x = []
    y = []
    cur.execute('SELECT avg_temp FROM WeatherData')
    temp_x = cur.fetchall()
    for i in temp_x:
        x.append(i[0])
    cur.execute('SELECT total_score FROM HappyData')
    temp_y = cur.fetchall()
    for i in temp_y:
        y.append(i[0])
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_xlabel('average temperature in degrees Celsius')
    ax.set_ylabel('total happiness score')
    ax.set_title('Scatterplot of the Average Temperature vs Total Happiness Score for Each City')
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r-")
    r = np.corrcoef(x, y)
    print("correlation coefficient: " + str(r[0,1]))
    fig.savefig('test3.png')
    plt.show()

def visualization_4(cur):
    x = []
    y = []
    cur.execute('SELECT avg_precipitation FROM WeatherData')
    temp_x = cur.fetchall()
    for i in temp_x:
        x.append(i[0])
    cur.execute('SELECT total_score FROM HappyData')
    temp_y = cur.fetchall()
    for i in temp_y:
        y.append(i[0])
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_xlabel('average precipitation in mm')
    ax.set_ylabel('total happiness score')
    ax.set_title('Scatterplot of the Average Temperature vs Total Happiness Score for Each City')
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r-")
    r = np.corrcoef(x, y)
    print("correlation coefficient: " + str(r[0,1]))
    fig.savefig('test4.png')
    plt.show()

def visualization_5(cur):
    cur.execute('SELECT avg_temp FROM WeatherData')
    column1 = cur.fetchall()
    x = stats.zscore(column1)
    cur.execute('SELECT avg_precipitation FROM WeatherData')
    column2 = cur.fetchall()
    y = stats.zscore(column2)
    zipped = list(zip(x, y))
    avg = []
    for i in zipped:
        avg.append((i[0][0] + i[1][0]) / 2)
    cur.execute('SELECT total_score FROM HappyData')
    tot_score = []
    temp_y = cur.fetchall()
    for i in temp_y:
        tot_score.append(i[0])
    fig, ax = plt.subplots()
    ax.scatter(avg, tot_score)
    ax.set_xlabel('average weather index')
    ax.set_ylabel('total happiness score')
    ax.set_title('Scatterplot of the weather index vs happiness score for each city')
    z = np.polyfit(avg, tot_score, 1)
    p = np.poly1d(z)
    plt.plot(avg, p(avg), "r-")
    r = np.corrcoef(avg, tot_score)
    print("correlation coefficient: " + str(r[0,1]))
    fig.savefig('test5.png')
    plt.show()

def visualization_6(cur):
    cur.execute('SELECT avg_temp, avg_precipitation, city, total_score FROM WeatherData, HappyData JOIN Locations WHERE Locations.id = WeatherData.location')
    x = cur.fetchall()
    print(x)





def main():
    cur, conn = setUpDatabase('finalData.db')
    # visualization_1(cur)
    # visualization_2(cur) 
    # visualization_3(cur)
    # visualization_4(cur)
    # visualization_5(cur)
    # visualization_6(cur)
    


if __name__ == "__main__":
    main()