# Libraries
import math

import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from masters.data_managers.utils import database_utils


# TODO relativni graf
# -- 2020
# -- Sights & Landmarks,830
# -- Nature & Parks,662
# -- Food & Drink,124
# -- Museums,115
# -- Spas & Wellness,65
# -- Fun & Games,45
# -- Outdoor Activities,35
# -- Shopping,26
#

# -- 2019
# -- Sights & Landmarks,6072
# -- Nature & Parks,4585
# -- Museums,868
# -- Food & Drink,498
# -- Spas & Wellness,251
# -- Shopping,169
# -- Outdoor Activities,134
# -- Traveller Resources,116
# Set data


def get_monthly_visits(country, year_from, year_to, year):
    sql = """
        select attraction_name, attraction_url, attraction_type, attraction_rate, review_location_type, count(attraction_url) as visits 
        from provinces
            join locations l on provinces.province_url = l.attraction_parent_url
            join reviews r on l.attraction_url = r.parent_url
        where review_date > {year_from}
            and review_date < {year_to}
        group by attraction_type
       --order by visits desc
""".format(country=country, year_from=year_from, year_to=year_to)
    connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro_updated.db")
    data = database_utils.get_data(connection, sql)
    month_arr = []
    type_arr = []
    for e in data:
        month_arr.append((e[2], e[5]))
        type_arr.append(year)
    return month_arr, type_arr

print("1")
month_arr, type_arr = get_monthly_visits("all", 20190100, 20200100, "2019")
print("2")
m, t = get_monthly_visits("all", 20200200, 20210100, "2020")
print("3")
data = {}
data['group'] = ['2019', '2020']

filt = ["None",
        "Other",
        "Nightlife",
        "Sights & Landmarks",
        "Boat Tours & Water Sports"]

for e in month_arr:
    if e[0] not in filt:
        data[e[0]] = [e[1], 0]

for e in m:
    if e[0] not in filt:
        if e[0] in data:
            data[e[0]][1] = e[1]
        else:
            data[e[0]] = [0, e[1]]

sum1 = 0
sum2 = 0
for k, v in data.items():
    if "group" in k:
        continue
    sum1 += v[0]
    sum2 += v[1]

for k, v in data.items():
    if "group" in k:
        continue
    s1 = math.log2(sum1)
    s2 = math.log2(sum2)
    v1 = math.log2(v[0] + 1)
    v2 = math.log2(v[1] + 1)
    r1 = math.ceil((v1 * 100) / s1)
    r2 = math.ceil((v2 * 100) / s2)
    relative1 = r1
    relative2 = r2
    relative1 = math.log2(math.ceil(v[0] * 100 / sum1) + 1)
    relative2 = math.log2(math.ceil(v[1] * 100 / sum2) + 1)
    data[k] = [relative1, relative2]

order = {'group': ['2019', '2020'],
         "Transportation": [],
         "Museums": [],
         "Events": [],
         "Concerts & Shows": [],
         "Casinos & Gambling": [],
         "Shopping": [],
         "Zoos & Aquariums": [],
         "Classes & Workshops": [],
         "Traveller Resources": [],
         "Fun & Games": [],
         "Spas & Wellness": [],
         "Tours": [],
         "Water & Amusement Parks": [],
        # "Sights & Landmarks": [],
         "Outdoor Activities": [],
         "Nature & Parks": [],
        # "Boat Tours & Water Sports": [],
         "Food & Drink": []}
for k, v in order.items():
    if k not in data:
        data[k] = [0, 0]
    order[k] = data[k]
df = pd.DataFrame(order)

# ------- PART 1: Create background

# number of variable
categories = list(df)[1:]
N = len(categories)

# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
ax = plt.subplot(111, polar=True)

# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)

# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([0.5, 2.5, 6], ["5%", "10%", "30%"], color="grey", size=7)
plt.ylim(0, 6)

# ------- PART 2: Add plots

# Plot each individual = each line of the data
# I don't do a loop, because plotting more than 3 groups makes the chart unreadable

# Ind1
values = df.loc[0].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="2019")
ax.fill(angles, values, 'b', alpha=0.1)

# Ind2
values = df.loc[1].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="2020")
ax.fill(angles, values, 'r', alpha=0.1)

# Add legend
plt.xticks(rotation=45)
plt.legend(loc='upper right', bbox_to_anchor=(0.05, 0.05))
plt.savefig(f'spider_net.png'.format())
plt.show()
