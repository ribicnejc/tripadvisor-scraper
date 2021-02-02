from masters.data_managers.utils import database_utils
from masters import settings

# Get data
sql = """
    select user_link, region_name, province_name, review_experience_date, review_id 
from reviews
         join locations l on l.attraction_url = reviews.parent_url
         join provinces p on p.province_url = l.attraction_parent_url
where country = 'slovenia'
  and reviews.review_date > 20200101
  and reviews.review_date < 20210101
order by user_link, review_experience_date, review_id
    """
connection = database_utils.create_connection("../data/databases/data.db")
data = database_utils.get_data(connection, sql)


def get_color(region_name):
    if region_name == "Lower Carniola Region":
        return "#9575cd"  # 7e57c2
    if region_name == "Inner Carniola Region":
        return "#7986cb"  # 5c6bc0
    if region_name == "Styria Region":
        return "#4db6ac"  # 26a69a
    if region_name == "Prekmurje Region":
        return "#81c784"  # 66bb6a
    if region_name == "Slovenian Littoral Region":
        return "#dce775"  # d4e157
    if region_name == "Upper Carniola Region":
        return "#ffd54f"  # ffca28
    if region_name == "Carinthia Region":
        return "#ff8a65"  # ff7043
    if region_name == "Slovenian Istria":
        return "#bcaaa4"  # a1887f
    if region_name == "Slovenia":
        return "#90a4ae"  # 78909c
    if region_name == "Kras":
        return "#64b5f6"  # 42a5f5
    else:
        return "#000000"


def get_border_color(region_name):
    if region_name == "Lower Carniola Region":
        return "#7e57c2"
    if region_name == "Inner Carniola Region":
        return "#5c6bc0"
    if region_name == "Styria Region":
        return "#26a69a"
    if region_name == "Prekmurje Region":
        return "#66bb6a"
    if region_name == "Slovenian Littoral Region":
        return "#d4e157"
    if region_name == "Upper Carniola Region":
        return "#ffca28"
    if region_name == "Carinthia Region":
        return "#ff7043"
    if region_name == "Slovenian Istria":
        return "#a1887f"
    if region_name == "Slovenia":
        return "#78909c"
    if region_name == "Kras":
        return "#42a5f5"
    else:
        return "#000000"


class Node(object):
    def __init__(self, username, region_name, province_name, review_date, review_id, node_id, group_id):
        self.group_id = group_id
        self.node_id = node_id
        self.review_id = review_id
        self.review_date = review_date
        self.province_name = province_name
        self.region_name = region_name
        self.username = username

    def get_node(self):
        return """  node 
  [
    id %s
    label "%s"
    group %s
    fill "%s"
    border "%s"
  ]
""" % (self.node_id, self.province_name.replace(" attractions", ""), self.group_id, get_color(self.region_name),
       get_border_color(self.region_name))


class Edge(object):
    def __init__(self, source, target, value):
        self.value = value
        self.target = target
        self.source = source

    def get_edge(self):
        return """  edge
  [
    source %s 
    target %s 
    value %s 
  ]
""" % (self.source, self.target, self.value)


# edge
# [
#   source 76
#   target 58
#   value 1
# ]

node = 0
node_ids = {}
group = 1
group_ids = {}
nodes = []
edges = []
edges_lib = {}
province_1 = None
province_2 = None
usr_1 = None
usr_2 = None

for line in data:
    username = line[0]
    region_name = line[1]
    province_name = line[2]
    review_date = line[3]
    review_id = line[4]
    try:
        tmp = node_ids[province_name]
    except:
        node_ids[province_name] = node
        node += 1
    try:
        tmp = group_ids[region_name]
    except:
        group_ids[region_name] = group
        group += 1

    node_obj = Node(username, region_name, province_name, review_date, review_id, node_ids[province_name],
                    group_ids[region_name])
    nodes.append(node_obj)

    if usr_1 is None:
        usr_1 = username
    if province_1 is None:
        province_1 = province_name
        continue
    if username == usr_1:
        province_2 = province_name
        try:
            if province_1 < province_2:
                val = edges_lib[province_1 + "," + province_2]
                val += 1
                edges_lib[province_1 + "," + province_2] = val
            else:
                val = edges_lib[province_2 + "," + province_1]
                val += 1
                edges_lib[province_2 + "," + province_1] = val
        except:
            if province_1 < province_2:
                edges_lib[province_1 + "," + province_2] = 1
            else:
                edges_lib[province_2 + "," + province_1] = 1
        province_2 = None
        continue
    else:
        usr_1 = username
        province_1 = province_name

for key, value in edges_lib.items():
    tmp = key.split(",")
    province_1 = tmp[0]
    province_2 = tmp[1]
    edge_obj = Edge(node_ids[province_1], node_ids[province_2], value)
    edges.append(edge_obj)

filtered_nodes = []
for edge in edges:
    filtered_nodes.append(edge.target)
    filtered_nodes.append(edge.source)

sorted_edges = sorted(edges, key=lambda x: x.value, reverse=True)
limited_edges = []
limited_nodes = []
region_hash = {}
provinces_in_regions = []
for edge in sorted_edges:
    it1 = list(filter(lambda x: x.node_id == edge.source, nodes))[0]
    try:
        val = region_hash[it1.region_name]
        if val < 8 and it1.province_name not in provinces_in_regions:
            region_hash[it1.region_name] = val + 1
            limited_nodes.append(it1)
            provinces_in_regions.append(it1.province_name)
            it2 = list(filter(lambda x: x.node_id == edge.target, nodes))[0]
            limited_nodes.append(it2)
            limited_edges.append(edge)
    except:
        region_hash[it1.region_name] = 1

filename = 'arcdiagram_slo_20.gml'
unique_dist = []
with open(filename, 'w') as f:
    f.write('Creator "igraph version 0.6 Wed Jan 30 10:28:57 2013"\n')
    f.write('Version 1\n')
    f.write('graph\n')
    f.write('[\n')
    f.write('  directed 0\n')
    for node in limited_nodes:
        if node.node_id not in unique_dist:
            f.write(node.get_node())
            unique_dist.append(node.node_id)
    for edge in limited_edges:
        f.write(edge.get_edge())
    f.write(']')
    f.close()

print(len(unique_dist))
