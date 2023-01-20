import numpy as np
import pandas
import pandas as pd
import xarray as xr
import datetime as dt
import cartopy as ccrs
import matplotlib.pyplot as plt
import util

extent = [-106, -89, 42.0, 30] #Lat and Long extent of map

# //ourdisk/hpc/ai2es/hail/nldn/raw/
filenames = ["TestData.txt", "TestData2.txt", "TestData3.csv"]
#filenames = ["McGovern1.asc", "McGovern2.asc", "McGovern3.asc", "McGovern4.asc", "McGovern5.asc"]
columns = ["Date", "Time", "Lat", "Lon", "Magnitude", "Type"]

print("Reading in files...")

dataframe = []

for filename in filenames:
    temp = pandas.read_csv(filename,header=None,delim_whitespace=True, names=columns)
    dataframe.append(temp)

df = pd.concat(dataframe, axis=0, ignore_index=True)

# lon = df[3]
# lat = df[2]

print("Done reading files...")

print(df)
df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
print(df)
df.drop('Date', inplace=True, axis=1)
df.drop('Time', inplace=True, axis=1)
startTime = df['datetime'][0].
endTime = startTime + dt.timedelta(0,300)
#lastTime = df['datetime'][len(df['datetime']-1)]
df = df.set_index('datetime')
df.sort_values(by='datetime', inplace=True)


xedge = np.arange(-106,-88,0.02083333)
yedge = np.arange(30,42,0.02083333)

print(startTime)
#startTime = startTime.replace(hour=0, minute=0, second=0, microsecond=0)
#print(lastTime)
print(endTime)

while(endTime <= lastTime):
    temp = df[slice(startTime.to_string(), endTime.to_string())]
    ax, cbar, C = util.boxbin(temp['Lon'], temp['Lat'], xedge, yedge, mincnt=0)
    if len(C) > 0:
        plt.savefig(f'images/lightningData{startTime}{endTime}.png', transparent=False, dpi=1000)  # Save figure
        #C.to_netcdf(f'images/lightningData{startTime}{endTime}.png')
    else:
        continue

    startTime = endTime
    endTime = endTime + dt.timedelta(0,300)

print("Done")

#set index to datetime, slice on that
#save netcdf, one for each 5 min lat, lon grid and time in file
#C matrix may be transposed
#
#
