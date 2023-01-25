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
import imageio.v2 as imageio
import os
import glob

extent = [-106, -89, 42.0, 30] #Lat and Long extent of map

# //ourdisk/hpc/ai2es/hail/nldn/raw/
#filenames = ["TestData.txt", "TestData2.txt", "TestData3.csv"]
filenames = ["McGovern1.asc", "McGovern2.asc", "McGovern3.asc", "McGovern4.asc", "McGovern5.asc"]
columns = ["Date", "Time", "Lat", "Lon", "Magnitude", "Type"]

print("Reading in files...")

dataframe = []

runStart = time.time()
os.makedirs(f'output/{runStart}')

for filename in filenames:
    df = pandas.read_csv(f'//ourdisk/hpc/ai2es/hail/nldn/raw/{filename}',header=None,delim_whitespace=True, names=columns)

    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df.drop('Date', inplace=True, axis=1)
    df.drop('Time', inplace=True, axis=1)
    startTime = df['datetime'][0].replace(second=0, microsecond=0)
    endTime = startTime + dt.timedelta(0, 300)
    lastTime = df['datetime'][len(df) - 1].replace(second=0, microsecond=0)
    df = df.set_index('datetime')
    df.sort_values(by='datetime', inplace=True)

    xedge = np.arange(-106, -88, 0.02083333)
    yedge = np.arange(30, 42, 0.02083333)

    while (endTime <= lastTime):
        temp = df[slice(startTime, endTime)]
        ax, cbar, C = util.boxbin(temp['Lon'], temp['Lat'], xedge, yedge, mincnt=0)
        if len(temp) > 0:
            plt.savefig(f'output/{runStart}/lightningData{startTime}{endTime}.png', transparent=False,
                        dpi=1000)  # Save figure
            print(f'Saved lightningData{startTime}{endTime}.png')
            # C.to_netcdf(f'output/{runStart}/lightningData{startTime}{endTime}.nc')
        else:
            pass

        startTime = endTime
        endTime = endTime + dt.timedelta(0, 300)
        plt.close('all')

    print("Done")

images = []

path = f'output/{runStart}'
for filename in sorted(glob.glob(os.path.join(path, 'Page*.png'))):
    images.append(imageio.imread(filename))
    print(f"Added {filename}")

imageio.mimsave(f'output/{runStart}/{runStart}.gif', images, duration=1)



#set index to datetime, slice on that
#save netcdf, one for each 5 min lat, lon grid and time in file
#C matrix may be transposed
#
#