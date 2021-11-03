from pyvis import network as net
from IPython.core.display import display, HTML
import math
from masters.data_managers.utils import database_utils
import datetime

"""DAO/DTO Logic below"""

global_node_names = {}

def subtract(d1, d2):
    da1 = datetime.datetime(int(d1[0:4]), int(d1[4:6]), int(d1[6:8]), 0, 0)
    da2 = datetime.datetime(int(d2[0:4]), int(d2[4:6]), int(d2[6:8]), 0, 0)
    delta = da1 - da2
    return abs(delta.days)


def merge_locations(old):
    sql = """select region_name, province_name, avg(location_lng) as location_lng, avg(location_lat) as location_lat, country from reviews
        join locations l on l.attraction_url = reviews.parent_url
        join provinces p on p.province_url = l.attraction_parent_url
    where location_lng > 13.344046 and location_lng < 16.616267
    and location_lat > 45.353430 and location_lat < 46.680789
    group by province_name"""
    connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
    data = database_utils.get_data(connection, sql)
    new_data = []
    dic = {}
    for j in data:
        if j[1] not in dic:
            #global_node_names["{lng}+{lat}".format(lat=j[2], lng=j[3])] = j[1].replace(" attractions", "")
            dic[j[1]] = j  # 0 region, 1 province, 4 country
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
            if len(trip) > 0:
                if trip[-1][5] != e[5] or trip[-1][6] != e[6]: # a-b-c-c-d -> a-b-c-d
                    trip.append(e)
            else:
                trip.append(e)
        else:
            if trip_started:
                # log the previous trip since new user arrived
                trips.append(trip)
                trip = []

            user = username
            start_trip_date = review_date
            previous_review_date = review_date
            if len(trip) > 0:
                if trip[-1][5] != e[5] or trip[-1][6] != e[6]:  # a-b-c-c-d -> a-b-c-d
                    trip.append(e)
            else:
                trip.append(e)
    return trips


sql = """select review_id, user_id, calculated_dates, review_date, review_experience_date, location_lat, location_lng, country, region_name, province_name, attraction_type, attraction_name, review_location_type, review_location_name from reviews
join locations l on l.attraction_url = reviews.parent_url
join provinces p on p.province_url = l.attraction_parent_url

where location_lng > 13.344046 and location_lng < 16.616267
and location_lat > 45.353430 and location_lat < 46.680789
and review_date < 20210000
and review_date > 20200000
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

bonds = []
for k, v in edge_weights.items():
    p1 = node_ids[k.split(";")[0]]
    p2 = node_ids[k.split(";")[1]]
    bonds.append([p1, p2, v])


g3 = net.Network(height='600px', width='60%', heading='', directed=False)

comm1 = ["Bled" ,
"Ljubljana",
"Postojna",
"Bohinjsko Jezero" ,
"Zgornje Gorje" ,
"Zagreb" ,
"Kranjska Gora" ,
"Koper" ,
"Kobarid",
"Ptuj" ,
"Karlovac" ,
"Varazdin" ,
"Maribor" ,
"Podcetrtek"]
comm2 = [
"Trieste",
"Sgonico",
"Aquileia",
"Tarvisio",
"Muggia",
"Gorizia",
"Duino",
"Grado",
"Cividale del Friuli",
"MonfalconeGradisca d'Isonzo" ,
]
comm3 = ["Klagenfurt", "Keutschach am See", "Villach"]
comm4 = ["Piran", "Strunjan", "Izola", "Marezige"]

# show only nodes that are part of edges
node_set = set()
for k, v in edge_weights.items():
    p1 = node_ids[k.split(";")[0]]
    p2 = node_ids[k.split(";")[1]]
    node_set.add(p1)
    node_set.add(p2)

filtered_nodes = set()
for k, v in nodes.items():
    scale = 400
    lbl = v[9].replace(" attractions", "")
    id_set = node_ids[k]
    lat = float(v[5])
    lng = float(v[6])
    if id_set not in node_set:
        continue
    if lbl in comm1:
        g3.add_node(id_set, label=lbl, y=(((scale * -1) * lat) + 47 * scale),
                    x=(((scale * 1) * lng) - 30 * scale), physics=False, size=15, color='orange')
    elif lbl in comm2:
        g3.add_node(id_set, label=lbl, y=(((scale * -1) * lat) + 47 * scale),
                    x=(((scale * 1) * lng) - 30 * scale), physics=False, size=15, color='yellow')
    elif lbl in comm3:
        g3.add_node(id_set, label=lbl, y=(((scale * -1) * lat) + 47 * scale),
                    x=(((scale * 1) * lng) - 30 * scale), physics=False, size=15, color='green')
    elif lbl in comm4:
        g3.add_node(id_set, label=lbl, y=(((scale * -1) * lat) + 47 * scale),
                    x=(((scale * 1) * lng) - 30 * scale), physics=False, size=15, color='red' )
    else:
        filtered_nodes.add(id_set)
        g3.add_node(id_set, label=" ", y=(((scale * -1) * lat) + 47 * scale),
                    x=(((scale * 1) * lng) - 30 * scale), physics=False, size=7)

new_bonds = []
for bond in bonds:
    if bond[0] in filtered_nodes or bond[1] in filtered_nodes:
        continue
    new_bonds.append(bond)
bonds = new_bonds
g3.add_edges(bonds)

g3.show_buttons()
#g3.set_edge_smooth('continous')
g3.show('komune2.html')
display(HTML('komune2.html'))

# font was 10, stroke was 3, edge scale factor was 0.75
