import unittest
import sqlite3
import json
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from numpy import percentile
import csv

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def calculation(cur):
    cur.execute('SELECT temperature FROM WeatherData JOIN Temperatures ON Temperatures.id = WeatherData.average_temp_id')
    temperatures = cur.fetchall()
    cur.execute('SELECT total_score FROM HappyData')
    happy_scores = cur.fetchall()
    cur.execute('SELECT average_precipitation_id FROM WeatherData')
    precip = cur.fetchall()
    cur.execute('SELECT city FROM HappyData')
    city_names = cur.fetchall()
    return temperatures, happy_scores, precip, city_names

def write_csv(x, y, names_city, file_name, headers):
    
    file = open(file_name, mode='w', newline='', encoding="utf8")
    writer = csv.writer(file, delimiter=',')
    writer.writerow(headers)
    for i in range(len(x)):
        writer.writerow([names_city[i], x[i], y[i]])
    file.close() 

def visualization1(temp, happy, city_names):
    x = []
    y = []
    names_city = []
    for i in temp:
        x.append(i[0])
    for i in happy:
        y.append(i[0])
    for i in city_names:
        names_city.append(i[0])

    write_csv(x, y, names_city, "file1.csv", ['City', 'Temperature', 'Happiness Score'])
    fig, ax = plt.subplots()
    ax.scatter(x, y, color='#32db84')
    ax.set_xlabel('temperature in degrees Celcius')
    ax.set_ylabel('total happiness score')
    ax.set_title('Happiness Scores vs. Average Temperatures for Different US Cities')
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r-")
    r = np.corrcoef(x, y)
    print("correlation coefficient: " + str(r[0,1]))

    s1 = sorted(x)
    s2 = sorted(y)
    avg1 = (s1[0] + s1[-1]) / 2
    avg2 = (s2[0] + s2[-1]) / 2
    plt.axvline(avg1)
    plt.axhline(avg2)
    fig.savefig('v1.png')
    plt.show()

def visualization2(precip, happy, city_names):
    x = []
    y = []
    names_city = []
    for i in precip:
        x.append(i[0])
    for i in happy:
        y.append(i[0])
    for i in city_names:
        names_city.append(i[0])

    write_csv(x, y, names_city, "file2.csv", ['City', 'Precipitation', 'Happiness Score'])

    fig, ax = plt.subplots()
    ax.scatter(x, y, color='#7303fc')
    ax.set_xlabel('precipitation in mm')
    ax.set_ylabel('total happiness score')
    ax.set_title('Happiness Scores vs. Precipitation for Different US Cities')
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r-")
    r = np.corrcoef(x, y)
    print("correlation coefficient: " + str(r[0,1]))

    s1 = sorted(x)
    s2 = sorted(y)
    avg1 = (s1[0] + s1[-1]) / 2
    avg2 = (s2[0] + s2[-1]) / 2
    plt.axvline(avg1)
    plt.axhline(avg2)

    fig.savefig('v2.png')
    plt.show()

def box_and_wiskers(data, x_label, fig_name, title, csv_name):
    good_data = []
    for i in data:
        good_data.append(i[0])
    fig1, ax1 = plt.subplots()

    ax1.set_title(title)
    ax1.set_xlabel(x_label)

    plt.boxplot(good_data, vert=False)
    fig1.savefig(fig_name)   
    plt.show()

    quartiles = percentile(good_data, [25, 50, 75]).tolist()
    data_min, data_max = min(good_data), max(good_data)

    iqr = stats.iqr(good_data, interpolation='midpoint')

    file = open(csv_name, mode='w', newline='', encoding="utf8")
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['Min', 'Q1', 'Median', 'Q3', 'Max', 'IQR'])
    writer.writerow([data_min, quartiles[0], quartiles[1], quartiles[2], data_max, iqr])
    file.close()


def main():
    cur, conn = setUpDatabase('finalData1.db')
    temperatures, happy_scores, precipitation, city_names = calculation(cur)
    visualization1(temperatures, happy_scores, city_names)
    visualization2(precipitation, happy_scores, city_names)
    box_and_wiskers(precipitation, 'Precipitation (mm)', 'vis3.png', 'Boxplot Precipitation', 'precip.csv')
    box_and_wiskers(temperatures, 'Temperature (Deg. Celcius)', 'vis4.png', 'Boxplot Temperature', 'temp.csv')
    box_and_wiskers(happy_scores, 'Happiness Scores', 'vis5.png', 'Boxplot Happiness Scores', 'happy.csv')

    


if __name__ == "__main__":
    main()