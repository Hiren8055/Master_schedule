from PySide2 import QtWidgets
from PySide2.QtWidgets import QScrollArea
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
from qt_material import apply_stylesheet
import pandas as pd
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedFormatter


class PlotWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Matplotlib Plot")
        
        self.figure = Figure(figsize=(10, 50))
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
        self.canvas.setMinimumSize(1000, 4000)
        self.canvas.setMinimumSize(1001, 4001)
    def excel_to_pandas(self, filename):
        df_dict = pd.read_excel(filename, sheet_name=['DN', 'UP'])
        down_up = dict()
        for key, df in df_dict.items():
            df = df.iloc[2:]
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
            list_2d = []
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
                column_df = column_df[column_df.astype(str).str.contains(r'\d', na=False)]
                column_df = pd.DataFrame(column_df)
                row_indices = column_df.index.tolist()
                datapoints = column_df.iloc[:, 0].tolist()

                # Create the 2-dimensional list
                list_2d = list_2d + [row_indices, datapoints]
            down_up[key] = list_2d
            down_up[key + key] = df.index

        y_axis = list(dict.fromkeys(down_up['DNDN'].values.tolist()))
        down_up.pop("DNDN")
        down_up.pop("UPUP")
        return down_up,y_axis
    def conversion(self, station_dict):
    # this wil multiply with ratios for plotting
        for key, value in station_dict.items():
            for i in range(len(value)):
                if i % 2 == 1:  # Check if it's an alternative column
                    for j in range(len(value[i])):
                        time_string = value[i][j]
                        hours, minutes, seconds = map(int, time_string.split(':'))

                        # Convert hours, minutes, and seconds to a decimal representation of hours
                        time_in_hours = hours + (minutes / 60) + (seconds / 3600)

                        # after_decimal = time_in_hours % 1
                        # rescaled_value = after_decimal * 3/5

                        # time_in_hours = int(time_in_hours) + rescaled_value

                        # Update the value in the dictionary
                        value[i][j] = str(round(time_in_hours, 2))

                    value[i] = [float(num) for num in value[i]]   
        return station_dict
    def add_24_down_up(self, down_up):
        arr_2= down_up['DN']
        for hi in range(1, len(arr_2),2):
            arr_2[hi] = [x + 24 if x < 1 else x for x in arr_2[hi]]
        down_up['DN'] = arr_2
        arr_2 = down_up['UP']
        # Add 24 to each element  the arrayin
        for h in range(1, len(arr_2),2):
            arr_2[h] = [x + 24 if x < 23 else x for x in arr_2[h]]
        down_up['UP'] = arr_2
        return down_up
    def plot_trains(self,station_dict, y_axis):
        axes = self.figure.subplots(nrows=4, ncols=1)
        for key, arr_2d in station_dict.items():
            for i in range(0, len(arr_2d), 2):
                for j in range(len(arr_2d[i])):
                    arr_2d[i][j] = y_axis.index(arr_2d[i][j])
        # Subplot 1: 0-8
        axes[0].minorticks_on()
        xa_0 = np.linspace(0, 8, 240)
        for key, arr_2d in station_dict.items():
            for i in range(0, len(arr_2d), 2):
                axes[0].plot(arr_2d[i+1], arr_2d[i], color='red')
        for i in range(len(y_axis)):
            y_index = y_axis[i]
            ya = [y_index] * len(xa_0)
            axes[0].plot(xa_0, ya, color='blue', linewidth=1, linestyle=(10, (1, 1.328)))
        axes[0].xaxis.grid(True, which='major', linestyle='-', color='black')
        axes[0].xaxis.grid(True, which='minor', linestyle='-')
        axes[0].xaxis.set_minor_locator(MultipleLocator(10 / 60))
        axes[0].set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8])
        axes[0].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
        axes[0].set_yticks(range(len(y_axis)))
        axes[0].set_yticklabels(y_axis)
        axes[0].tick_params(axis='x', which='minor', labelbottom=True)
        axes[0].tick_params(labeltop=True, labelright=True)
        minor_labels = ["10", "20", "30", "40", "50"] * 8
        minor_labels.insert(0, "")
        formatter = FixedFormatter(minor_labels)
        axes[0].xaxis.set_minor_formatter(formatter)
        axes[0].tick_params(axis='x', which='minor', labelsize=6)
        axes[0].set_xlim(0, 8)
        axes[0].set_ylim(0, len(y_axis))

        # Subplot 2: 8-16
        axes[1].minorticks_on()
        xa_1 = np.linspace(8, 16, 240)
        for key, arr_2d in station_dict.items():
            for i in range(0, len(arr_2d), 2):
                axes[1].plot(arr_2d[i+1], arr_2d[i], color='red')
        for i in range(len(y_axis)):
            y_index = y_axis[i]
            ya = [y_index] * len(xa_1)
            axes[1].plot(xa_1, ya, color='blue', linewidth=1, linestyle=(10, (1, 1.328)))
        axes[1].xaxis.grid(True, which='major', linestyle='-', color='black')
        axes[1].xaxis.grid(True, which='minor', linestyle='-')
        axes[1].xaxis.set_minor_locator(MultipleLocator(10 / 60))
        axes[1].set_xticks([8, 9, 10, 11, 12, 13, 14, 15, 16])
        axes[1].set_xticklabels([8, 9, 10, 11, 12, 13, 14, 15, 16])
        axes[1].set_yticks(range(len(y_axis)))
        axes[1].set_yticklabels(y_axis)
        axes[1].tick_params(axis='x', which='minor', labelbottom=True)
        axes[1].tick_params(labeltop=True, labelright=True)
        minor_labels = ["10", "20", "30", "40", "50"] * 8
        minor_labels.insert(0, "")
        formatter = FixedFormatter(minor_labels)
        axes[1].xaxis.set_minor_formatter(formatter)
        axes[1].tick_params(axis='x', which='minor', labelsize=6)
        axes[1].set_xlim(8, 16)
        axes[1].set_ylim(0, len(y_axis))

        # Subplot 3: 16-24
        axes[2].minorticks_on()
        xa_2 = np.linspace(16, 24, 240)
        for key, arr_2d in station_dict.items():
            for i in range(0, len(arr_2d), 2):
                axes[2].plot(arr_2d[i+1], arr_2d[i], color='red')
        for i in range(len(y_axis)):
            y_index = y_axis[i]
            ya = [y_index] * len(xa_2)
            axes[2].plot(xa_2, ya, color='blue', linewidth=1, linestyle=(10, (1, 1.328)))
        axes[2].xaxis.grid(True, which='major', linestyle='-', color='black')
        axes[2].xaxis.grid(True, which='minor', linestyle='-')
        axes[2].xaxis.set_minor_locator(MultipleLocator(10 / 60))
        axes[2].set_xticks([16, 17, 18, 19, 20, 21, 22, 23, 24])
        axes[2].set_xticklabels([16, 17, 18, 19, 20, 21, 22, 23, 24])
        axes[2].set_yticks(range(len(y_axis)))
        axes[2].set_yticklabels(y_axis)
        axes[2].tick_params(axis='x', which='minor', labelbottom=True)
        axes[2].tick_params(labeltop=True, labelright=True)
        minor_labels = ["10", "20", "30", "40", "50"] * 8
        minor_labels.insert(0, "")
        formatter = FixedFormatter(minor_labels)
        axes[2].xaxis.set_minor_formatter(formatter)
        axes[2].tick_params(axis='x', which='minor', labelsize=6)
        axes[2].set_xlim(16, 24)
        axes[2].set_ylim(0, len(y_axis))
        
        # Subplot 3: 16-24
        axes[3].minorticks_on()
        xa_3 = np.linspace(24, 32, 240)
        for key, arr_2d in station_dict.items():
            for i in range(0, len(arr_2d), 2):
                axes[3].plot(arr_2d[i+1], arr_2d[i], color='red')
        for i in range(len(y_axis)):
            y_index = y_axis[i]
            ya = [y_index] * len(xa_3)
            axes[3].plot(xa_3, ya, color='blue', linewidth=1, linestyle=(10, (1, 1.328)))
        axes[3].xaxis.grid(True, which='major', linestyle='-', color='black')
        axes[3].xaxis.grid(True, which='minor', linestyle='-')
        axes[3].xaxis.set_minor_locator(MultipleLocator(10 / 60))
        axes[3].set_xticks([24,25,26,27,28,29,30,31,32])
        axes[3].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
        axes[3].set_yticks(range(len(y_axis)))
        axes[3].set_yticklabels(y_axis)
        axes[3].tick_params(axis='x', which='minor', labelbottom=True)
        axes[3].tick_params(labeltop=True, labelright=True)
        minor_labels = ["10", "20", "30", "40", "50"] * 8
        minor_labels.insert(0, "")
        formatter = FixedFormatter(minor_labels)
        axes[3].xaxis.set_minor_formatter(formatter)
        axes[3].tick_params(axis='x', which='minor', labelsize=6)
        axes[3].set_xlim(24, 32)
        axes[3].set_ylim(0, len(y_axis))
        
        plt.tight_layout()
        self.canvas.draw()

    #     for me, ax in enumerate(axes):
    #         ax.set_title(f"Subplot {me+1}")
    #         # Save each subplot as a separate PDF
    #         plt.savefig(f"subplot_{me+1}.pdf")
        # plt.savefig("myImagePDF.pdf", format="pdf")
        # plt.show()

    def load_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
        if file_name:
            # data = pd.read_excel(file_name)
            down_up, y_labes =  self.excel_to_pandas(file_name)
            down_up = self.conversion(down_up)
            down_up = self.add_24_down_up(down_up)
            # x = data["x"]
            # y = data["y"]             
            self.figure.clear()
            self.plot_trains(down_up, y_labes)
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
    # apply_stylesheet(app, theme='dark_blue.xml')
    window.show()
    app.exec_()