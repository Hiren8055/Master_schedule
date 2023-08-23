import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedFormatter
import copy
import matplotlib.transforms as mtransforms
from collide_labels import collision_text_updn

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

def add_keys(new_dict):
    """Add keys in dictionary"""
    for key in new_dict:
        k = 1
        for i in range(len(new_dict[key]) // 3):
            new_dict[key].insert(k + 2, key)
            k += 4
    return new_dict

def extract_first_elem(new_dict):
    """Extracting first element of array  """

    collision_updn = [[], [], [], [], []] # Extracting first element of x and y

    k = 1 
    for i in range(len(new_dict["UP"]) // 4):
            collision_updn[0].append(new_dict['UP'][k - 1])
            if new_dict['DN'][k + 1][-1] >= 24: 
                collision_updn[1].append(new_dict['UP'][k + 1][-1] - 24)
            else: 
                collision_updn[1].append(new_dict['UP'][k + 1][-1])            
            collision_updn[2].append(new_dict['UP'][k][0])
            k += 4

    new_data = []
    for i in range(len(collision_updn[0])):
        new_data.append([collision_updn[0][i], collision_updn[1][i], collision_updn[2][i],])
    new_data.sort(key=lambda row: (row[2], row[1]))

    data1 = new_data.copy()

    new_data0 = [data1[i][0] for i in range(len(new_data))]
    new_data1 = [data1[i][1] for i in range(len(new_data))]
    new_data2 = [data1[i][2] for i in range(len(new_data))]
    new_data = [new_data0, new_data1, new_data2]

    collision_updn = new_data.copy()
    print("extract first element: ", collision_updn)
    return collision_updn

def extract_last_elem(new_dict):
    """Extracting first element of array  """

    collision_updn_for_last = [[], [], [], [], []] # Extracting first element of x and y

    k = 1 
    for i in range(len(new_dict["DN"]) // 4):
            collision_updn_for_last[0].append(new_dict['DN'][k - 1])
            if new_dict['DN'][k + 1][-1] >= 24: 
                collision_updn_for_last[1].append(new_dict['DN'][k + 1][-1] - 24)
            else: 
                collision_updn_for_last[1].append(new_dict['DN'][k + 1][-1])
                
            collision_updn_for_last[2].append(new_dict['DN'][k][-1])
            k += 4

    new_data = []
    for i in range(len(collision_updn_for_last[0])):
        new_data.append([collision_updn_for_last[0][i], collision_updn_for_last[1][i], collision_updn_for_last[2][i]])
    new_data.sort(key=lambda row: (row[2], row[1]))

    data1 = new_data.copy()

    new_data0 = [data1[i][0] for i in range(len(new_data))]
    new_data1 = [data1[i][1] for i in range(len(new_data))]
    new_data2 = [data1[i][2] for i in range(len(new_data))]
    new_data = [new_data0, new_data1, new_data2]

    collision_updn_for_last = new_data.copy()
    print("extract last element: ", collision_updn_for_last)    
    return collision_updn_for_last


def merging_fist_and_last_element(collision_updn, collsion_updn_for_last):

    collision_merged = [[], [], [], [], []]
    for i in range(len(collsion_updn_for_last)):
        collision_merged[i] = collision_updn[i] + collsion_updn_for_last[i]

    new_data = []
    for i in range(len(collision_merged[0])):
        new_data.append([collision_merged[0][i], collision_merged[1][i], collision_merged[2][i]])
    new_data.sort(key=lambda row: (row[2], row[1]))

    data1 = new_data.copy()

    new_data0 = [data1[i][0] for i in range(len(new_data))]
    new_data1 = [data1[i][1] for i in range(len(new_data))]
    new_data2 = [data1[i][2] for i in range(len(new_data))]
    new_data = [new_data0, new_data1, new_data2]

    collision_merged = new_data.copy()

    return collision_merged

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
        
        """ Called a func"""
        new_dict = add_keys(new_dict)
        
        new_dict['UPDN'] = new_dict['UP'] + new_dict['DN']

        """ Called a func"""
        collision_updn = extract_first_elem(new_dict)

        """ Called a func"""        
        collision_updn_for_last = extract_last_elem(new_dict)

        """ Called a func"""
        collision_merged = merging_fist_and_last_element(collision_updn, collision_updn_for_last)
        # print('merged_func: ', len(collision_merged[0]), len(collision_merged[1]), len(collision_merged[2]))
        # print('merged_func: ', collision_merged)
    ########################################## collision text for up and down #################################################\
        
        collision_text_updn(collision_updn, collision_updn_for_last, collision_merged, new_dict, axes)  
        # collision_text_updn(collision_updn, new_dict)  
        def intersection(station_dict):
            # "Input with train array and output plot intersection at particular y"
            # have to use conversion function in between to convert the time and axis domain
            # have to only give the intersection in mid subplot with index 1
            
            # intercept_station = 10


            def intercept_selection_pts(y_target,index,updn):
                # add try and except in function 
                # index = 2 # have to automate for other even indexes
                
                above_intercept_station = y_target - 1
                below_intercept_station = y_target + 1
                # print(station_dict["UP"][index],station_dict["UP"][1])
                # print(station_dict["UP"][index].index(y_target))
                
                

                def find(arr1,arr2, target):
                    x,y = None, None
                    # for i in range(len(arr[0])):
                    arr = [arr1,arr2]
                    print("arr",arr)
                    for i in range(len(arr[0])):
                        # print(arr[0][i],target)
                        if arr[0][i] == target:
                            x,y =  arr[1][i], target
                    return x,y
                
                
                # find the 10 if not then look for 9 and 11
                tenth_x, tenth_y = find(station_dict[updn][index],station_dict[updn][index+1],y_target)
                print(tenth_x, tenth_y)
                if tenth_x == None:
                    ele_x,ele_y = find(station_dict[updn][index],station_dict[updn][index+1],below_intercept_station)
                    print(ele_x,ele_y)
                    if ele_x == None:
                        return False
                        # no intersection
                    else:
                        nin_x,nin_y = find(station_dict[updn][index],above_intercept_station)
                        print(nin_x,nin_y) 
                        return [[nin_x,ele_x],[nin_y,ele_y]]
                else:
                    return [tenth_x, tenth_y]

                # if station_dict[updn][index].index(intercept_station):
                #     intercept_index = station_dict[updn][index].index(intercept_station)
                # print(station_dict[updn][index+1][intercept_index])
                # have to select the index of 10 or not then go for below 10 and above 10 ie is 11
                # find 10 in list and get the index 


            def intercept(y_target, x ,y):
                # find the points for intersection
                x_target = np.interp(y_target,x,y)
                print("The x-value for y = 18 virar is:", x_target)
                return x_target, y_target

            def add_arrow_labels_intercept(x, y):
                # selection of graph for inx and iny
                inx, iny = 0, 0   #NOTE: not necessary
                # for 0, 0
                if (0 <= x < 8 and 0 <= y <= 9 ) :
                    # print("condition triggered for label")
                    inx = 0;iny = 0 
                    print(x,y) 
                elif (24 <= x <= 32 and 0 <= y <= 9):
                    # print("condition triggered for label MINUSING")
                    x = x - 24
                    # inx = 0;iny = 0
                # for 0, 1
                elif (8 <= x < 16 and 0 <= y <= 9) :
                    # print("condition triggered for label")
                    inx = 0;iny = 1
                # for 0, 2
                elif (16 <= x <= 24 and 0 <= y <= 9) :
                    # print("condition triggered for label")
                    inx = 0;iny = 2
                # for 1, 0
                elif (0 <= x < 8 and 10 <= y <= 31) :
                    # print("condition triggered for label")
                    inx = 1;iny = 0
                elif (24 <= x <= 32 and 10 <= y <= 31):
                    # print("condition triggered for label MINUSING")
                    x = x - 24
                    inx = 1;iny = 0
                # for 1, 1
                elif (8 <= x < 16 and 10 <= y <= 31) :
                    # print("condition triggered for label")
                    inx = 1;iny = 1
                # for 1, 2
                elif (16 <= x <= 24 and 10 <= y <= 31) :
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
            # have to make for every train which is going up
            # put this intersection point in bottom 
            # send the array to arpit of intersection for labels and arrow
            print("station_dict",station_dict)
            # VR 18
            def intercept_pts(updn):
                # drawing fucntion for intersecting points
                inter_plot_arr = []
                print(len(station_dict))
                # updn = "UP"
                
                if updn == "UP":
                    y_target = 30
                elif updn == "DN":
                    y_target = 10
                # try:
                arr_index = []
                for i in range(0,len(station_dict[updn]),2):
                    # print(i)
                    # trains_dict[updn][]
                    print("station_dict",station_dict[updn][i])
                    inter_arr = intercept_selection_pts(y_target,i, updn)
                    print("inter_arr",inter_arr)
                    if inter_arr == False:
                        continue    
                    elif inter_arr[1]!=y_target:
                        x_target, y_target = intercept(y_target, inter_arr[0] ,inter_arr[1])
                        inter_plot_arr.append([x_target, y_target])
                        arr_index.append(i)
                    else:
                        x_target, y_target = inter_arr[0], inter_arr[1]
                        inter_plot_arr.append([x_target, y_target])
                        arr_index.append(i)
                        
                print(len(inter_plot_arr),len(arr_index)) 
                print(arr_index)      
                print(trains_dict)
                print(len(trains_dict["UP"]))
                for i in range(len(inter_plot_arr)):
                    inx, iny,_,_ = add_arrow_labels_intercept(inter_plot_arr[i][0],inter_plot_arr[i][1])
                    # print("inx",inx, iny)
                    axes[inx][iny].plot(inter_plot_arr[i][0],inter_plot_arr[i][1], 'o-') # have to automate for all the
                    print("arr_index[i]//2",arr_index[i],arr_index[i]//2)
                    axes[inx][iny].text(inter_plot_arr[i][0], inter_plot_arr[i][1] + 1, trains_dict[updn][arr_index[i]//2], rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
                    if inx == 1 and iny==0:
                        print("intersection train",inx,iny,trains_dict[updn][i])
                    axes[inx][iny].arrow(inter_plot_arr[i][0], inter_plot_arr[i][1], 0, 0.5, head_width = 0, width = 0.005, clip_on = False)   
                # except:
                    # print("there should only two present in excel up and down")
                return inter_plot_arr
            # will have a intersection array for down and up
            # def intercept_plot(inter_plot_arr):
                                  
            
            intercept_pts("UP")
            intercept_pts("DN")
            # inter_plot_arr = inter_plot_arr_up+inter_plot_arr_dn
            # print("inter_plot_arr",inter_plot_arr)
            # intercept_plot(inter_plot_arr) 
        
        intersection(station_dict)
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
    saving = True
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
