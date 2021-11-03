# naredi graf, frekvenčne porazdelitve števila komentarjev po mesecih
# frekvenca med datumom objave in datumom izkušnje

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from masters.data_managers.utils import database_utils


# df = sns.load_dataset('iris')
def map_date(date):
    month = date[4:6]
    if month == "01":
        return "Jan"
    if month == "02":
        return "Feb"
    if month == "03":
        return "Mar"
    if month == "04":
        return "Apr"
    if month == "05":
        return "Maj"
    if month == "06":
        return "Jun"
    if month == "07":
        return "Jul"
    if month == "08":
        return "Avg"
    if month == "09":
        return "Sep"
    if month == "10":
        return "Okt"
    if month == "11":
        return "Nov"
    if month == "12":
        return "Dec"


def get_monthly_visits(country, year_from, year_to):
    sql = """
        select review_experience_date, review_date
        from provinces
                 join locations l on provinces.province_url = l.attraction_parent_url
                 join reviews r on l.attraction_url = r.parent_url
        where country = '{country}'
          and r.review_date > {year_from}
          and r.review_date < {year_to}
        order by review_date
            """.format(country=country, year_from=year_from, year_to=year_to)
    connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro.db")
    data = database_utils.get_data(connection, sql)

    month_arr = []
    type_arr = []
    for el in data:
        month_arr.append(map_date(el[1]))
        type_arr.append("Date of comment")

    for el in data:
        month_arr.append(map_date(el[0]))
        type_arr.append("Date of experience")

    f, axes = plt.subplots(1, 1, figsize=(7, 7), sharex=True)
    d = {'Month': month_arr, 'Tip': type_arr}
    df = pd.DataFrame(data=d)
    # sns.distplot(df, label="2020")
    sns.histplot(data=df, x="Month", hue="Tip", kde=True,
                 multiple="dodge")
    plt.savefig(f'{country}-{year_from}-slovensko.png'.format(country=country, year_from=year_from))
    plt.show()


get_monthly_visits('slovenia', 20200100, 20210100)
# get_monthly_visits('slovenia', 20190100, 20200100)
