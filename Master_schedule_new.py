# TODO
# - Clear dots in pdf (30 dots) 
# - Resolve graph_plotting
# - check for specific time domain plots.
# 1. Excel sheet to numpy array. 
# 2. Conversion 0.99 to 0.59  5/3 ratio.
# 3. Numpy array to visualization.
# %%
import pandas as pd
import copy
# %%
import matplotlib.pyplot as plt
import numpy as np
from plot import plot_trains
# TODO: HAVE TO PERFORM IT FOR ALL THE COLUMNS IN SHEETS "DOWN"
# HAVE TO ACCESS ANOTHER SHEET NAMED "UP"
import re
from collections import Counter

class DuplicateTrainError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class WrongStationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def excel_to_pandas(filename):
    df_dict = pd.read_excel(filename, sheet_name=['DN', 'UP'], header=None)
    y_axis = ["CCG","BCT","DDR","BA","BDTS","ADH","BVI","BYR","BSR","NSP","VR","VTN","SAH","KLV","PLG","UOI","BOR","VGN","DRD","GVD","BRRD","UBR","SJN","BLD","KEB","VAPI","BAGD","UVD","PAD","ATUL","BL","DGI","JRS","BIM","AML","ACL","VDH","HXR","GNST","NVS","MRL","SCH","BHET","UDN","ST"]
    y_labes = ["CCG 0.0","BCT 14.66","DDR 10.17","BA 14.66","BDTS 15.29","ADH 29.32","BVI 33.98","BYR 43.11","BSR 51.78","NSP 55.85","VR 59.98","VTN 68.42","SAH 76.74","KLV 82.55","PLG 90.92","UOI 97.15","BOR 102.8","VGN 111.5","DRD 123.7","GVD 134.8","BRRD 139.0","UBR 144.0","SJN 149.4","BLD 160.9","KEB 165.8","VAPI 172.0","BAGD 179.0","UVD 182.0","PAD 187.7","ATUL 191.0","BL 198.22","DGI 207.21","JRS 212.28","BIM 216.41","AML 221.72","ACL 225.33","VDH 228.87","HXR 232.0","GNST 234.0","NVS 237.33","MRL 245.63","SCH 252.26","BHET 257.3","UDN 262.77","ST 266.78"]    # print(down_up)
    down_up = dict()
    dwn_upp = dict()
    for key, df in df_dict.items():
        df.drop(1, axis=1, inplace=True)
        df.columns = range(df.columns.size)
        trains_list = df.iloc[0,1:].copy(deep=False).tolist()
        trains_list = trains_list.tolist()
        counter = Counter(trains_list)
        duplicates = [item for item, count in counter.items() if count > 1]
        if duplicates:
            raise DuplicateTrainError(f"Following duplicate trains are present in spread sheet: {', '.join(duplicates)}")
        df.drop(0, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.iloc[:, 0].fillna(method="ffill", inplace=True)
        df.iloc[:, 0]= df.iloc[:, 0].str.strip()
        first_column_series = df.iloc[:,0].copy(deep=False).rename(None)
        wrong_stations = first_column_series.isin(y_axis)
        if (wrong_stations==False).any():
            wrong_stations = first_column_series[~wrong_stations].tolist
            raise WrongStationError(f"The following stations in the excel sheet are wrong:{', '.join(wrong_stations)}.\nPlease use only use from the following station names: {', '.join(y_axis)}.")
        df.set_index(first_column_series,drop = True, inplace=True)
        df.drop(0, axis=1, inplace=True)
        df.columns = range(df.columns.size)
        df = df.astype(str)
        p1, p2 = r'\d\d:\d\d:\d\d', r'\d:\d\d:\d\d'
        for label, column in df.items():
            bool_index = column.str.contains(p2, regex=True, na=False)
            df.loc[~bool_index, label] = np.nan
        regex = lambda x,p: re.findall(p,x)
        df = df.applymap(lambda cell: regex(cell,p1)[0] if regex(cell,p1) else (regex(cell,p2)[0] if regex(cell,p2) else print(f"Regex error {cell}")), na_action = 'ignore')
        list_2d = []
        #TODO: add warning for duplicate train numbers
        # df = df.loc[:,~df.columns.duplicated()].copy()
        for label, column in df.items():
            column.dropna(inplace=True)
            row_indices = column.index.tolist()
            datapoints = column.tolist()
            list_2d = list_2d + [row_indices, datapoints] #Create the 2-dimensional list
            #TODO: add try and except raise error in panel to user for formating issue
        down_up[key] = list_2d
        dwn_upp[key] = trains_list
    return down_up,y_axis, y_labes, dwn_upp 

def conversion(station_dict):
    # this wil multiply with ratios for plotting
    # print(station_dict.items())
    for key, value in station_dict.items():
        for i in range(len(value)):
            if i % 2 == 1:  # Check if it's an alternative column
                for j in range(len(value[i])):
                    time_string = value[i][j]
                    hours, minutes, seconds = map(int, time_string.split(':'))

                    # Convert hours, minutes, and seconds to a decimal representation of hours
                    time_in_hours = hours + (minutes / 60) + (seconds / 3600)

                    after_decimal = time_in_hours % 1
                    time_in_hours = int(time_in_hours) + after_decimal

                    # Update the value in the dictionary
                    value[i][j] = str(round(time_in_hours, 2))

                value[i] = [float(num) for num in value[i]]
    return station_dict

def add_24_down_up(down_up):
    y = False
    for key, arr_2 in down_up.items():
        for hi in range(1, len(arr_2),2):
            for x in range(len(arr_2[hi])-1):
                if(arr_2[hi][x+1] < arr_2[hi][x]):
                    y = x+1
            if(y):
                # print(True)
                arr_4 = [arr_2[hi][i] + 24 for i in range(y, len(arr_2[hi]))]
                arr_2[hi]= arr_2[hi][:y]+ arr_4
            y = False
        down_up[key] = arr_2
    # print("add_24",down_up)
    return down_up

down_up, y_axis, y_labes, dwn_upp =  excel_to_pandas('HIREN2.xlsx')

for key in dwn_upp:
    dwn_upp[key] = [value for value in dwn_upp[key]]

# print(down_up)
# TODO: sort the list separately according to 3 X 3 plot

# Function for capping the list
def select(down_up):
    # Check all the possible
    # MAJOR PROBLEM IS IN UP TRAINS STARTING OF TRAI
    # sort the issue by caping and checking the results of major issue area
    # Check what is the issue regarding the ccg station as train plots are above the ccg station 

    # minor problem is with down trains 
    
    new_dict = {"DN":[],"UP":[]}
    # for i in range(1,len(down_up["DN"])):

    # i = 1
    # while i<len(down_up["UP"]):
    #     # if (9 < int(down_up["UP"][i][0][1:3]) < 13):# and (70 < int(down_up["UP"][i][0][4:6]) < 80):
    #     new_dict["UP"].append(down_up["UP"][i-1])
    #     new_dict["UP"].append(down_up["UP"][i])
    #     i+=2

    i = 1
    while i<len(down_up["DN"]):
        # if (22 < int(down_up["DN"][i][0][1:3]) < 27):# and (70 < int(down_up["UP"][i][0][4:6]) < 80):
        # if (8 < int(down_up["DN"][i][0][1:3]) < 20):# and (70 < int(down_up["UP"][i][0][4:6]) < 80):
        new_dict["DN"].append(down_up["DN"][i-1])
        new_dict["DN"].append(down_up["DN"][i])
        i+=2

    return new_dict
# new = select(down_up)

# down_up = conversion(new)
# down_up = add_24_down_up(down_up)
# plot_trains(down_up, y_axis, y_labes, dwn_upp)


# print("down_up",down_up)
try:
    down_up = conversion(down_up)
except DuplicateTrainError as e:
    print(e)
except WrongStationError as e:
    print(e)
# print("conversion down_up",down_up)
down_up = add_24_down_up(down_up)
# print("add_24_down_up down_up",down_up,dwn_upp)
plot_trains(down_up, y_axis, y_labes, dwn_upp)
