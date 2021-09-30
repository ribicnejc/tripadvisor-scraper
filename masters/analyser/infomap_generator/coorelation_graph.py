from pyvis import network as net
from IPython.core.display import display, HTML
import math
from masters.data_managers.utils import database_utils
import datetime

#  infomap test.pajek . --ftree

"""DAO/DTO Logic below"""


def subtract(d1, d2):
    da1 = datetime.datetime(int(d1[0:4]), int(d1[4:6]), int(d1[6:8]), 0, 0)
    da2 = datetime.datetime(int(d2[0:4]), int(d2[4:6]), int(d2[6:8]), 0, 0)
    delta = da1 - da2
    return abs(delta.days)


def merge_locations(old):
    sql = """select region_name, province_name, avg(location_lng) as location_lng, avg(location_lat) as location_lat, country from reviews
        join locations l on l.attraction_url = reviews.parent_url
        join provinces p on p.province_url = l.attraction_parent_url
    group by region_name"""
    connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
    data = database_utils.get_data(connection, sql)
    new_data = []
    dic = {}
    for j in data:
        if j[4] not in dic:
            dic[j[4]] = j  # 0 region, 1 province, 4 country
    for i in old:
        j = dic[i[7]]  # 9 province, 8 region, 7 country
        tmp = list(i)
        tmp[6] = str(j[2])
        tmp[5] = str(j[3])
        new_data.append(tmp)
    return new_data


def prepare_data(sql):
    connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
    data = database_utils.get_data(connection, sql)

    """ Comment below if you don't want to merge data """
    data = merge_locations(data)

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
                trips.append(trip)
                trip = []
                # reset the values for a new trip
                start_trip_date = review_date
                previous_review_date = review_date
            previous_review_date = review_date
            trip.append(e)
        else:
            if trip_started:
                # log the previous trip since new user arrived
                trips.append(trip)
                trip = []

            user = username
            start_trip_date = review_date
            previous_review_date = review_date
            trip.append(e)
    return trips


sql = """select review_id, user_id, calculated_dates, review_date, review_experience_date, location_lat, location_lng, country, region_name, province_name, attraction_type, attraction_name, review_location_type, review_location_name from reviews
join locations l on l.attraction_url = reviews.parent_url
join provinces p on p.province_url = l.attraction_parent_url
where review_date < 20200000
and review_date > 20180000
order by user_id, cast(review_id as INTEGER) asc
""".format()

trips = prepare_data(sql)

""" Here on tourism flow detection """


def get_key(trip):
    key = ""
    for e in trip:
        lat = e[5]
        lng = e[6]
        key += "{lat}+{lng};".format(lat=lat, lng=lng)
    return key


flows = {}
for trip in trips:
    key = get_key(trip)
    if key in flows:
        flows[key].append(trip)
    else:
        flows[key] = [trip]

""" Tourism flow visualisation """
id_set = {}
labels = {}
id_num = 0

new_flows = {}
#  Filter flows

# More than n repetitions
for k, v in flows.items():
    if len(v) > 2:
        new_flows[k] = v

flows = new_flows
new_flows = {}
# Longer than n locations
for k, v in flows.items():
    if len(v[0]) > 2:
        new_flows[k] = v

flows = new_flows
#  Setup node ids
for k, v in flows.items():
    for e in k.split(";"):
        if e == '':
            break
        if e not in id_set:
            id_set[e] = id_num
            labels[e] = v[0][0][7]  # 11 attraction name, 8 region, 7 ukraine
            id_num += 1

bonds_set = {}
for k, v in flows.items():
    prev_e = None
    for e in k.split(";"):
        if e == '':
            break
        lat = e.split("+")[0]
        lng = e.split("+")[1]
        if prev_e is not None and prev_e != e:
            lat_p = prev_e.split("+")[0]
            lng_p = prev_e.split("+")[1]
            bond = "{p1},{p2}".format(p1=id_set[e], p2=id_set[prev_e])
            if bond not in bonds_set:
                bonds_set[bond] = 0
            bonds_set[bond] = bonds_set[bond] + len(v)  # tu prišteva povezavi število ponovitev
        prev_e = e
    prev_e = None

bonds = []
for k, v in bonds_set.items():
    p1 = int(k.split(",")[0])
    p2 = int(k.split(",")[1])
    bonds.append([p1, p2, (v)])
lats = []
lngs = []
for k, v in id_set.items():
    lat = k.split("+")[0]
    lng = k.split("+")[1]
    lats.append(float(lat))
    lngs.append(float(lng))

filename = 'first_one'
with open(filename, 'w+') as f:
    f.write("*Vertices " + str(len(lats)) + "\n")
    nodes = set()
    for node_i in range(len(lats)):
        key = str(lats[node_i]) + "+" + str(lngs[node_i])
        if node_i not in nodes:
            f.write("{num} {title} {w}\n".format(num=node_i, title=labels[key], w=1.0))
            nodes.add(node_i)
    f.write("*Arcs " + str(len(bonds)) + "\n")
    for bond in bonds:
        f.write("{from_n} {to} {w}\n".format(from_n=bond[0], to=bond[1], w=bond[2]))
    f.close()

# font was 10, stroke was 3, edge scale factor was 0.75
