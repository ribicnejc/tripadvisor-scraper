import math

from masters.data_managers.utils import database_utils
import datetime
from random import random
import random
from calendar import monthrange


def get_unique_locations():
    sql1 = """select * from locations""".format()
    conn = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
    c2 = database_utils.get_data(conn, sql1)
    return c2

connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
cursor = get_unique_locations()
tmp_val = 1
random.seed(123)
for location in cursor:
    pid = location[3]
    new_pid = pid.split("-Reviews")
    new_pid = new_pid[0].split('-d')
    if len(new_pid) < 2:
        new_pid = "None"
        break
    else:
        new_pid = new_pid[1]

    new_pid = ((random.random() * 20) - 10) / 500
    new_pid2 = ((random.random() * 20) - 10) / 500
    sql = ''' UPDATE locations
                SET attraction_id = "{new_pid}"
                WHERE attraction_url = "{pid}"'''.format(pid=pid, new_pid=(new_pid))
    cur = connection.cursor()
    cur.execute(sql)
    sql = ''' UPDATE locations
                    SET attraction_id_2 = "{new_pid}"
                    WHERE attraction_url = "{pid}"'''.format(pid=pid, new_pid=(new_pid2))
    cur = connection.cursor()
    cur.execute(sql)

connection.commit()
print("Reviews updated with new date")

# ALTER TABLE reviews
#  ADD calculated_dates VARCHAR;
