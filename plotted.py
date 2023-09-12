#changes - function comment
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
from preprocessing import intersection

from labels import *
class plotted_():
    def __init__(self, figure, y_axis, y_labes,canvas, layout,export_button,axes, scroll_area, toolbar) -> None:
        # self.excel_to_pandas = excel_to_pandas
        # self.select = select
        # self.conversion = conversion
        # self.add_24_down_up = add_24_down_up
        self.add_arrow_labels = add_arrow_labels
        self.extract_current_axes = extract_current_axes
        self.merging_dn_fist_and_up_last_element = merging_dn_fist_and_up_last_element
        self.merging_up_fist_and_dn_last_element = merging_up_fist_and_dn_last_element
        self.extract_dn_elem= extract_dn_elem
        self.extract_up_elem = extract_up_elem
        self.add_keys= add_keys
        self.add_lables = add_lables
        self.figure= figure
        self.y_axis = y_axis
        self.y_labes = y_labes
        self.canvas = canvas
        self.layout = layout
        self.export_button = export_button
        self.axes = axes
        self.scroll_area = scroll_area
        self.toolbar = toolbar




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

########################################## collision text for up and down ############################################

            def collision_text_updn1(collision_merged1):
                """ this function takes care of labels up-end and down-start """
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

                    if abs(x - previous_x) <= 0.03 and y == previous_y:
                        # print('label is overlapping')
                        label_var = '/'
                        len_of_labels = len(label_)
                        y_buffer_both_up = y_buffer_both_up + (extract_current_axes(x, y) * len_of_labels) + 1
                        # y_buffer_both_up = y_buffer_both_up + (0.07 * len_of_labels) + 1
                        """y_overlap_both_up is y axis for text which is different in arrows y axis that is original 'y' """
                        y_overlap_both_up = y - y_buffer_both_up 
                    else:
                        label_var = ''
                        y_buffer_both_up = 0
                        y_overlap_both_up = y - y_buffer_both_up                         

                    label = label_var + label_

                    inx, iny, x, y = self.add_arrow_labels(x, y)
                    self.axes[inx][iny].text(x - 0.05, y_overlap_both_up - 0.7, label, rotation = 'vertical', fontsize=13) 
                    self.axes[inx][iny].arrow(x, y, 0, - 0.5, width = 0.005, clip_on = False)

                    previous_x, previous_y = x, y

                    k += 3



            def collision_text_updn( collision_merged):   
                """ this function takes care of labels up-start and down-end"""
                k = 1
                previous_x, previous_y= 0, 0
                label_var = ''
                y_overlap_both_up = 0
                y_buffer_both_up = 0
                # original_x = 0

                for i in range(len(collision_merged[0])):
                    
                    label_ = collision_merged[0][i]
                    x = collision_merged[1][i]
                    y = collision_merged[2][i]

                    if abs(x - previous_x) <= 0.03 and y == previous_y:
                        label_var = '/'
                        len_of_labels = len(label_)
                        y_buffer_both_up = y_buffer_both_up + (extract_current_axes(x, y) * len_of_labels) + 1.4
                        # y_buffer_both_up = y_buffer_both_up + (0.08 * len_of_labels) + 1.4
                        """y_overlap_both_up is y axis for text which is different in arrows y axis that is 'y' """
                        y_overlap_both_up = y + y_buffer_both_up 
                    else:
                        label_var = ''
                        y_buffer_both_up = 0
                        y_overlap_both_up = y + y_buffer_both_up                         

                    # label = new_dict['UPDN'][k - 1] + label_var
                    label = label_ + label_var

                    # original_x = x
                    inx, iny, x, y = self.add_arrow_labels(x, y)
                    self.axes[inx][iny].text(x - 0.05, y_overlap_both_up + 1.9, label, rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
                    self.axes[inx][iny].arrow(x, y, 0, 0.5, width = 0.005, clip_on = False)
                    previous_x, previous_y = x, y
                    k += 3
            
            collision_text_updn(collision_merged)  
            collision_text_updn1(collision_merged1)

            intersection(station_dict, self.axes, trains_dict)

        plot_labels()
        self.canvas.draw()
