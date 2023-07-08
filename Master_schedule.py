# TODO
# - Clear dots in pdf (30 dots) 
# - Resolve graph_plotting
# - check for specific time domain plots.
# 1. Excel sheet to numpy array. 
# 2. Conversion 0.99 to 0.59  5/3 ratio.
# 3. Numpy array to visualization.
# %%
import pandas as pd
# %%
import matplotlib.pyplot as plt
import numpy as np
from plot import plot_trains
# TODO: HAVE TO PERFORM IT FOR ALL THE COLUMNS IN SHEETS "DOWN"
# HAVE TO ACCESS ANOTHER SHEET NAMED "UP"


def excel_to_pandas(filename):
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
            column_df = column_df.str.replace('1900-01-01 ', '')
            column_df = column_df.replace(r'([\s_-]+|^$|(\.))', np.nan, regex=True)
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
        down_up[key] = list_2d
        down_up[key + key] = df.index
        dwn_upp[key] = trains_list
    y_axis = ["CCG","BCT","DDR","BA","BDTS","ADH","BVI","BYR","BSR","NSP","VR","VTN","SAH","KLV","PLG","UOI","BOR","VGN","DRD","GVD","BRRD","UBR","SJN","BLD","KEB","VAPI","BAGD","UVD","PAD","ATUL","BL","DGI","JRS","BIM","AML","ACL","VDH","HXR","GNST","NVS","MRL","SCH","BHET","UDN","ST"]
    down_up.pop("DNDN")
    down_up.pop("UPUP")
    return down_up,y_axis, dwn_upp

def conversion(station_dict):
    # this wil multiply with ratios for plotting
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
    arr_2= down_up['DN']
    y = False
    for key, arr_2 in down_up.items():
        for hi in range(1, len(arr_2),2):
            for x in range(len(arr_2[hi])-1):
                if(arr_2[hi][x+1] < arr_2[hi][x]):
                    y = x+1
            if(y):
                arr_4 = [arr_2[hi][i] + 24 for i in range(y, len(arr_2[hi]))]
                arr_2[hi]= arr_2[hi][:y]+ arr_4
            y = False
        down_up[key] = arr_2
    return down_up


down_up, y_labes, dwn_upp =  excel_to_pandas('HIREN.xlsx')
for key in dwn_upp:
    dwn_upp[key] = [value for value in dwn_upp[key]]



down_up = conversion(down_up)
down_up = add_24_down_up(down_up)
plot_trains(down_up, y_labes, dwn_upp)
