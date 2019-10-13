import sqlite3

from masters.data_structures.ReviewInfomap import ReviewInfomap
from masters.data_structures.AttractionInfomap import AttractionInfomap
from masters.data_structures.EdgeInfomap import EdgeInfomap


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def get_review_by_location_name(conn, review_name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviews WHERE location_name = ?", (review_name,))
    for row in cur.fetchall():
        return row


def get_reviews():
    conn = create_connection('../database/data.db')
    cur = conn.cursor()
    cur.execute(
        "select * from reviews order by user_id, review_id asc")
    reviews = []
    attractions = get_attractions_cursor()
    for review in cur.fetchall():
        url = review[11]
        if 'html' not in url:
            url = get_review_by_location_name(conn, review[1])[11]
        review_data = ReviewInfomap(review[1],
                                    review[2],
                                    review[3],
                                    review[4],
                                    review[5],
                                    review[6],
                                    review[7],
                                    review[8],
                                    review[9],
                                    review[10],
                                    url,
                                    review[12],
                                    attractions[url])
        reviews.append(review_data)
    return reviews


def get_attractions_cursor():
    conn = create_connection('../database/data.db')
    cur = conn.cursor()
    cur.execute("select * from attractions")
    attractions = dict()
    i = 1
    for attraction in cur.fetchall():
        attr = AttractionInfomap(attraction[0], attraction[0], i)
        attractions[attr.attraction_url] = attr
        i += 1
    return attractions


def save_pajek_format(edges, name):
    filename = 'infomap_data/' + name
    vertices = {}
    for edge in edges.items():
        vertices[edge[1].review_from.attraction.attraction_url] = edge[1].review_from.attraction.number
        vertices[edge[1].review_to.attraction.attraction_url] = edge[1].review_to.attraction.number
    with open(filename, 'w+') as f:
        f.write("*Vertices " + str(vertices.__len__()) + "\n")
        for vertice in vertices.items():
            f.write(str(vertice[1]) + " \"" + vertice[0].split("-Reviews-")[1] + "\" 1.0\n")
        f.write("*Edges " + str(edges.__len__()) + "\n")
        for edge in edges.items():
            f.write(edge[0] + " " + str(edge[1].weight) + "\n")


def get_key_from_locations(l1, l2):
    if l1.number < l2.number:
        return str(l1.number) + " " + str(l2.number)
    return str(l2.number) + " " + str(l1.number)


def get_edges():
    edges = {}
    prev = None
    for review in get_reviews():
        if prev is None:
            prev = review
            continue
        if review.user_id == prev.user_id:  # if is the same user
            if review.review_date - prev.review_date < 30:  # if time between visit is less then 30
                key = get_key_from_locations(review.attraction, prev.attraction)  # get key for edges
                if edges.get(key):
                    edges[key] = EdgeInfomap(edges[key].weight + 1, prev, review)
                else:
                    edges[key] = EdgeInfomap(1, prev, review)
        prev = review
    return edges


def filter_edges(edges):
    new_edges = {}
    for edge in edges.items():
        if edge[1].weight > 20:
            new_edges[edge[0]] = edge[1]
    return new_edges


def get_pajek_format():
    # get all edges top map {n - m: {from, to, weight}} position to position weight
    edges = get_edges()
    print("Edges grouped...")

    edges = filter_edges(edges)
    print("Edges filtered...")

    save_pajek_format(edges, 'sl_w20.net')
    print("Pajek saved...")

get_pajek_format()
