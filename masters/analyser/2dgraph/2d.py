import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from masters.data_managers.utils import database_utils


def graph(year_from, year_to, country, color):
    sql = """
    select location_lng as x, location_lat as y, country
    from provinces
             join locations l on provinces.province_url = l.attraction_parent_url
             join reviews r on l.attraction_url = r.parent_url
    where r.review_date > {year_from}
      and r.review_date < {year_to}
        """.format(country=country, year_from=year_from, year_to=year_to)
    connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro.db")
    data = database_utils.get_data(connection, sql)

    sl_x_arr = []
    sl_y_arr = []
    cr_x_arr = []
    cr_y_arr = []
    au_x_arr = []
    au_y_arr = []
    it_x_arr = []
    it_y_arr = []
    hu_x_arr = []
    hu_y_arr = []
    for el in data:
        if el[2] == "slovenia":
            sl_x_arr.append(float(el[0]))
            sl_y_arr.append(float(el[1]))
        if el[2] == "croatia":
            cr_x_arr.append(float(el[0]))
            cr_y_arr.append(float(el[1]))
        if el[2] == "italy":
            it_x_arr.append(float(el[0]))
            it_y_arr.append(float(el[1]))
        if el[2] == "austria":
            au_x_arr.append(float(el[0]))
            au_y_arr.append(float(el[1]))
        if el[2] == "hungary":
            hu_x_arr.append(float(el[0]))
            hu_y_arr.append(float(el[1]))

    sl_dataset = {'SLat': sl_x_arr, 'SLng': sl_y_arr}
    au_dataset = {'Zemljepisna širina': au_x_arr, 'Zemljepisna dolžina': au_y_arr}
    it_dataset = {'ILat': it_x_arr, 'ILng': it_y_arr}
    hu_dataset = {'HLat': hu_x_arr, 'HLng': hu_y_arr}
    cr_dataset = {'CLat': cr_x_arr, 'CLng': cr_y_arr}

    sldset = pd.DataFrame(data=sl_dataset)
    audset = pd.DataFrame(data=au_dataset)
    itdset = pd.DataFrame(data=it_dataset)
    hudset = pd.DataFrame(data=hu_dataset)
    crdset = pd.DataFrame(data=cr_dataset)

    #fig, ax = plt.subplots(figsize=(10, 7))

    #sns.set_theme()
    #sns.scatterplot(x=audset['Lat'], y=audset['Lng'], color="#7dbeff", label="Austria")
    #sns.scatterplot(x=itdset['ILat'], y=itdset['ILng'], color="#75bf5c", label="Italy")
    #sns.scatterplot(x=hudset['HLat'], y=hudset['HLng'], color="#ce9cff", label="Hungary")
    #sns.scatterplot(x=crdset['CLat'], y=crdset['CLng'], color="#ffc37e", label="Croatia")
    #sns.scatterplot(x=sldset['SLat'], y=sldset['SLng'], color="#ff4e60", label="Slovenia")

    sns.scatterplot(x=audset['Zemljepisna širina'], y=audset['Zemljepisna dolžina'], color="#ccc", label="Avstrija")
    sns.scatterplot(x=itdset['ILat'], y=itdset['ILng'], color="#aaa", label="Italija")
    sns.scatterplot(x=hudset['HLat'], y=hudset['HLng'], color="#999", label="Madžarska")
    sns.scatterplot(x=crdset['CLat'], y=crdset['CLng'], color="#666", label="Hrvaška")
    sns.scatterplot(x=sldset['SLat'], y=sldset['SLng'], color="#000", label="Slovenija")

    #sns.jointplot(x=dset['Lat'], y=dset['Lng'], kind='scatter', color="#2980b9")
    #sns.jointplot(x=dset['Lng'], y=dset['Lat'], kind='scatter', color="#c0392b")

    plt.savefig(f'{country}-{year_from}-scatter.png'.format(country=country, year_from=year_from))
    plt.show()


# 2980b9
# c0392b
# 2980b9
graph(20190101, 20210101, "all", "#bb3f3f")
