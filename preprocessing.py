
import numpy as np
import pandas as pd
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

def excel_to_pandas( filename):
    df_dict = pd.read_excel(filename, sheet_name=['DN', 'UP'], header=None)
    down_up = dict()
    dwn_upp = dict()
    y_axis = ["CCG","BCT","DDR","BA","BDTS","ADH","BVI","BYR","BSR","NSP","VR","VTN","SAH","KLV","PLG","UOI","BOR","VGN","DRD","GVD","BRRD","UBR","SJN","BLD","KEB","VAPI","BAGD","UVD","PAD","ATUL","BL","DGI","JRS","BIM","AML","ACL","VDH","HXR","GNST","NVS","MRL","SCH","BHET","UDN","ST"]
    for key, df in df_dict.items():
        df.drop(1, axis=1, inplace=True)
        df.columns = range(df.columns.size)
        trains_list = df.iloc[0,1:].copy(deep=False).tolist()
        counter = Counter(trains_list)
        duplicates = [str(item) for item, count in counter.items() if count > 1]
        if duplicates:
            raise DuplicateTrainError(f"Following duplicate trains are present in spread sheet: {', '.join(duplicates)}")
        df.drop(0, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.iloc[:, 0].fillna(method="ffill", inplace=True)
        df.iloc[:, 0]= df.iloc[:, 0].str.strip()
        first_column_series = df.iloc[:,0].copy(deep=False).rename(None)
        wrong_stations = first_column_series.isin(y_axis)
        if (wrong_stations==False).any():
            wrong_stations = set(first_column_series[~wrong_stations].tolist())
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
    return down_up, dwn_upp


def select( down_up,dwn_upp):

    new_dict = {"DN":[],"UP":[]}

    # i = 1
    # while i<len(down_up["UP"]):
    #     # if (9 < int(down_up["UP"][i][0][1:3]) < 13):# and (70 < int(down_up["UP"][i][0][4:6]) < 80):
    #     new_dict["UP"].append(down_up["UP"][i-1])
    #     new_dict["UP"].append(down_up["UP"][i])
    #     i+=2
    i = 1
    sheet = "DN"
    train_dict = {sheet:[]}
    while i<len(down_up[sheet]):
        # print(down_up[sheet][i][0].split(":")[0])
        # print(dwn_upp[sheet][1])
        # if (22 < int(down_up[sheet][i][0][1:3]) < 27):# and (70 < int(down_up["UP"][i][0][4:6]) < 80):
        if (0 <= int(down_up[sheet][i][0].split(":")[0]) <=8):# and (70 < int(down_up["UP"][i][0][4:6]) < 80):
        # print(dwn)
            # print((i-1)//2)
            # print(dwn_upp[sheet][(i-1)//2])
            train_dict[sheet].append(dwn_upp[sheet][(i-1)//2])
            new_dict[sheet].append(down_up[sheet][i-1])
            new_dict[sheet].append(down_up[sheet][i])
        i+=2
    # print("train_dict",train_dict)
    return new_dict, train_dict

def conversion( station_dict):
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

def add_24_down_up( down_up):
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