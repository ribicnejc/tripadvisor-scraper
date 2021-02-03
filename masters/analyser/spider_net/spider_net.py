# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

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
sum2019 = 0 + 0 + 498 + 868 + 251 + 99 + 134 + 168
sum2020 = 0 + 0 + 124 + 115 + 65 + 45 + 35 + 26
df = pd.DataFrame({
    'group': ['2019', '2020'],
    # 'Sights & Landmarks': [6072 / sum2019, 830 / sum2020],
    # 'Nature & Parks': [4585 / sum2019, 662 / sum2020],
    'Food & Drink': [498 / sum2019, 124 / sum2020],
    'Museums': [868 / sum2019, 115 / sum2020],
    'Spas & Wellness': [251 / sum2019, 65 / sum2020],
    'Fun & Games': [99 / sum2019, 45 / sum2020],
    'Outdoor Activities': [134 / sum2019, 35 / sum2020],
    'Shopping': [168 / sum2019, 26 / sum2020]
})

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
plt.yticks([0.1, 0.3, 0.5], ["10%", "30%", "50%"], color="grey", size=7)
plt.ylim(0, 0.5)

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
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

plt.show()
