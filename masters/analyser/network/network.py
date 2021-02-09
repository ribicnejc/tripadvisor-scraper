# libraries
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Build a dataframe with your connections
df = pd.DataFrame({'from': ['Ljubljana', 'B', 'C', 'Ljubljana'], 'to': ['D', 'Ljubljana', 'E', 'C'], 'value': [1, 10, 5, 5]})

# Build your graph
G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph())

# Custom the nodes:
nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, width=df['value'],
        )#edge_cmap=plt.cm.Blues)

plt.show()