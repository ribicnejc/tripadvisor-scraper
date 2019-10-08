import sqlite3


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


def get_reviews_cursor():
    conn = create_connection('../database/data.db')
    cur = conn.cursor()
    cur.execute(
        "select user_id, review_id, review_date, review_rate, place_rate, attraction_id, country_of_origin from reviews order by user_id, review_id asc")
    return cur.fetchall()


def get_attractions_cursor():
    conn = create_connection('../database/data.db')
    cur = conn.cursor()
    cur.execute("select * from attractions")
    return cur.fetchall()


def save_pajek_format(vertices, edges, name):
    filename = 'infomap_data/' + name
    with open(filename, 'w+') as f:
        f.write("*Vertices " + str(vertices.__len__()) + "\n")
        for vertice in vertices.items():
            f.write(str(vertice[1]) + " \"" + vertice[0].split("-Reviews-")[1] + "\" 1.0\n")
        f.write("*Edges " + str(edges.__len__()) + "\n")
        for edge in edges.items():
            f.write(edge[0] + " " + str(edge[1]) + "\n")


def get_key_from_locations(l1, l2, locations):
    k1 = locations[l1]
    k2 = locations[l2]
    if k1 < k2:
        return str(k1) + " " + str(k2)
    return str(k2) + " " + str(k1)


def get_pajek_format():
    attractions = {}
    i = 1
    for attraction in get_attractions_cursor():
        attractions.__setitem__(attraction[0], i)
        i += 1
    edges = {}
    prev = None
    for review in get_reviews_cursor():
        if prev is None:
            prev = review
            continue
        if review[0] == prev[0]:  # if is the same user
            if int(review[2]) - int(prev[2]) < 30:  # if time between visit is less then 30
                key = get_key_from_locations(review[5], prev[5], attractions)  # get key for edges
                if edges.get(key):
                    edges.__setitem__(key, edges.get(key) + 1)
                else:
                    edges.__setitem__(key, 1)
        prev = review
    save_pajek_format(attractions, edges, 'sl-cr-hu-au-it.net')


get_pajek_format()
