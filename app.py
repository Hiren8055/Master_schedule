from PySide2 import QtWidgets
from PySide2.QtWidgets import QScrollArea
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import Bbox, TransformedBbox
from qt_material import apply_stylesheet
import pandas as pd
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedFormatter


class PlotWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Matplotlib Plot")
        
        self.figure = Figure(figsize=(10, 50))
        # self.figure.set_dpi(100)

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.canvas)
        
        self.button = QtWidgets.QPushButton("Load Excel File")
        self.button.clicked.connect(self.load_file)
        
        self.export_button = QtWidgets.QPushButton("Export Plot as PDF")
        self.export_button.clicked.connect(self.export_plot)
        self.export_button.setEnabled(False)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.export_button)
        self.canvas.setMinimumSize(2000, 8000)
        self.canvas.setMaximumSize(2001, 8001)
        
    def excel_to_pandas(self, filename):
        df_dict = pd.read_excel(filename, sheet_name=['DN', 'UP'], header=None)
        down_up = dict()
        dwn_upp = dict()
        for key, df in df_dict.items():
            first_filled_row_index = df.first_valid_index() #gives index of first non-empty row.
            last_filled_row_index = df.last_valid_index() #gives index of last non-empty row. 
            df = df.loc[first_filled_row_index:last_filled_row_index] #removes starting and ending empty rows
            df = df[2:] #remove unnecessary top and bottom rows
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
                column_df = column_df.str.replace('\d+\-\d+\-\d+', '')

    #             column_df = column_df.dropna()
    #             mask = column_df.str.contains(r'\.+')
    #             column_df[mask] = np.nan
                column_df = column_df.dropna()
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
            dwn_upp[key] = trains_list
        y_axis = ["CCG","BCT","DDR","BA","BDTS","ADH","BVI","BYR","BSR","NSP","VR","VTN","SAH","KLV","PLG","UOI","BOR","VGN","DRD","GVD","BRRD","UBR","SJN","BLD","KEB","VAPI","BAGD","UVD","PAD","ATUL","BL","DGI","JRS","BIM","AML","ACL","VDH","HXR","GNST","NVS","MRL","SCH","BHET","UDN","ST"]
        y_labes = ["CCG 0.0","BCT 14.66","DDR 10.17","BA 14.66","BDTS 15.29","ADH 29.32","BVI 33.98","BYR 43.11","BSR 51.78","NSP 55.85","VR 59.98","VTN 68.42","SAH 76.74","KLV 82.55","PLG 90.92","UOI 97.15","BOR 102.8","VGN 111.5","DRD 123.7","GVD 134.8","BRRD 139.0","UBR 144.0","SJN 149.4","BLD 160.9","KEB 165.8","VAPI 172.0","BAGD 179.0","UVD 182.0","PAD 187.7","ATUL 191.0","BL 198.22","DGI 207.21","JRS 212.28","BIM 216.41","AML 221.72","ACL 225.33","VDH 228.87","HXR 232.0","GNST 234.0","NVS 237.33","MRL 245.63","SCH 252.26","BHET 257.3","UDN 262.77","ST 266.78"]    # print(down_up)
        return down_up,y_axis, y_labes, dwn_upp
    
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
    
    def plot_trains(self,station_dict, y_axis, y_labes, trains_dict):
        axes = self.figure.subplots(nrows=9, ncols=1) #
        for key, arr_2d in station_dict.items():
            for i in range(0, len(arr_2d), 2):
                for j in range(len(arr_2d[i])):
                    arr_2d[i][j] = y_axis.index(arr_2d[i][j])
                    
        xa_0 = np.arange(0, 8, 0.03333)
        
        for i in range(len(y_axis)):
                y_index = y_axis[i]
                ya = [y_index] * len(xa_0)
                axes[8].scatter(xa_0, ya, marker=',',color='blue', s=10,snap=True)
        def plot(index,arr,start_sub_y_axis,end_sub_y_axis,ylim_start,ylim_end,xlim_start,xlim_end):
            # print(index)
            axes[index].minorticks_on()

            # ##print('station_dict : ', station_dict)
            # xa_0 = np.linspace(0, 8, 200)
            xa_0 = np.arange(xlim_start, xlim_end, 0.03333)
            for key, arr_2d in station_dict.items():
                # print("arr_2d",arr_2d)
                for i in range(0, len(arr_2d), 2):
                    arr_minus = np.array(arr_2d[i+1]) - 24  
                    axes[index].plot(arr_minus, arr_2d[i], color='red')
                    axes[index].plot(arr_2d[i+1], arr_2d[i], color='red')
            print("index", index)
            print("index", y_axis)
            for i in range(len(y_axis)):
                y_index = y_axis[i]
                ya = [y_index] * len(xa_0)
                axes[index].scatter(xa_0, ya, marker=',',color='blue', s=10,snap=True)
            axes[index].xaxis.grid(True, which='major', linestyle='-', color='black')
            axes[index].xaxis.grid(True, which='minor', linestyle='-')
            axes[index].xaxis.set_minor_locator(MultipleLocator(10 / 60))
            axes[index].set_xticks(arr)
            axes[index].set_xticklabels(arr)
            sub_y_axis = y_labes[start_sub_y_axis:end_sub_y_axis]
            # sub_y_axis = Reverse(sub_y_axis)
            # print(sub_y_axis)
            axes[index].set_ylim(start_sub_y_axis,end_sub_y_axis)
            # print(start_sub_y_axis,end_sub_y_axis)
            # print(range(start_sub_y_axis,end_sub_y_axis))
            # axes[index_0][index_1].set_yticks(range(start_sub_y_axis,end_sub_y_axis))
            axes[index].set_yticks(range(start_sub_y_axis,end_sub_y_axis))
            axes[index].set_yticklabels(sub_y_axis)


            axes[index].tick_params(axis='x', which='minor', labelbottom=True)
            axes[index].tick_params(labeltop=True, labelright=True)
            minor_labels = ["10", "20", "30", "40", "50"] * 8
            minor_labels.insert(0, "")

            formatter = FixedFormatter(minor_labels)
            axes[index].xaxis.set_minor_formatter(formatter)
            axes[index].tick_params(axis='x', which='minor', labelsize=6)
            axes[index].set_xlim(xlim_start,xlim_end)  
            axes[index].invert_yaxis()
            # bbox = axes[index].get_position()
            # axes[index].set_position([bbox.x0, bbox.y0*2, bbox.width*3, bbox.height*2])
            # scaled_bbox = Bbox.from_bounds(original_bbox.x0, original_bbox.y0, original_bbox.width * 2, original_bbox.height * 7)
            # trans_bbox = TransformedBbox(scaled_bbox, axes[index].transData)



        arr1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        arr2 = [8, 9, 10, 11, 12, 13, 14, 15, 16]
        arr3 = [16, 17, 18, 19, 20, 21, 22, 23, 24]
        
    #   (index_0,index_1,arr,start_sub_y_axis,end_sub_y_axis,ylim_start,ylim_end,xlim_start,xlim_end)
        plot(0,arr1,0,11,      0,15,        0,8)
        plot(1,arr1,10,31,    0,19,        0,8)   
        plot(2,arr1,30,45,    0,19,        0,8) 
        plot(3,arr2,0,11,     0,15,        8,16)
        plot(4,arr2,10,31,  0,19,        8,16)   
        plot(5,arr2,30,45,   0,19,        8,16)
        plot(6,arr3,0,11,     0,15,       16,24)
        plot(7,arr3,10,31,   0,19,       16,24)   
        plot(8,arr3,30,45,   0,19,       16,24)
        
        xa_0 = np.arange(0, 8, 0.03333)

        for i in range(len(y_axis)):
                y_index = y_axis[i]
                ya = [y_index] * len(xa_0)
                axes[8].scatter(xa_0, ya, marker=',',color='blue', s=0.6)

        plt.tight_layout()
        self.canvas.draw()

    def load_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
        if file_name:
            # data = pd.read_excel(file_name)
            down_up, y_axis, y_labes,  dwn_upp =  self.excel_to_pandas(file_name)
            down_up = self.conversion(down_up)
            down_up = self.add_24_down_up(down_up)
            # x = data["x"]
            # y = data["y"]             
            self.figure.clear()
            self.plot_trains(down_up, y_axis, y_labes, dwn_upp)
            # ax = self.figure.add_subplot(111)
            # ax.plot(x, y, "r-")
            # ax.set_xlabel("x")
            # ax.set_ylabel("y")
            # ax.set_title("Line Plot from Excel File")
            self.export_button.setEnabled(True)

    def export_plot(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Plot as PDF", "", "PDF Files (*.pdf)")
        if file_name:
            self.figure.savefig(file_name)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = PlotWindow()
    apply_stylesheet(app, theme='dark_blue.xml')
    window.show()
    app.exec_()

    def load_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
        if file_name:
            # data = pd.read_excel(file_name)
            down_up, y_axis,y_labes, dwn_upp =  self.excel_to_pandas(file_name)
            down_up = self.conversion(down_up)
            down_up = self.add_24_down_up(down_up)
            # x = data["x"]
            # y = data["y"]             
            self.figure.clear()
            self.plot_trains(down_up, y_axis, y_labes, dwn_upp)
            # ax = self.figure.add_subplot(111)
            # ax.plot(x, y, "r-")
            # ax.set_xlabel("x")
            # ax.set_ylabel("y")
            # ax.set_title("Line Plot from Excel File")
            self.export_button.setEnabled(True)

    def export_plot(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Plot as PDF", "", "PDF Files (*.pdf)")
        if file_name:
            self.figure.savefig(file_name)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = PlotWindow()
    apply_stylesheet(app, theme='dark_blue.xml')
    window.show()
    app.exec_()
