import numpy as np
import pandas as pd
import xarray as xr
import datetime as dt
import cartopy as ccrs
import matplotlib.pyplot as plt
import util

extent = [-106, -89, 42.0, 30] #Lat and Long extent of map

#filenames = ["TestData.txt", "TestData2.txt"]
filenames = ["McGovern1.asc", "McGovern2.asc", "McGovern3.asc", "McGovern4.asc", "McGovern5.asc"]
columns = ["Date", "Time", "Lat", "Lon", "Magnitude", "Type"]

print("Reading in files...")

dataframe = pd.DataFrame()

for filename in filenames:
    dataframe = pd.concat([dataframe, pd.read_csv(f"//ourdisk/hpc/ai2es/hail/nldn/raw/{filename}", header = None, delim_whitespace=True, names=columns)], axis=0)

print("Done reading files...")

dataframe['Date'] = dataframe['Date'].str.cat(dataframe['Time'], sep=' ')

dataframe['Date'] = pd.to_datetime(dataframe['Date'], format='%Y-%m-%d %H:%M:%S.%f')
dataframe = dataframe.drop(['Time'], axis=1)

dataframe.sort_values(by=['Date'], inplace=True)
dataframe = dataframe.reset_index()

print(dataframe['Date'])

gridrad = xr.open_dataset('gridrad_grid.nc')
print(f'Gridrad: {gridrad}')
ax, cbar, C = util.boxbin(dataframe['Lon'], dataframe["Lat"], gridrad["Longitude"], gridrad["Latitude"])
print(f"ax: {ax}")
print(f'cbar: {cbar}')
print(f'C: {C}')

plt.savefig(f'images/lightningData{0}.png', transparent=False, dpi=1000) #Save figure
 
