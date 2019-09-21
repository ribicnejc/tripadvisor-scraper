import sqlite3
import os


def create_database():
    database = "../data.db"

    sql_create_attraction_table = """ CREATE TABLE IF NOT EXISTS attractions (
                                        url text PRIMARY KEY,
                                        name text,
                                        lat text,
                                        lng text
                                    ); """

    sql_create_reviews_table = """CREATE TABLE IF NOT EXISTS reviews (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    location_name text,
                                    location_tags text,
                                    lat text,
                                    lng text,
                                    review_id text,
                                    review_date text,
                                    user_id text,
                                    review_rate text,
                                    place_rate text,
                                    username text
                                    FOREIGN KEY (attraction_id) REFERENCES attractions (url)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_attraction_table)

        # create tasks table
        create_table(conn, sql_create_reviews_table)
    else:
        print("Error! cannot create the database connection.")


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


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def insert_review(conn, review):
    sql = ''' INSERT INTO reviews(location_name,location_tags,lat,lng,review_id,review_date,user_id,review_rate,place_rate,username)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, review)


def insert_attractions(conn, attraction):
    sql = ''' INSERT INTO attractions(url, name, lat, lng)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, attraction)
    conn.commit()


def fill_attractions():
    folder = "../../scraped_data/data_attractions_slovenia"

    conn = create_connection("../data.db")

    for file in os.listdir(folder):
        file = folder + "/" + file
        with open(file) as f:
            line = f.readline()
            while line:
                line = line.replace("\n", "")
                insert_attractions(conn, (line, None, None, None))
                line = f.readline()


create_database()
fill_attractions()

# /Attraction_Review-g14941859-d14798776-Reviews-Cheeky_Pineapple_Travel-Zgornji_Brnik_Upper_Carniola_Region.html