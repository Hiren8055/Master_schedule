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


    # Subplot 1: 0-8
    def plot(p,q,arr,a,b,c,d,e,f):
        axes[p][q].minorticks_on()

        # ##print('station_dict : ', station_dict)
        # xa_0 = np.linspace(0, 8, 200)
        xa_0 = np.arange(0, 8, 0.03333)
        for key, arr_2d in station_dict.items():
            for i in range(0, len(arr_2d), 2):
                arr_minus = np.array(arr_2d[i+1])
                arr_minus = arr_minus - 24
                axes[p][q].plot(arr_minus, arr_2d[i], color='red')
                axes[p][q].plot(arr_2d[i+1], arr_2d[i], color='red')

        for i in range(len(y_axis)):
            y_index = y_axis[i]
            ya = [y_index] * len(xa_0)
            axes[p][q].scatter(xa_0, ya, marker=',',color='blue', s=0.3)
            
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
        
        axes[p][q].xaxis.grid(True, which='major', linestyle='-', color='black')
        axes[p][q].xaxis.grid(True, which='minor', linestyle='-')
        axes[p][q].xaxis.set_minor_locator(MultipleLocator(10 / 60))
        axes[p][q].set_xticks(arr)
        axes[p][q].set_xticklabels(arr)
        print("length of y_axis",len(y_axis))
        # slicing for subplots
        sub_y_axis = y_axis[a:b]
        axes[p][q].set_ylim(c, d)
        print("sub 0 0", sub_y_axis)
        ##print("for tick",sub_y_axis)
        print("range",range(len(sub_y_axis)))
        axes[p][q].set_yticks(range(len(sub_y_axis)))
        # sub_y_axis[-4:] = "    "       # buffer at last
        #print("for before fnkg",sub_y_axis)
        
        axes[p][q].set_yticklabels(sub_y_axis)
        axes[p][q].tick_params(axis='x', which='minor', labelbottom=True)
        axes[p][q].tick_params(labeltop=True, labelright=True)

        minor_labels = ["10", "20", "30", "40", "50"] * 8
        minor_labels.insert(0, "")
        formatter = FixedFormatter(minor_labels)
        axes[p][q].xaxis.set_minor_formatter(formatter)
        axes[p][q].tick_params(axis='x', which='minor', labelsize=6)
        axes[p][q].set_xlim(e,f)  

    arr1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    arr2 = [8, 9, 10, 11, 12, 13, 14, 15, 16]
    arr3 = [16, 17, 18, 19, 20, 21, 22, 23, 24]

    #plot(axes[i],[j],xticklables,yaxis,ylim,xlim)
    
    plot(0,0,arr1,4,9,0,15,0,8)
    plot(1,0,arr1,10,39,0,19,0,8)   
    plot(2,0,arr1,30,49,0,19,0,8) 

    plot(0,1,arr2,4,9,0,15,8,16)
    plot(1,1,arr2,10,39,0,19,8,16)   
    plot(2,1,arr2,30,49,0,19,8,16)

    plot(0,2,arr3,4,9,0,15,16,24)
    plot(1,2,arr3,10,39,0,19,16,24)   
    plot(2,2,arr3,30,49,0,19,16,24)
    
         
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



