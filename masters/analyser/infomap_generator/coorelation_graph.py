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
    sql = """select region_name, province_name, avg(location_lng) as location_lng, avg(location_lat) as location_lat, country, province_name from reviews
        join locations l on l.attraction_url = reviews.parent_url
        join provinces p on p.province_url = l.attraction_parent_url
    group by province_name"""
    connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
    data = database_utils.get_data(connection, sql)
    new_data = []
    dic = {}
    for j in data:
        if j[5] not in dic:
            dic[j[5]] = j  # 0 region, 1 province, 4 country, 5 province
    for i in old:
        j = dic[i[9]]  # 9 province, 8 region, 7 country
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

where location_lng > 13.344046 and location_lng < 16.616267
and location_lat > 45.353430 and location_lat < 46.680789
and review_date < 20201000
and review_date > 20200700
--and country = 'slovenia'
order by user_id, cast(review_id as INTEGER) asc
""".format()

trips = prepare_data(sql)

""" Here on tourism flow detection """
def get_node_key(e):
    lat = e[5]
    lng = e[6]
    key = "{lat}+{lng}".format(lat=lat, lng=lng)
    return key

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

edge_weights = {}
node_weights = {}
nodes = {}
node_ids = {}
ids = 0
for trip in trips:
    prev_node = None
    for node in trip:
        key = get_node_key(node)
        if key not in node_weights:
            node_weights[key] = 1
            nodes[key] = node
            node_ids[key] = ids
            ids += 1
        else:
            node_weights[key] += 1
        if prev_node is not None:
            key = get_key([prev_node, node])
            if key not in edge_weights:
                edge_weights[key] = 1
            else:
                edge_weights[key] += 1
        prev_node = node

#  filtering
filtered = set()
for k, w in edge_weights.items():
    nodes_tmp = k.split(";")
    n_id1 = node_ids[nodes_tmp[0]]
    n_id2 = node_ids[nodes_tmp[1]]
    if w > 5:
        filtered.add(n_id2)
        filtered.add(n_id1)

filename = 'slovenia_2020_extra'
with open(filename, 'w+') as f:
    f.write("*Vertices " + str(len(nodes)) + "\n")
    for k, v in nodes.items():
        node_i = node_ids[k]
        label = v[9].replace(" attractions", "")
        w = node_weights[k]
        if node_i in filtered:
            f.write("{num} \"{title}\" {w}\n".format(num=node_i, title=label, w=w))
    f.write("*Arcs " + str(len(edge_weights)) + "\n")
    for k, w in edge_weights.items():
        nodes = k.split(";")
        n_id1 = node_ids[nodes[0]]
        n_id2 = node_ids[nodes[1]]
        if n_id1 != n_id2 and n_id1 in filtered and n_id2 in filtered:
            f.write("{from_n} {to} {w}\n".format(from_n=n_id1, to=n_id2, w=w))
    f.close()
