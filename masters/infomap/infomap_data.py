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
    cur.execute("select * from reviews")
    return cur.fetchall()


def get_attractions_cursor():
    conn = create_connection('../database/data.db')
    cur = conn.cursor()
    cur.execute("select * from attractions")
    return cur.fetchall()

def get_pajek_format():
    get_reviews_cursor()
