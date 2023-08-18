import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedFormatter
import copy
import matplotlib.transforms as mtransforms


def add_lables(new_dict, train_dictionary):
    """Add lables in dictionary"""

    for key in new_dict:
        k = 0
        # range_ = (2 * len(new_dict[key]) - int(1/2 * len(new_dict[key]))) // 3
        range_ = len(new_dict[key]) // 2
        for i in range(range_):
            new_dict[key].insert(k, str(train_dictionary[key][i]))
            k += 3 
    return new_dict

def sorting_array(new_dict):
    """ Sorting in ascending and decending order"""

    # for key in new_dict:
    pairs = []
    k = 1
    for i in range(len(new_dict['UPDN']) // 3):
        x = new_dict['UPDN'][k]
        y = new_dict['UPDN'][k+1]
        z = new_dict['UPDN'][k - 1]
        pairs.append([z, x, y])
        k += 3
    pairs.sort(key=lambda pair: pair[1][0])

    sorted_list = [elem for pair in pairs for elem in pair]
    new_dict['UPDN'] = sorted_list

    return new_dict

def extract_first_elem(new_dict):
    """Extracting first element of array  """

    collision_updn = [[], []] # Extracting first element of x and y

    k = 1 
    for i in range(len(new_dict["UPDN"]) // 3):
            collision_updn[0].append(new_dict['UPDN'][k + 1][0])
            collision_updn[1].append(new_dict['UPDN'][k][0])
            k += 3 

    new_data = []
    for i in range(len(collision_updn[0])):
        new_data.append([collision_updn[0][i], collision_updn[1][i]])
    new_data.sort(key=lambda row: (row[1], row[0]))

    data1 = new_data.copy()

    new_data0 = [data1[i][0] for i in range(len(new_data))]
    new_data1 = [data1[i][1] for i in range(len(new_data))]
    new_data = [new_data0, new_data1]
    collision_updn = new_data.copy()

    print('collision updn: ', collision_updn)

    return collision_updn

def extract_last_elem(new_dict):
    """Extracting first element of array  """
    collision_updn_for_last = [[], []] # Extracting last element of x and y
    k = 1 
    for i in range(len(new_dict["UPDN"]) // 3):
            collision_updn_for_last[0].append(new_dict['UPDN'][k + 1][-1])
            collision_updn_for_last[1].append(new_dict['UPDN'][k][-1])
            k += 3 
    print('collision updn_for_last: before', collision_updn_for_last)
    new_data = []
    for i in range(len(collision_updn_for_last[0])):
        new_data.append([collision_updn_for_last[0][i], collision_updn_for_last[1][i]])
    new_data.sort(key=lambda row: (row[1], row[0]))            

    data1 = new_data.copy()

    new_data0 = [data1[i][0] for i in range(len(new_data))]
    new_data1 = [data1[i][1] for i in range(len(new_data))]
    new_data = [new_data0, new_data1]
    collision_updn_for_last = new_data.copy()

    print("collision_updn_for_last: ", collision_updn_for_last)
    return collision_updn_for_last

def is_sorted_ascending(lst):
    """this function checkes the list is sorted in ascending or not if yes then it is 'DN' list"""
    return lst == sorted(lst)
# Subplot 1: 0-8
def plot(index_0,index_1,arr,start_sub_y_axis,end_sub_y_axis,ylim_start,ylim_end,xlim_start,xlim_end, axes, station_dict, y_axis):
    axes[index_0][index_1].minorticks_on()

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
    # sub_y_axis = Reverse(sub_y_axis)
    # print(sub_y_axis)
    axes[index_0][index_1].set_ylim(start_sub_y_axis,end_sub_y_axis)
    # print(start_sub_y_axis,end_sub_y_axis)
    # print(range(start_sub_y_axis,end_sub_y_axis))
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
    axes[index_0][index_1].invert_yaxis()

def plot_trains(station_dict, y_axis, y_labes,trains_dict):
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10, 50))
    # have to make  3 x 3 grid
    fig.set_figheight(100)
# set width of each subplot as 8
    fig.set_figwidth(100)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            for j in range(len(arr_2d[i])):
                arr_2d[i][j] = y_axis.index(arr_2d[i][j])
    dup_train_dict = copy.deepcopy(trains_dict)


######################################################################################################    
    arr1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    arr2 = [8, 9, 10, 11, 12, 13, 14, 15, 16]
    arr3 = [16, 17, 18, 19, 20, 21, 22, 23, 24]
    
#   (index_0, index_1, arr, start_sub_y_axis, end_sub_y_axis, ylim_start, ylim_end, xlim_start, xlim_end)
    plot(0,0,arr1,0,11,      0,15,        0,8, axes, station_dict, y_axis)
    plot(1,0,arr1,10,31,    0,19,        0,8, axes, station_dict, y_axis)   
    plot(2,0,arr1,30,45,    0,19,        0,8, axes, station_dict, y_axis) 

    plot(0,1,arr2,0,11,     0,15,        8,16, axes, station_dict, y_axis)
    plot(1,1,arr2,10,31,  0,19,        8,16, axes, station_dict, y_axis)   
    plot(2,1,arr2,30,45,   0,19,        8,16, axes, station_dict, y_axis)

    plot(0,2,arr3,0,11,     0,15,       16,24, axes, station_dict, y_axis)
    plot(1,2,arr3,10,31,   0,19,       16,24, axes, station_dict, y_axis)   
    plot(2,2,arr3,30,45,   0,19,       16,24, axes, station_dict, y_axis)

#########################################################################################
    def plot_labels():
        new_dict = copy.deepcopy(station_dict)
 
        """ Called a func"""
        new_dict = add_lables(new_dict, trains_dict)
        
        new_dict['UPDN'] = new_dict['UP'] + new_dict['DN']
            
        """ Called a func"""
        new_dict = sorting_array(new_dict)

        """ Called a func"""        
        collision_updn_for_last = extract_last_elem(new_dict)

        """ Called a func"""
        collision_updn= extract_first_elem(new_dict)
        # print("printing collsion array after calling ", collision_updn)
    ########################################## collision text for up and down #################################################
    ####################################################### UP Text ###########################################################
        # def collision_text_updn(collision_updn, collision_updn_for_last, new_dict):   
        def collision_text_updn(collision_updn,  new_dict):   
            """ this function takes cares in overlapping of labels"""
            """ Variables Declaration"""
            k = 1
            last_y = 0
            # print("value of collision array are: ", collision_updn)
            dup_x = np.array(collision_updn[0])        # having x co-ordinates      
            # print("value of dupx are: ", dup_x)
            dup_y = np.array(collision_updn[1])        # having y co-ordinates      
            previous_x, previous_y= 0, 0
            label_var = ''
            y_overlap_both_up = 0
            y_buffer_both_up = 0

            for i in range(len(new_dict['UPDN']) // 3):
                
                # print('i am printing i: ', i)
                # print('dup_x: ', dup_x)
                x = dup_x[0]
                y = dup_y[0]
                
                dup_x = np.delete(dup_x, 0)
                dup_y = np.delete(dup_y, 0)

                y_last = new_dict['UPDN'][k][-1] 
                x_last = new_dict['UPDN'][k + 1][-1] 

                range_of_x = x + 0.12            # 0.7 is x size of labels
                range_of_y = y + 0.9

                # if i == 0:                       # NOTE: THIS IS REQ
                #     overlap_increment = i

                # if len(dup_x[dup_x < range_of_x]) == 0 or len(dup_y[dup_y < range_of_y]) == 0:     # NOTE: IF IS REQUIRED
                #     if y == last_y :
                #         # axes[2].text(x + overlap_increment, y - 2.5, trains_dict['DN'][i], rotation = 'vertical', fontsize=9)
                #         axes[index_0][index_1].text(x + overlap_increment, y + 1, new_dict['UP'][k - 1], rotation = 'vertical', fontsize=9)
                #         # print("I am in FIRST shifting plot ", new_dict['DN'][k - 1], x)    
                #     else:
                #     #     ## normal text
                #         axes[index_0][index_1].text(x, y + 1, new_dict['UP'][k - 1], rotation = 'vertical', fontsize=9) 
                #         overlap_increment = 0   
                #         # print("I am in normal plot ", new_dict['DN'][k - 1], x)
                # else:              
                #     ## perform shifting
                #     axes[index_0][index_1].text(x + overlap_increment, y + 1, new_dict['UP'][k - 1], rotation = 'vertical', fontsize=9) 
                #     # print("I am in shifting plot ", new_dict['DN'][k - 1], x)                
                #     overlap_increment += 0.12   
                #     last_y = y
                # print("this",x, y + 1, new_dict['UP'][k - 1])               # NOTE: INSIDE IF
                # axes[0][0].text(x, y + 1, new_dict['UP'][k - 1], rotation = 'vertical', fontsize=9) 

    #-------------------------FOR LABELS
                def add_arrow_labels(x, y):
                    inx, iny = 0, 0   #NOTE: not necessary
                    # for 0, 0
                    if (0 <= x < 8 and 0 <= y <= 11 ) :
                        # print("condition triggered for label")
                        inx = 0;iny = 0  
                    elif (24 <= x <= 32 and 0 <= y <= 11):
                        # print("condition triggered for label MINUSING")
                        x = x - 24
                        # inx = 0;iny = 0
                    # for 0, 1
                    elif (8 <= x < 16 and 0 <= y <= 11) :
                        # print("condition triggered for label")
                        inx = 0;iny = 1
                    # for 0, 2
                    elif (16 <= x <= 24 and 0 <= y <= 11) :
                        # print("condition triggered for label")
                        inx = 0;iny = 2
                    # for 1, 0
                    elif (0 <= x < 8 and 11 < y <= 31) :
                        # print("condition triggered for label")
                        inx = 1;iny = 0
                    elif (24 <= x <= 32 and 11 < y <= 31):
                        # print("condition triggered for label MINUSING")
                        x = x - 24
                        inx = 1;iny = 0
                    # for 1, 1
                    elif (8 <= x < 16 and 11 < y <= 31) :
                        # print("condition triggered for label")
                        inx = 1;iny = 1
                    # for 1, 2
                    elif (16 <= x <= 24 and 11 < y <= 31) :
                        # print("condition triggered for label")
                        inx = 1;iny = 2
                    # for 2, 0
                    elif (0 <= x < 8 and 31 < y <= 45) :
                        # print("condition triggered for label")
                        inx = 2;iny = 0
                    elif (24 <= x <= 32 and 31 < y <= 45):
                        # print("condition triggered for label MINUSING")
                        x = x - 24
                        inx = 2;iny = 0
                    # for 2, 1
                    elif (8 <= x < 16 and 31 < y <= 45) :
                        # print("condition triggered for label")
                        inx = 2;iny = 1
                    # for 2, 2
                    elif (16 <= x <= 24 and 31 < y <= 45) :
                        # print("condition triggered for label")
                        inx = 2;iny = 2 
                    return inx, iny, x, y

                    """ This is for 'DOWN' """
                if is_sorted_ascending(new_dict['UPDN'][k]) and len(new_dict['UPDN'][k + 1]) != 1:       
                    c = 0 
                    """Label for end"""
                    inx, iny, x, y = add_arrow_labels(x, y)
                    axes[inx][iny].text(x, y - 0.7, new_dict['UPDN'][k - 1], rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
                    axes[inx][iny].arrow(x, y, 0, -0.5, width = 0.005, clip_on = False)

                    """Label for End"""
                    inx, iny, x_last, y_last = add_arrow_labels(x_last, y_last)
                    axes[inx][iny].text(x_last, y_last + 1, new_dict['UPDN'][k - 1], rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
                    axes[inx][iny].arrow(x_last, y_last, 0, 0.5, head_width = 0, width = 0.005, clip_on = False) 

                    """ This is for 'UP' """
                else:
                    c = 1
                    """Label for start"""
                    """CASE 1: ABOIDING OVERLAPPING FOR BOTH UP"""
                    if x == previous_x and y == previous_y:
                        label_var = '/'
                        len_of_labels = len(new_dict['UPDN'][k - 1])
                        y_buffer_both_up = y_buffer_both_up + (0.06 * len_of_labels)
                        """y_overlap_both_up is y axis for text which is different in arrows y axis that is original 'y' """
                        y_overlap_both_up = y + y_buffer_both_up 
                    else:
                        label_var = ''
                        y_buffer_both_up = 0
                        y_overlap_both_up = y + y_buffer_both_up                         

                    label = new_dict['UPDN'][k - 1] + label_var

                    inx, iny, x, y = add_arrow_labels(x, y)
                    # print('value of both y are: ', y, y_overlap_both_up)
                    axes[inx][iny].text(x, y_overlap_both_up + 0.8, label, rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
                    axes[inx][iny].arrow(x, y, 0, 0.5, width = 0.005, clip_on = False)

                    """Label for End"""
                    inx, iny, x_last, y_last = add_arrow_labels(x_last, y_last)
                    axes[inx][iny].text(x_last, y_last - 0.6, new_dict['UPDN'][k - 1], rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
                    axes[inx][iny].arrow(x_last, y_last, 0, - 0.5, head_width = 0, width = 0.005, clip_on = False)

                # for case 1
                if c:
                    previous_x, previous_y = x, y
                ###############################################################################
                k += 3
        # collision_text_updn(collision_updn, collision_updn_for_last, new_dict)  
        collision_text_updn(collision_updn, new_dict)  

    plot_labels() 
####################################################################################################################
    plt.tight_layout()
#     for me, ax in enumerate(axes):
#         ax.set_title(f"Subplot {me+1}")
#         # Save each subplot as a separate PDF
#         plt.savefig(f"subplot_{me+1}.pdf")
    def saving_pdf():
        buf = 0.001
        fig.savefig(
        "frac00.pdf",
        bbox_inches = mtransforms.Bbox([[0, 0.666], [0.335,1]]).transformed( # [[xmin, ymin], [xmax, ymax]]
            fig.transFigure - fig.dpi_scale_trans
        ),format="pdf")
        fig.savefig(
        "frac01.pdf",
        bbox_inches = mtransforms.Bbox([[0.335 - buf, 0.666], [0.667,1]]).transformed( # [[xmin, ymin], [xmax, ymax]]
            fig.transFigure - fig.dpi_scale_trans
        ),format="pdf")
        fig.savefig(
        "frac02.pdf",
        bbox_inches = mtransforms.Bbox([[0.667, 0.666], [1.002,1]]).transformed( # [[xmin, ymin], [xmax, ymax]]
            fig.transFigure - fig.dpi_scale_trans
        ),format="pdf")




        fig.savefig(
        "frac10.pdf",
        bbox_inches=mtransforms.Bbox([[0, 0.34 ], [0.335, 0.666 ]]).transformed( # [[xmin, ymin], [xmax, ymax]]
            fig.transFigure - fig.dpi_scale_trans
        ),format="pdf")
        fig.savefig(
        "frac11.pdf",
        bbox_inches=mtransforms.Bbox([[0.335 - buf, 0.34], [0.667, 0.666]]).transformed( # [[xmin, ymin], [xmax, ymax]]
            fig.transFigure - fig.dpi_scale_trans
        ),format="pdf")
        fig.savefig(
        "frac12.pdf",
        bbox_inches=mtransforms.Bbox([[0.667, 0.34 ], [1.002, 0.666 ]]).transformed( # [[xmin, ymin], [xmax, ymax]]
            fig.transFigure - fig.dpi_scale_trans
        ),format="pdf")




        # fig.savefig(
        # "frac2.pdf",
        # bbox_inches=mtransforms.Bbox([[0, 0.25], [1, 0.5]]).transformed(
        #     fig.transFigure - fig.dpi_scale_trans
        # ),format="pdf")

        fig.savefig(
        "frac20.pdf",
        bbox_inches=mtransforms.Bbox([[0, 0], [0.335, 0.34-3*buf]]).transformed( # [[xmin, ymin], [xmax, ymax]]
            fig.transFigure - fig.dpi_scale_trans
        ),format="pdf")
        fig.savefig(
        "frac21.pdf",
        bbox_inches=mtransforms.Bbox([[0.335 - buf, 0], [0.667, 0.34-3*buf]]).transformed( # [[xmin, ymin], [xmax, ymax]]
            fig.transFigure - fig.dpi_scale_trans
        ),format="pdf")
        fig.savefig(
        "frac22.pdf",
        bbox_inches=mtransforms.Bbox([[0.667, 0], [1.002, 0.34-3*buf]]).transformed( # [[xmin, ymin], [xmax, ymax]]
            fig.transFigure - fig.dpi_scale_trans
        ),format="pdf")
    
    # Make the boolean vallue false if saving is not required it makes the process slow
    saving = False
    if saving == True:
        saving_pdf()
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


######################################################## RECYCLE BIN ######################################################################
# 1. ############################## collision text function ##########################################

        # def collision_text(collision_up, new_dict):   
        #     """still only done for "DN" """
        #     k = 1
        #     last_y = 0
        #     dup_x = np.array(collision_up[0])
        #     dup_y = np.array(collision_up[1])
        #     print(len(new_dict['UP']) // 3)
        #     for i in range(len(new_dict['UP']) // 3): 
        #         # print("dup x and y are: ", dup_x, dup_y)
        #         try:
        #             dup_x = np.delete(dup_x, 0)
        #             dup_y = np.delete(dup_y, 0)
        #         except Exception as e:
        #             pass
        #         y = new_dict['UP'][k][0]
        #         x = new_dict['UP'][k + 1][0]            #19.67 + 0.7 = 20.37
        #         # print("x and y are in all i : ",i , x, y) 
        #         # print(collision_up)
        #         ## Define the range to check
        #         range_of_x = x + 0.12            # 0.7 is x size of labels
        #         range_of_y = y + 0.9

        #         if i == 0:
        #             overlap_increment = i

        #         if len(dup_x[dup_x < range_of_x]) == 0 or len(dup_y[dup_y < range_of_y]) == 0:
        #         #     if y == last_y :
        #         #         # axes[2].text(x + overlap_increment, y - 2.5, trains_dict['DN'][i], rotation = 'vertical', fontsize=9)
        #         #         axes[index_0][index_1].text(x + overlap_increment, y + 1, new_dict['UP'][k - 1], rotation = 'vertical', fontsize=9)
        #         #         # print("I am in FIRST shifting plot ", new_dict['DN'][k - 1], x)    
        #         #     else:
        #         #     #     ## normal text
        #         #         axes[index_0][index_1].text(x, y + 1, new_dict['UP'][k - 1], rotation = 'vertical', fontsize=9) 
        #         #         overlap_increment = 0   
        #         #         # print("I am in normal plot ", new_dict['DN'][k - 1], x)
        #         # else:              
        #         #     ## perform shifting
        #         #     axes[index_0][index_1].text(x + overlap_increment, y + 1, new_dict['UP'][k - 1], rotation = 'vertical', fontsize=9) 
        #         #     # print("I am in shifting plot ", new_dict['DN'][k - 1], x)                
        #         #     overlap_increment += 0.12   
        #         #     last_y = y
        #             print("this",x, y + 1, new_dict['UP'][k - 1])
        #             axes[index_0][index_1].text(x, y + 1, new_dict['UP'][k - 1], rotation = 'vertical', fontsize=9) 
        #         k += 3
        
        # collision_text(collision_up, new_dict)         

####################################################################################################################        
    #printing first element
    # global elements
    # elements = [[], []]
    # k = 1
    # for i in range(len(new_dict["UP"]) // 3):
    #     elements[0].append(new_dict['UP'][k + 1][0])
    #     elements[1].append(new_dict['UP'][k][0])
    #     k += 3
    # for j in range(len(new_dict["DN"]) // 3):
    #     elements[0].append(new_dict['DN'][k + 1][0])
    #     elements[1].append(new_dict['DN'][k][0])
    #     k += 3        

# After this collision array is there
####################################################################################################################
