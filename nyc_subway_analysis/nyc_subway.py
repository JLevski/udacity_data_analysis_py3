import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

nyc_subway_weather = pd.read_csv('nyc_subway_weather.csv')

days = nyc_subway_weather.groupby('day_week')
traffic_by_day = days.mean()[['ENTRIESn_hourly', 'EXITSn_hourly']]

rain = nyc_subway_weather.groupby('rain')
traffic_by_rain = rain.mean()[['ENTRIESn_hourly', 'EXITSn_hourly']]

hour_of_day = nyc_subway_weather.groupby('hour')
traffic_by_hour = hour_of_day.mean()[['ENTRIESn_hourly', 'EXITSn_hourly']]

temperature_rounded = pd.DataFrame(nyc_subway_weather).round({'tempi': 0})
temp = temperature_rounded.groupby('tempi')
traffic_by_temp = temp.mean()[['ENTRIESn_hourly', 'EXITSn_hourly']]

temp_and_precip = temperature_rounded.groupby(['tempi', 'precipi'], as_index=False)
traffic_by_temp_precip = temp_and_precip.mean()
scaled_entries = (traffic_by_temp_precip['ENTRIESn_hourly'] /
                  traffic_by_temp_precip['ENTRIESn_hourly'].std())

# Using Pandas to plot charts
fig, axes = plt.subplots(nrows=2, ncols=2)

df0 = pd.DataFrame(traffic_by_day)
df1 = pd.DataFrame(traffic_by_rain)
df2 = pd.DataFrame(traffic_by_hour)
df3 = pd.DataFrame(traffic_by_temp)

df0.plot(ax=axes[0, 0])
ax1 = df1.plot.bar(ax=axes[0, 1])
ax1.set_xticklabels(['no rain', 'rain'])
df2.plot(ax=axes[1, 0])
df3.plot(ax=axes[1, 1])

fig.tight_layout()
plt.show()

plt.figure()
plt.scatter(traffic_by_temp_precip['tempi'], traffic_by_temp_precip['precipi'],
            s=scaled_entries)
plt.show()
