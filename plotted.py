from PySide2 import QtWidgets
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QScrollArea, QMessageBox, QApplication
from matplotlib.figure import Figure
from matplotlib import patches
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
from labels import *
from intersection import intersection

class plotted_():
    intersection = intersection
    def __init__(self, figure, y_axis, y_labes,canvas, layout,export_button,axes, scroll_area, toolbar) -> None:
        # self.excel_to_pandas = excel_to_pandas
        # self.select = select
        # self.conversion = conversion
        # self.add_24_down_up = add_24_down_up
        self.add_arrow_labels = add_arrow_labels
        self.extract_current_axes = extract_current_axes_us_de
        self.extract_current_axes = extract_current_axes_ue_ds
        self.merge_elements = merge_elements
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
        self.artist_list = []


    def plot(self,index_0,index_1,arr,start_sub_y_axis,end_sub_y_axis,ylim_start,ylim_end,xlim_start,xlim_end, color_dict, station_dict, rect_dict):
        self.axes[index_0][index_1].minorticks_on()
        # xa_0 = np.linspace(0, 8, 200)
        xa_0 = np.arange(xlim_start, xlim_end, 0.03333)
        for arr_2d, color_list in zip(station_dict.values(), color_dict.values()):
            self.canvas.flush_events()
            for i in range(0, len(arr_2d), 2):
                arr_minus = np.array(arr_2d[i+1])
                self.canvas.flush_events()
                arr_minus = arr_minus - 24
                line_color = color_list[int(i/2)]
                # print("train",arr_minus,arr_2d[i],arr_2d[i+1])
                (ln1,) = self.axes[index_0][index_1].plot(arr_minus, arr_2d[i], color=line_color)
                (ln2,) = self.axes[index_0][index_1].plot(arr_2d[i+1], arr_2d[i], color=line_color)
                self.artist_list.append(ln1)
                self.artist_list.append(ln2)
                self.canvas.flush_events()
        for i in range(len(self.y_axis)):
            y_index = self.y_axis[i]
            self.canvas.flush_events()
            ya = [y_index] * len(xa_0)
            self.artist_list.append(self.axes[index_0][index_1].scatter(xa_0, ya, marker=',',color='blue', s=0.52))
            self.canvas.flush_events()

        for key, box_list in rect_dict.items():
            if key =="DN":
                grid = "-----"
            elif key =="UP":
                grid = "|||"
            for station, start_time, end_time in box_list:
                xmin = start_time
                xmax = end_time
                ymax = station - 0.15
                ymin = station - 0.85
                rect = patches.Rectangle((xmin, ymin), width=xmax-xmin, height= ymax-ymin, alpha=0.6, edgecolor='m', hatch=grid, facecolor='none')
                self.artist_list.append(self.axes[index_0][index_1].add_patch(rect))

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
        self.canvas.flush_events()


        self.axes[index_0][index_1].tick_params(axis='x', which='minor', labelbottom=True)
        self.axes[index_0][index_1].tick_params(labeltop=True, labelright=True)
        minor_labels = ["10", "20", "30", "40", "50"] * 8
        minor_labels.insert(0, "")
        self.canvas.flush_events()


        formatter = FixedFormatter(minor_labels)
        self.axes[index_0][index_1].xaxis.set_minor_formatter(formatter)
        self.axes[index_0][index_1].tick_params(axis='x', which='minor', labelsize=6)
        self.axes[index_0][index_1].set_xlim(xlim_start,xlim_end)  
        self.axes[index_0][index_1].invert_yaxis()
        self.canvas.flush_events()


    def plot_trains(self, station_dict, trains_dict, color_dict, rect_dict, express_flag):
        self.axes = self.figure.subplots(nrows=3, ncols=3)
        # have to make  3 x 3 grid
        # set width of each subplot as 8
        for key, arr_2d in station_dict.items():
            self.canvas.flush_events()
            
            for i in range(0, len(arr_2d), 2):
                self.canvas.flush_events()

                for j in range(len(arr_2d[i])):
                    arr_2d[i][j] = self.y_axis.index(arr_2d[i][j])
                    self.canvas.flush_events()

        # dup_train_dict = copy.deepcopy(trains_dict)
        self.canvas.flush_events()


        for key, box_list in rect_dict.items():
            for i, (station, *_) in enumerate(box_list):
                station = self.y_axis.index(station)
                box_list[i] = station,*_,

    ######################################################################################################    
        arr1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        arr2 = [8, 9, 10, 11, 12, 13, 14, 15, 16]
        arr3 = [16, 17, 18, 19, 20, 21, 22, 23, 24]
        
    #   (index_0, index_1, arr, start_sub_y_axis, end_sub_y_axis, ylim_start, ylim_end, xlim_start, xlim_end)
        self.plot(0,0,arr1,0,30,      0,15,        0,8, color_dict, station_dict, rect_dict)
        self.plot(1,0,arr1,29,50,    0,19,        0,8, color_dict, station_dict, rect_dict)   
        self.plot(2,0,arr1,49,64,    0,19,        0,8, color_dict, station_dict, rect_dict) 

        self.plot(0,1,arr2,0,30,      0,15,        8,16, color_dict,   station_dict, rect_dict)
        self.plot(1,1,arr2,29,50,    0,19,       8,16,  color_dict,  station_dict, rect_dict)
        self.plot(2,1,arr2,49,64,    0,19,       8,16,  color_dict,  station_dict, rect_dict)

        self.plot(0,2,arr3,0,30,      0,15,       16,24,  color_dict,  station_dict, rect_dict)
        self.plot(1,2,arr3,29,50,    0,19,       16,24,  color_dict,  station_dict, rect_dict)
        self.plot(2,2,arr3,49,64,    0,19,        16,24,  color_dict,  station_dict, rect_dict)

        def plot_labels():

            # up_intersecting_trains = self.intersection(station_dict, trains_dict)
            # Sort the direction of arrows and labels
            # To get the whether the train is up and down have to bring the parameter for up and down
            up_inter, dn_inter = self.intersection(station_dict, trains_dict)

            new_dict = copy.deepcopy(station_dict)
            """ Called a func to add lebels in dictionary"""
            new_dict = self.add_lables(new_dict, trains_dict)
            
            """ Called a func to add keys in dictionary"""
            new_dict = self.add_keys(new_dict)
            
            new_dict['UPDN'] = new_dict['UP'] + new_dict['DN']
            print(new_dict)               
            #format: "DN": 'label', '[y]', '[x]', key..... "UP": 'label', '[y]', '[x]', key
            """ Called a func that extract up start and up end elements"""
            upStart, upEnd = self.extract_up_elem(new_dict,up_inter)  

            """ Called a func that extract dn start and dn end elements"""        
            dnStart, dnEnd = self.extract_dn_elem(new_dict,dn_inter)

            """ Called a func that colab up start and dn end elements"""
            upStart_dnEnd = self.merge_elements(upStart, dnEnd)
            print("upStart_dnEnd",upStart_dnEnd)
            """ Called a func that colab dn start and up end elements"""        
            upEnd_dnStart = self.merge_elements(dnStart, upEnd)
            print("upEnd_dnStart",upEnd_dnStart )

########################################## collision text for up and down #################################################\
            
            def upEnd_dnStart_label(upEnd_dnStart):
                """ this function takes care of labels up-end and down-start labels and arrows"""
                self.canvas.flush_events()
                k = 1
                previous_x, previous_y= 0, 0
                label_var = ''
                final_y = 0
                y_buffer = 0
                arrow_label_buffer = 0

                for i in range(len(upEnd_dnStart[0])):
                    self.canvas.flush_events()

                    label_ = upEnd_dnStart[0][i]
                    x = upEnd_dnStart[1][i]
                    y = upEnd_dnStart[2][i]
                    key = upEnd_dnStart[3][i]
                    len_of_labels = len(label_)
                    arrow_plot_buffer, arrow_label_buffer, slash_buffer,first_axes_flag, second_axes_flag = extract_current_axes_ue_ds(x, y)

                    if abs(x - previous_x) <= 0.03 and y == previous_y:
                        label_var = '/'
                        y_buffer = y_buffer + (slash_buffer * len_of_labels) 
                        final_y = y - y_buffer 
                    else:
                        label_var = ''
                        y_buffer = 0
                        y_buffer = arrow_label_buffer * len_of_labels 
                        final_y = y - y_buffer                         

                    label = label_var + label_

                    inx, iny, x, y= self.add_arrow_labels(x, y)
                    if x > 24:
                        dup_x = x - 24
                    else:
                        dup_x = x
                    if first_axes_flag or second_axes_flag:    
                        # print("first", first_axes_flag)
                        # print("second", second_axes_flag)
                        # print(x,x - 0.02) 
                        # if x>=24 and x - 0.02 < 24:
                        #     x = x+0.02

                        if first_axes_flag and y == 29:
                            # check which one is true
                            # print(inx,iny)
                            self.artist_list.append(self.axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True))  # NOTE: INSIDE IF
                            if key == 'UP':
                                self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y, 0, -0.5, width = 0.005, clip_on = False))
                            else:
                                self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer, 0, 0.5, width = 0.005, clip_on = False))
                            # to plot vr labels on 2nd axes
                            print("internal express",express_flag)
                            if express_flag:
                                # print('printing inx buffer before', arrow_plot_buffer, arrow_label_buffer, slash_buffer,first_axes_flag)
                                arrow_plot_buffer, arrow_label_buffer, slash_buffer,first_axes_flag, second_axes_flag = extract_current_axes_ue_ds(dup_x, y + 2)
                                # print('printing inx buffer after', arrow_plot_buffer, arrow_label_buffer, slash_buffer,first_axes_flag)
                                # inx = 1
                                # self.artist_list.append(self.axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True))  # NOTE: INSIDE IF
                                # if key == 'UP':
                                #     self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y, 0, -0.5, width = 0.005, clip_on = False))
                                # else:
                                #     self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer, 0, 0.5, width = 0.005, clip_on = False))

                        elif second_axes_flag and y==49 :
                            self.artist_list.append(self.axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True))  # NOTE: INSIDE IF
                            if key == 'UP':
                                self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y, 0, -0.5, width = 0.005, clip_on = False))
                            else:
                                self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer, 0, 0.5, width = 0.005, clip_on = False))
                            # to plot vr labels on 2nd axes 
                            # inx = 2
                            # arrow_plot_buffer, arrow_label_buffer, slash_buffer,first_axes_flag, second_axes_flag = extract_current_axes_ue_ds(dup_x, y+2)
                            # self.artist_list.append(self.axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True))  # NOTE: INSIDE IF
                            # if key == 'UP':
                            #     self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y , 0, -0.5, width = 0.005, clip_on = False))
                            # else:
                            #     self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer, 0, 0.5, width = 0.005, clip_on = False))
                        # else:
                    
                        # if not (first_axes_flag or second_axes_flag or y==49 or y==29) :
                        print("else print", label)
                        self.artist_list.append(self.axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True))  # NOTE: INSIDE IF
                        if key == 'UP':
                            self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y , 0, -0.5, width = 0.005, clip_on = False))
                        else:
                            self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer, 0, 0.5, width = 0.005, clip_on = False))
                    previous_x, previous_y = x, y
                    k += 3

            def upStart_dnEnd_label( upStart_dnEnd):   
                """this function takes care of labels up-start and down-end lab"""
                self.canvas.flush_events()
                k = 1
                previous_x, previous_y= 0, 0
                label_var = ''
                final_y = 0
                y_buffer = 0
                self.canvas.flush_events()

                for i in range(len(upStart_dnEnd[0])):
                    label_ = upStart_dnEnd[0][i]
                    x = upStart_dnEnd[1][i]
                    y = upStart_dnEnd[2][i]
                    key = upStart_dnEnd[3][i]
                    len_of_labels = len(label_)
                    arrow_plot_buffer, arrow_label_buffer, slash_buffer, first_axes_flag, second_axes_flag = extract_current_axes_us_de(x, y)
                    if abs(x - previous_x) <= 0.03 and y == previous_y:
                        label_var = '/'
                        y_buffer = y_buffer + (slash_buffer * len_of_labels) 
                        final_y = y + y_buffer 
                    else:
                        label_var = ''
                        y_buffer = 0
                        y_buffer = arrow_label_buffer * len_of_labels
                        final_y = y + y_buffer                         

                    label = label_ + label_var

                    inx, iny, x, y = self.add_arrow_labels(x, y)
                    self.canvas.flush_events()
                    # if flag is true have to repeat it plot with x = 1 which is in x = 0
                    # if second_ flag is true have to repeat it with plot x = 2 which is in x = 1
                    # print(x,x-0.02)
                    # if x>=24 and x - 0.02 < 24:
                    #     x = x+0.02
                    if x > 24:
                        dup_x = x - 24
                    else:
                        dup_x = x
                    if first_axes_flag or second_axes_flag:    

                        if first_axes_flag and y == 29:
                            # check which one is true
                            self.artist_list.append(self.axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True))  # NOTE: INSIDE IF
                            if key == 'UP': #UP
                                self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer, 0, -0.5, width = 0.005, clip_on = False))
                            else:
                                self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))
                            print("upstart 1 final plot", inx, iny,x - 0.02, final_y + arrow_label_buffer, label) 
                            # to plot vr labels on 2nd axes 
                            print("internal express",express_flag)
                            if express_flag:
                                arrow_plot_buffer, arrow_label_buffer, slash_buffer, first_axes_flag, second_axes_flag = extract_current_axes_us_de(dup_x, y + 2)
                                inx = 1
                                self.artist_list.append(self.axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True))  # NOTE: INSIDE IF
                                if key == 'UP': #UP
                                    self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer, 0, -0.5, width = 0.005, clip_on = False))
                                else:
                                    self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))
                                print("upstart 2 final plot", inx, iny,x - 0.02, final_y + arrow_label_buffer, label) 

                        elif second_axes_flag and y == 49:
                            self.artist_list.append(self.axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True))  # NOTE: INSIDE IF
                            if key == 'UP': #UP
                                self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer, 0, -0.5, width = 0.005, clip_on = False))
                            else:
                                self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))
                            print("upstart else 1 final plot", inx, iny,x - 0.02, final_y + arrow_label_buffer, label) #triggered

                            # to plot vr labels on 2nd axes 
                            inx = 2
                            arrow_plot_buffer, arrow_label_buffer, slash_buffer, first_axes_flag, second_axes_flag = extract_current_axes_us_de(dup_x, y + 2)
                            self.artist_list.append(self.axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True))  # NOTE: INSIDE IF
                            if key == 'UP': #UP
                                self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer, 0, -0.5, width = 0.005, clip_on = False))
                            else:
                                self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))
                            print("upstart else 2 final plot", inx, iny,x - 0.02, final_y + arrow_label_buffer, label) #triggered

                        # else:
                        # should not be in first and should not b1
                    
                      
                    # if not (first_axes_flag or second_axes_flag) or y!=49 or y!=29 :
                    self.artist_list.append(self.axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True))  # NOTE: INSIDE IF
                    if key == 'UP': #UP
                        self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer, 0, -0.5, width = 0.005, clip_on = False))
                    else:
                        self.artist_list.append(self.axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))
                        print("upstart final plot", inx, iny,x - 0.02, final_y + arrow_label_buffer, label) #triggered
                    
                    
                    # self.artist_list.append(self.axes[inx][iny].text(x - 0.02, final_y + arrow_label_buffer, label, rotation  = 'vertical', fontsize=8, picker=True))  # NOTE: INSIDE IF
                    # if key == 'UP':
                    #     self.artist_list.append(self.axes[inx][iny].arrow(x, y + arrow_plot_buffer, 0, -0.5, width = 0.005, clip_on = False))
                    # else:
                    #     self.artist_list.append(self.axes[inx][iny].arrow(x, y, 0, 0.5, width = 0.005, clip_on = False))
                    previous_x, previous_y = x, y
                    k += 3
        
            upEnd_dnStart_label(upEnd_dnStart)
            upStart_dnEnd_label(upStart_dnEnd)  

            # up_inter, dn_inter = self.intersection(station_dict, trains_dict)
            # print("intersection",up_inter, dn_inter)
        plot_labels()
        self.canvas.figure.subplots_adjust(left = 0.017, hspace=0.8)
        self.canvas.draw()
