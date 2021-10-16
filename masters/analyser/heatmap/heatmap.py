#  https://www.storybench.org/how-to-build-a-heatmap-in-python/
import numpy as np
import pandas as pd
import gmaps
import gmaps.datasets

from IPython.display import display

crime = pd.read_csv("crime.csv", encoding='unicode_escape')

gmaps.configure(api_key='YOUR_GOOGLE_MAPS_API_KEY')

Lon = np.arange(-71.21, -71, 0.0021)
Lat = np.arange(42.189, 42.427, 0.00238)
Crime_counts = np.zeros((100, 100))
crime_2018 = crime[crime['YEAR'] == 2018]

for a in range(len(crime_2018)):
    for b1 in range(100):
        if Lat[b1] - 0.00105 <= crime_2018['Lat'].values[a] < Lat[b1] + 0.00105:
            for b2 in range(100):
                if Lon[b2] - 0.00119 <= crime_2018['Long'].values[a] < Lon[b2] + 0.00119:
                    Crime_counts[b1, b2] += 1

longitude_values = [Lon,]*100
latitude_values = np.repeat(Lat,100)
Crime_counts.resize((10000,))

heatmap_data = {'Counts': Crime_counts, 'latitude': latitude_values, 'longitude' : np.concatenate(longitude_values)}
df = pd.DataFrame(data=heatmap_data)
locations = df[['latitude', 'longitude']]
weights = df['Counts']

new_york_coordinates = (30.2690717, 77.9910673)

fig = gmaps.figure(center=new_york_coordinates, zoom_level=17)
#fig = gmaps.figure()
heatmap_layer = gmaps.heatmap_layer(locations, weights=weights)
fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))

fig.open()

display(fig)
