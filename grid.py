import os
import time
import numpy as np
import pandas
import pandas as pd
import xarray as xr
import datetime as dt
import cartopy as ccrs
import matplotlib.pyplot as plt
import util
#import imageio.v2 as imageio
import os
import glob
import netCDF4 as nc

extent = [-106, -89, 42.0, 30] #Lat and Long extent of map

# //ourdisk/hpc/ai2es/hail/nldn/raw/
filenames = ["TestData.txt", "TestData2.txt", "TestData3.csv"]
#filenames = ["McGovern1.asc"]
columns = ["Date", "Time", "Lat", "Lon", "Magnitude", "Type"]

print("Reading in files...")

runStart = time.time()
os.makedirs(f'output/{runStart}')

xedge = np.arange(-106, -88, 0.02083333)
yedge = np.arange(30, 42, 0.02083333)
xmid = []
ymid = []



i=0
while(i < len(xedge)-1):
    xmid.append((xedge[i]+xedge[i+1])/2)
    i+=1
i=0
while(i < len(yedge)-1):
    ymid.append((yedge[i]+yedge[i+1])/2)
    i+=1


for filename in filenames:
    df = pandas.read_csv(f'{filename}',header=None,delim_whitespace=True, names=columns)

    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df.drop('Date', inplace=True, axis=1)
    df.drop('Time', inplace=True, axis=1)
    startTime = df['datetime'][0].replace(second=0, microsecond=0)
    endTime = startTime + dt.timedelta(0, 86400)
    lastTime = df['datetime'][len(df) - 1].replace(second=0, microsecond=0)
    df = df.set_index('datetime')
    df.sort_values(by='datetime', inplace=True)

    beginDate = startTime.replace(hour=0, minute=0, second=0, microsecond=0)

    while (startTime <= lastTime):
        tempArray = xr.Dataset()
        currentTime = startTime
        while currentTime <= endTime:
            temp = df[slice(currentTime, currentTime+dt.timedelta(0, 300))]
            ax, cbar, C = util.boxbin(temp['Lon'], temp['Lat'], xedge, yedge, mincnt=0)
            if len(temp) > 0:

                if currentTime == startTime:
                    tempArray = xr.Dataset(data_vars=dict(strikes=(["x", "y"], C)),
                                         coords=dict(lon=(["x"], xmid), lat=(["y"], ymid),
                                                     time=(['time'], np.arange(startTime, endTime, 300000000))),
                                           attrs=dict(description="Lightning data"),)
                else:
                    tempArray2 = xr.Dataset(data_vars=dict(strikes=(["x", "y"], C)),
                                           coords=dict(lon=(["x"], xmid), lat=(["y"], ymid),
                                                       time=(['time'], np.arange(startTime, endTime, 300000000))),
                                       attrs=dict(description="Lightning data"), )
                    tempArray = xr.concat([tempArray, tempArray2], data_vars='all', dim='i')
            else:
                pass

            currentTime = currentTime+dt.timedelta(0, 300)

        tempArray.to_netcdf(path=f'output/{runStart}/lightningData{str(startTime).split(" ")[0]}.nc')
        print(f"Saved netcdf lightningData{str(startTime).split(' ')[0]}.nc")
        startTime = endTime
        endTime = endTime + dt.timedelta(0, 86400)
