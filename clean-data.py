import pandas as pd
import numpy as np
import os 
# ---------
# clean and store raw temp data
# ---------

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("ghcnd_all") if isfile(join("ghcnd_all", f))]

colnames = ["ID", "Year", "Month", "Element"]

colspecs = [(0,11),(11, 15),(15, 17),(17, 21)]

headers = ["VALUE", "MFLAG", "QFLAG", "SFLAG"]

i = 21
j = 24

for day in range(31):
    for header in headers:
        colnames.append(f"{header}{day+1}")

    spacer = 21 + day*8
    colspecs.append((spacer, spacer + 5))
    colspecs.append((spacer + 5, spacer + 6))
    colspecs.append((spacer + 6, spacer + 7))
    colspecs.append((spacer + 7, spacer + 8))

keepnames = [name for name in colnames if (name in ["ID", "Year", "Month", "Element"]) or "VALUE" in name]

df_list = []

for f in onlyfiles:
    if f[0:2] != "US": continue

    path = join("ghcnd_all", f)

    df = pd.read_fwf(path, 
                     colspecs = colspecs,
                     names = colnames)


    df = df[keepnames]
    df = df[df["Year"] >= 2019]

    df["Date"] = df["Year"].astype(str) + "-" + df["Month"].astype(str)
    df.drop(["Year", "Month"], axis = 1)

    df = df.replace(-9999, np.nan)

    df_list.append(df)

df_with_all_stations = pd.concat(df_list, axis=1)
df_with_all_stations.to_csv("all_stations_2019-2021.csv", index = False)

# ---------
# clean and store metadata
# ---------

path = "ghcnd-stations.txt"
colspecs = [(0, 11), (12, 20), (21, 30), (31, 37), (38, 40), (41, 71)]
colnames = ["ID", "LATITUDE", "LONGITUDE", "STNELEV", "STATE", "NAME"]

df = pd.read_fwf(path, 
                 colspecs = colspecs,
                 names = colnames)

df.to_csv("station-metadata.csv", index = False)