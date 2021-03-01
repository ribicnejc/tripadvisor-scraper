import sqlite3
import codecs
import os
import zipfile

from masters.utils import unicode_utils

db = "../../data/databases/slo_aus_ita_hun_cro.db"


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


def unzip_fill_provinces(file, country):
    conn = create_connection(db)
    counter = 0
    with zipfile.ZipFile(file) as z:
        for filename in z.namelist():
            if not os.path.isdir(filename):
                # read the file
                with z.open(filename) as f:
                    for line in f:
                        province = unicode_utils.byte_to_string(line)
                        province = province.replace("\n", "")
                        print(counter)
                        counter += 1
                        insert_province(conn, tuple(province.split(", ")) + (country,))
    conn.commit()


def unzip_fill_locations(file):
    conn = create_connection(db)
    counter = 0
    with zipfile.ZipFile(file) as z:
        for filename in z.namelist():
            if not os.path.isdir(filename):
                # read the file
                with z.open(filename) as f:
                    for line in f:
                        location = unicode_utils.byte_to_string(line)
                        location = location.replace("\n", "")
                        print(counter)
                        counter += 1
                        insert_location(conn, tuple(location.split(", ")))
    conn.commit()


def unzip_fill_reviews(file):
    conn = create_connection(db)
    counter = 0
    with zipfile.ZipFile(file) as z:
        for filename in z.namelist():
            if not os.path.isdir(filename):
                # read the file
                with z.open(filename) as f:
                    for line in f:
                        review = unicode_utils.byte_to_string(line)
                        review = review.replace("\n", "")
                        print(str(counter) + " " + file)
                        counter += 1
                        insert_review(conn, tuple(review.split(", ")))
    conn.commit()


# create_database()
def bulk_provinces():
    """Fill provinces"""
    unzip_fill_provinces("../../data/provinces/provinces_aus.zip", "austria")
    unzip_fill_provinces("../../data/provinces/provinces_cro.zip", "croatia")
    unzip_fill_provinces("../../data/provinces/provinces_hun.zip", "hungary")
    unzip_fill_provinces("../../data/provinces/provinces_ita.zip", "italy")
    unzip_fill_provinces("../../data/provinces/provinces_slo.zip", "slovenia")


def bulk_locations():
    """Fill locations"""
    unzip_fill_locations("../../data/locations/locations_aus.zip")
    unzip_fill_locations("../../data/locations/locations_cro.zip")
    unzip_fill_locations("../../data/locations/locations_hun.zip")
    unzip_fill_locations("../../data/locations/locations_ita.zip")
    unzip_fill_locations("../../data/locations/locations_slo.zip")


def bulk_reviews():
    """Fill reviews"""
    # SLO
    unzip_fill_reviews("../../data/reviews/reviews_slo.zip")
    # CRO
    unzip_fill_reviews("../../data/reviews/reviews_cro_1.zip")
    # HUN
    unzip_fill_reviews("../../data/reviews/reviews_hun_1.zip")
    unzip_fill_reviews("../../data/reviews/reviews_hun_2.zip")
    # AUS
    unzip_fill_reviews("../../data/reviews/reviews_aus_1.zip")
    unzip_fill_reviews("../../data/reviews/reviews_aus_2.zip")
    # ITA
    unzip_fill_reviews("../../data/reviews/reviews_ita_1.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_2.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_3.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_4.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_5.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_6.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_7.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_8.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_9.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_10.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_11.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_12.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_13.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_14.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_16.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_17.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_18.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_19.zip")
    unzip_fill_reviews("../../data/reviews/reviews_ita_30x.zip")
    # OVERKILL
    unzip_fill_reviews("../../data/reviews/reviews_overkill_1.zip")
    unzip_fill_reviews("../../data/reviews/reviews_overkill_2.zip")


create_database()
bulk_provinces()
bulk_locations()
bulk_reviews()
