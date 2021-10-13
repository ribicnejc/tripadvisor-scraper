from pyvis import network as net
from IPython.core.display import display, HTML
import math
from masters.data_managers.utils import database_utils
import datetime
import decimal

"""DAO/DTO Logic below"""

global_node_names = {}

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


sql = """select review_id, user_id, calculated_dates, review_date, review_experience_date,
       (location_lat * 1.0 + l.attraction_id) as location_lat,
       (location_lng * 1.0 + l.attraction_id_2) as location_lng,
       country, region_name, province_name, attraction_type, attraction_name, review_location_type, review_location_name from reviews
join locations l on l.attraction_url = reviews.parent_url
join provinces p on p.province_url = l.attraction_parent_url
where review_date < 20200000
and review_date > 20190000
and cast(location_lat as decimal) < 41.986482 and cast(location_lat as decimal) > 41.786401
and cast(location_lng as decimal) > 12.345257 and cast(location_lng as decimal) < 12.632454
--and cast(review_last_page as INTEGER) > 20
--and review_location_breadcrumbs like '%Province of Rome%'
--and region_name = 'Lazio'--'Upper Carniola Region'--'Lazio'
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
# Contain specific type of location
for k, v in flows.items():
    for loc in v[0]:
        var = ';'.join(map(str, loc))
        if "Religious" in var or "Churches" in var or "Cathedrals" in var:  # "Cathedrals, Religious, Art Museums"
            new_flows[k] = v

flows = new_flows


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
            bond = "{p1},{p2}".format(p1=e, p2=prev_e)
            if bond not in bonds_set:
                bonds_set[bond] = 0
            bonds_set[bond] = bonds_set[bond] + len(v)  # tu prišteva povezavi število ponovitev
        prev_e = e
    prev_e = None

new_flows = {}
#  Filter flows

# More than n repetitions
for k, v in flows.items():
    if len(v) > 0:
        new_flows[k] = v

flows = new_flows
new_flows = {}
# Longer than n locations
for k, v in flows.items():
    if len(v[0]) > 1:
        new_flows[k] = v

flows = new_flows

#  Setup node ids
for k, v in flows.items():
    i = -1
    for e in k.split(";"):
        i += 1
        if e == '':
            break
        if e not in id_set:
            id_set[e] = id_num
            global_node_names[e] = v[0][i][11]
            labels[e] = global_node_names[e]  # 11 attraction name, 8 region, 7 ukraine
            id_num += 1



bonds = []
for k, v in bonds_set.items():
    p1 = k.split(",")[0]
    p2 = k.split(",")[1]
    if p1 in id_set and p2 in id_set:
        bonds.append([id_set[p1], id_set[p2], v, p1, p2])

new_bonds = []
new_id_set = {}
#  number of repetition of flow
for bond in bonds:
    v = bond[2]
    if v > 20:
        new_bonds.append([id_set[bond[3]], id_set[bond[4]], v / 30])
        new_id_set[bond[3]] = bond[0]
        new_id_set[bond[4]] = bond[1]
bonds = new_bonds
id_set = new_id_set

g3 = net.Network(height='600px', width='60%', heading='', directed=False)

for k, v in id_set.items():
    lat = k.split("+")[0]
    lng = k.split("+")[1]
    scale = 20000
    y = (((scale * -1) * decimal.Decimal(lat)) + 41 * scale)
    x = (((scale * 1) * decimal.Decimal(lng)) - 12 * scale)
    _y = float(y)
    _x = float(x)
    g3.add_node(v, label=labels[k], y=_y, x=_x, physics=False, size=5)

g3.add_edges(bonds)

g3.show_buttons()
#g3.set_edge_smooth('dynamic')
g3.show('country_2019_rome-ruins.html')
display(HTML('country_2019_rome-ruins.html'))

# font was 10, stroke was 3, edge scale factor was 0.75
