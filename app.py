from PySide2 import QtWidgets
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QScrollArea, QMessageBox, QApplication, QProgressBar,QLineEdit,QLabel
from PySide2.QtCore import QObject, QThread, Signal, QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.transforms import Bbox, TransformedBbox
from qt_material import apply_stylesheet
from collections import Counter
from blit_manager import BlitManager
from preprocessing import excel_to_pandas, select, conversion, conversion_box, box_add_24, add_24_down_up, DuplicateTrainError, WrongStationError, SameLengthError, EmptyListError, WrongTimeFormatError
from labels import *
from plotted import plotted_
from matplotlib.text import Text
from Draggable import dragged
import pprint
pp = pprint.PrettyPrinter(indent=0.1)

global dragger

class CustomNavToolbar(NavigationToolbar):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.zoomed_in = False
        self.dragger = None
    def set_dragger(self):
        self.dragger = dragger
    def zoom(self, *args, **kwargs):
        self.set_dragger()
        self.dragger.bm.on_zoom()
        super().zoom(self, *args, **kwargs)
        self.zoomed_in = True
        self.dragger.bm.adjust_subplots()
        global dragger
        dragger = self.dragger
    def home(self, *args, **kwargs):
        self.set_dragger()
        if self.zoomed_in is True:
            self.dragger.bm.on_home(self.zoomed_in)
            self.zoomed_in = False
            super().home(self, *args, **kwargs)
            self.dragger.bm.adjust_subplots()
            global dragger
            dragger = self.dragger
        else:
            super().home(self, *args, **kwargs)
            
        super().home(self, *args, **kwargs)
        self.dragger.bm.adjust_subplots()
class ExportWorker(QObject):
    update_signal = Signal(int)
    # new_fig = Figure(figsize=(10, 50))
    def __init__(self, file_name, canvas):
        super().__init__()
        self.file_name = file_name
        self.canvas = canvas
        self.figure = canvas.figure
        print("Worker initialize")
    def run(self):
        print("I am running")
        try:
            axes = self.figure.axes
            extent = [ax.get_tightbbox().transformed(self.figure.dpi_scale_trans.inverted()) for ax in axes]
            # print(extent)
            extent = [Bbox([[b.x0-0.3,b.y0-0.6],[b.x1+0.3,b.y1+0.7]]) for b in extent]
            xmin,xmax = extent[0].x0,extent[0].x1
            extent[3] = Bbox([[xmin, extent[3].y0],[xmax,extent[3].y1]])
            # print(extent)
            print("Lets make a pdf")
            with PdfPages(self.file_name) as pdf:
                print("3 2 1 Gooo!!")
                for i, bbox in zip(range(12,101,11),extent):
                    print(f"i:{i}, bbox:{bbox}")
                    pdf.savefig(self.figure, bbox_inches=bbox, pad_inches=1)
                    self.update_signal.emit(i)
        except Exception as e:
                print(f"Error raised: {e}")


class PlotWindow(QtWidgets.QWidget):
    excel_to_pandas = excel_to_pandas
    def __init__(self):
        super().__init__()
        self.select = select
        self.timer = QTimer(self)
        self.conversion = conversion
        self.conversion_box = conversion_box
        self.add_24_down_up = add_24_down_up
        self.box_add_24 = box_add_24
        self.add_arrow_labels = add_arrow_labels
        self.merge_elements = merge_elements
        self.extract_dn_elem= extract_dn_elem
        self.extract_up_elem = extract_up_elem
        self.add_keys= add_keys
        self.add_lables = add_lables
        self.figure = Figure(figsize=(10, 50))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = CustomNavToolbar(self.canvas)
        self.y_axis = ["CCG","MEL","CYR","GTR","BCT","MX","PL","PBHD","DDR","MRU","MM","BA","BDTS","KHAR","STC","VLP","ADH","JOS","RMAR","GMN","MDD","KILE","BVI","DIC",'MIRA',"BYR","NIG","BSR","NSP","VR","VTN","SAH","KLV","PLG","UOI","BOR","VGN","DRD","GVD","BRRD","UBR","SJN","BLD","KEB","VAPI","BAGD","UVD","PAD","ATUL","BL","DGI","JRS","BIM","AML","ACL","VDH","HXR","GNST","NVS","MRL","SCH","BHET","UDN","ST"]
        self.y_labes = ["CCG 0.0","MEL 1.30","CYR 2.21","GTR 3.59","BCT 4.48","MX 5.95","PL 7.67","PBHD 8.89","DDR 10.17","MRU 11.75","MM 12.93","BA 14.66","BDTS 15.29","KHAR 16.29","STC 17.61","VLP 19.67","ADH 21.83","JOS 23.52","RMAR 25.37","GMN 26.9","MDD 29.32","KILE 31.22","BVI 33.98","DIC 36.34",'MIRA 39.76',"BYR 43.11","NIG 47.79","BSR 51.78","NSP 55.85","VR 59.98","VTN 68.42","SAH 76.74","KLV 82.55","PLG 90.92","UOI 97.15","BOR 102.8","VGN 111.5","DRD 123.7","GVD 134.8","BRRD 139.0","UBR 144.0","SJN 149.4","BLD 160.9","KEB 165.8","VAPI 172.0","BAGD 179.0","UVD 182.0","PAD 187.7","ATUL 191.0","BL 198.22","DGI 207.21","JRS 212.28","BIM 216.41","AML 221.72","ACL 225.33","VDH 228.87","HXR 232.0","GNST 234.0","NVS 237.33","MRL 245.63","SCH 252.26","BHET 257.3","UDN 262.77","ST 266.78"]    # print(down_up)        self.setWindowTitle("Matplotlib Plot")
        self.new_canvas = None
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.canvas)
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        self.button = QtWidgets.QPushButton("Load Excel File")
        self.button.clicked.connect(self.load_file)
        self.axes = None
        self.export_button = QtWidgets.QPushButton("Export Plot as PDF")
        self.export_button.clicked.connect(self.export_plot)
        self.export_button.setEnabled(False)
        self.layout = QtWidgets.QGridLayout(self)
        self.remarks_label= QLabel()
        self.days_label = QLabel()
        self.remarks_label.setText("Remarks")
        self.days_label.setText("Days")
        self.remark_textbox = QLineEdit(self)
        self.days_textbox = QLineEdit(self)
        self.layout.addWidget(self.toolbar,0,0,1,2)
        self.layout.addWidget(self.progress_bar,1,0,1,2)
        self.layout.addWidget(self.scroll_area,2,0,1,2)
        self.layout.addWidget(self.remarks_label,3,0)
        self.layout.addWidget(self.remark_textbox,4,0)
        self.layout.addWidget(self.days_label,3,1)
        self.layout.addWidget(self.days_textbox,4,1)
        self.layout.addWidget(self.button,5,0)  
        self.layout.addWidget(self.export_button,5,1)
        self.canvas.setMinimumSize(5800, 5000)
        self.canvas.setMaximumSize(5801, 5001)
        self.bm = None
        self.artist_list = []
        self.dragged_axes = None
        self.loaded = False
        self.blit = True
        self.arr_drag_dict = None

    def load_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
        if file_name:
            try:
                if self.loaded is True:
                    self.bm.stop_work()
                    self.bm = None
                    self.scroll_area.hide()
                    self.toolbar.hide()
                    self.layout.removeWidget(self.toolbar)
                    self.toolbar.deleteLater()
                    self.toolbar = None
                    self.layout.removeWidget(self.scroll_area)
                    self.scroll_area.deleteLater()
                    self.scroll_area = None
                    self.timer = QTimer(self)
                    self.timer.start(1000)
                    self.timer.stop()
                    self.scroll_area = QScrollArea()
                    self.scroll_area.setWidgetResizable(True)
                    self.figure = Figure(figsize=(10, 50))
                    self.canvas = FigureCanvas(self.figure)
                    self.canvas.setMinimumSize(5800, 5000)
                    self.canvas.setMaximumSize(5801, 5001)
                    self.toolbar = CustomNavToolbar(self.canvas)
                    self.progress_bar.move(0,0)
                    self.layout.addWidget(self.toolbar,0,0,1,2)    
                    self.scroll_area.setWidget(self.canvas)
                    self.layout.addWidget(self.scroll_area,2,0,1,2)
                    self.toolbar.show()
                    self.scroll_area.show()
                print(str(self.remark_textbox.text()))
                print(str(self.days_textbox.text()))
                remark_var = str(self.remark_textbox.text())
                days_var = str(self.days_textbox.text())
                self.pl = plotted_(self.figure, self.y_axis, self.y_labes, self.canvas, self.layout,self.export_button,self.axes, self.scroll_area, self.toolbar)
                self.plot_trains = self.pl.plot_trains
                self.loaded = True
                select_flag = False
                down_up, dwn_upp, color_dict, rect_dict, express_flag =  self.excel_to_pandas(file_name, self.y_axis, remark_var,days_var)
                if select_flag:
                    down_up, dwn_upp = self.select(down_up, dwn_upp)
                down_up = self.conversion(down_up)
                pp.pprint(f"1st:{rect_dict}")
                rect_dict = self.conversion_box(rect_dict)
                pp.pprint(f"conversion:{rect_dict}")
                down_up = self.add_24_down_up(down_up)
                rect_dict = self.box_add_24(rect_dict)
                pp.pprint(f"24 add:{rect_dict}") 
                self.figure.clear()
                self.arr_drag_dict = self.plot_trains(down_up, dwn_upp, color_dict, rect_dict,express_flag)
                self.export_button.setEnabled(True)
                self.bm = None
                self.bm = BlitManager(self.canvas, self.pl.artist_list)
                global dragger
                dragger = dragged(self.canvas,self.arr_drag_dict, self.bm)
                self.canvas.mpl_connect("pick_event", dragger.on_pick_event)
                # self.canvas.mpl_connect("motion_notify_event", self.on_motion_event)
                self.canvas.mpl_connect("button_release_event", dragger.on_release_event)
                self.canvas.figure.subplots_adjust(left = 0.017, hspace = 1.3)
                dragger.bm.adjust_subplots()
                self.canvas.draw()
            except DuplicateTrainError as e:
                QMessageBox.critical(self, "Error", str(e))
            except WrongStationError as e:
                QMessageBox.critical(self, "Error", str(e))
            except SameLengthError as e:
                QMessageBox.critical(self, "Error", str(e))
            except EmptyListError as e:
                QMessageBox.critical(self, "Error", str(e))              
            except WrongTimeFormatError as e:
                QMessageBox.critical(self, "Error", str(e)) 

    def export_plot(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Plot as PDF", "", "PDF Files (*.pdf)")
        if file_name:
            self.bm.canvas.mpl_disconnect(self.bm.cid)
            self.bm.cid = None
            self.scroll_area.takeWidget()
            self.layout.removeWidget(self.toolbar)
            self.export_button.setEnabled(False)
            self.progress_bar.show()
            self.export_worker = ExportWorker(file_name,self.canvas)
            self.export_thread = QThread()
            self.export_worker.moveToThread(self.export_thread)
            self.export_thread.started.connect(self.export_worker.run)
            self.export_worker.update_signal.connect(self.update_progress_bar)
            self.export_thread.finished.connect(self.export_thread.deleteLater)
            self.export_thread.start()
    def update_progress_bar(self, progress):
        self.progress_bar.setValue(progress)
        if progress == 100:
            self.bm.cid = self.bm.canvas.mpl_connect("draw_event", self.bm.on_draw)
            self.export_thread.quit()
            self.export_thread.wait()
            self.progress_bar.hide()
            self.progress_bar.setValue(0)
            self.layout.addWidget(self.toolbar)
            self.scroll_area.setWidget(self.canvas)
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    apply_stylesheet(app, theme='dark_blue.xml')
    window = PlotWindow()
    window.show()
    app.exec_()
