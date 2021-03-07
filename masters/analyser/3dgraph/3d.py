from mpl_toolkits import mplot3d
import random
# https://python-graph-gallery.com/82-marginal-plot-with-seaborn/
import numpy as np
import matplotlib.pyplot as plt
from masters.data_managers.utils import database_utils
from masters import settings
import math
#TODO naredi 2D ker je 3D nepregledno
# Get data
sql = """
select location_lat as x, location_lng as y, count(attraction_name) as z
from provinces
         join locations l on provinces.province_url = l.attraction_parent_url
         join reviews r on l.attraction_url = r.parent_url
where country = 'italy'
  and r.review_date > 20200101
  and r.review_date < 20210101
group by attraction_name
    """
connection = database_utils.create_connection("../../data/databases/slo_aus_ita_hun_cro.db")
data = database_utils.get_data(connection, sql)

# https://towardsdatascience.com/an-easy-introduction-to-3d-plotting-with-matplotlib-801561999725

num_bars = len(data)
x_pos = []
y_pos = []
z_pos = [0] * num_bars
z_size = []
for el in data:
    x_pos.append(float(el[0]))
    y_pos.append(float(el[1]))
    z_size.append((int(el[2])))

fig = plt.figure()
ax = plt.axes(projection="3d")

x_size = [0.05] * num_bars  # np.ones(num_bars)
y_size = [0.05] * num_bars  # np.ones(num_bars)

ax.bar3d(x_pos, y_pos, z_pos, x_size, y_size, z_size, color='aqua')
plt.show()
