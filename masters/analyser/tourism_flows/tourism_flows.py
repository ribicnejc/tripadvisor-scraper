from pyvis import network as net
from IPython.core.display import display, HTML
import math
from masters.data_managers.utils import database_utils
import datetime

"""DAO/DTO Logic below"""


def subtract(d1, d2):
    da1 = datetime.datetime(int(d1[0:4]), int(d1[4:6]), int(d1[6:8]), 0, 0)
    da2 = datetime.datetime(int(d2[0:4]), int(d2[4:6]), int(d2[6:8]), 0, 0)
    delta = da1 - da2
    return abs(delta.days)


def prepare_data(sql):
    connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
    data = database_utils.get_data(connection, sql)

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
--where country = 'slovenia'
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
    if len(v) > 10:
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
            labels[e] = v[0][0][11]
            id_num += 1

bonds = []
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
            bonds.append([id_set[e], id_set[prev_e], 3])
        prev_e = e
    prev_e = None

lats = []
lngs = []
for k, v in id_set.items():
    lat = k.split("+")[0]
    lng = k.split("+")[1]
    lats.append(float(lat))
    lngs.append(float(lng))
g3 = net.Network(height='600px', width='80%', heading='', directed=True)

for atom in range(len(lats)):
    key = str(lats[atom]) + "+" + str(lngs[atom])
    scale = 1000
    g3.add_node(id_set[key], label=labels[key], y=(((scale * -1) * lats[atom]) + 47 * scale),
                x=(((scale * 1) * lngs[atom]) - 30 * scale), physics=False, size=5)

g3.add_edges(bonds)

g3.show('g3.html')
display(HTML('g3.html'))
