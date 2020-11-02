import sqlite3
import codecs
import os
import re


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
                                    username text,
                                    attraction_id text,
                                    country_of_origin text,
                                    FOREIGN KEY (attraction_id) REFERENCES attractions (url)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create attractions table
        create_table(conn, sql_create_attraction_table)

        # create reviews table
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
    sql = ''' INSERT INTO reviews(location_name,location_tags,lat,lng,review_id,review_date,user_id,review_rate,place_rate,username,attraction_id,country_of_origin)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, review)


def insert_attractions(conn, attraction):
    print("Inserting attraction: " + attraction[0])
    sql = ''' INSERT OR REPLACE INTO attractions(url, name, lat, lng)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, attraction)


def get_review_by_location_name(conn, review_name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviews WHERE location_name = ?", (review_name,))
    for row in cur.fetchall():
        return row


def fill_attractions(folder):
    conn = create_connection("../data.db")
    counter = 0
    for file in os.listdir(folder):
        file = folder + "/" + file
        with open(file) as f:
            line = f.readline()
            while line:
                line = line.replace("\n", "")
                print(counter)
                counter = counter + 1
                insert_attractions(conn, (line, None, None, None))
                line = f.readline()
    conn.commit()


def fill_reviews(folder, country):
    conn = create_connection("../data.db")
    counter = 0
    for file in os.listdir(folder):
        file = folder + "/" + file
        with open(file, encoding='utf-8') as f:
            if counter == 480:
                print("hmm")
            f.readline()  # this will read just comma separated values.
            line = f.readline()
            while line:
                print(str(counter) + ":" + line)
                counter += 1
                line = line.replace("\n", "")
                line_len = line.split(", ").__len__()
                if "DD6949832F578136ADA626B6C98961A7" in line:
                    debug = 1
                if line_len < 5:
                    line = f.readline()
                    continue
                if line_len > 11:
                    line = correct_data(conn, line)
                if line_len < 11:
                    line = correct_data(conn, line)

                insert_review(conn, tuple(line.split(", ")) + (country,))
                line = f.readline()
    conn.commit()


def correct_data(conn, line):
    if line.split(", ").__len__() < 11:
        previous_review = get_review_by_location_name(conn, line.split(', ')[0])
        line = line + ", " + previous_review[-1]

    lst = line.split(", ")
    url = lst[-1]
    usr = lst[-2]
    pr = lst[-3]

    tmp = line.split(usr + ", ")
    last_number = re.findall(r'\d+', tmp[0])[-1]
    split_index = tmp[0].rfind(last_number) + 1
    first_part = tmp[0][0:split_index]
    usr = pr + "_" + usr
    first_part += ", " + usr
    second_part = tmp[1]
    line = first_part + ", " + second_part
    lst = line.split(", ")
    pr = lst[-3]

    rr = lst[-4]
    uid = lst[-5]
    rd = lst[-6]
    ri = lst[-7]
    lng = lst[-8]
    lat = lst[-9]
    lt = lst[-10]
    nm = ' '.join(lst[0:-10])
    return nm + ", " + lt + ", " + lat + ", " + lng + ", " + ri + ", " + rd + ", " + uid + ", " + rr + ", " + pr + ", " + usr + ", " + url


create_database()
fill_attractions("../../scraped_data/data_attractions_slovenia")
fill_attractions("../../scraped_data/data_attractions_croatia")
fill_attractions("../../scraped_data/data_attractions_hungary")
fill_attractions("../../scraped_data/data_attractions_austria")
fill_attractions("../../scraped_data/data_attractions_italy")
#
fill_reviews("../../scraped_data/data_reviews_slovenia", "slovenia")
fill_reviews("../../scraped_data/data_reviews_croatia", "croatia")
fill_reviews("../../scraped_data/data_reviews_hungary", "hungary")
fill_reviews("../../scraped_data/data_reviews_austria", "austria")
fill_reviews("../../scraped_data/data_reviews_italy", "italy")

# /Attraction_Review-g14941859-d14798776-Reviews-Cheeky_Pineapple_Travel-Zgornji_Brnik_Upper_Carniola_Region.html


#
# do 17 10 je treba dobit temo
#
# # poženi od karmen algoritem na podatkih
# poglej kaj se da dodat temu algoritmu če se fokusiramo na par točk
# oziroma če dodamo še informacijo o ocenah lokacij zravn.
# #
# #
# #
# #
