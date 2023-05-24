import os
import numpy as np
import pandas
import pandas as pd
import xarray as xr
import datetime as dt
import util
import os
import glob
import argparse

def create_parser():
    '''
    Create argument parser
    '''
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description='', fromfile_prefix_chars='@')

    parser.add_argument('--input_acs_files_glob', type=str, default="/ourdisk/hpc/ai2es/hail/nldn/raw_temp/*")
    parser.add_argument('--output_dir', type=str, default="/ourdisk/hpc/ai2es/hail/nldn/gridded")

    return parser

# extent = [-106, -89, 42.0, 30] #Lat and Long extent of map
columns = ["Date", "Time", "Lat", "Lon", "Magnitude", "Type"] #Input dataframe columns

parser = create_parser()
args = parser.parse_args()
args = vars(args)

filenames = glob.glob(args["input_acs_files_glob"])
output_dir = args["output_dir"]

xedge = np.arange(-106, -88, 0.02083333) #Get edges with gridrad
yedge = np.arange(30, 42, 0.02083333) #Get edges with gridrad
xmid = [] #Blank array
ymid = [] #Blank array

i=0
while(i < len(xedge)-1):
    xmid.append((xedge[i]+xedge[i+1])/2) #Calculate and append midpoints
    i+=1
i=0
while(i < len(yedge)-1):
    ymid.append((yedge[i]+yedge[i+1])/2) #Calculate and append midpoints
    i+=1


for filename in filenames: #Do individually for each file
    df = pandas.read_csv(filename, header=None,delim_whitespace=True, names=columns) #Read in dataframe

    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])  #Create datetime column
    df.drop('Date', inplace=True, axis=1) #Drop date axis
    df.drop('Time', inplace=True, axis=1) #Drop time axis
    df.sort_values(by='datetime', inplace=True)  # Sort by time
    startTime = df['datetime'][0].replace(hour=0, minute=0, second=0, microsecond=0) #Get start time of file
    endTime = startTime.replace(hour=0, minute=0, second=0, microsecond=0) + dt.timedelta(0, 86400) #Get end of first day
    lastTime = df['datetime'][len(df) - 1].replace(second=0, microsecond=0) #Get last time in file
    df = df.set_index('datetime') #Set index to datetime in dataframe

    while (startTime <= lastTime): #Loop through entire file
        currentTime = startTime #Get current time within dataframe
        lightning_events_ds_list = []
        times_list = []

        while currentTime < endTime: #Loop through each day
            sliced_df = df[slice(currentTime, currentTime+dt.timedelta(0, 300))] #Slice on 5 minutes
            lightning_events = util.boxbin(sliced_df['Lon'], sliced_df['Lat'], xedge, yedge, mincnt=0) #Create mesh (Randy's code)
            lightning_events_ds = xr.Dataset(
                data_vars=dict(strikes=(["x", "y"], lightning_events)),
                coords=dict(
                    lon=(["x"], xmid),
                    lat=(["y"], ymid),
                ),
                attrs=dict(description="Lightning data"),
            )  # Create dataset

            lightning_events_ds_list.append(lightning_events_ds)
            times_list.append(currentTime)
            currentTime = currentTime+dt.timedelta(0, 300) #Increase current time by 5 minutes

        single_day_ds = xr.concat(lightning_events_ds_list, data_vars='all', dim='time')

        single_day_ds = single_day_ds.assign_coords(time=times_list)
        single_day_ds = single_day_ds.fillna(0)

        output_path = os.path.join(output_dir, str(startTime).split(" ")[0] + ".nc")
        single_day_ds.to_netcdf(output_path) #Save

        startTime = endTime #Reset start time
        endTime = endTime + dt.timedelta(0, 86400) #Increase end time by one day