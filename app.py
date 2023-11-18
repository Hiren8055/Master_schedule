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
from preprocessing import excel_to_pandas, select, conversion, conversion_box, box_add_24, add_24_down_up, DuplicateTrainError, WrongStationError, SameLengthError, EmptyListError, WrongTimeFormatError, WrongBoxTimeFormatError, BoxColumnLengthError, IncorrectLengthOfRowsBoxError, ExportThreadError
from labels import *
from plotted import plotted_
from matplotlib.text import Text
from Draggable import dragged
import traceback
import matplotlib.pyplot as plt
import pickle
import time
import pprint
import multiprocessing as mp
from multiprocessing import shared_memory
import logging
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
            super().home(self, *args, **kwargs)
            self.dragger.bm.adjust_subplots()
            global dragger
            dragger = self.dragger
            QMessageBox.critical(self, "Alert", "Please press home again, and wait while the all labels on plot load, it might take some while.") 
        else:
            self.dragger.bm.after_home(True)
        self.dragger.bm.adjust_subplots()
        self.zoomed_in = False

def save_pdfs(axes_indices, filenames, conn, shm):
    shm = shared_memory.SharedMemory(name=shm.name)
    fig = pickle.loads(shm.buf[:])
    axes = fig.get_axes()
    print(f"filenames are : {filenames}")
    for i, index in enumerate(axes_indices):
        b = axes[index].get_tightbbox().transformed(fig.dpi_scale_trans.inverted())            
        bbox = Bbox([[b.x0-0.3,b.y0-0.6],[b.x1+0.3,b.y1+0.7]])
        fig.savefig(filenames[i], bbox_inches=bbox, pad_inches=1)
        conn.send(11)
    shm.close()

class ExportWorker(QObject):
    update_signal = Signal(int)
    error_signal = Signal(str)
    # new_fig = Figure(figsize=(10, 50))
    def __init__(self, file_name, fig_bytes):
        super().__init__()
        self.file_name = file_name
        self.file_axes = ["0-8_CCG-VR","8-16_CCG-VR","16-24_CCG-VR", "0-8_VR-BL", "8-16_VR-BL", "16-24_VR-BL", "0-8_BL-ST", "8-16_BL-ST", "16-24_BL-ST"]
        self.counter = 1
        self.cores, self.axes_to_cores = self.process_distribution()   
        self.fig_bytes = fig_bytes
        self.fig = pickle.loads(fig_bytes)
        self.shm = self.save_fig_to_shared_memory()
        print("Worker initialize")
    def process_distribution(self):
        cores = mp.cpu_count()
        # cores = 4
        if cores >= 9:
            axes_to_cores = [1,1,1,1,1,1,1,1,1]
            cores = 9
        else:
            axes_to_cores = []
            q, r = divmod(9, cores)
            for i in range(cores):
                extra = max(0,r-i)
                if extra:
                    r-=1
                    axes_to_cores.append(q+1)
                else:
                    axes_to_cores.append(q)
        return cores, axes_to_cores
    def save_fig_to_shared_memory(self):
        # Create a shared memory space and copy the figure bytes into it
        shm = shared_memory.SharedMemory(create=True, size=len(self.fig_bytes), name="fig_shared_memory")
        shm.buf[:len(self.fig_bytes)] = self.fig_bytes
        return shm
    def spawn_process(self):
        parent_conn, child_conn = mp.Pipe()
        processes = []
        curr_axes = self.axes_to_cores[0]
        for i in range(1, self.cores):
            axes_indices = list(range(curr_axes, curr_axes+self.axes_to_cores[i]))
            print(f"i:{i} axes index:{axes_indices}")
            pre, post = tuple(self.file_name.split("."))
            filenames = [pre+self.file_axes[ax]+"."+post for ax in axes_indices]
            p = mp.Process(target=save_pdfs, args=(axes_indices, filenames, child_conn, self.shm))
            processes.append(p)
            p.start()
            curr_axes = axes_indices[-1]+1
        for p in processes:
            p.join()
        for _ in processes:
            count = parent_conn.recv()
            self.counter += count
            self.update_signal.emit(self.counter)
    def run(self):
        print("I am running")
        try:
            axes = self.fig.axes
            print(axes)
            print(f"meri lambai hai {len(axes)}")
            axes_indices = list(range(0, self.axes_to_cores[0]+1))
            print(axes_indices)
            print(self.axes_to_cores)
            for index in axes_indices:
                b = axes[index].get_tightbbox().transformed(self.fig.dpi_scale_trans.inverted())
                bbox = Bbox([[b.x0-0.3,b.y0-0.6],[b.x1+0.3,b.y1+0.7]])
                pre, post = tuple(self.file_name.split("."))
                filename = pre+self.file_axes[index]+"."+post
                if index == 0:
                    self.spawn_process()
                self.fig.savefig(filename, bbox_inches=bbox, pad_inches=1)
                self.counter+= 11
                self.update_signal.emit(self.counter)
            self.shm.close()
            self.shm.unlink()
        except Exception as e:
            # error_message = f"Error in thread: {e}"
            # tb = traceback.format_exc()
            # self.error_signal.emit(f"{error_message}\n the Traceback is: {tb}")
            # logging.error(error_message)
            # logging.error(traceback.format_exc())
            self.error_signal.emit(f"Something went wrong while exporting, please restart the application and check the excel format.")

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
        # self.progress_bar.hide()
        self.button = QtWidgets.QPushButton("Load Excel File")
        self.button.clicked.connect(self.load_file)
        self.axes = None
        self.export_button = QtWidgets.QPushButton("Export Plot")
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
                    self.toolbar.move(0,0)
                    self.layout.addWidget(self.toolbar,0,0,1,2)    
                    self.scroll_area.setWidget(self.canvas)
                    self.layout.addWidget(self.scroll_area,2,0,1,2)
                    self.toolbar.show()
                    self.scroll_area.show()
                # print(str(self.remark_textbox.text()))
                # print(str(self.days_textbox.text()))
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
                # pp.pprint(f"1st:{rect_dict}")
                rect_dict = self.conversion_box(rect_dict)
                # pp.pprint(f"conversion:{rect_dict}")
                down_up = self.add_24_down_up(down_up)
                rect_dict = self.box_add_24(rect_dict)
                # pp.pprint(f"24 add:{rect_dict}") 
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
            except WrongBoxTimeFormatError as e:
                QMessageBox.critical(self, "Error", str(e)) 
            except BoxColumnLengthError as e:
                QMessageBox.critical(self, "Error", str(e)) 
            except IncorrectLengthOfRowsBoxError as e:
                QMessageBox.critical(self, "Error", str(e))
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e)) 
    def make_pickle(self):
        fig_bytes = pickle.dumps(self.figure)
        return fig_bytes

    def export_plot(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Plot", "", "PDF Files (*.pdf);;PNG Files (*.png);;SVG Files (*.svg)")
        try:
            if file_name:
                # self.layout.removeWidget(self.toolbar)
                self.export_button.setEnabled(False)
                fig_pickle = self.make_pickle()
                self.export_worker = ExportWorker(file_name, fig_pickle)
                self.export_thread = QThread()
                self.export_worker.moveToThread(self.export_thread)
                self.export_thread.started.connect(self.export_worker.run)
                self.export_worker.update_signal.connect(self.update_progress_bar)
                self.export_worker.update_signal.connect(self.update_progress_bar)
                self.export_thread.finished.connect(self.export_thread.deleteLater)
                self.export_thread.start()
        except Exception as e:
            QMessageBox.critical(self, "Error", "Something went wrong while exporting. Please restart application and check excel format.")
    def raise_export_exception(self):
        raise ExportThreadError
    def update_progress_bar(self, progress):
        try:
            self.progress_bar.setValue(progress)
        except Exception as e:
            QMessageBox.critical(self, "Alert", "Your file is exporting successfully, please don't refer to progress bar as it has stopped working and check your files.")
        try:
            if progress == 100:
                self.export_thread.quit()
                self.bm.cid = self.bm.canvas.mpl_connect("draw_event", self.bm.on_draw)
                self.export_thread.wait()
                self.bm.exporting = False
                # self.progress_bar.hide()
                self.progress_bar.setValue(0)
        except Exception as e:
            QMessageBox.critical(self, "Alert", "Your file has exported succesfully.")
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    apply_stylesheet(app, theme='dark_blue.xml')
    window = PlotWindow()
    window.show()
    app.exec_()
