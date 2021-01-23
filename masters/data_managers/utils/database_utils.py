import sqlite3
import codecs
import os
import re


def get_review_by_location_name(conn, review_name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviews WHERE location_name = ?", (review_name,))
    for row in cur.fetchall():
        return row


def get_location_urls(conn):
    cur = conn.cursor()
    sql = """
        select * from provinces p
        join locations l on p.province_url = l.attraction_parent_url
        where country = 'hungary'
    """
    cur.execute(sql)
    return cur.fetchall()


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
