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

temp_precip = temperature_rounded.groupby(['tempi', 'precipi'], as_index=False)
traffic_by_temp_precip = temp_precip.mean()
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
# plt.show()

plt.figure()
plt.scatter(traffic_by_temp_precip['tempi'], traffic_by_temp_precip['precipi'],
            s=scaled_entries)
# plt.show()

# Basic functionality with pandas


# correlation between two variables
def correlation(x, y):
    x_std = (x - x.mean()) / x.std(ddof=0)
    y_std = (y - y.mean()) / y.std(ddof=0)
    return (x_std * y_std).mean()


entries = nyc_subway_weather['ENTRIESn_hourly']
cum_entries = nyc_subway_weather['ENTRIESn']
rain = nyc_subway_weather['meanprecipi']
temp = nyc_subway_weather['meantempi']

print("Entries and rain: ", correlation(entries, rain))
print("Entries and temp: ", correlation(entries, temp))
print("Temp and rain: ", correlation(temp, rain))
print("Entries and cumulative entries: ", correlation(entries, cum_entries))


# calculating hourly entries and exits using cumulative figures
def get_hourly_values(cumul, control):
    hourly = (cumul - cumul.shift(1)).dropna()
    control_hourly = (control).dropna()
    return pd.concat([hourly, control_hourly], axis=1)


print(get_hourly_values(cum_entries, entries))


# set day of week
def convert_weekday(weekday):
    if weekday == 0:
        return 'Monday'
    elif weekday == 1:
        return 'Tuesday'
    elif weekday == 2:
        return 'Wednesday'
    elif weekday == 3:
        return 'Thursday'
    elif weekday == 4:
        return 'Friday'
    elif weekday == 5:
        return 'Saturday'
    elif weekday == 6:
        return 'Sunday'
    else:
        return 'Error'


def convert_weekdays(weekdays):
    return weekdays.applymap(convert_weekday)


weekday_df = nyc_subway_weather[['UNIT', 'day_week']].set_index('UNIT')

print(convert_weekdays(weekday_df))


# apply works on each column rather than across the DF. This can return by
# column results. Here return the second highest value in each column

def second_largest_column(col):
    sort_col = col.sort_values(ascending=False)
    return sort_col.iloc[1]


def second_largest(df):
    return df.apply(second_largest_column)


entries_and_exits = nyc_subway_weather[['ENTRIESn_hourly', 'EXITSn_hourly']]
print(second_largest(entries_and_exits))
