import numpy as np
import pandas as pd
import xarray as xr
import datetime as dt

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

netcdf = xr.open_dataset('gridrad_grid.nc')
print(netcdf)

