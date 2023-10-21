from itertools import chain
import numpy as np
import pandas as pd
import re
from collections import Counter
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import QMessageBox
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=0.1)

class DuplicateTrainError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class WrongStationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class SameLengthError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class EmptyListError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
class WrongTimeFormatError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class WrongBoxTimeFormatError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
class BoxColumnLengthError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)  

class IncorrectLengthOfRowsBoxError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)  

class WrongStrictBoxTimeFormatError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def excel_to_pandas(self, filename,y_axis, remark_var, days_var):
    """
    return
    down_up: dict containing all stations and hault timings {'DN':[[station_name],[timings]], 'UP':[[station_name],[timings]]}
    dwn_upp: list with all train number (trains)"""
    df_dict = pd.read_excel(filename, sheet_name=None, header=None, dtype = "object")
    bx_dict = dict()
    rect_dict = dict()
    express_flag =False
    for key in df_dict:
        print(key)
    bx_dict["BOX_DN"] = df_dict.pop("BOX_DN")
    bx_dict["BOX_UP"] = df_dict.pop("BOX_UP")
    down_up = dict()
    dwn_upp = dict()
    color_dict = dict()
    unit_test_dict = dict()
    for key, df in bx_dict.items():
        df.drop(0,axis=1,inplace=True)
        type_str = lambda x: str(x)
        df = df.map(type_str, na_action='ignore')
        df.columns = range(df.columns.size)
        df.iloc[0,:] = df.iloc[0,:].str.strip()
        df
        stations = df.iloc[0,:].squeeze().copy(deep=False)
        wrong_stations = stations.isin(y_axis)
        # time_start = df[1,:].squeeze().copy(deep=False)
        # time_end = df[2,:].squeeze().copy(deep=False)
        pattern = r'(^\d\d:\d\d(?!:))'
        time_df = df[df.index % 3 != 2].copy(deep = False)
        stacked_series = time_df.stack()
        matches = stacked_series.str.extractall(pattern)
        matched_values = matches[0].tolist()
        if matched_values:
            matched_values = [str(item) for item in matched_values]
            raise WrongBoxTimeFormatError(f"The following cells in the BOX sheets have HH:MM time format, please use HH:MM:SS format instead:{', '.join(matched_values)}")
        p1, p2 = r'\d\d:\d\d:\d\d', r'\d:\d\d:\d\d'
        new_df = df.iloc[1:,:].map(type_str, na_action='ignore')
        pattern_checker = r'((^\d?\d:\d\d:\d\d$)|^nan$|^$|^\s*$)'
        num_rows = len(stations)
        wrong_box_rows = []
        for i, row in enumerate(new_df.iterrows()):
            if len(row) > num_rows:
                wrong_box_rows.append(str(i))
        if wrong_box_rows:
            raise IncorrectLengthOfRowsBoxError(f"The following rows in the {str(key)} sheet's number of values in the row exceeds the number of stations provided: row{', row'.join(wrong_box_rows)}\nKindly check the stations in {str(key)} sheet and correct the number of values in the rows.")
        val_checker = pd.DataFrame()
        for i, (index, row) in enumerate(new_df.iterrows()):
            if i % 3 == 0:
                val_checker = pd.concat([val_checker,row], axis = 0)
        values = val_checker.copy(deep=False).stack()
        non_matches = values[~values.str.match(pattern_checker, na=False)].astype(str).tolist()
        if non_matches:
            message = f"The following Time values in {str(key)} sheet are either of incorrect format or have extra characters or space along with time: {', '.join(non_matches)}\nKindly correct the given values."
            QMessageBox.critical(self, "Warning", message)
        new_str_df = new_df.astype(str)
        for label, column in new_str_df.items():
            bool_index = column.str.contains(p2, regex=True, na=False)
            bool_index[2::3] = True
            new_df.loc[~bool_index, label] = np.nan
        regex = lambda x,p: re.findall(p,x)
        def mapper(cell, p1, p2):
            if cell is pd.NA or cell is np.nan:
                return pd.NA
            elif match_p1 := regex(cell,p1):
                return match_p1[0]
            elif match_p2 := regex(cell,p2):
                return match_p2[0]
            else:
                print(f"Regex error {cell}")
                return np.nan
        new_str_df = new_df.astype(str)
        for i, (index, row) in enumerate(new_str_df.iterrows()):
            if i % 3 != 2:
                new_df.loc[index, :] = row.apply(mapper, args = (p1, p2,))
        df.iloc[1:,:] = new_df
        df.columns = df.iloc[0,:]
        df.drop(0,axis=0,inplace=True)
        df.reset_index(drop=True,inplace=True)
        time_df = df[df.index % 3 != 2].copy(deep = False)
        remark_df = df[df.index % 3 == 2].copy(deep = False)
        rect_dict[key] = [(label,time1,time2,remark,) if remark!=np.nan else (label,time1,time2,) for (label,c),(_,c_) in zip(time_df.items(),remark_df.items()) for  time1,time2,remark in zip(c.dropna().to_list()[::3],c.dropna().to_list()[1::3],c_.to_list()[::3])]
        box_col_len_err = [label for label,col in df.items() if len(col.dropna()[::3].to_list())%3!=0]
        pp.pprint(rect_dict)
        # if box_col_len_err:
        #     raise BoxColumnLengthError(f"Following stations in the BOX sheets have either incorrect number of timings for boxes or wrong timing format. Please follow provided format:{', '.join(box_col_len_err)}")    
    for key, df in df_dict.items():
        df.drop(1, axis=1, inplace=True)
        df.columns = range(df.columns.size)
        color_list = df.iloc[0,1:].copy(deep=False).tolist()
        for column in df.columns:
            if pd.api.types.is_string_dtype(df[column].dtype):
                # Check if the above two cells are strings and not NaN
                remark = bool(pd.notna(df.at[1, column])) 
                days = bool(pd.notna(df.at[2, column]))            
                if remark or days:
                    # Concatenate values and update the cell
                    df.at[3, column] = f"{str(df.at[1, column]) + ' ' if remark else ''}{str(df.at[2, column]) + ' ' if days else ''}{df.at[3, column]}"
                # if remark or days:
                #     # Concatenate values and update the cell
                #     # if remark_var is not none remark_var == remark
                #     remark_val = str(df.at[1, column])
                #     days_val = str(df.at[2, column])
                #     df.at[3, column] = f"{remark_val + ' ' if remark else ''}{days_val + ' ' if days else ''}{df.at[3, column]}"
                #     # check whether the remark var is p
                #     if regex(remark_val, remark_var):
                #         df[column]= pd.NA
                #         df.rename(columns = {column:pd.NA}, inplace =True)
                    
                #     if regex(days_val, days_var):
                #         df[column]= pd.NA
                #         df.rename(columns = {column:pd.NA}, inplace =True)
        df.drop(2, axis=0, inplace=True)
        df.drop(1, axis=0, inplace=True)
        df.drop(0, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.iloc[0,0] = np.nan
        print(df)
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
        pattern = r'(^\d\d:\d\d(?!:))'
        stacked_series = df.stack()
        matches = stacked_series.str.extractall(pattern)
        matched_values = matches[0].tolist()
        if matched_values:
            matched_values = [str(item) for item in matched_values]
            raise WrongTimeFormatError(f"The following cells have HH:MM time format, please use HH:MM:SS format instead:{', '.join(matched_values)}")
        p1, p2 = r'\d\d:\d\d:\d\d', r'\d:\d\d:\d\d'
        for label, column in df.items():
            bool_index = column.str.contains(p2, regex=True, na=False)
            df.loc[~bool_index, label] = np.nan
        regex = lambda x,p: re.findall(p,x)
        df = df.applymap(lambda cell: regex(cell,p1)[0] if regex(cell,p1) else (regex(cell,p2)[0] if regex(cell,p2) else print(f"Regex error {cell}")), na_action = 'ignore')
        list_2d = []
        unit_test = []
        len_err = []
        empty_err = []
        
        # df = df.loc[:,~df.columns.duplicated()].copy()
        for index, (label, column) in enumerate(df.items()):
            column.dropna(inplace=True)
            row_indices = column.index.tolist()
            datapoints = column.tolist()
            if not datapoints:
                empty_err.append(trains_list[index])
            #     continue
            # print(row_indices)
            # print(len(row_indices))
            # can we revert if all
            #  if any train is greater then its not for local
            if len(row_indices) >=30:
                express_flag = True

            if len(row_indices) != len(datapoints):
                len_err.append(trains_list[index])
            unit_test = unit_test + [(trains_list[index], color_list[index], row_indices, datapoints,)]
            # list_2d = list_2d + [list(row_indices), list(datapoints)] #Create the 2-dimensional list
        if len_err:
            raise SameLengthError(f"Following trains have do not have same length stations and timings: {', '.join(len_err)}")
        # if empty_err:
            # empty_err = [str(item) for item in empty_err]
            # raise EmptyListError(f"Following trains have do have empty lists: {', '.join(empty_err)}")
        unit_test = [(train,clr,stns,time,) for train,clr,stns,time in unit_test if stns and time]
        trains_list,color_list,station_list,train_timings = tuple(list(i) for i in tuple(zip(*unit_test)))
        for stns,timings in zip(station_list,train_timings):
            list_2d = list_2d + [stns,timings]

        
        unit_test_dict[key] = unit_test
        down_up[key] = list_2d
        dwn_upp[key] = trains_list
        color_dict[key] = color_list

    # print("express_flag",express_flag)
    return down_up, dwn_upp, color_dict, rect_dict, express_flag

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
        if (19 <= int(down_up[sheet][i][0].split(":")[0]) <=20):# and (70 < int(down_up["UP"][i][0][4:6]) < 80):
        # print(dwn)
            # print((i-1)//2)
            # print(dwn_upp[sheet][(i-1)//2])
            train_dict[sheet].append(dwn_upp[sheet][(i-1)//2])
            new_dict[sheet].append(down_up[sheet][i-1])
            new_dict[sheet].append(down_up[sheet][i])
        i+=2
    # print("train_dict",train_dict)
    return new_dict, train_dict


def time_to_float(time_string):
    hours, minutes, seconds = map(int, time_string.split(':'))
    # Convert hours, minutes, and seconds to a decimal representation of hours
    time_in_hours = hours + (minutes / 60) + (seconds / 3600)
    after_decimal = time_in_hours % 1
    time_in_hours = int(time_in_hours) + after_decimal
    rounded_time = round(time_in_hours, 2)
    return rounded_time

def conversion(station_dict):
    for key, value in station_dict.items():
        for i in range(len(value)):
            if i % 2 == 1:  # Check if it's an alternative column
                for j in range(len(value[i])):
                    value[i][j] = time_to_float(value[i][j])
    return station_dict

def conversion_box(rect_dict):
    for key, box_list in rect_dict.items():
        for i, (label,start_time,end_time,*_) in enumerate(box_list):
            box_list[i] = label, time_to_float(start_time), time_to_float(end_time), _,
    return rect_dict

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
    return down_up

def box_add_24(rect_dict):
    for key, box_list in rect_dict.items():
        for i, (label,start_time,end_time,*_) in enumerate(box_list):
            box_24 = []
            if end_time < start_time:
                end_time+=24
                box_list[i] = label, start_time, end_time, _,
                box_24.append(tuple([label, start_time - 24, end_time - 24, _]))
            else:
                box_24.append(tuple([label, start_time - 24, end_time - 24, _,]))
        box_list.extend(box_24)
    return rect_dict
