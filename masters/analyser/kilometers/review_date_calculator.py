import math

from masters.data_managers.utils import database_utils
import datetime
from calendar import monthrange


def get_reviews_for_month(date):
    sql1 = """select * from reviews
    where review_date = '{date}'
    order by review_date""".format(date=date)
    conn = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
    c2 = database_utils.get_data(conn, sql1)
    return c2


sql = """
select review_date, count(review_id) from provinces
    join locations l on provinces.province_url = l.attraction_parent_url
    join reviews r on l.attraction_url = r.parent_url
group by review_date
        """
connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
data = database_utils.get_data(connection, sql)
print("Grouped by done")
fixed_dates = {}
correct_date = 0
for e in data:
    date = e[0]
    if date == "None":
        continue
    if len(date) < 8 or len(date) > 8:
        continue
    fixed_dates[date] = []
    norm = e[1]
    month_days = monthrange(int(date[0:4]), int(date[4:6]))[1]
    for i in range(month_days):
        if norm < month_days:
            norm = month_days
        for j in range(math.ceil((norm / month_days))):
            if i < 9:
                correct_date = date[0:4] + date[4:6] + "0" + str((i + 1))
            else:
                correct_date = date[0:4] + date[4:6] + str((i + 1))
            fixed_dates[date].append(correct_date)
    for i in range(1000):
        fixed_dates[date].append(correct_date)  # this is for the last day - edge case

print("New dates calculated")

sql = """select * from reviews order by review_id"""
connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
data = database_utils.get_data(connection, sql)

print("Reviews ordered by id")
correction_list = None
counter = 0
dlen = len(data)
loop = 0
for e in data:
    loop += 1
    print("Setting entry: " + str(loop))
    review_date = e[9]
    if len(review_date) < 8 or len(review_date) > 8:
        continue
    if review_date == "None" or review_date == "review_date":
        continue
    review_id = e[8]
    if correction_list is None or review_date[0:6] != correction_list[0][0:6]:
        correction_list = fixed_dates[review_date]
        counter = 0
    calculated_date = correction_list[counter]

    sql = ''' UPDATE reviews
                  SET calculated_dates = "{calc}"
                  WHERE review_id = "{revid}"'''.format(calc=calculated_date, revid=review_id)
    cur = connection.cursor()
    cur.execute(sql)
    counter += 1

connection.commit()
print("Reviews updated with new date")

# ALTER TABLE reviews
#  ADD calculated_dates VARCHAR;
