import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedFormatter
from adjustText import adjust_text
import matplotlib.transforms as mtransforms

def plot_trains(station_dict, y_axis, y_labes,trains_dict):
    y_axis.insert(0," ")
    y_axis.insert(0,"  ")
    y_axis.insert(0,"   ")
    y_axis.insert(0,"    ")
    y_axis.append("     ")
    y_axis.append("      ")
    y_axis.append("       ")
    y_axis.append("        ")
    #print(" ")
    # #print("Trains dictionary: ", trains_dict)
    #print(" ")
# Arrow:
#     eg. axes[2].arrow(20, 25, 0, 1, width = 0.01, head_width=0.1, head_length=0.1, color = 'blue')
#     20---> x axis
#     25 --> y axis
#     1 --> size of line segment
 

    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10, 50))
    # have to make  3 x 3 grid
    fig.set_figheight(100)
# set width of each subplot as 8
    fig.set_figwidth(100)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            for j in range(len(arr_2d[i])):
                arr_2d[i][j] = y_axis.index(arr_2d[i][j])
    def Reverse(lst):
        new_lst = lst[::-1]
        return new_lst

    # Subplot 1: 0-8
    def plot(index_0,index_1,arr,start_sub_y_axis,end_sub_y_axis,ylim_start,ylim_end,xlim_start,xlim_end):
        axes[index_0][index_1].minorticks_on()

        # ##print('station_dict : ', station_dict)
        # xa_0 = np.linspace(0, 8, 200)
        xa_0 = np.arange(0, 8, 0.03333)
        for key, arr_2d in station_dict.items():
            for i in range(0, len(arr_2d), 2):
                arr_minus = np.array(arr_2d[i+1])
                arr_minus = arr_minus - 24
                axes[index_0][index_1].plot(arr_minus, arr_2d[i], color='red')
                axes[index_0][index_1].plot(arr_2d[i+1], arr_2d[i], color='red')

        for i in range(len(y_axis)):
            y_index = y_axis[i]
            ya = [y_index] * len(xa_0)
            axes[index_0][index_1].scatter(xa_0, ya, marker=',',color='blue', s=0.3)


        axes[index_0][index_1].xaxis.grid(True, which='major', linestyle='-', color='black')
        axes[index_0][index_1].xaxis.grid(True, which='minor', linestyle='-')
        axes[index_0][index_1].xaxis.set_minor_locator(MultipleLocator(10 / 60))
        axes[index_0][index_1].set_xticks(arr)
        axes[index_0][index_1].set_xticklabels(arr)
        
        sub_y_axis = y_axis[start_sub_y_axis:end_sub_y_axis]
        sub_y_axis = Reverse(sub_y_axis)
        print(sub_y_axis)
        axes[index_0][index_1].set_ylim(start_sub_y_axis,end_sub_y_axis)
        print(start_sub_y_axis,end_sub_y_axis)
        print(range(start_sub_y_axis,end_sub_y_axis))
        # axes[index_0][index_1].set_yticks(range(start_sub_y_axis,end_sub_y_axis))
        axes[index_0][index_1].set_yticks(range(start_sub_y_axis,end_sub_y_axis))
        axes[index_0][index_1].set_yticklabels(sub_y_axis)


        axes[index_0][index_1].tick_params(axis='x', which='minor', labelbottom=True)
        axes[index_0][index_1].tick_params(labeltop=True, labelright=True)
        minor_labels = ["10", "20", "30", "40", "50"] * 8
        minor_labels.insert(0, "")

        formatter = FixedFormatter(minor_labels)
        axes[index_0][index_1].xaxis.set_minor_formatter(formatter)
        axes[index_0][index_1].tick_params(axis='x', which='minor', labelsize=6)
        axes[index_0][index_1].set_xlim(xlim_start,xlim_end)  
    arr1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    arr2 = [8, 9, 10, 11, 12, 13, 14, 15, 16]
    arr3 = [16, 17, 18, 19, 20, 21, 22, 23, 24]
    
#   (index_0,index_1,arr,start_sub_y_axis,end_sub_y_axis,ylim_start,ylim_end,xlim_start,xlim_end)
    plot(0,0,arr1,4,15,      0,15,        0,8)
    plot(1,0,arr1,14,35,    0,19,        0,8)   
    plot(2,0,arr1,34,49,    0,19,        0,8) 

    plot(0,1,arr2,4,15,     0,15,        8,16)
    plot(1,1,arr2,14,35,   0,19,        8,16)   
    plot(2,1,arr2,34,49,   0,19,        8,16)

    plot(0,2,arr3,4,15,     0,15,       16,24)
    plot(1,2,arr3,14,35,   0,19,       16,24)   
    plot(2,2,arr3,34,49,   0,19,       16,24)
    
         
    plt.tight_layout()
#     for me, ax in enumerate(axes):
#         ax.set_title(f"Subplot {me+1}")
#         # Save each subplot as a separate PDF
#         plt.savefig(f"subplot_{me+1}.pdf")
    buf = 0.001
    # fig.savefig(
    # "frac00.pdf",
    # bbox_inches = mtransforms.Bbox([[0, 0.666], [0.335,1]]).transformed( # [[xmin, ymin], [xmax, ymax]]
    #     fig.transFigure - fig.dpi_scale_trans
    # ),format="pdf")
    # fig.savefig(
    # "frac01.pdf",
    # bbox_inches = mtransforms.Bbox([[0.335 - buf, 0.666], [0.667,1]]).transformed( # [[xmin, ymin], [xmax, ymax]]
    #     fig.transFigure - fig.dpi_scale_trans
    # ),format="pdf")
    # fig.savefig(
    # "frac02.pdf",
    # bbox_inches = mtransforms.Bbox([[0.667, 0.666], [1.002,1]]).transformed( # [[xmin, ymin], [xmax, ymax]]
    #     fig.transFigure - fig.dpi_scale_trans
    # ),format="pdf")




    # fig.savefig(
    # "frac10.pdf",
    # bbox_inches=mtransforms.Bbox([[0, 0.34 ], [0.335, 0.666 ]]).transformed( # [[xmin, ymin], [xmax, ymax]]
    #     fig.transFigure - fig.dpi_scale_trans
    # ),format="pdf")
    # fig.savefig(
    # "frac11.pdf",
    # bbox_inches=mtransforms.Bbox([[0.335 - buf, 0.34], [0.667, 0.666]]).transformed( # [[xmin, ymin], [xmax, ymax]]
    #     fig.transFigure - fig.dpi_scale_trans
    # ),format="pdf")
    # fig.savefig(
    # "frac12.pdf",
    # bbox_inches=mtransforms.Bbox([[0.667, 0.34 ], [1.002, 0.666 ]]).transformed( # [[xmin, ymin], [xmax, ymax]]
    #     fig.transFigure - fig.dpi_scale_trans
    # ),format="pdf")




    # # fig.savefig(
    # # "frac2.pdf",
    # # bbox_inches=mtransforms.Bbox([[0, 0.25], [1, 0.5]]).transformed(
    # #     fig.transFigure - fig.dpi_scale_trans
    # # ),format="pdf")

    # fig.savefig(
    # "frac20.pdf",
    # bbox_inches=mtransforms.Bbox([[0, 0], [0.335, 0.34-3*buf]]).transformed( # [[xmin, ymin], [xmax, ymax]]
    #     fig.transFigure - fig.dpi_scale_trans
    # ),format="pdf")
    # fig.savefig(
    # "frac21.pdf",
    # bbox_inches=mtransforms.Bbox([[0.335 - buf, 0], [0.667, 0.34-3*buf]]).transformed( # [[xmin, ymin], [xmax, ymax]]
    #     fig.transFigure - fig.dpi_scale_trans
    # ),format="pdf")
    # fig.savefig(
    # "frac22.pdf",
    # bbox_inches=mtransforms.Bbox([[0.667, 0], [1.002, 0.34-3*buf]]).transformed( # [[xmin, ymin], [xmax, ymax]]
    #     fig.transFigure - fig.dpi_scale_trans
    # ),format="pdf")


    #print("saved-------------------------")
    # for i, ax in enumerate(axes.flat):
    #     ax.set_title('Plot {}'.format(i+1))
    #     plt.savefig('subplot_{}.pdf'.format(i+1), format="pdf")
    #     ax.clear()
    plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
    plt.show()
