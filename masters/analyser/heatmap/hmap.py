# library
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create a dataset
df = pd.DataFrame(np.random.random((1000, 1000)))

# Default heatmap: just a visualization of this square matrix
sns.heatmap(df)
plt.show()