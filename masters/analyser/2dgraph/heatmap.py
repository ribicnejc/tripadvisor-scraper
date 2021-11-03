import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from masters.data_managers.utils import database_utils


def graph(year_from, year_to, country, color):
    sql = """
    select location_lng as x, location_lat as y
    from provinces
             join locations l on provinces.province_url = l.attraction_parent_url
             join reviews r on l.attraction_url = r.parent_url
    where  r.review_date > {year_from}
      and r.review_date < {year_to}
        """.format(country=country, year_from=year_from, year_to=year_to)
    connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
    data = database_utils.get_data(connection, sql)

    x_arr = []
    y_arr = []
    for el in data:
        x_arr.append(float(el[0]))
        y_arr.append(float(el[1]))

    dataset = {'Zemljepisna širina': x_arr, 'Zemljepisna dolžina': y_arr}
    dset = pd.DataFrame(data=dataset)
    sns.set_theme()
    sns.set_style("white")
    #fig, ax = plt.subplots(figsize=(10, 8))
    plt.figure(figsize=(8, 6))
    # Custom the inside plot: options are: “scatter” | “reg” | “resid” | “kde” | “hex”
    #sns.jointplot(x=dset['Lat'], y=dset['Lng'], kind='scatter', color=color)
    #plt.savefig(f'{country}-{year_from}-scatter.png'.format(country=country, year_from=year_from))
    sns.kdeplot(x=dset['Zemljepisna širina'], y=dset['Zemljepisna dolžina'], cmap="Reds", shade=True, bw_adjust=.5)
    #sns.jointplot(x=dset['Lat'], y=dset['Lng'], kind='kde', color=color)
    plt.savefig(f'{country}-{year_from}-kde.png'.format(country=country, year_from=year_from))
    plt.show()



# 2980b9
# c0392b
#graph(20200300, 20210101, "slovenia", "#2980b9")
graph(20190100, 20200100, "slovenia", "#bb3f3f")