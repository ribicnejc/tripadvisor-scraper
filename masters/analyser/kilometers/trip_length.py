"""Histogram, ki prikazuje koliko so turisti prepotovali glede na državo. 1km, 2km, 3km, 5km, ... 100+km"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import math
from matplotlib.ticker import PercentFormatter

from masters.data_managers.utils import database_utils
import datetime

def map_date(date):
    month = date[4:6]
    year = " " + date[0:4]
    if month == "01":
        return "Jan" + year
    if month == "02":
        return "Feb" + year
    if month == "03":
        return "Mar" + year
    if month == "04":
        return "Apr" + year
    if month == "05":
        return "May" + year
    if month == "06":
        return "Jun" + year
    if month == "07":
        return "Jul" + year
    if month == "08":
        return "Aug" + year
    if month == "09":
        return "Sep" + year
    if month == "10":
        return "Oct" + year
    if month == "11":
        return "Nov" + year
    if month == "12":
        return "Dec" + year


def subtract(d1, d2):
    da1 = datetime.datetime(int(d1[0:4]), int(d1[4:6]), int(d1[6:8]), 0, 0)
    da2 = datetime.datetime(int(d2[0:4]), int(d2[4:6]), int(d2[6:8]), 0, 0)
    delta = da1 - da2
    return abs(delta.days)


def kilometers_traveled(country, year_from, year_to, year):
    sql = """select review_id, user_id, calculated_dates, review_date, review_experience_date from reviews
where calculated_dates < {year_to}
and calculated_dates > {year_from}
order by user_id, cast(review_id as INTEGER) asc
            """.format(country=country, year_from=year_from, year_to=year_to)
    connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
    data = database_utils.get_data(connection, sql)


    """št. objav v 1 dnevu, 2h, 3h, 5h, 10h"""
    start_trip_date = 0
    review_date = 0
    previous_review_date = 0
    user = "abc"
    trip_started = False
    trips = []

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
                trips.append(subtract(previous_review_date, start_trip_date) + 1)
                # reset the values for a new trip
                start_trip_date = review_date
                previous_review_date = review_date
            previous_review_date = review_date
        else:
            if trip_started:
                # log the previous trip since new user arrived
                trips.append(subtract(previous_review_date, start_trip_date) + 1)
            user = username
            start_trip_date = review_date
            previous_review_date = review_date

    # 1 Day, 2 Days, 3 Days, 4-5 Days, 6-10 Days, 11-15 Days, 16+ Days
    title_arr = []
    days_arr = []
    k, a, b, c, d, e, f, g = 2, 2, 2, 2, 2, 2, 2, 2
    trips = sorted(trips)
    for lenght in trips:
        if lenght < 1:
            title_arr.append("1")
            days_arr.append("Trip time")
            k += 1
        elif 1 <= lenght < 2:
            title_arr.append("2")
            days_arr.append("Trip time")
            a += 1
        elif 1 < lenght < 3:
            title_arr.append("3")
            days_arr.append("Trip time")
            b += 1
        elif 2 < lenght < 4:
            title_arr.append("4")
            days_arr.append("Trip time")
            c += 1
        elif 3 < lenght < 6:
            title_arr.append("5-6")
            days_arr.append("Trip time")
            d += 1
        elif 5 < lenght < 11:
            title_arr.append("7-11")
            days_arr.append("Trip time")
            e += 1
        elif 10 < lenght < 16:
            title_arr.append("12-16")
            days_arr.append("Trip time")
            f += 1
        elif lenght > 15:
            title_arr.append("17+")
            days_arr.append("Trip time")
            g += 1

    all = a + b + c + d + e + f + g + k

    a = math.ceil(a / math.log10(a))
    b = math.ceil(b / math.log10(b))
    c = math.ceil(c / math.log10(c))
    d = math.ceil(d / math.log10(d))
    e = math.ceil(e / math.log10(e))
    f = math.ceil(f / math.log10(f))
    g = math.ceil(g / math.log10(g))
    k = math.ceil(k / math.log10(k))

    all = a + b + c + d + e + f + g + k

    a = math.ceil((a * 100) / all)
    b = math.ceil((b * 100) / all)
    c = math.ceil((c * 100) / all)
    d = math.ceil((d * 100) / all)
    e = math.ceil((e * 100) / all)
    f = math.ceil((f * 100) / all)
    g = math.ceil((g * 100) / all)
    k = math.ceil((k * 100) / all)

    title_arr = []
    days_arr = []
    for i in range(k):
        title_arr.append("1")
        days_arr.append(year)
    for i in range(a):
        title_arr.append("2")
        days_arr.append(year)

    for i in range(b):
        title_arr.append("3")
        days_arr.append(year)

    for i in range(c):
        title_arr.append("4")
        days_arr.append(year)

    for i in range(d):
        title_arr.append("5-6")
        days_arr.append(year)

    for i in range(e):
        title_arr.append("7-11")
        days_arr.append(year)

    for i in range(f):
        title_arr.append("12-16")
        days_arr.append(year)

    for i in range(g):
        title_arr.append("17+")
        days_arr.append(year)

    f, axes = plt.subplots(1, 1, figsize=(7, 7), sharex=True)
    return title_arr, days_arr


title_arr, days_arr = kilometers_traveled('slovenia', 20180100, 20200100, "2019")

title_arr2, days_arr2 = kilometers_traveled('slovenia', 20200100, 20210100, "2020")

for e in title_arr2:
    title_arr.append(e)

for e in days_arr2:
    days_arr.append(e)

d = {'Days': title_arr, 'Year of travel': days_arr}
df = pd.DataFrame(data=d)
plt.xticks(rotation=45)
sns.histplot(data=df, x="Days", hue="Year of travel", kde=False,
             multiple="dodge")
plt.savefig(f'trip_lenght.png'.format())
plt.show()