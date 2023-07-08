import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedFormatter
from adjustText import adjust_text
import matplotlib.transforms as mtransforms

def plot_trains(station_dict, y_axis, trains_dict):
    y_axis.insert(0," ")
    y_axis.insert(0,"  ")
    y_axis.insert(0,"   ")
    y_axis.insert(0,"    ")
    y_axis.append("     ")
    y_axis.append("      ")
    y_axis.append("       ")
    y_axis.append("        ")
    print(" ")
    # print("Trains dictionary: ", trains_dict)
    print(" ")
# Arrow:
#     eg. axes[2].arrow(20, 25, 0, 1, width = 0.01, head_width=0.1, head_length=0.1, color = 'blue')
#     20---> x axis
#     25 --> y axis
#     1 --> size of line segment
 
# have to make  3 x 3 grid
  
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(10, 50))
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            for j in range(len(arr_2d[i])):
                arr_2d[i][j] = y_axis.index(arr_2d[i][j])


    # Subplot 1: 0-8
    axes[0][0].minorticks_on()

    # print('station_dict : ', station_dict)
    # xa_0 = np.linspace(0, 8, 200)
    xa_0 = np.arange(0, 8, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[0][0].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_0)
        axes[0][0].scatter(xa_0, ya, marker=',',color='blue', s=0.3)
        
    ### ARROW DowN        
    # k = 1    
    # for i in range(len(station_dict['DN']) // 2):    
    #     if 0 <= station_dict['DN'][k][0] <= 8:
    #         axes[0].text(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - 2.3, trains_dict['DN'][i], rotation = 'vertical', fontsize=9)
    #         axes[0].arrow(station_dict['DN'][k][0], station_dict['DN'][k - 1][0], 0, 1, width = 0.005)
    #     k += 2
    
    # ### ARROW UP        
    # k = 1    
    # for i in range(len(station_dict['UP']) // 2):    
    #     if 0 <= station_dict['UP'][k][0] <= 8:
    #         axes[0].text(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1.3, trains_dict['UP'][i], rotation = 'vertical', fontsize=9)
    #         axes[0].arrow(station_dict['UP'][k][0], station_dict['UP'][k - 1][0], 0, -1, width = 0.005)
    #     k += 2     
    
    axes[0][0].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[0][0].xaxis.grid(True, which='minor', linestyle='-')
    axes[0][0].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[0][0].set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8])
    axes[0][0].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])

    # slicing for subplots
    sub_y_axis = y_axis[0:19]
    print("for tick",sub_y_axis)
    axes[0][0].set_yticks(range(len(sub_y_axis)))
    sub_y_axis[-4:] = "    "       # buffer at last
    print("for before",sub_y_axis)

    axes[0][0].set_yticklabels(sub_y_axis)
    axes[0][0].tick_params(axis='x', which='minor', labelbottom=True)
    axes[0][0].tick_params(labeltop=True, labelright=True)

    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[0][0].xaxis.set_minor_formatter(formatter)
    axes[0][0].tick_params(axis='x', which='minor', labelsize=6)
    axes[0][0].set_xlim(0, 8)
    axes[0][0].set_ylim(0, len(sub_y_axis))
  

# have to give buffer before the plots for arrow

    axes[1][0].minorticks_on()

    # print('station_dict : ', station_dict)
    # xa_0 = np.linspace(0, 8, 200)
    xa_0 = np.arange(0, 8, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[0][1].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_0)
        axes[0][1].scatter(xa_0, ya, marker=',',color='blue', s=0.3)

    axes[1][0].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[1][0].xaxis.grid(True, which='minor', linestyle='-')
    axes[1][0].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[1][0].set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8])
    axes[1][0].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])

    # slicing for subplots
    sub_y_axis = y_axis[10:39]
    print("for ticks",sub_y_axis)
    axes[1][0].set_yticks(range(len(sub_y_axis)))
    sub_y_axis[0:4] = "    "       # buffer at last
    sub_y_axis[-4:] = "    "       # buffer at last
    print("for labels",sub_y_axis)
    axes[1][0].set_yticklabels(sub_y_axis)
    axes[1][0].tick_params(axis='x', which='minor', labelbottom=True)
    axes[1][0].tick_params(labeltop=True, labelright=True)

    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[1][0].xaxis.set_minor_formatter(formatter)
    axes[1][0].tick_params(axis='x', which='minor', labelsize=6)
    axes[1][0].set_xlim(0, 8)
    axes[1][0].set_ylim(0, len(sub_y_axis))


    axes[2][0].minorticks_on()

    # print('station_dict : ', station_dict)
    # xa_0 = np.linspace(0, 8, 200)
    xa_0 = np.arange(0, 8, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[0][1].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_0)
        axes[0][1].scatter(xa_0, ya, marker=',',color='blue', s=0.3)

    axes[2][0].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[2][0].xaxis.grid(True, which='minor', linestyle='-')
    axes[2][0].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[2][0].set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8])
    axes[2][0].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])

    # slicing for subplots
    print(y_axis)
    sub_y_axis = y_axis[30:]
    print("for ticks",sub_y_axis)
    axes[2][0].set_yticks(range(len(sub_y_axis)))
    sub_y_axis[0:4] = "    "       # buffer at last
    sub_y_axis[-4:] = "    "       # buffer at last
    print("for labels",sub_y_axis)
    axes[2][0].set_yticklabels(sub_y_axis)
    axes[2][0].tick_params(axis='x', which='minor', labelbottom=True)
    axes[2][0].tick_params(labeltop=True, labelright=True)

    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[2][0].xaxis.set_minor_formatter(formatter)
    axes[2][0].tick_params(axis='x', which='minor', labelsize=6)
    axes[2][0].set_xlim(0, 8)
    axes[2][0].set_ylim(0, len(sub_y_axis))







    # Subplot 2: 8-16
    axes[0][1].minorticks_on()
    xa_1 =np.arange(8, 16, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[0][1].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_1)
        axes[0][1].scatter(xa_1, ya, marker=',',color='blue', s=0.3)
        
    ### ARROW DowN        
    # k = 1    
    # for i in range(len(station_dict['DN']) // 2):    
    #     if 8 <= station_dict['DN'][k][0] <= 16:
    #         axes[1].text(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - 2.3, trains_dict['DN'][i], rotation = 'vertical', fontsize=9)
    #         axes[1].arrow(station_dict['DN'][k][0], station_dict['DN'][k - 1][0], 0, 1, width = 0.005)
    #     k += 2  
        
    ### ARROW UP        
    # k = 1    
    # for i in range(len(station_dict['UP']) // 2):    
    #     if 8 <= station_dict['UP'][k][0] <= 16:
    #         axes[1].text(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1.3, trains_dict['UP'][i], rotation = 'vertical', fontsize=9)
    #         axes[1].arrow(station_dict['UP'][k][0], station_dict['UP'][k - 1][0], 0, -1, width = 0.005)
    #     k += 2
        
    axes[0][1].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[0][1].xaxis.grid(True, which='minor', linestyle='-')
    axes[0][1].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[0][1].set_xticks([8, 9, 10, 11, 12, 13, 14, 15, 16])
    axes[0][1].set_xticklabels([8, 9, 10, 11, 12, 13, 14, 15, 16])

    sub_y_axis = y_axis[0:19]
    print("8 -16 for tick",sub_y_axis)
    axes[0][1].set_yticks(range(len(sub_y_axis)))
    sub_y_axis[-4:] = "    "       # buffer at last
    print("8 -16 for before",sub_y_axis)

    axes[0][1].set_yticklabels(sub_y_axis)
    axes[0][1].tick_params(axis='x', which='minor', labelbottom=True)
    axes[0][1].tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[0][1].xaxis.set_minor_formatter(formatter)
    axes[0][1].tick_params(axis='x', which='minor', labelsize=6)
    axes[0][1].set_xlim(8, 16)
    axes[0][1].set_ylim(0, len(sub_y_axis))



    axes[1][1].minorticks_on()

    xa_1 =np.arange(8, 16, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[1][1].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_1)
        axes[1][1].scatter(xa_1, ya, marker=',',color='blue', s=0.3)
        
    ### ARROW DowN        
    # k = 1    
    # for i in range(len(station_dict['DN']) // 2):    
    #     if 8 <= station_dict['DN'][k][0] <= 16:
    #         axes[1].text(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - 2.3, trains_dict['DN'][i], rotation = 'vertical', fontsize=9)
    #         axes[1].arrow(station_dict['DN'][k][0], station_dict['DN'][k - 1][0], 0, 1, width = 0.005)
    #     k += 2  
        
    ### ARROW UP        
    # k = 1    
    # for i in range(len(station_dict['UP']) // 2):    
    #     if 8 <= station_dict['UP'][k][0] <= 16:
    #         axes[1].text(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1.3, trains_dict['UP'][i], rotation = 'vertical', fontsize=9)
    #         axes[1].arrow(station_dict['UP'][k][0], station_dict['UP'][k - 1][0], 0, -1, width = 0.005)
    #     k += 2
        
    axes[1][1].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[1][1].xaxis.grid(True, which='minor', linestyle='-')
    axes[1][1].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[1][1].set_xticks([8, 9, 10, 11, 12, 13, 14, 15, 16])
    axes[1][1].set_xticklabels([8, 9, 10, 11, 12, 13, 14, 15, 16])
    sub_y_axis = y_axis[10:39]
    print("for ticks",sub_y_axis)
    axes[1][1].set_yticks(range(len(sub_y_axis)))
    sub_y_axis[0:4] = "    "       # buffer at last
    sub_y_axis[-4:] = "    "       # buffer at last
    print("for labels",sub_y_axis)
    axes[1][1].set_yticklabels(sub_y_axis)
    axes[1][1].tick_params(axis='x', which='minor', labelbottom=True)
    axes[1][1].tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[1][1].xaxis.set_minor_formatter(formatter)
    axes[1][1].tick_params(axis='x', which='minor', labelsize=6)
    axes[1][1].set_xlim(8, 16)
    axes[1][1].set_ylim(0, len(sub_y_axis))




    axes[2][1].minorticks_on()

    xa_1 =np.arange(8, 16, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[1][1].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_1)
        axes[1][1].scatter(xa_1, ya, marker=',',color='blue', s=0.3)
        
    ### ARROW DowN        
    # k = 1    
    # for i in range(len(station_dict['DN']) // 2):    
    #     if 8 <= station_dict['DN'][k][0] <= 16:
    #         axes[1].text(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - 2.3, trains_dict['DN'][i], rotation = 'vertical', fontsize=9)
    #         axes[1].arrow(station_dict['DN'][k][0], station_dict['DN'][k - 1][0], 0, 1, width = 0.005)
    #     k += 2  
        
    ### ARROW UP        
    # k = 1    
    # for i in range(len(station_dict['UP']) // 2):    
    #     if 8 <= station_dict['UP'][k][0] <= 16:
    #         axes[1].text(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1.3, trains_dict['UP'][i], rotation = 'vertical', fontsize=9)
    #         axes[1].arrow(station_dict['UP'][k][0], station_dict['UP'][k - 1][0], 0, -1, width = 0.005)
    #     k += 2
        
    axes[2][1].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[2][1].xaxis.grid(True, which='minor', linestyle='-')
    axes[2][1].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[2][1].set_xticks([8, 9, 10, 11, 12, 13, 14, 15, 16])
    axes[2][1].set_xticklabels([8, 9, 10, 11, 12, 13, 14, 15, 16])
    
    sub_y_axis = y_axis[30:]
    print("for ticks",sub_y_axis)
    axes[2][1].set_yticks(range(len(sub_y_axis)))
    sub_y_axis[0:4] = "    "       # buffer at last
    sub_y_axis[-4:] = "    "       # buffer at last
    print("for labels",sub_y_axis)
    axes[2][1].set_yticklabels(sub_y_axis)
    axes[2][1].tick_params(axis='x', which='minor', labelbottom=True)
    axes[2][1].tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[2][1].xaxis.set_minor_formatter(formatter)
    axes[2][1].tick_params(axis='x', which='minor', labelsize=6)
    axes[2][1].set_xlim(8, 16)
    axes[2][1].set_ylim(0, len(sub_y_axis))




    # Subplot 3: 16-24
    
    axes[0][2].minorticks_on()
    xa_2 = np.arange(16, 24, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[0][2].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_2)
        axes[0][2].scatter(xa_2, ya, marker=',',color='blue', s=0.3)

    ### ARROW DowN         
    # k = 1  
    # arrow_lis = []
    # for i in range(len(station_dict['DN']) // 2):    
    #     if 16 <= station_dict['DN'][k][0] <= 24:
    #         arrow_lis.append(station_dict['DN'][k][0])
    #         count = arrow_lis.count(station_dict['DN'][k][0])
    #         # print(arrow_lis)
            

    ### ARROW UP   
    # k = 1    
    # for i in range(len(station_dict['UP']) // 2):    
    #     if 16 <= station_dict['UP'][k][0] <= 24:
    #         axes[2].text(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1.3, trains_dict['UP'][i], rotation = 'vertical', fontsize=9)
    #         axes[2].arrow(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1, 0, -1, width = 0.005)
    #     k += 2    
    
    # fontsize = 7
    # offset = 2.3

    # k = 1
    # texts = []
    # i = 0
    # for _ in trains_dict['DN']:
    #     axes[2].arrow(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - 1, 0, 1, width = 0.005)
    #     texts.append(axes[2].text(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - offset, trains_dict['DN'][i], rotation='vertical', fontsize=fontsize))
        
    #     x_positions = [station_dict['DN'][k][0], station_dict['DN'][k][0]]
    #     y_positions = [station_dict['DN'][k - 1][0] - offset, station_dict['DN'][k - 1][0] - offset - 0.5]        
    #     k += 2
    #     i += 1
   
    # adjust_text(texts, ax=axes[2], expand=(0.5, 0.5), time_lim=1, force_text=(1,0))
    
    axes[0][2].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[0][2].xaxis.grid(True, which='minor', linestyle='-')
    axes[0][2].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[0][2].set_xticks([16, 17, 18, 19, 20, 21, 22, 23, 24])
    axes[0][2].set_xticklabels([16, 17, 18, 19, 20, 21, 22, 23, 24])
    sub_y_axis = y_axis[0:19]
    print("for tick",sub_y_axis)
    axes[0][0].set_yticks(range(len(sub_y_axis)))
    sub_y_axis[-4:] = "    "       # buffer at last
    print("for before",sub_y_axis)
    axes[0][2].set_yticklabels(sub_y_axis)
    axes[0][2].tick_params(axis='x', which='minor', labelbottom=True)
    axes[0][2].tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[0][2].xaxis.set_minor_formatter(formatter)
    axes[0][2].tick_params(axis='x', which='minor', labelsize=6)
    axes[0][2].set_xlim(16, 24)
    axes[0][2].set_ylim(0, len(sub_y_axis))
    



    
    axes[1][2].minorticks_on()
    xa_2 = np.arange(16, 24, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[0][2].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_2)
        axes[0][2].scatter(xa_2, ya, marker=',',color='blue', s=0.3)


    axes[1][2].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[1][2].xaxis.grid(True, which='minor', linestyle='-')
    axes[1][2].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[1][2].set_xticks([16, 17, 18, 19, 20, 21, 22, 23, 24])
    axes[1][2].set_xticklabels([16, 17, 18, 19, 20, 21, 22, 23, 24])
    sub_y_axis = y_axis[10:39]
    print("for ticks",sub_y_axis)
    axes[1][2].set_yticks(range(len(sub_y_axis)))
    sub_y_axis[0:4] = "    "       # buffer at last
    sub_y_axis[-4:] = "    "       # buffer at last
    print("for labels",sub_y_axis)
    axes[1][2].set_yticklabels(sub_y_axis)
    axes[1][2].tick_params(axis='x', which='minor', labelbottom=True)
    axes[1][2].tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[1][2].xaxis.set_minor_formatter(formatter)
    axes[1][2].tick_params(axis='x', which='minor', labelsize=6)
    axes[1][2].set_xlim(16, 24)
    axes[1][2].set_ylim(0, len(sub_y_axis))



    axes[2][2].minorticks_on()
    xa_2 = np.arange(16, 24, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[0][2].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_2)
        axes[0][2].scatter(xa_2, ya, marker=',',color='blue', s=0.3)


    axes[2][2].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[2][2].xaxis.grid(True, which='minor', linestyle='-')
    axes[2][2].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[2][2].set_xticks([16, 17, 18, 19, 20, 21, 22, 23, 24])
    axes[2][2].set_xticklabels([16, 17, 18, 19, 20, 21, 22, 23, 24])
    sub_y_axis = y_axis[30:]
    print("for ticks",sub_y_axis)
    axes[2][2].set_yticks(range(len(sub_y_axis)))
    sub_y_axis[0:4] = "    "       # buffer at last
    sub_y_axis[-4:] = "    "       # buffer at last
    print("for labels",sub_y_axis)
    axes[2][2].set_yticklabels(sub_y_axis)
    axes[2][2].tick_params(axis='x', which='minor', labelbottom=True)
    axes[2][2].tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[2][2].xaxis.set_minor_formatter(formatter)
    axes[2][2].tick_params(axis='x', which='minor', labelsize=6)
    axes[2][2].set_xlim(16, 24)
    axes[2][2].set_ylim(0, len(sub_y_axis))


    # Subplot 4: 24-31
       
    axes[3][0].minorticks_on()
    xa_3 = np.arange(24, 32, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[3][0].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_3)
        axes[3][0].scatter(xa_3, ya, marker=',',color='blue', s=0.3)
        
        
    # ### ARROW DowN       
    # # k = 1    
    # # for i in range(len(station_dict['DN']) // 2):    
    # #     if 24 <= station_dict['DN'][k][0] <= 32:
    # #         axes[3].text(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - 2.3, trains_dict['DN'][i], rotation = 'vertical', fontsize=9)
    # #         axes[3].arrow(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - 1, 0, 1, width = 0.005)
    # #     k += 2
        
    # ### ARROW UP        
    # # k = 1    
    # # for i in range(len(station_dict['UP']) // 2):    
    # #     if 24 <= station_dict['UP'][k][0] <= 32:
    # #         axes[3].text(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1.3, trains_dict['UP'][i], rotation = 'vertical', fontsize=9)
    # #         axes[3].arrow(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1, 0, -1, width = 0.005)
    # #     k += 2     
        
    axes[3][0].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[3][0].xaxis.grid(True, which='minor', linestyle='-')
    axes[3][0].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[3][0].set_xticks([24,25,26,27,28,29,30,31,32])
    axes[3][0].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
    sub_y_axis = y_axis[0:19]
    print("for tick",sub_y_axis)
    axes[3][0].set_yticks(range(len(sub_y_axis)))
    sub_y_axis[-4:] = "    "       # buffer at last
    print("for before",sub_y_axis)
    axes[3][0].set_yticklabels(sub_y_axis)
    axes[3][0].tick_params(axis='x', which='minor', labelbottom=True)
    axes[3][0].tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[3][0].xaxis.set_minor_formatter(formatter)
    axes[3][0].tick_params(axis='x', which='minor', labelsize=6)
    axes[3][0].set_xlim(24, 32)
    axes[3][0].set_ylim(0, len(sub_y_axis))
    
    

    
    axes[3][1].minorticks_on()
    xa_3 = np.arange(24, 32, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[3][1].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_3)
        axes[3][1].scatter(xa_3, ya, marker=',',color='blue', s=0.3)
    
    axes[3][1].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[3][1].xaxis.grid(True, which='minor', linestyle='-')
    axes[3][1].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[3][1].set_xticks([24,25,26,27,28,29,30,31,32])
    axes[3][1].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
    sub_y3ax1s = y_axis[10:39]
    print("for ticks",sub_y_axis)
    axes[3][1].set_yticks(range(len(sub_y_axis)))
    sub_y_axis[0:4] = "    "       # buffer at last
    sub_y_axis[-4:] = "    "       # buffer at last
    print("for labels",sub_y_axis)
    axes[3][1].set_yticklabels(sub_y_axis)
    axes[3][1].tick_params(axis='x', which='minor', labelbottom=True)
    axes[3][1].tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[3][1].xaxis.set_minor_formatter(formatter)
    axes[3][1].tick_params(axis='x', which='minor', labelsize=6)
    axes[3][1].set_xlim(24, 32)
    axes[3][1].set_ylim(0, len(sub_y_axis))


     
    axes[3][2].minorticks_on()
    xa_3 = np.arange(24, 32, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[3][2].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_3)
        axes[3][2].scatter(xa_3, ya, marker=',',color='blue', s=0.3)
    
    axes[3][2].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[3][2].xaxis.grid(True, which='minor', linestyle='-')
    axes[3][2].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[3][2].set_xticks([24,25,26,27,28,29,30,31,32])
    axes[3][2].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
    sub_y3ax2s = y_axis[30:]
    print("for ticks",sub_y_axis)
    axes[3][2].set_yticks(range(len(sub_y_axis)))
    sub_y_axis[0:4] = "    "       # buffer at last
    sub_y_axis[-4:] = "    "       # buffer at last
    print("for labels",sub_y_axis)
    axes[3][2].set_yticklabels(sub_y_axis)
    axes[3][2].tick_params(axis='x', which='minor', labelbottom=True)
    axes[3][2].tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[3][2].xaxis.set_minor_formatter(formatter)
    axes[3][2].tick_params(axis='x', which='minor', labelsize=6)
    axes[3][2].set_xlim(24, 32)
    axes[3][2].set_ylim(0, len(sub_y_axis))






    plt.tight_layout()
#     for me, ax in enumerate(axes):
#         ax.set_title(f"Subplot {me+1}")
#         # Save each subplot as a separate PDF
#         plt.savefig(f"subplot_{me+1}.pdf")
    fig.savefig(
    "frac0.pdf",
    bbox_inches=mtransforms.Bbox([[0, 0.75], [1,1]]).transformed(
        fig.transFigure - fig.dpi_scale_trans
    ),format="pdf")
    fig.savefig(
    "frac1.pdf",
    bbox_inches=mtransforms.Bbox([[0, 0.5], [1, 0.75]]).transformed(
        fig.transFigure - fig.dpi_scale_trans
    ),format="pdf")
    fig.savefig(
    "frac2.pdf",
    bbox_inches=mtransforms.Bbox([[0, 0.25], [1, 0.5]]).transformed(
        fig.transFigure - fig.dpi_scale_trans
    ),format="pdf")
    fig.savefig(
    "frac3.pdf",
    bbox_inches=mtransforms.Bbox([[0, 0], [1, 0.25]]).transformed(
        fig.transFigure - fig.dpi_scale_trans
    ),format="pdf")


    print("saved-------------------------")
    # for i, ax in enumerate(axes.flat):
    #     ax.set_title('Plot {}'.format(i+1))
    #     plt.savefig('subplot_{}.pdf'.format(i+1), format="pdf")
    #     ax.clear()
    plt.show()
