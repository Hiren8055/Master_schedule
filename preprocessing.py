from itertools import chain
import numpy as np
import pandas as pd
import re
from collections import Counter
from PySide2.QtWidgets import QMessageBox
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=0.1)

class OmittedSheetsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

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

class ExportThreadError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def excel_to_pandas(self, filename,y_axis, remark_var, days_var):
    """
    return
    down_up: dict containing all stations and hault timings {'DN':[[station_name],[timings]], 'UP':[[station_name],[timings]]}
    dwn_upp: list with all train number (trains)"""
    self.canvas.flush_events()
    df_dict = pd.read_excel(filename, sheet_name=None, header=None, dtype = "object")
    self.canvas.flush_events()
    bx_dict = dict()
    rect_dict = dict()
    express_flag = False
    # for key in df_dict:
    #     #print(key)
    sheets = ["DN","UP","BOX_DN","BOX_UP"]
    omitted_sheets = []
    for sheet in sheets:
        if sheet not in df_dict:
            omitted_sheets.append(sheet)
    if omitted_sheets:
            raise OmittedSheetsError(f"Either wrong names are given to sheets or the sheets are absent in the excel file. Please use the provided naming conventions for sheets and that all sheets are present. Following are the absent sheets:{', '.join(omitted_sheets)}")
    bx_dict["BOX_DN"] = df_dict.pop("BOX_DN")
    bx_dict["BOX_UP"] = df_dict.pop("BOX_UP")
    down_up = dict()
    dwn_upp = dict()
    color_dict = dict()
    unit_test_dict = dict()
    regex = lambda x,p: re.findall(p,x)
    ea_trt= r"(EA|TRT)"
    for key, df in bx_dict.items():
        self.canvas.flush_events()
        df.drop(0,axis=1,inplace=True)
        if df.iloc[1:,:].isnull().all().all():
            continue
        type_str = lambda x: str(x)
        df = df.map(type_str, na_action='ignore')
        df.columns = range(df.columns.size)
        df.iloc[0,:] = df.iloc[0,:].str.strip()
        stations = df.iloc[0,:].squeeze().copy(deep=False)
        wrong_stations = stations.isin(y_axis)
        # time_start = df[1,:].squeeze().copy(deep=False)
        # time_end = df[2,:].squeeze().copy(deep=False)
        pattern = r'(^\d\d:\d\d(?!:))'
        time_df = df[df.index % 3 != 2].copy(deep = False)
        stacked_series = time_df.stack()
        matches = stacked_series.str.extractall(pattern)
        matched_values = matches[0].tolist()
        self.canvas.flush_events()
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
        self.canvas.flush_events()
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
        def mapper(cell, p1, p2):
            if cell is pd.NA or cell is np.nan:
                return pd.NA
            elif match_p1 := regex(cell,p1):
                return match_p1[0]
            elif match_p2 := regex(cell,p2):
                return match_p2[0]
            else:
                # #print(f"Regex error {cell}")
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
        rect_dict[key] = [(label,time1,time2,remark,) for (label,c),(_,c_) in zip(time_df.items(),remark_df.items()) for  time1,time2,remark in zip(c.dropna().to_list()[::2],c.dropna().to_list()[1::2],c_.to_list())]
        box_col_len_err = [label for label,col in time_df.items() if len(col.dropna().to_list())%2!=0]
        self.canvas.flush_events()
        #pp.p#print(rect_dict)
        if box_col_len_err:
            raise BoxColumnLengthError(f"Following stations in the BOX sheets have either incorrect number of timings for boxes or wrong timing format. Please follow provided format:{', '.join(box_col_len_err)}")    
    for key, df in df_dict.items():
        self.canvas.flush_events()
        df.drop(1, axis=1, inplace=True)    
        df.columns = range(df.columns.size)
        print(df)
        # df = df.drop(df[df.apply(lambda row: bool(regex(row.astype(str).iat[0], ea_trt)), axis=0)].index)
        df = df[~df[0].str.contains(ea_trt, na=False, case=False, regex=True)]
        df.reset_index(drop = True, inplace=True)
        print(df)
        df_ = pd.DataFrame()
        df_ = pd.concat([df_, df.iloc[:,0]])
        for col, srs in df.items():
            # Check if the above two cells are strings and not NaN
            remark = srs.at[1] is not np.nan
            days = srs.at[2] is not np.nan
            if remark or days:
                # Concatenate values and update the cell
                # if remark_var is not none remark_var == remark
                remark_val = str(srs.at[1])
                days_val = str(srs.at[2])
                srs.at[3] = f"{remark_val + ' ' if remark else ''}{days_val + ' ' if days else ''}{srs.at[3]}"
                regex_remark = None
                regex_days = None
                if remark_var or days_var:
                    # check whether the remark var is p
                    if remark_var:
                        regex_remark = regex(remark_val, remark_var)
                    if days_var: 
                        regex_days = regex(days_val, days_var)
                    
                    if remark_var and days_var and regex_remark and regex_days:
                        # #print("Should not work both")
                        df_ = pd.concat([df_,srs], axis=1)
                    elif (bool(remark_var) ^ bool(days_var)) and ((remark_var and regex_remark) or (days_var and regex_days)):
                        df_ = pd.concat([df_,srs], axis=1)
                else:
                    df[col] = srs
                self.canvas.flush_events()
        if remark_var or days_var:
            df = df_.copy(deep=False)
        color_list = df.iloc[0,1:].copy(deep=False).tolist()
        df.drop(2, axis=0, inplace=True)
        df.drop(1, axis=0, inplace=True)
        df.drop(0, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.iloc[0,0] = np.nan
        # #print(df)
        trains_list = df.iloc[0,1:].copy(deep=False).tolist()
        counter = Counter(trains_list)
        duplicates = [str(item) for item, count in counter.items() if count > 1]
        if duplicates:
            raise DuplicateTrainError(f"Following duplicate trains are present in spread sheet: {', '.join(duplicates)}")
        self.canvas.flush_events()
        df.drop(0, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.iloc[:, 0].ffill(inplace=True)
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
        matches = stacked_series.astype(str).str.extractall(pattern)
        matched_values = matches[0].tolist()
        if matched_values:
            matched_values = [str(item) for item in matched_values]
            raise WrongTimeFormatError(f"The following cells have HH:MM time format, please use HH:MM:SS format instead:{', '.join(matched_values)}")
        p1, p2 = r'\d\d:\d\d:\d\d', r'\d:\d\d:\d\d'
        for label, column in df.items():
            bool_index = column.str.contains(p2, regex=True, na=False)
            df.loc[~bool_index, label] = np.nan
            self.canvas.flush_events()
        regex = lambda x,p: re.findall(p,x)
        df = df.applymap(lambda cell: regex(cell,p1)[0] if regex(cell,p1) else (regex(cell,p2)[0] if regex(cell,p2) else None), na_action = 'ignore')
        list_2d = []
        unit_test = []
        len_err = []
        empty_err = []

        # df = df.loc[:,~df.columns.duplicated()].copy()
        for index, (label, column) in enumerate(df.items()):
            self.canvas.flush_events()
            column.dropna(inplace=True)
            row_indices = column.index.tolist()
            datapoints = column.tolist()
            if not datapoints:
                empty_err.append(trains_list[index])
            #     continue
            # #print(row_indices)
            # #print(len(row_indices))
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
        self.canvas.flush_events()
        unit_test = [(train,clr,stns,time,) for train,clr,stns,time in unit_test if stns and time]
        self.canvas.flush_events()
        trains_list,color_list,station_list,train_timings = tuple(list(i) for i in tuple(zip(*unit_test)))
        self.canvas.flush_events()
        for stns,timings in zip(station_list,train_timings):
            list_2d = list_2d + [stns,timings]
        self.canvas.flush_events()
        unit_test_dict[key] = unit_test
        down_up[key] = list_2d
        dwn_upp[key] = trains_list
        color_dict[key] = color_list

    # #print("express_flag",express_flag)
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
        # #print(down_up[sheet][i][0].split(":")[0])
        # #print(dwn_upp[sheet][1])
        # if (22 < int(down_up[sheet][i][0][1:3]) < 27):# and (70 < int(down_up["UP"][i][0][4:6]) < 80):
        if (19 <= int(down_up[sheet][i][0].split(":")[0]) <=20):# and (70 < int(down_up["UP"][i][0][4:6]) < 80):
        # #print(dwn)
            # #print((i-1)//2)
            # #print(dwn_upp[sheet][(i-1)//2])
            train_dict[sheet].append(dwn_upp[sheet][(i-1)//2])
            new_dict[sheet].append(down_up[sheet][i-1])
            new_dict[sheet].append(down_up[sheet][i])
        i+=2
    # #print("train_dict",train_dict)
    return new_dict, train_dict


def time_to_float(time_string):
    hours, minutes, seconds = map(int, time_string.split(':'))
    # Convert hours, minutes, and seconds to a decimal representation of hours
    time_in_hours = hours + (minutes / 60) + (seconds / 3600)
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
        for i, (label,start_time,end_time,remark) in enumerate(box_list):
            box_list[i] = label, time_to_float(start_time), time_to_float(end_time), remark,
    return rect_dict

def add_24_down_up(down_up):
    y = False
    for key, arr_2 in down_up.items():
        for hi in range(1, len(arr_2),2):
            for x in range(len(arr_2[hi])-1):
                if(arr_2[hi][x+1] < arr_2[hi][x]):
                    y = x+1
            if(y):
                # #print(True)
                arr_4 = [arr_2[hi][i] + 24 for i in range(y, len(arr_2[hi]))]
                arr_2[hi]= arr_2[hi][:y]+ arr_4
            y = False
        down_up[key] = arr_2
    return down_up

def box_add_24(rect_dict):
    for key, box_list in rect_dict.items():
        box_24 = []
        for i, (label,start_time,end_time,remark) in enumerate(box_list):
            if end_time < start_time:
                end_time+=24
                box_list[i] = label, start_time, end_time, remark,
                box_24.append(tuple([label, start_time - 24, end_time - 24, remark]))
        box_list.extend(box_24)
    return rect_dict
