from masters.data_managers.utils import database_utils
from masters import settings

# Get data
sql = """
    select user_link, region_name, province_name, review_experience_date, review_id 
from reviews
         join locations l on l.attraction_url = reviews.parent_url
         join provinces p on p.province_url = l.attraction_parent_url
where country = 'slovenia'
  and reviews.review_date > 20190101
  and reviews.review_date < 20200101
order by user_link, review_experience_date, review_id
    """
connection = database_utils.create_connection("../data/databases/data.db")
data = database_utils.get_data(connection, sql)


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
    fill "#%s2c771"
    border "#8e9f5a"
  ]
""" % (self.node_id, self.province_name, self.group_id, self.group_id)

        # node
        # [
        #     id 43
        #     label "Woman2"
        #     group 5
        #     fill "#b2c771"
        #     border "#8e9f5a"
        # ]


class Edge(object):
    def __init__(self, source, target, value):
        self.value = value
        self.target = target
        self.source = source

    def get_edge(self):
        tmp = """  edge
  [
    source %s 
    target %s 
    value %s 
  ]
""" % (self.source, self.target,self.value)

        return tmp
        # return "  edge\n" \
        #        "  [\n" \
        #        "    source %s" \
        #        "    target %s" \
        #        "    value %s" \
        #        "  ]\n" % (self.source, self.target, self.value)


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
            # TODO trip direction issue
            val = edges_lib[province_1 + "," + province_2]
            val += 1
            edges_lib[province_1 + "," + province_2] = val
        except:
            edges_lib[province_1 + "," + province_2] = 1
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

filename = 'arcdiagram_slo.gml'
unique_dist = []
with open(filename, 'w') as f:
    f.write('Creator "igraph version 0.6 Wed Jan 30 10:28:57 2013"\n')
    f.write('Version 1\n')
    f.write('graph\n')
    f.write('[\n')
    f.write('  directed 0\n')
    for node in nodes:
        if node.node_id not in unique_dist:
            f.write(node.get_node())
            unique_dist.append(node.node_id)
    for edges in edges:
        f.write(edges.get_edge())
    f.write(']')
    f.close()

print(len(unique_dist))