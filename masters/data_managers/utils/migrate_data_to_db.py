import sqlite3
import codecs
import os

db = "../../data/databases/data_ukr.db"


def create_database():
    database = db

    sql_create_provinces_table = """ CREATE TABLE IF NOT EXISTS provinces (
                                        province_name text,
                                        region_name text,
                                        province_url text,
                                        country text,
                                        PRIMARY KEY (province_url)                                        
                                    ); """

    sql_create_locations_table = """ CREATE TABLE IF NOT EXISTS locations (
                                        attraction_name text,
                                        attraction_rate text,
                                        attraction_type text,
                                        attraction_url text,
                                        attraction_parent_url text,
                                        PRIMARY KEY (attraction_url),    
                                        FOREIGN KEY (attraction_parent_url) REFERENCES provinces (province_url)                                    
                                    ); """

    sql_create_review_table = """ CREATE TABLE IF NOT EXISTS reviews (
                                        review_location_name text,
                                        review_current_page text,
                                        review_last_page text,
                                        review_location_type text,
                                        review_location_breadcrumbs text,
                                        review_location_rate text,
                                        location_lat text,
                                        location_lng text,
                                        review_id text,
                                        review_date text,
                                        review_experience_date text,
                                        review_rate text,
                                        user_name text,
                                        user_link text,
                                        user_id text,
                                        extra text,
                                        parent_url text,
                                        PRIMARY KEY (review_id),    
                                        FOREIGN KEY (parent_url) REFERENCES locations (attraction_url)                                    
                                    ); """
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create provinces table
        create_table(conn, sql_create_provinces_table)
        # create locations table
        create_table(conn, sql_create_locations_table)
        # create review table
        create_table(conn, sql_create_review_table)
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


def insert_province(conn, province):
    print("Inserting province: " + province[0])
    sql = ''' INSERT OR REPLACE INTO provinces(province_name, region_name, province_url, country)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, province)


def insert_location(conn, location):
    print("Inserting location: " + location[0])
    sql = ''' INSERT OR REPLACE INTO locations(attraction_name, attraction_rate, attraction_type, attraction_url, attraction_parent_url)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, location)


def insert_review(conn, review):
    print("Inserting review: " + review[0])
    sql = ''' INSERT OR REPLACE INTO reviews(review_location_name, review_current_page, review_last_page,
                    review_location_type, review_location_breadcrumbs, review_location_rate, location_lat,
                    location_lng, review_id, review_date, review_experience_date,
                    review_rate, user_name, user_link, user_id, extra, parent_url)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, review)


def fill_provinces(folder, country):
    conn = create_connection(db)
    counter = 0
    for file in os.listdir(folder):
        file = folder + "/" + file
        with open(file) as f:
            line = f.readline()
            while line:
                line = line.replace("\n", "")
                print(counter)
                counter = counter + 1
                insert_province(conn, tuple(line.split(", ")) + (country,))
                line = f.readline()
    conn.commit()


def fill_locations(folder):
    conn = create_connection(db)
    counter = 0
    for file in os.listdir(folder):
        file = folder + "/" + file
        with open(file) as f:
            line = f.readline()
            while line:
                line = line.replace("\n", "")
                print(counter)
                counter += 1
                insert_location(conn, tuple(line.split(", ")))
                line = f.readline()
    conn.commit()


def fill_reviews(folder):
    conn = create_connection(db)
    counter = 0
    for file in os.listdir(folder):
        file = folder + "/" + file
        with open(file) as f:
            line = f.readline()
            while line:
                line = line.replace("\n", "")
                print(counter)
                counter += 1
                insert_review(conn, tuple(line.split(", ")))
                line = f.readline()
    conn.commit()


create_database()
# fill_provinces("../scraped_data/data_provinces/ukr", "ukraine")
# fill_provinces("../scraped_data/data_provinces/cro", "croatia")
# fill_provinces("../scraped_data/data_provinces/slo", "slovenia")
# fill_provinces("../scraped_data/data_provinces/hun", "hungary")
# fill_provinces("../scraped_data/data_provinces/aus", "austria")
# fill_provinces("../scraped_data/data_provinces/ita", "italy")
# fill_locations("../scraped_data/data_locations/slo")
# fill_locations("../scraped_data/data_locations/cro")
# fill_locations("../scraped_data/data_locations/ukr")
# fill_locations("../scraped_data/data_locations/aus")
# fill_locations("../scraped_data/data_locations/hun")
# fill_locations("../scraped_data/data_locations/ita")

fill_reviews("../../scraped_data/data_reviews/ukr")
