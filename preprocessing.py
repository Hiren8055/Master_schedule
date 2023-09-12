
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

def intersection(station_dict, axes, trains_dict):
    pass
#     # "Input with train array and output plot intersection at particular y"
#     # have to use conversion function in between to convert the time and axis domain
#     # have to only give the intersection in mid subplot with index 1
    
#     # intercept_station = 10


#     def intercept_selection_pts(y_target,index,updn):
#         # add try and except in function 
#         # index = 2 # have to automate for other even indexes
        
#         above_intercept_station = y_target - 1
#         below_intercept_station = y_target + 1
#         # print(station_dict["UP"][index],station_dict["UP"][1])
#         # print(station_dict["UP"][index].index(y_target))
        
        

#         def find(arr1,arr2, target):
#             x,y = None, None
#             # for i in range(len(arr[0])):
#             arr = [arr1,arr2]
#             # print("arr",arr)
#             for i in range(len(arr[0])):
#                 # print(arr[0][i],target)
#                 if arr[0][i] == target:
#                     x,y =  arr[1][i], target
#             return x,y
        
        
#         # find the 10 if not then look for 9 and 11
#         tenth_x, tenth_y = find(station_dict[updn][index],station_dict[updn][index+1],y_target)
#         # print(tenth_x, tenth_y)
#         if tenth_x == None:
#             ele_x,ele_y = find(station_dict[updn][index],station_dict[updn][index+1],below_intercept_station)
#             # print(ele_x,ele_y)
#             if ele_x == None:
#                 return False
#                 # no intersection
#             else:
#                 nin_x,nin_y = find(station_dict[updn][index],above_intercept_station)
#                 # print(nin_x,nin_y) 
#                 return [[nin_x,ele_x],[nin_y,ele_y]]
#         else:
#             return [tenth_x, tenth_y]

#         # if station_dict[updn][index].index(intercept_station):
#         #     intercept_index = station_dict[updn][index].index(intercept_station)
#         # print(station_dict[updn][index+1][intercept_index])
#         # have to select the index of 10 or not then go for below 10 and above 10 ie is 11
#         # find 10 in list and get the index 


#     def intercept(y_target, x ,y):
#         # find the points for intersection
#         x_target = np.interp(y_target,x,y)
#         # print("The x-value for y = 18 virar is:", x_target)
#         return x_target, y_target

#     def add_arrow_labels_intercept(x, y):
#         # selection of graph for inx and iny
#         inx, iny = 0, 0   #NOTE: not necessary
#         # for 0, 0
#         if (0 <= x < 8 and 0 <= y <= 9 ) :
#             # print("condition triggered for label")
#             inx = 0;iny = 0 
#             # print(x,y) 
#         elif (24 <= x <= 32 and 0 <= y <= 9):
#             # print("condition triggered for label MINUSING")
#             x = x - 24
#             # inx = 0;iny = 0
#         # for 0, 1
#         elif (8 <= x < 16 and 0 <= y <= 9) :
#             # print("condition triggered for label")
#             inx = 0;iny = 1
#         # for 0, 2
#         elif (16 <= x <= 24 and 0 <= y <= 9) :
#             # print("condition triggered for label")
#             inx = 0;iny = 2
#         # for 1, 0
#         elif (0 <= x < 8 and 10 <= y <= 31) :
#             # print("condition triggered for label")
#             inx = 1;iny = 0
#         elif (24 <= x <= 32 and 10 <= y <= 31):
#             # print("condition triggered for label MINUSING")
#             x = x - 24
#             inx = 1;iny = 0
#         # for 1, 1
#         elif (8 <= x < 16 and 10 <= y <= 31) :
#             # print("condition triggered for label")
#             inx = 1;iny = 1
#         # for 1, 2
#         elif (16 <= x <= 24 and 10 <= y <= 31) :
#             # print("condition triggered for label")
#             inx = 1;iny = 2
#         # for 2, 0
#         elif (0 <= x < 8 and 31 < y <= 45) :
#             # print("condition triggered for label")
#             inx = 2;iny = 0
#         elif (24 <= x <= 32 and 31 < y <= 45):
#             # print("condition triggered for label MINUSING")
#             x = x - 24
#             inx = 2;iny = 0
#         # for 2, 1
#         elif (8 <= x < 16 and 31 < y <= 45) :
#             # print("condition triggered for label")
#             inx = 2;iny = 1
#         # for 2, 2
#         elif (16 <= x <= 24 and 31 < y <= 45) :
#             # print("condition triggered for label")
#             inx = 2;iny = 2 
#         return inx, iny, x, y
#     # have to make for every train which is going up
#     # put this intersection point in bottom 
#     # send the array to arpit of intersection for labels and arrow
#     # print("station_dict",station_dict)
#     # VR 18
#     def intercept_pts(updn):
#         # drawing fucntion for intersecting points
#         inter_plot_arr = []
#         # print(len(station_dict))
#         # updn = "UP"
        
#         if updn == "UP":
#             y_target = 30
#         elif updn == "DN":
#             y_target = 10
#         # try:
#         arr_index = []
#         for i in range(0,len(station_dict[updn]),2):
#             # print(i)
#             # trains_dict[updn][]
#             # print("station_dict",station_dict[updn][i])
#             inter_arr = intercept_selection_pts(y_target,i, updn)
#             # print("inter_arr",inter_arr)
#             if inter_arr == False:
#                 continue    
#             elif inter_arr[1]!=y_target:
#                 x_target, y_target = intercept(y_target, inter_arr[0] ,inter_arr[1])
#                 inter_plot_arr.append([x_target, y_target])
#                 arr_index.append(i)
#             else:
#                 x_target, y_target = inter_arr[0], inter_arr[1]
#                 inter_plot_arr.append([x_target, y_target])
#                 arr_index.append(i)
                
#         # print(len(inter_plot_arr),len(arr_index)) 
#         # print(arr_index)      
#         # print(trains_dict)
#         print(len(trains_dict["UP"]))
#         for i in range(len(inter_plot_arr)):
#             inx, iny,_,_ = add_arrow_labels_intercept(inter_plot_arr[i][0],inter_plot_arr[i][1])
#             # print("inx",inx, iny)
#             # axes[inx][iny].plot(inter_plot_arr[i][0],inter_plot_arr[i][1], 'o-') # have to automate for all the
#             # print("arr_index[i]//2",arr_index[i],arr_index[i]//2)
#             axes[inx][iny].text(inter_plot_arr[i][0], inter_plot_arr[i][1] + 1, trains_dict[updn][arr_index[i]//2], rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
#             # if inx == 1 and iny==0:
#                 # print("intersection train",inx,iny,trains_dict[updn][i])
#             axes[inx][iny].arrow(inter_plot_arr[i][0], inter_plot_arr[i][1], 0, 0.5, head_width = 0, width = 0.005, clip_on = False)   
#         # except:
#             # print("there should only two present in excel up and down")
#         return inter_plot_arr
#     # will have a intersection array for down and up
#     # def intercept_plot(inter_plot_arr):

#     intercept_pts("UP")
#     intercept_pts("DN")
#     # inter_plot_arr = inter_plot_arr_up+inter_plot_arr_dn
#     # print("inter_plot_arr",inter_plot_arr)
#     # intercept_plot(inter_plot_arr) 
