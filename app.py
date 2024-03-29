import warnings
from PySide2 import QtWidgets
from PySide2.QtGui import QFont, QKeyEvent, QKeySequence
from PySide2.QtWidgets import QShortcut, QComboBox, QScrollArea, QMessageBox, QApplication, QProgressBar,QLineEdit,QLabel
from PySide2.QtCore import QObject, QThread, Signal, QTimer, Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.transforms import Bbox, TransformedBbox
from qt_material import apply_stylesheet
from collections import Counter
from blit_manager import BlitManager
from preprocessing import excel_to_pandas, select, conversion, conversion_box, box_add_24, add_24_down_up, DuplicateTrainError, WrongStationError, SameLengthError, EmptyListError, WrongTimeFormatError, WrongBoxTimeFormatError, BoxColumnLengthError, IncorrectLengthOfRowsBoxError, ExportThreadError, OmittedSheetsError
from labels import *
from plotted import plotted_
from matplotlib.text import Text
from Draggable import dragged
from drop_down import CheckableComboBox
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
            QMessageBox.critical(self, "Alert", "Please press home again, and wait while all the labels on plot load. Do not drag the labels while they load. Please wait, it might take a while.") 
        else:
            self.dragger.bm.after_home(True)
        self.dragger.bm.adjust_subplots()
        self.zoomed_in = False

def save_pdfs(axes_indices, filenames, conn, shm, section):
    shm = shared_memory.SharedMemory(name=shm.name)
    fig = pickle.loads(shm.buf[:])
    axes = fig.get_axes()
    #print(f"filenames are : {filenames}")
    for i, index in enumerate(axes_indices):
        b = axes[index].get_tightbbox().transformed(fig.dpi_scale_trans.inverted())
        bbox = Bbox([[b.x0-0.3,b.y0-0.6],[b.x1+0.3,b.y1+0.7]])
        fig.savefig(filenames[i], bbox_inches=bbox, pad_inches=1)
        if section[:-1] == "ST-BSL":
            conn.send(16)
        elif section[:-1] == "CCG-ST":
            conn.send(11)
    shm.close()

class ExportWorker(QObject):
    update_signal = Signal(int)
    error_signal = Signal(str)
    # new_fig = Figure(figsize=(10, 50))
    def __init__(self, file_name, fig_bytes, section):
        super().__init__()
        self.file_name = file_name
        self.section = section
        print(f"section is: {section}")
        if self.section and self.section == "CCG-ST":
            self.counter = 1
            self.file_axes = ["_0-8_CCG-VR","_8-16_CCG-VR","_16-24_CCG-VR", "_0-8_VR-BL", "_8-16_VR-BL", "_16-24_VR-BL", "_0-8_BL-ST", "_8-16_BL-ST", "_16-24_BL-ST"]
        elif self.section and self.section == "ST-BSL":
            self.counter = 4
            self.file_axes =  ["_0-8_ST-NDB","_8-16_ST-NDB","_16-24_ST-NDB", "_0-8_NDB-NSL", "_8-16_NDB-NSL", "_16-24_NDB-NSL"]
        self.cores, self.axes_to_cores = self.process_distribution()   
        self.fig_bytes = fig_bytes
        self.fig = pickle.loads(fig_bytes)
        self.shm = self.save_fig_to_shared_memory()
        #print("Worker initialize")
    def process_distribution(self):
        cores = mp.cpu_count()
        # cores = 4
        if cores >= 9 and self.section == "CCG-ST":
            axes_to_cores = [1,1,1,1,1,1,1,1,1]
            cores = 9
        elif cores>=6 and self.section == "ST-BSL":
            axes_to_cores = [1,1,1,1,1,1]
            cores = 6
        else:
            axes_to_cores = []
            if self.section == "CCG-ST":
                q, r = divmod(9, cores)
            elif self.section == "ST-BSL":
                q,r = divmod(6, cores)
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
            #print(f"i:{i} axes index:{axes_indices}")
            pre, post = tuple(self.file_name.split("."))
            filenames = [pre+self.file_axes[ax]+"."+post for ax in axes_indices]
            p = mp.Process(target=save_pdfs, args=(axes_indices, filenames, child_conn, self.shm, self.section+"x"))
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
        #print("I am running")
        try:
            axes = self.fig.axes
            #print(axes)
            #print(f"meri lambai hai {len(axes)}")
            axes_indices = list(range(0, self.axes_to_cores[0]+1))
            #print(axes_indices)
            #print(self.axes_to_cores)
            for index in axes_indices:
                b = axes[index].get_tightbbox().transformed(self.fig.dpi_scale_trans.inverted())
                bbox = Bbox([[b.x0-0.3,b.y0-0.6],[b.x1+0.3,b.y1+0.7]])
                pre, post = tuple(self.file_name.split("."))
                filename = pre+self.file_axes[index]+"."+post
                if index == 0:
                    self.spawn_process()
                self.fig.savefig(filename, bbox_inches=bbox, pad_inches=1)
                if self.section == "CCG-ST":
                    self.counter+= 11
                elif self.section == "ST-BSL":
                    self.counter+= 16
                self.update_signal.emit(self.counter)
            self.shm.close()
            self.shm.unlink()
        except Exception as e:
            error_message = f"Error in thread: {e}"
            tb = traceback.format_exc()
            self.error_signal.emit(f"{error_message}\n the Traceback is: {tb}")
            logging.error(error_message)
            logging.error(traceback.format_exc())
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
        self.y_axis = None
        self.y_labes = None
        self.ccg_st_list = ["CCG","MEL","CYR","GTR","BCT","MX","PL","PBHD","DDR","MRU","MM","BA","BDTS","KHAR","STC","VLP","ADH","JOS","RMAR","GMN","MDD","KILE","BVI","DIC",'MIRA',"BYR","NIG","BSR","NSP","VR","VTN","SAH","KLV","PLG","UOI","BOR","VGN","DRD","GVD","BRRD","UBR","SJN","BLD","KEB","VAPI","BAGD","UVD","PAD","ATUL","BL","DGI","JRS","BIM","AML","ACL","VDH","HXR","GNST","NVS","MRL","SCH","BHET","UDN","ST"]
        self.ccg_st_labes = ["CCG 0.0","MEL 1.30","CYR 2.21","GTR 3.59","BCT 4.48","MX 5.95","PL 7.67","PBHD 8.89","DDR 10.17","MRU 11.75","MM 12.93","BA 14.66","BDTS 15.29","KHAR 16.29","STC 17.61","VLP 19.67","ADH 21.83","JOS 23.52","RMAR 25.37","GMN 26.9","MDD 29.32","KILE 31.22","BVI 33.98","DIC 36.34",'MIRA 39.76',"BYR 43.11","NIG 47.79","BSR 51.78","NSP 55.85","VR 59.98","VTN 68.42","SAH 76.74","KLV 82.55","PLG 90.92","UOI 97.15","BOR 102.8","VGN 111.5","DRD 123.7","GVD 134.8","BRRD 139.0","UBR 144.0","SJN 149.4","BLD 160.9","KEB 165.8","VAPI 172.0","BAGD 179.0","UVD 182.0","PAD 187.7","ATUL 191.0","BL 198.22","DGI 207.21","JRS 212.28","BIM 216.41","AML 221.72","ACL 225.33","VDH 228.87","HXR 232.0","GNST 234.0","NVS 237.33","MRL 245.63","SCH 252.26","BHET 257.3","UDN 262.77","ST 266.78"]    # #print(down_up)        self.setWindowTitle("Matplotlib Plot")
        self.st_bsl_list = ["ST", "UDN", "NOL", "CHM", "BGMR", "GGAR", "BIY", "TBV", "MGRL", "MID", "KRAI", "LTV", "VYA", "KKRD", "DSD", "USD", "LKKD", "BBAI", "NWU", "KFF", "6CPD", "KHTG", "KBH", "BAWD", "DWD", "NDB", "CUE", "TISI", "RNL", "DDE", "VKH", "SNSL", "SNK", "HOL", "NDN", "BEW", "PDP", "BRTK", "AN", "TKHE", "BHEN", "DXG", "CHLK", "PLD", "JL", "BSL"]
        self.st_bsl_labes = ["ST 3.99","UDN 00.0","NOL 5.6","CHM 11.1","BGMR 15.5","GGAR 20.6","BIY 27.1","TBV 33.6","MGRL 36.8","MID 41.6","KRAI 47.4","LTV 49.4","VYA 56.8","KKRD 68.1","DSD 70.7","USD 75.6","LKKD 81.1","BBAI 87.5","NWU 99.1","KFF 104.00","6CPD 115.4","KHTG 125.0","KBH 133.5","BAWD 140.4","DWD 147.2","NDB 156.31","CUE 161.06","TISI 169.24","RNL 178.72","DDE 190.68","VKH 198.85","SNSL 204.2","SNK 210.13","HOL 217.92","NDN 223.35","BEW 230.16","PDP 235.74","BRTK 243.9","AN 251.52","TKHE 263.0","BHEN 269.6","DXG 276.47","CHLK 283.7","PLD 295.21","JL 306.93","BSL 331.93"]
        self.new_canvas = None
        self.save_ongoing = False
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.canvas)
        self.progress_bar = QProgressBar()
        # self.progress_bar.hide()
        self.load_button = QtWidgets.QPushButton("Load Excel File")
        self.load_button.clicked.connect(self.load_file)
        self.axes = None
        self.export_button = QtWidgets.QPushButton("Export Plot")
        self.export_button.clicked.connect(self.export_plot)
        self.export_button.setEnabled(False)
        self.remarks_label= QLabel()
        self.days_label = QLabel()
        self.title_label = QLabel()
        self.section_label = QLabel()
        self.remarks_label.setText("Remarks")
        self.days_label.setText("Days")
        self.title_label.setText("Title")
        self.section_label.setText("Section")
        self.remark_textbox = QLineEdit(self)
        self.days_drop_down = CheckableComboBox(self)
        self.days_drop_down.addItems(['Mo','Tu','We','Th','Fr','Sa','Su','Daily'])
        self.title_textbox = QLineEdit(self)
        self.section_drop_down = QComboBox(self)
        self.section_drop_down.addItems(["CCG-ST", "ST-BSL"])
        reload_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        reload_shortcut.activated.connect(self.ctrl_r)
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.ctrl_s)
        self.reload = False
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setColumnStretch(0, 1)  
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 1)
        self.layout.setColumnStretch(3, 1)
        self.layout.addWidget(self.toolbar,0,0,1,4)
        self.layout.addWidget(self.progress_bar,1,0,1,4)
        self.layout.addWidget(self.scroll_area,2,0,1,4)
        self.layout.addWidget(self.title_label,3,0,1,1)
        self.layout.addWidget(self.title_textbox,4,0,1,1)
        self.layout.addWidget(self.remarks_label,3,1,1,1)
        self.layout.addWidget(self.remark_textbox,4,1,1,1)
        self.layout.addWidget(self.days_label,3,2,1,1)
        self.layout.addWidget(self.days_drop_down,4,2,1,1)
        self.layout.addWidget(self.section_label,3,3,1,1)
        self.layout.addWidget(self.section_drop_down,4,3,1,1)
        self.layout.addWidget(self.load_button,5,0,1,2)
        self.layout.addWidget(self.export_button,5,2,1,2)
        self.canvas.setMinimumSize(5800, 5000)
        self.canvas_size = [5800,5000]
        self.canvas.setMaximumSize(5801, 5001)
        self.bm = None
        self.artist_list = []
        self.dragged_axes = None
        self.loaded = False
        self.blit = True
        self.arr_drag_dict = None
        self.loading = False
        self.loaded_section = None
        self.previous_name = None
    def ctrl_r(self):
        self.reload = True
        self.load_file()
    
    def ctrl_s(self):
        if self.loaded is True:
            self.export_plot()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Equal:
            self.canvas_size = [int(dim+dim/4) for dim in self.canvas_size] 
            x, y = self.canvas_size
            self.canvas.setMinimumSize(x, y)
            self.canvas.setMaximumSize(x+1,y+1)            
        elif event.key() == Qt.Key_Minus:
            self.canvas_size = [int(dim-dim/4) for dim in self.canvas_size] 
            x, y = self.canvas_size
            self.canvas.setMinimumSize(x, y)
            self.canvas.setMaximumSize(x+1,y+1)
        elif event.key() == Qt.Key_Home:
            self.canvas_size = [5800, 5000]
            x, y = self.canvas_size
            self.canvas.setMinimumSize(x, y)
            self.canvas.setMaximumSize(x+1,y+1)
        
    def load_file(self):
        if not self.reload:
            file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
            self.previous_name = file_name
        else:
            file_name = self.previous_name
            self.reload = False

        if file_name:
            try:
                self.export_button.setEnabled(False)
                if self.loading is True:
                    pass
                else:
                    self.load_button.setEnabled(False)
                    self.loading = True
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
                        self.layout.addWidget(self.toolbar,0,0,1,6)    
                        self.scroll_area.setWidget(self.canvas)
                        self.layout.addWidget(self.scroll_area,2,0,1,6)
                        self.toolbar.show()
                        self.scroll_area.show()
                    
                    section_var = self.section_drop_down.currentText()
                    remark_var = str(self.remark_textbox.text())
                    days_list = self.days_drop_down.currentData()
                    days_var = str("|".join(days_list))
                    if days_var:
                        days_var = f"({days_var})"
                    title_var = str(self.title_textbox.text())
                    if section_var == "CCG-ST":
                        self.y_axis = self.ccg_st_list
                        self.y_labes = self.ccg_st_labes
                    else:
                        self.y_axis = self.st_bsl_list
                        self.y_labes = self.st_bsl_labes
                    self.pl = plotted_(self.figure, self.y_axis, self.y_labes, self.canvas, self.layout,self.export_button,self.axes, self.scroll_area, self.toolbar)
                    if section_var == "CCG-ST":
                        self.plot_trains = self.pl.plot_trains_ccg_st
                    else:
                        self.plot_trains = self.pl.plot_trains_st_bsl
                    select_flag = False
                    down_up, dwn_upp, color_dict, rect_dict, express_flag =  self.excel_to_pandas(file_name, self.y_axis, remark_var,days_var)
                    if select_flag:
                        down_up, dwn_upp = self.select(down_up, dwn_upp)
                    down_up = self.conversion(down_up)
                    self.canvas.flush_events()
                    # #pp.p#print(f"1st:{rect_dict}")
                    rect_dict = self.conversion_box(rect_dict)
                    # #pp.p#print(f"conversion:{rect_dict}")
                    down_up = self.add_24_down_up(down_up)
                    rect_dict = self.box_add_24(rect_dict)
                    # #pp.p#print(f"24 add:{rect_dict}") 
                    self.figure.clear()
                    self.arr_drag_dict = self.plot_trains(down_up, dwn_upp, color_dict, rect_dict, express_flag, title_var, section_var)
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
                    self.loaded = True
                    self.loading = False
                    self.loaded_section = section_var
                    self.export_button.setEnabled(True)
                    self.load_button.setEnabled(True)
                    self.canvas.flush_events()
            except DuplicateTrainError as e:
                QMessageBox.critical(self, "Error", str(e))
                self.load_button.setEnabled(True)
                self.loaded_section = None
                self.loaded = False
                self.export_button.setEnabled(False)
                self.loading = False
            except WrongStationError as e:
                QMessageBox.critical(self, "Error", str(e))
                self.load_button.setEnabled(True)
                self.loaded_section = None
                self.loaded = False
                self.export_button.setEnabled(False)
                self.loading = False
            except SameLengthError as e:
                QMessageBox.critical(self, "Error", str(e))
                self.load_button.setEnabled(True)
                self.loaded_section = None
                self.loaded = False
                self.export_button.setEnabled(False)
                self.loading = False
            except EmptyListError as e:
                QMessageBox.critical(self, "Error", str(e))
                self.load_button.setEnabled(True)
                self.loaded_section = None
                self.loaded = False
                self.export_button.setEnabled(False)
                self.loading = False
            except WrongTimeFormatError as e:
                QMessageBox.critical(self, "Error", str(e))
                self.load_button.setEnabled(True)
                self.loaded_section = None
                self.loaded = False
                self.export_button.setEnabled(False)
                self.loading = False
            except WrongBoxTimeFormatError as e:
                QMessageBox.critical(self, "Error", str(e))
                self.load_button.setEnabled(True)
                self.loaded_section = None
                self.loaded = False
                self.export_button.setEnabled(False)
                self.loading = False
            except BoxColumnLengthError as e:
                QMessageBox.critical(self, "Error", str(e))
                self.load_button.setEnabled(True)
                self.loaded_section = None
                self.loaded = False
                self.export_button.setEnabled(False)
                self.loading = False
            except IncorrectLengthOfRowsBoxError as e:
                QMessageBox.critical(self, "Error", str(e))
                self.load_button.setEnabled(True)
                self.loaded_section = None
                self.loaded = False
                self.export_button.setEnabled(False)
                self.loading = False
            except OmittedSheetsError as e:
                QMessageBox.critical(self, "Error", str(e))
                self.load_button.setEnabled(True)
                self.loaded_section = None
                self.loaded = False
                self.export_button.setEnabled(False)
                self.loading = False
            except Exception as e:
                QMessageBox.critical(self, "Error", "Error while loading chart or reading data, please restart the application and check Excel format.") 
                tb = traceback.format_exc()
                print(str(e))
                print(str(tb))
                self.loaded_section = None
                self.loaded = False
                self.export_button.setEnabled(False)
                self.loading = False

    def make_pickle(self):
        fig_bytes = pickle.dumps(self.figure)
        return fig_bytes

    def export_plot(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Plot", "", "PDF Files (*.pdf);;PNG Files (*.png);;SVG Files (*.svg)")
        try:
            if file_name and not self.save_ongoing:
                # self.layout.removeWidget(self.toolbar)
                self.save_ongoing = True
                self.canvas.setMinimumSize(5800, 5000)
                self.canvas.setMaximumSize(5801, 5001)                
                self.export_button.setEnabled(False)
                fig_pickle = self.make_pickle()
                self.export_worker = ExportWorker(file_name, fig_pickle, self.loaded_section)
                self.export_thread = QThread()
                self.export_worker.moveToThread(self.export_thread)
                self.export_thread.started.connect(self.export_worker.run)
                self.export_worker.update_signal.connect(self.update_progress_bar)
                self.export_worker.error_signal.connect(self.raise_export_exception)
                self.export_thread.finished.connect(self.export_thread.deleteLater)
                self.export_thread.start()
        except ExportThreadError as e:
            QMessageBox.critical(self, "Error", str(e))
            tb = traceback.format_exc()
            print(str(e))
            print(str(tb))
            self.save_ongoing = False
            self.export_button.setEnabled(False)
            self.loaded_section = None
            self.loaded = False
        except Exception as e:
            QMessageBox.critical(self, "Error", "Something went wrong while exporting. Please restart application and check excel format.")
            tb = traceback.format_exc()
            print(str(e))
            print(str(tb))
            self.save_ongoing = False
            self.export_button.setEnabled(False)
            self.loaded_section = None
            self.loaded = False

    def raise_export_exception(self, tb):
        print(tb)
        raise ExportThreadError("Error hahahaha")
    
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
                self.save_ongoing = False
                self.export_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Alert", "Your file has exported succesfully.")

if __name__ == "__main__":
    mp.freeze_support()
    warnings.filterwarnings("ignore")
    app = QtWidgets.QApplication([])
    apply_stylesheet(app, theme='dark_blue.xml')
    window = PlotWindow()
    window.show()
    app.exec_()