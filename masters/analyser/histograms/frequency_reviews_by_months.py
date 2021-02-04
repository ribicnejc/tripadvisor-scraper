# TODO naredi graf, frekvenčne porazdelitve števila komentarjev po mesecih
# TODO frekvenca med datumom objave in datumom izkušnje

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# df = sns.load_dataset('iris')

# plot
f, axes = plt.subplots(1, 1, figsize=(7, 7), sharex=True)

# Control the number of bins

d = {'Mesec': ["Jan", "Feb", "Feb", "Mar"]}
df = pd.DataFrame(data=d)
# sns.distplot(df, label="2020")
tips = sns.load_dataset("tips")

penguins = sns.load_dataset("penguins")
sns.histplot(data=df, x="Mesec", kde=True)
plt.legend()
plt.show()

# sns.distplot(df["sepal_length"], color="skyblue", ax=axes[0, 0])
# sns.distplot(df["sepal_width"], color="olive", ax=axes[0, 1])
# sns.distplot(df["petal_length"], color="gold", ax=axes[1, 0])
# sns.distplot(df["petal_width"], color="teal", ax=axes[1, 1])
# plt.show()

# Import library and dataset
# import seaborn as sns
# import matplotlib.pyplot as plt

# df = sns.load_dataset('iris')

# Method 1: on the same Axis
# sns.distplot(df["sepal_length"], color="skyblue", label="Sepal Length")
# sns.distplot(df["sepal_width"], color="red", label="Sepal Width")

# Make default histogram of sepal length
# sns.distplot(df["sepal_length"])
# sns.plt.show()
