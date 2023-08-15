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
from plot_new import plot_trains
# TODO: HAVE TO PERFORM IT FOR ALL THE COLUMNS IN SHEETS "DOWN"
# HAVE TO ACCESS ANOTHER SHEET NAMED "UP"


def excel_to_pandas(filename):
    """
    output
    down_up: time and train in single array alternatively
    y_axis:
    y_labes:
    dwn_upp:
    """
    df_dict = pd.read_excel(filename, sheet_name=['DN', 'UP'], header=None)
    down_up = dict()
    dwn_upp = dict()
    for key, df in df_dict.items():
        first_filled_row_index = df.first_valid_index()
        df = df.loc[first_filled_row_index:]
        df = df[2:]
        df = df[:-3]
        df = df.iloc[::-1]
        first_non_empty_row = df.apply(lambda row: row.notnull().any(), axis=1).idxmax()
        df = df.loc[first_non_empty_row:]
        df = df.iloc[::-1]
        df = df.loc[~(df.iloc[:, 0].isna() & df.iloc[:, 0].shift().isin(["EA", "TRT"]))]
        df = df.loc[~df.iloc[:, 0].isin(["EA", "TRT"])]
        df.iloc[:, 0].fillna(method="ffill", inplace=True)
        df = df.dropna(subset=df.columns[2:], how="all")
        df = df.reset_index(drop=True)
        df = df.drop(df.columns[1], axis=1)
        df.iloc[0, 0] = np.nan
        df.columns = df.iloc[0]
        df = df.drop(0)
        first_column_series = df.iloc[:, 0]
        df = df.iloc[:, 1:]
        first_column_series = first_column_series.rename(None)
        first_column_series = first_column_series.str.strip()
        df = df.set_index(first_column_series)
        trains_list = df.columns.tolist()
        list_2d = []
        df = df.loc[:,~df.columns.duplicated()].copy()

        for column_name in df.columns:
            
            column_df = df[column_name]
            column_df = column_df.dropna()
            column_df = column_df.astype(str)
            column_df = column_df.str.replace('01-01-1900', '')
            column_df = column_df.str.replace('1900-01-01', '')
            column_df = column_df.str.replace('1900-01-02', '')
            column_df = column_df.str.replace('1900-01-08', '')
            column_df = column_df.str.replace('1900-01-24', '')
            column_df = column_df.str.replace('1900-01-22', '')
            column_df = column_df.replace(r'([\s_-]+^$(\.))', np.nan, regex=True)
#             column_df = column_df.dropna()
#             mask = column_df.str.contains(r'\.+')
#             column_df[mask] = np.nan
            column_df = column_df.dropna()
#             column_df = column_df[column_df != "......"]
            column_df = column_df[column_df.astype(str).str.contains(r'\d\d:\d\d:\d\d', na=False)]
            column_df = pd.DataFrame(column_df)
            row_indices = column_df.index.tolist()
            datapoints = column_df.iloc[:, 0].tolist()

            # Create the 2-dimensional list
            list_2d = list_2d + [row_indices, datapoints]
            
            #TODO: add try and except raise error in panel to user for formating issue
            if len(column_df) == 1:
                # print(column_df)
                print("Formatting problem check the Dates format.")
            
        down_up[key] = list_2d
        down_up[key + key] = df.index # WHY
        dwn_upp[key] = trains_list
    y_axis = ["CCG","BCT","DDR","BA","BDTS","ADH","BVI","BYR","BSR","NSP","VR","VTN","SAH","KLV","PLG","UOI","BOR","VGN","DRD","GVD","BRRD","UBR","SJN","BLD","KEB","VAPI","BAGD","UVD","PAD","ATUL","BL","DGI","JRS","BIM","AML","ACL","VDH","HXR","GNST","NVS","MRL","SCH","BHET","UDN","ST"]
    y_labes = ["CCG 0.0","BCT 14.66","DDR 10.17","BA 14.66","BDTS 15.29","ADH 29.32","BVI 33.98","BYR 43.11","BSR 51.78","NSP 55.85","VR 59.98","VTN 68.42","SAH 76.74","KLV 82.55","PLG 90.92","UOI 97.15","BOR 102.8","VGN 111.5","DRD 123.7","GVD 134.8","BRRD 139.0","UBR 144.0","SJN 149.4","BLD 160.9","KEB 165.8","VAPI 172.0","BAGD 179.0","UVD 182.0","PAD 187.7","ATUL 191.0","BL 198.22","DGI 207.21","JRS 212.28","BIM 216.41","AML 221.72","ACL 225.33","VDH 228.87","HXR 232.0","GNST 234.0","NVS 237.33","MRL 245.63","SCH 252.26","BHET 257.3","UDN 262.77","ST 266.78"]
    down_up.pop("DNDN") 
    down_up.pop("UPUP")
    # print(down_up)
    return down_up,y_axis,y_labes, dwn_upp

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

down_up, y_axis, y_labes, dwn_upp =  excel_to_pandas('HIREN_new.xlsx')

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

    i = 1
    while i<len(down_up["UP"]):
        if (9 < int(down_up["UP"][i][0][1:3]) < 13):# and (70 < int(down_up["UP"][i][0][4:6]) < 80):
            new_dict["UP"].append(down_up["UP"][i-1])
            new_dict["UP"].append(down_up["UP"][i])
        i+=2

    # i = 1
    # while i<len(down_up["DN"]):
    #     # if (0 < int(down_up["UP"][i][0][1:3]) < 2):# and (70 < int(down_up["UP"][i][0][4:6]) < 80):
    #     new_dict["DN"].append(down_up["DN"][i-1])
    #     new_dict["DN"].append(down_up["DN"][i])
    #     i+=2

    return new_dict
new = select(down_up)

down_up = conversion(new)
down_up = add_24_down_up(down_up)
plot_trains(down_up, y_axis, y_labes, dwn_upp)


# # print("down_up",down_up)
# down_up = conversion(down_up)
# # print("conversion down_up",down_up)
# down_up = add_24_down_up(down_up)
# # print("add_24_down_up down_up",down_up,dwn_upp)
# plot_trains(down_up, y_axis, y_labes, dwn_upp)