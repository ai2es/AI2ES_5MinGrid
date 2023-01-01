import numpy as np
import pandas as pd
import xarray as xr
import datetime as dt
import cartopy as ccrs
import matplotlib.pyplot as plt
import util

extent = [-106, -89, 42.0, 30] #Lat and Long extent of map

filenames = ["TestData.txt", "TestData2.txt"]
#filenames = ["McGovern1.asc", "McGovern2.asc", "McGovern3.asc", "McGovern4.asc", "McGovern5.asc"]
columns = ["Date", "Time", "Lat", "Lon", "Magnitude", "Type"]

print("Reading in files...")

dataframe = pd.DataFrame()

for filename in filenames:
    dataframe = pd.concat([dataframe, pd.read_csv(filename, header = None, delim_whitespace=True, names=columns)], axis=0)

dataframe['Date'] = dataframe['Date'].str.cat(dataframe['Time'], sep=' ')

dataframe['Date'] = pd.to_datetime(dataframe['Date'], format='%Y-%m-%d %H:%M:%S.%f')
dataframe = dataframe.drop(['Time'], axis=1)

dataframe.sort_values(by=['Date'], inplace=True)
dataframe = dataframe.reset_index()

print(dataframe['Date'])

gridrad = xr.open_dataset('gridrad_grid.nc')
print(gridrad)
ax,cbar,C = util.boxbin(dataframe['Lon'], dataframe["Lat"], gridrad["Longitude"], gridrad["Latitude"])
central_lon = np.mean(extent[:2]) # Get central longitude
central_lat = np.mean(extent[2:]) # Get central latitude
ax = plt.axes(projection=ccrs.crs.AlbersEqualArea(central_lon, central_lat)) #Create map
ax.set_extent(extent) #Set bounds
ax.add_feature(ccrs.feature.OCEAN) #Add ocean to map
ax.add_feature(ccrs.feature.LAND, edgecolor='black') #Add land to map
ax.add_feature(ccrs.feature.LAKES, edgecolor='black') #Add lakes to map
ax.add_feature(ccrs.feature.RIVERS) #Add rivers to map
ax.add_feature(ccrs.feature.STATES) #Add states to map
ax.gridlines() #Add gridlines

plt.savefig(f'images/lightningData{0}.png', transparent=False, dpi=1000) #Save figure
print("E")

