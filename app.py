from PySide2 import QtWidgets
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QScrollArea, QMessageBox, QApplication
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from matplotlib.transforms import Bbox, TransformedBbox
from qt_material import apply_stylesheet
import pandas as pd
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedFormatter
import re
import copy
from collections import Counter


class DuplicateTrainError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class WrongStationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class PlotWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Matplotlib Plot")
        
        self.figure = Figure(figsize=(10, 50), tight_layout=True)
         # self.figure.set_dpi(100)
        
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.canvas)
        
        self.button = QtWidgets.QPushButton("Load Excel File")
        self.button.clicked.connect(self.load_file)
        self.axes = None
        self.export_button = QtWidgets.QPushButton("Export Plot as PDF")
        self.export_button.clicked.connect(self.export_plot)
        self.export_button.setEnabled(False)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.export_button)
        self.canvas.setMinimumSize(5500, 2500)
        self.canvas.setMaximumSize(5501, 2501)
        self.y_axis = ["CCG","BCT","DDR","BA","BDTS","ADH","BVI","BYR","BSR","NSP","VR","VTN","SAH","KLV","PLG","UOI","BOR","VGN","DRD","GVD","BRRD","UBR","SJN","BLD","KEB","VAPI","BAGD","UVD","PAD","ATUL","BL","DGI","JRS","BIM","AML","ACL","VDH","HXR","GNST","NVS","MRL","SCH","BHET","UDN","ST"]
        self.y_labes = ["CCG 0.0","BCT 14.66","DDR 10.17","BA 14.66","BDTS 15.29","ADH 29.32","BVI 33.98","BYR 43.11","BSR 51.78","NSP 55.85","VR 59.98","VTN 68.42","SAH 76.74","KLV 82.55","PLG 90.92","UOI 97.15","BOR 102.8","VGN 111.5","DRD 123.7","GVD 134.8","BRRD 139.0","UBR 144.0","SJN 149.4","BLD 160.9","KEB 165.8","VAPI 172.0","BAGD 179.0","UVD 182.0","PAD 187.7","ATUL 191.0","BL 198.22","DGI 207.21","JRS 212.28","BIM 216.41","AML 221.72","ACL 225.33","VDH 228.87","HXR 232.0","GNST 234.0","NVS 237.33","MRL 245.63","SCH 252.26","BHET 257.3","UDN 262.77","ST 266.78"]    # print(down_up)

    def add_lables(self, new_dict, train_dictionary):
        """Add lables in dictionary"""
        for key in new_dict:
            k = 0
            # range_ = (2 * len(new_dict[key]) - int(1/2 * len(new_dict[key]))) // 3
            range_ = len(new_dict[key]) // 2
            for i in range(range_):
                new_dict[key].insert(k, str(train_dictionary[key][i]))
                k += 3 
        return new_dict
    
    def add_keys(self, new_dict):
        """Add keys in dictionary"""
        for key in new_dict:
            k = 1
            for i in range(len(new_dict[key]) // 3):
                new_dict[key].insert(k + 2, key)
                k += 4
        return new_dict

    def extract_up_elem(self,new_dict):
        """Extracting first element of array  """

        """for up start"""
        collision_updn = [[], [], []] # Extracting first element of x and y

        k = 1 
        for i in range(len(new_dict["UP"]) // 4):         
                # print("length: ", len(new_dict['UP'][k + 1]))
                # print("y axis", new_dict['UP'][k + 1])
                # print("last elem", new_dict['UP'][k + 1][0])                                               
                collision_updn[0].append(new_dict['UP'][k - 1])                                        
                if new_dict['UP'][k + 1][0] >= 24:                                                        
                    collision_updn[1].append(new_dict['UP'][k + 1][0] - 24)                           
                else:                                                                                    
                    collision_updn[1].append(new_dict['UP'][k + 1][0])            
                collision_updn[2].append(new_dict['UP'][k][0])
                k += 4

        new_data = []
        for i in range(len(collision_updn[0])):
            new_data.append([collision_updn[0][i], collision_updn[1][i], collision_updn[2][i],])
        new_data.sort(key=lambda row: (row[2], row[1]))

        data1 = new_data.copy()

        new_data0 = [data1[i][0] for i in range(len(new_data))]
        new_data1 = [data1[i][1] for i in range(len(new_data))]
        new_data2 = [data1[i][2] for i in range(len(new_data))]
        new_data = [new_data0, new_data1, new_data2]

        collision_updn = new_data.copy()

        """for up end"""    

        collision_updn1 = [[], [], []] # Extracting first element of x and y

        k = 1 
        for i in range(len(new_dict["UP"]) // 4):         
                # print("length: ", len(new_dict['UP'][k + 1]))
                # print("y axis", new_dict['UP'][k + 1])
                # print("last elem", new_dict['UP'][k + 1][0])                                               
                collision_updn1[0].append(new_dict['UP'][k - 1])                                        
                if new_dict['UP'][k + 1][-1] >= 24:                                                        
                    collision_updn1[1].append(new_dict['UP'][k + 1][-1] - 24)                           
                else:                                                                                    
                    collision_updn1[1].append(new_dict['UP'][k + 1][-1])            
                collision_updn1[2].append(new_dict['UP'][k][-1])
                k += 4

        new_data = []
        for i in range(len(collision_updn1[0])):
            new_data.append([collision_updn1[0][i], collision_updn1[1][i], collision_updn1[2][i],])
        new_data.sort(key=lambda row: (row[2], row[1]))

        data1 = new_data.copy()

        new_data0 = [data1[i][0] for i in range(len(new_data))]
        new_data1 = [data1[i][1] for i in range(len(new_data))]
        new_data2 = [data1[i][2] for i in range(len(new_data))]
        new_data = [new_data0, new_data1, new_data2]

        collision_updn1 = new_data.copy()

        return collision_updn, collision_updn1    #start, end

    def extract_dn_elem(self,new_dict):
        """Extracting first element of array  """

        """for dn end"""
        collision_updn_for_last = [[], [], []] # Extracting first element of x and y

        k = 1 
        for i in range(len(new_dict["DN"]) // 4):

                collision_updn_for_last[0].append(new_dict['DN'][k - 1])
                if new_dict['DN'][k + 1][-1] >= 24: 
                    collision_updn_for_last[1].append(new_dict['DN'][k + 1][-1] - 24)
                else: 
                    collision_updn_for_last[1].append(new_dict['DN'][k + 1][-1])
                    
                collision_updn_for_last[2].append(new_dict['DN'][k][-1])
                k += 4

        new_data = []
        for i in range(len(collision_updn_for_last[0])):
            new_data.append([collision_updn_for_last[0][i], collision_updn_for_last[1][i], collision_updn_for_last[2][i]])
        new_data.sort(key=lambda row: (row[2], row[1]))

        data1 = new_data.copy()

        new_data0 = [data1[i][0] for i in range(len(new_data))]
        new_data1 = [data1[i][1] for i in range(len(new_data))]
        new_data2 = [data1[i][2] for i in range(len(new_data))]
        new_data = [new_data0, new_data1, new_data2]

        collision_updn_for_last = new_data.copy()   #down end

        """for dn start"""
        collision_updn_for_last1 = [[], [], []] # Extracting first element of x and y

        k = 1 
        for i in range(len(new_dict["DN"]) // 4):
                collision_updn_for_last1[0].append(new_dict['DN'][k - 1])
                if new_dict['DN'][k + 1][0] >= 24: 
                    collision_updn_for_last1[1].append(new_dict['DN'][k + 1][0] - 24)
                else: 
                    collision_updn_for_last1[1].append(new_dict['DN'][k + 1][0])
                    
                collision_updn_for_last1[2].append(new_dict['DN'][k][0])
                k += 4

        new_data = []
        for i in range(len(collision_updn_for_last1[0])):
            new_data.append([collision_updn_for_last1[0][i], collision_updn_for_last1[1][i], collision_updn_for_last1[2][i]])
        new_data.sort(key=lambda row: (row[2], row[1]))

        data1 = new_data.copy()

        new_data0 = [data1[i][0] for i in range(len(new_data))]
        new_data1 = [data1[i][1] for i in range(len(new_data))]
        new_data2 = [data1[i][2] for i in range(len(new_data))]
        new_data = [new_data0, new_data1, new_data2]

        collision_updn_for_last1 = new_data.copy()   # down start

        return collision_updn_for_last1, collision_updn_for_last       #start, end


    def merging_up_fist_and_dn_last_element(self, collision_up, collision_dn):

        collision_merged = [[], [], []]
        for i in range(len(collision_dn)):
            collision_merged[i] = collision_up[i] + collision_dn[i]

        new_data = []
        for i in range(len(collision_merged[0])):
            new_data.append([collision_merged[0][i], collision_merged[1][i], collision_merged[2][i]])
        new_data.sort(key=lambda row: (row[2], row[1]))

        data1 = new_data.copy()

        new_data0 = [data1[i][0] for i in range(len(new_data))]
        new_data1 = [data1[i][1] for i in range(len(new_data))]
        new_data2 = [data1[i][2] for i in range(len(new_data))]
        new_data = [new_data0, new_data1, new_data2]

        collision_merged = new_data.copy()

        return collision_merged
    
    def merging_dn_fist_and_up_last_element(self, collision_up1, collision_dn1):

        collision_merged1 = [[], [], []]
        for i in range(len(collision_dn1)):
            collision_merged1[i] = collision_up1[i] + collision_dn1[i]

        new_data = []
        for i in range(len(collision_merged1[0])):
            new_data.append([collision_merged1[0][i], collision_merged1[1][i], collision_merged1[2][i]])
        new_data.sort(key=lambda row: (row[2], row[1]))

        data1 = new_data.copy()

        new_data0 = [data1[i][0] for i in range(len(new_data))]
        new_data1 = [data1[i][1] for i in range(len(new_data))]
        new_data2 = [data1[i][2] for i in range(len(new_data))]
        new_data = [new_data0, new_data1, new_data2]

        collision_merged1 = new_data.copy()

        return collision_merged1

    def add_arrow_labels(self, x, y):
        inx, iny = 0, 0   #NOTE: not necessary
        # for 0, 0
        if (0 <= x < 8 and 0 <= y <= 11 ) :
            # print("condition triggered for label")
            inx = 0;iny = 0  
        elif (24 <= x <= 32 and 0 <= y <= 11):
            # print("condition triggered for label MINUSING")
            x = x - 24
            # inx = 0;iny = 0
        # for 0, 1
        elif (8 <= x < 16 and 0 <= y <= 11) :
            # print("condition triggered for label")
            inx = 0;iny = 1
        # for 0, 2
        elif (16 <= x <= 24 and 0 <= y <= 11) :
            # print("condition triggered for label")
            inx = 0;iny = 2
        # for 1, 0
        elif (0 <= x < 8 and 11 < y <= 31) :
            # print("condition triggered for label")
            inx = 1;iny = 0
        elif (24 <= x <= 32 and 11 < y <= 31):
            # print("condition triggered for label MINUSING")
            x = x - 24
            inx = 1;iny = 0
        # for 1, 1
        elif (8 <= x < 16 and 11 < y <= 31) :
            # print("condition triggered for label")
            inx = 1;iny = 1
        # for 1, 2
        elif (16 <= x <= 24 and 11 < y <= 31) :
            # print("condition triggered for label")
            inx = 1;iny = 2
        # for 2, 0
        elif (0 <= x < 8 and 31 < y <= 45) :
            # print("condition triggered for label")
            inx = 2;iny = 0
        elif (24 <= x <= 32 and 31 < y <= 45):
            # print("condition triggered for label MINUSING")
            x = x - 24
            inx = 2;iny = 0
        # for 2, 1
        elif (8 <= x < 16 and 31 < y <= 45) :
            # print("condition triggered for label")
            inx = 2;iny = 1
        # for 2, 2
        elif (16 <= x <= 24 and 31 < y <= 45) :
            # print("condition triggered for label")
            inx = 2;iny = 2 
        return inx, iny, x, y
   

    def excel_to_pandas(self, filename):
        df_dict = pd.read_excel(filename, sheet_name=['DN', 'UP'], header=None)
        down_up = dict()
        dwn_upp = dict()
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
            wrong_stations = first_column_series.isin(self.y_axis)
            if (wrong_stations==False).any():
                wrong_stations = set(first_column_series[~wrong_stations].tolist())
                raise WrongStationError(f"The following stations in the excel sheet are wrong:{', '.join(wrong_stations)}.\nPlease use only use from the following station names: {', '.join(self.y_axis)}.")
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


    def excel_to_pandas(self, filename):
        df_dict = pd.read_excel(filename, sheet_name=['DN', 'UP'], header=None)
        down_up = dict()
        dwn_upp = dict()
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
            wrong_stations = first_column_series.isin(self.y_axis)
            if (wrong_stations==False).any():
                wrong_stations = set(first_column_series[~wrong_stations].tolist())
                raise WrongStationError(f"The following stations in the excel sheet are wrong:{', '.join(wrong_stations)}.\nPlease use only use from the following station names: {', '.join(self.y_axis)}.")
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
    
    def conversion(self, station_dict):
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

    def add_24_down_up(self, down_up):
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
    def plot(self,index_0,index_1,arr,start_sub_y_axis,end_sub_y_axis,ylim_start,ylim_end,xlim_start,xlim_end, station_dict):
        self.axes[index_0][index_1].minorticks_on()

        # xa_0 = np.linspace(0, 8, 200)
        xa_0 = np.arange(xlim_start, xlim_end, 0.03333)
        for key, arr_2d in station_dict.items():
            for i in range(0, len(arr_2d), 2):
                arr_minus = np.array(arr_2d[i+1])
                arr_minus = arr_minus - 24
                self.axes[index_0][index_1].plot(arr_minus, arr_2d[i], color='red')
                self.axes[index_0][index_1].plot(arr_2d[i+1], arr_2d[i], color='red')

        for i in range(len(self.y_axis)):
            y_index = self.y_axis[i]
            ya = [y_index] * len(xa_0)
            self.axes[index_0][index_1].scatter(xa_0, ya, marker=',',color='blue', s=0.3)


        self.axes[index_0][index_1].xaxis.grid(True, which='major', linestyle='-', color='black')
        self.axes[index_0][index_1].xaxis.grid(True, which='minor', linestyle='-')
        self.axes[index_0][index_1].xaxis.set_minor_locator(MultipleLocator(10 / 60))
        self.axes[index_0][index_1].set_xticks(arr)
        self.axes[index_0][index_1].set_xticklabels(arr)
        sub_y_axis = self.y_labes[start_sub_y_axis:end_sub_y_axis]
        # sub_y_axis = Reverse(sub_y_axis)
        # print(sub_y_axis)
        self.axes[index_0][index_1].set_ylim(start_sub_y_axis,end_sub_y_axis)
        # print(start_sub_y_axis,end_sub_y_axis)
        # print(range(start_sub_y_axis,end_sub_y_axis))
        # self.axes[index_0][index_1].set_yticks(range(start_sub_y_axis,end_sub_y_axis))
        self.axes[index_0][index_1].set_yticks(range(start_sub_y_axis,end_sub_y_axis))
        self.axes[index_0][index_1].set_yticklabels(sub_y_axis)


        self.axes[index_0][index_1].tick_params(axis='x', which='minor', labelbottom=True)
        self.axes[index_0][index_1].tick_params(labeltop=True, labelright=True)
        minor_labels = ["10", "20", "30", "40", "50"] * 8
        minor_labels.insert(0, "")

        formatter = FixedFormatter(minor_labels)
        self.axes[index_0][index_1].xaxis.set_minor_formatter(formatter)
        self.axes[index_0][index_1].tick_params(axis='x', which='minor', labelsize=6)
        self.axes[index_0][index_1].set_xlim(xlim_start,xlim_end)  
        self.axes[index_0][index_1].invert_yaxis()

    def plot_trains(self, station_dict, trains_dict):
        self.axes = self.figure.subplots(nrows=3, ncols=3)
        # have to make  3 x 3 grid
        # set width of each subplot as 8
        for key, arr_2d in station_dict.items():
            for i in range(0, len(arr_2d), 2):
                for j in range(len(arr_2d[i])):
                    arr_2d[i][j] = self.y_axis.index(arr_2d[i][j])
        dup_train_dict = copy.deepcopy(trains_dict)

    ######################################################################################################    
        arr1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        arr2 = [8, 9, 10, 11, 12, 13, 14, 15, 16]
        arr3 = [16, 17, 18, 19, 20, 21, 22, 23, 24]
        
    #   (index_0, index_1, arr, start_sub_y_axis, end_sub_y_axis, ylim_start, ylim_end, xlim_start, xlim_end)
        self.plot(0,0,arr1,0,11,      0,15,        0,8, station_dict)
        self.plot(1,0,arr1,10,31,    0,19,        0,8, station_dict)   
        self.plot(2,0,arr1,30,45,    0,19,        0,8, station_dict) 

        self.plot(0,1,arr2,0,11,     0,15,        8,16,  station_dict)
        self.plot(1,1,arr2,10,31,  0,19,        8,16,  station_dict)   
        self.plot(2,1,arr2,30,45,   0,19,        8,16,  station_dict)

        self.plot(0,2,arr3,0,11,     0,15,       16,24,  station_dict)
        self.plot(1,2,arr3,10,31,   0,19,       16,24,  station_dict)   
        self.plot(2,2,arr3,30,45,   0,19,       16,24,  station_dict)

        def plot_labels():
            new_dict = copy.deepcopy(station_dict)
    
            """ Called a func"""
            new_dict = self.add_lables(new_dict, trains_dict)
            
            """ Called a func"""
            new_dict = self.add_keys(new_dict)
            
            new_dict['UPDN'] = new_dict['UP'] + new_dict['DN']

            """ Called a func"""
            # collision_updn = [[], [], []]
            collision_up, collision_up1 = self.extract_up_elem(new_dict)

            """ Called a func"""        
            collision_dn, collision_dn1 = self.extract_dn_elem(new_dict)

            """ Called a func"""
            collision_merged = self.merging_up_fist_and_dn_last_element(collision_up, collision_dn1)

            """ Called a func"""        
            collision_merged1 = self.merging_dn_fist_and_up_last_element(collision_dn, collision_up1)

        ########################################## collision text for up and down #################################################\
            # intersection(station_dict, axes, trains_dict)
            def collision_text_updn(collision_merged):   
                """ this function takes cares in overlapping of labels"""

                """ Variables Declaration"""
                k = 1
                last_y = 0

                previous_x, previous_y= 0, 0
                label_var = ''
                y_overlap_both_up = 0
                y_buffer_both_up = 0
                # original_x = 0

                for i in range(len(collision_merged[0])):
                    
                    label_ = collision_merged[0][i]
                    x = collision_merged[1][i]
                    y = collision_merged[2][i]

                    range_of_x = x + 0.12            # 0.7 is x size of labels
                    range_of_y = y + 0.9

                    if abs(x - previous_x) <= 0.03 and y == previous_y:
                        # print('label is overlapping')
                        label_var = '/'
                        len_of_labels = len(label_)
                        y_buffer_both_up = y_buffer_both_up + (0.06 * len_of_labels) + 1.4
                        """y_overlap_both_up is y axis for text which is different in arrows y axis that is original 'y' """
                        y_overlap_both_up = y + y_buffer_both_up 
                    else:
                        # print('label is NOT overlapping')
                        label_var = ''
                        y_buffer_both_up = 0
                        y_overlap_both_up = y + y_buffer_both_up                         

                    # label = new_dict['UPDN'][k - 1] + label_var
                    label = label_ + label_var

                    # original_x = x
                    inx, iny, x, y = self.add_arrow_labels(x, y)
                    self.axes[inx][iny].text(x - 0.02, y_overlap_both_up + 1.9, label, rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
                    self.axes[inx][iny].arrow(x, y, 0, 0.5, width = 0.005, clip_on = False)
                    previous_x, previous_y = x, y
                    k += 3
            def collision_text_updn1(collision_merged1):
                """ this function takes cares in overlapping of labels"""
                """ Variables Declaration"""
                k = 1

                previous_x, previous_y= 0, 0
                label_var = ''
                y_overlap_both_up = 0
                y_buffer_both_up = 0
                # original_x = 0

                for i in range(len(collision_merged1[0])):
                    
                    label_ = collision_merged1[0][i]
                    x = collision_merged1[1][i]
                    y = collision_merged1[2][i]

                    # print(previous_x, x, previous_y, y)
                    if abs(x - previous_x) <= 0.03 and y == previous_y:
                        # print('label is overlapping')
                        label_var = '/'
                        len_of_labels = len(label_)
                        y_buffer_both_up = y_buffer_both_up + (0.045 * len_of_labels) + 1
                        """y_overlap_both_up is y axis for text which is different in arrows y axis that is original 'y' """
                        y_overlap_both_up = y - y_buffer_both_up 
                    else:
                        # print('label is NOT overlapping')
                        label_var = ''
                        y_buffer_both_up = 0
                        y_overlap_both_up = y - y_buffer_both_up                         

                    # label = new_dict['UPDN'][k - 1] + label_var
                    label = label_var + label_

                    # original_x = x
                    inx, iny, x, y = self.add_arrow_labels(x, y)
                    self.axes[inx][iny].text(x - 0.02, y_overlap_both_up - 0.6, label, rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
                    self.axes[inx][iny].arrow(x, y, 0, - 0.5, width = 0.005, clip_on = False)

                    previous_x, previous_y = x, y


                    ###############################################################################
                    k += 3
            collision_text_updn(collision_merged)  
            collision_text_updn1(collision_merged1)
        plot_labels()
        self.canvas.draw()
        

    def load_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
        if file_name:
            try:
                down_up, dwn_upp =  self.excel_to_pandas(file_name)
                down_up = self.conversion(down_up)
                down_up = self.add_24_down_up(down_up)            
                self.figure.clear()
                self.plot_trains(down_up, dwn_upp)
                self.export_button.setEnabled(True)
            except DuplicateTrainError as e:
                QMessageBox.critical(self, "Error", str(e))
            except WrongStationError as e:
                QMessageBox.critical(self, "Error", str(e))

    def export_plot(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Plot as PDF", "", "PDF Files (*.pdf)")
        if file_name:
            num_rows, num_cols = self.axes.shape
            extent = [self.axes[i, j].get_tightbbox().transformed(self.figure.dpi_scale_trans.inverted()) for i in range(num_rows) for j in range(num_cols)]
            with PdfPages(file_name) as pdf:
                for bbox in extent:
                    pdf.savefig(self.figure, bbox_inches=bbox, pad_inches=1)
                    print("page saved \n")
# def set_global_font():
#     font = QFont()
#     font.setPointSize(40)  # Set the desired font size
#     QtWidgets.QApplication.setFont(font)
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    # set_global_font()
    apply_stylesheet(app, theme='dark_blue.xml')
        #              , extra={
        #     "QMessageBox": {
        #         "setStyleSheet": """
        #         QMessageBox QLabel {
        #             font-size: 140px;
        #         }
        #         """
        #     }
        # })
    window = PlotWindow()
    window.show()
    app.exec_()