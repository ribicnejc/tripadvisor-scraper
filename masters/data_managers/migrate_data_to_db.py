import sqlite3
import codecs
import os


def create_database():
    database = "data.db"

    sql_create_provinces_table = """ CREATE TABLE IF NOT EXISTS provinces (
                                        province_name text,
                                        region_name text,
                                        province_url text,
                                        country text,
                                        PRIMARY KEY (province_url)                                        
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create provinces table
        create_table(conn, sql_create_provinces_table)
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


def fill_provinces(folder, country):
    conn = create_connection("data.db")
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


create_database()
fill_provinces("../scraped_data/data_provinces/ukr", "ukraine")
