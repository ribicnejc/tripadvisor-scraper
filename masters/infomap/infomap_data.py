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
        "select user_id, review_id, review_date, review_rate, place_rate, attraction_id, country_of_origin from reviews where country_of_origin = 'slovenia' order by user_id, review_id asc")
    return cur.fetchall()


def get_attractions_cursor():
    conn = create_connection('../database/data.db')
    cur = conn.cursor()
    cur.execute("select * from attractions")
    return cur.fetchall()


def get_pajek_format():
    attractions = []
    for attraction in get_attractions_cursor():
        attractions.append(attraction[0])

    filename = 'infomap_data/slovenia.net'
    with open(filename, 'a+') as f:
        f.write("*Vertices " + str(attractions.__len__()) + "\n")
        i = 1
        for attraction in attractions:
            f.write(str(i) + " " + attraction.split("-Reviews-")[1] + " 1.0\n")
            i += 1
    # for review in get_reviews_cursor():


get_pajek_format()