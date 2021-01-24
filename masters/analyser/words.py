from wordcloud import WordCloud
import matplotlib.pyplot as plt
from masters.data_managers.utils import database_utils

# Get data
sql = """select review_location_type from provinces join locations l on provinces.province_url = l.attraction_parent_url
join reviews r on l.attraction_url = r.parent_url
where country = 'slovenia'"""
connection = database_utils.create_connection("../data/databases/data.db")
data = database_utils.get_data(connection, sql)

# Create a list of word
text = (
    "Python Python Python Matplotlib Matplotlib Seaborn Network Plot Violin Chart Pandas Datascience Wordcloud Spider Radar Parrallel Alpha Color Brewer Density Scatter Barplot Barplot Boxplot Violinplot Treemap Stacked Area Chart Chart Visualization Dataviz Donut Pie Time-Series Wordcloud Wordcloud Sankey Bubble")
all_words = ""
for word in data:
    tmp = word[0].replace(" ", "").replace("&", " ")
    all_words = all_words + " " + tmp

text = (all_words)
# Create the wordcloud object
wordcloud = WordCloud(width=480, height=480, margin=0).generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()
