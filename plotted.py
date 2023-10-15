from matplotlib import patches
import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedFormatter
import copy
from labels import add_lables, add_keys, extract_up_elem, extract_dn_elem, merge_elements
from label_arrow import *
from intersection import intersection

class plotted_():
    intersection = intersection
    def __init__(self, figure, y_axis, y_labes, canvas, layout,export_button,axes, scroll_area, toolbar) -> None:
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
        xa_0 = np.arange(xlim_start, xlim_end, 0.03333)
        for arr_2d, color_list in zip(station_dict.values(), color_dict.values()):
            self.canvas.flush_events()
            for i in range(0, len(arr_2d), 2):
                arr_minus = np.array(arr_2d[i+1])
                self.canvas.flush_events()
                arr_minus = arr_minus - 24
                line_color = color_list[int(i/2)]
                (ln1,) = self.axes[index_0][index_1].plot(arr_minus, arr_2d[i], color=line_color, linewidth = 0.7)
                (ln2,) = self.axes[index_0][index_1].plot(arr_2d[i+1], arr_2d[i], color=line_color,linewidth = 0.7)
                self.artist_list.append(ln1)
                self.artist_list.append(ln2)
                self.canvas.flush_events()
        for i in range(len(self.y_axis)):
            y_index = self.y_axis[i]
            self.canvas.flush_events()
            ya = [y_index] * len(xa_0)
            self.artist_list.append(self.axes[index_0][index_1].scatter(xa_0, ya, marker=',',color='blue', s=0.52, alpha = 0.7))
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

        self.axes[index_0][index_1].set_ylim(start_sub_y_axis,end_sub_y_axis)
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

        self.canvas.flush_events()

        for key, box_list in rect_dict.items():
            for i, (station, *_) in enumerate(box_list):
                station = self.y_axis.index(station)
                box_list[i] = station,*_,

    ######################################################################################################    
        arr1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        arr2 = [8, 9, 10, 11, 12, 13, 14, 15, 16]
        arr3 = [16, 17, 18, 19, 20, 21, 22, 23, 24]
        
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

            # Sort the direction of arrows and labels
            # To get the whether the train is up and down have to bring the parameter for up and down
            up_inter, dn_inter = self.intersection(station_dict, trains_dict)

            new_dict = copy.deepcopy(station_dict)

            """ Called a func to add lebels in dictionary"""
            new_dict = self.add_lables(new_dict, trains_dict)
            
            """ Called a func to add keys in dictionary"""
            new_dict = self.add_keys(new_dict)
            
            #formatfor below ditionary: {"DN": 'label', '[y]', '[x]', key..... ,"UP": 'label', '[y]', '[x]', key}
            new_dict['UPDN'] = new_dict['UP'] + new_dict['DN']

            """ Called a func that extract up start and up end elements"""
            upStart, upEnd = self.extract_up_elem(new_dict,up_inter)  

            """ Called a func that extract dn start and dn end elements"""        
            dnStart, dnEnd = self.extract_dn_elem(new_dict,dn_inter)

            """ Called a func that colab up start and dn end elements"""
            upStart_dnEnd = self.merge_elements(upStart, dnEnd)

            """ Called a func that colab dn start and up end elements"""        
            upEnd_dnStart = self.merge_elements(dnStart, upEnd)

########################################## collision text for up and down #################################################\

            upEnd_dnStart_label(self.canvas, self.axes, express_flag, self.artist_list, upEnd_dnStart)
            upStart_dnEnd_label(self.canvas, self.axes, express_flag, self.artist_list, upStart_dnEnd)  

        plot_labels()
        self.canvas.figure.subplots_adjust(left = 0.017, hspace = 0.8)
