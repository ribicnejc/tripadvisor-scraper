"""Histogram, ki prikazuje koliko so turisti prepotovali glede na državo. 1km, 2km, 3km, 5km, ... 100+km"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import math
from matplotlib.ticker import PercentFormatter

from masters.data_managers.utils import database_utils
import datetime


def get_path_distance(list):
    lat1 = list[0][5]
    lon1 = list[0][6]
    distance = 0
    for e in list:
        lat2, lon2 = e[5], e[6]
        dist = get_kilometers(float(lat1), float(lon1), float(lat2), float(lon2))
        distance += dist
        lat1 = lat2
        lon1 = lon2
    return distance


def get_kilometers(lat1, lon1, lat2, lon2):
    R = 6371000  # metres
    fi1 = lat1 * math.pi / 180
    fi2 = lat2 * math.pi / 180
    deltafi = (lat2 - lat1) * math.pi / 180
    delta = (lon2 - lon1) * math.pi / 180

    a = math.sin(deltafi / 2) * math.sin(deltafi / 2) + math.cos(fi1) * math.cos(fi2) * math.sin(delta / 2) * math.sin(delta / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return (R * c) / 1000  # in km

def subtract(d1, d2):
    da1 = datetime.datetime(int(d1[0:4]), int(d1[4:6]), int(d1[6:8]), 0, 0)
    da2 = datetime.datetime(int(d2[0:4]), int(d2[4:6]), int(d2[6:8]), 0, 0)
    delta = da1 - da2
    return abs(delta.days)


def kilometers_traveled(country, year_from, year_to, year):
    sql = """select review_id, user_id, calculated_dates, review_date, review_experience_date, location_lat, location_lng from reviews
where calculated_dates > {year_from}
    and calculated_dates < {year_to}
order by user_id, cast(review_id as INTEGER) asc
""".format(country=country, year_from=year_from, year_to=year_to)
    connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
    data = database_utils.get_data(connection, sql)


    """št km prepotovanih: 5km 10km 20km 50km 100km 150+km"""
    start_trip_date = 0
    review_date = 0
    previous_review_date = 0
    user = "abc"
    trip_started = False
    trips = []
    trip = []

    for e in data:
        username = e[1]
        review_date = e[2]
        if review_date == 'None' or review_date is None:
            continue
        if trip_started is False:
            # set values for new trip
            user = username
            start_trip_date = review_date
            previous_review_date = review_date
            trip_started = True
        if user == username:
            if subtract(review_date, previous_review_date) > 14:
                # log the trip
                trips.append(get_path_distance(trip))
                trip = []
                # reset the values for a new trip
                start_trip_date = review_date
                previous_review_date = review_date
            previous_review_date = review_date
            trip.append(e)
        else:
            if trip_started:
                # log the previous trip since new user arrived
                trips.append(get_path_distance(trip))
                trip = []

            user = username
            start_trip_date = review_date
            previous_review_date = review_date
            trip.append(e)

    # 1-5 Km,  6-20 Km, 21-50 Km, 51-100 Km, 101-150 Km, 150+ Km
    # 1-5, 6-20, 21-100, 101-250, 250-350, 350+
    title_arr = []
    days_arr = []
    a, b, c, d, e, f, g = 2, 2, 2, 2, 2, 2, 2
    trips = sorted(trips)
    for lenght in trips:
        if 0 < lenght < 6:
            title_arr.append("1-5")
            days_arr.append("Trip time")
            a += 1
        elif 5 < lenght < 21:
            title_arr.append("6-20")
            days_arr.append("Trip time")
            b += 1
        elif 20 < lenght < 100:
            title_arr.append("21-100")
            days_arr.append("Trip time")
            c += 1
        elif 100 < lenght < 251:
            title_arr.append("101-250")
            days_arr.append("Trip time")
            d += 1
        elif 250 < lenght < 501:
            title_arr.append("251-500")
            days_arr.append("Trip time")
            e += 1
        elif 500 < lenght < 850:
            title_arr.append("501-850")
            days_arr.append("Trip time")
            f += 1
        elif lenght > 850:
            title_arr.append("850+")
            days_arr.append("Trip time")
            g += 1

    all = a + b + c + d + e + f + g

    a = math.ceil(a / math.log2(a))
    b = math.ceil(b / math.log2(b))
    c = math.ceil(c / math.log2(c))
    d = math.ceil(d / math.log2(d))
    e = math.ceil(e / math.log2(e))
    f = math.ceil(f / math.log2(f))
    g = math.ceil(g / math.log2(g))

    all = a + b + c + d + e + f + g

    a = math.ceil((a * 100) / all)
    b = math.ceil((b * 100) / all)
    c = math.ceil((c * 100) / all)
    d = math.ceil((d * 100) / all)
    e = math.ceil((e * 100) / all)
    f = math.ceil((f * 100) / all)
    g = math.ceil((g * 100) / all)

    # 1-5 Km,  6-20 Km, 21-50 Km, 51-100 Km, 101-150 Km, 150+ Km
    title_arr = []
    days_arr = []
    for i in range(a):
        title_arr.append("1-5")
        days_arr.append(year)

    for i in range(b):
        title_arr.append("6-20")
        days_arr.append(year)

    for i in range(c):
        title_arr.append("21-100")
        days_arr.append(year)

    for i in range(d):
        title_arr.append("101-250")
        days_arr.append(year)

    for i in range(e):
        title_arr.append("251-500")
        days_arr.append(year)

    for i in range(f):
        title_arr.append("501-850")
        days_arr.append(year)

    for i in range(g):
        title_arr.append("850+")
        days_arr.append(year)

    f, axes = plt.subplots(1, 1, figsize=(7, 7), sharex=True)
    return title_arr, days_arr


title_arr, days_arr = kilometers_traveled('slovenia', 20180100, 20200100, "2019")
title_arr2, days_arr2 = kilometers_traveled('slovenia', 20200100, 20210100, "2020")

for e in title_arr2:
    title_arr.append(e)

for e in days_arr2:
    days_arr.append(e)

d = {'Kilometers traveled': title_arr, 'Year of travel': days_arr}
df = pd.DataFrame(data=d)
plt.xticks(rotation=45)
sns.histplot(data=df, x="Kilometers traveled", hue="Year of travel", kde=True,
             multiple="dodge")
plt.savefig(f'kilometers_traveled.png'.format())
plt.show()