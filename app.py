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

from preprocessing import excel_to_pandas, select, conversion, add_24_down_up
from labels import *
from plotted import plotted_
class DuplicateTrainError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class WrongStationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class PlotWindow(QtWidgets.QWidget, plotted_):
    def __init__(self, parent=None):
        super().__init__(parent)
        # main functions
        # preprocessing
        self.excel_to_pandas = excel_to_pandas
        self.select = select
        self.conversion = conversion
        self.add_24_down_up = add_24_down_up
        self.add_arrow_labels = add_arrow_labels
        self.exact_current_axes = extract_current_axes
        self.merging_dn_fist_and_up_last_element = merging_dn_fist_and_up_last_element
        self.merging_up_fist_and_dn_last_element = merging_up_fist_and_dn_last_element
        self.extract_dn_elem= extract_dn_elem
        self.extract_up_elem = extract_up_elem
        self.add_keys= add_keys
        self.add_lables = add_lables

        # labels
        self.figure = Figure(figsize=(10, 50), tight_layout=True)
        self.y_axis = ["CCG","BCT","DDR","BA","BDTS","ADH","BVI","BYR","BSR","NSP","VR","VTN","SAH","KLV","PLG","UOI","BOR","VGN","DRD","GVD","BRRD","UBR","SJN","BLD","KEB","VAPI","BAGD","UVD","PAD","ATUL","BL","DGI","JRS","BIM","AML","ACL","VDH","HXR","GNST","NVS","MRL","SCH","BHET","UDN","ST"]
        self.y_labes = ["CCG 0.0","BCT 14.66","DDR 10.17","BA 14.66","BDTS 15.29","ADH 29.32","BVI 33.98","BYR 43.11","BSR 51.78","NSP 55.85","VR 59.98","VTN 68.42","SAH 76.74","KLV 82.55","PLG 90.92","UOI 97.15","BOR 102.8","VGN 111.5","DRD 123.7","GVD 134.8","BRRD 139.0","UBR 144.0","SJN 149.4","BLD 160.9","KEB 165.8","VAPI 172.0","BAGD 179.0","UVD 182.0","PAD 187.7","ATUL 191.0","BL 198.22","DGI 207.21","JRS 212.28","BIM 216.41","AML 221.72","ACL 225.33","VDH 228.87","HXR 232.0","GNST 234.0","NVS 237.33","MRL 245.63","SCH 252.26","BHET 257.3","UDN 262.77","ST 266.78"]    # print(down_up)
        
        self.setWindowTitle("Matplotlib Plot")
        
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

        pl = plotted_(self.figure,self.y_axis,self.y_labes, self.canvas, self.layout,self.export_button,self.axes, self.scroll_area, self.toolbar)
        self.plot_trains = pl.plot_trains



# new = select(down_up)
# down_up = conversion(new)
# down_up = add_24_down_up(down_up)
# plot_trains(down_up, y_axis, y_labes, dwn_upp)    

    def load_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
        if file_name:
            # n = new()
            try:
                select_flag =  False
                
                down_up, dwn_upp =  self.excel_to_pandas(file_name)
                # print("dwn_upp",dwn_upp)
                if select_flag:                    
                    down_up, dwn_upp = self.select(down_up, dwn_upp)
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
