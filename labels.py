import numpy as np
def add_lables( new_dict, train_dictionary):
        """Add lables in dictionary"""
        for key in new_dict:
            k = 0
            # range_ = (2 * len(new_dict[key]) - int(1/2 * len(new_dict[key]))) // 3
            range_ = len(new_dict[key]) // 2
            for i in range(range_):
                
                new_dict[key].insert(k, str(train_dictionary[key][i]))
                k += 3 
        return new_dict
    
def add_keys( new_dict):
    """Add keys in dictionary"""
    for key in new_dict:
        k = 1
        for i in range(len(new_dict[key]) // 3):
            new_dict[key].insert(k + 2, key)
            k += 4
    return new_dict

def extract_up_elem(new_dict):
    """Extracting first element of array  """

    """for up start"""
    collision_updn = [[], [], []] # Extracting first element of x and y

    k = 1 
    # print(len(new_dict["DN"]+new_dict["UP"]))                                             
    # print(len(new_dict["UP"]))
    # print(len(new_dict["UP"]) // 4)
    # print(new_dict['UP'])
    for i in range(len(new_dict["UP"]) // 4):    
        # print(k)     
        # print("length: ", len(new_dict['UP'][k + 1]))
        # print("y axis", new_dict['UP'][k + 1])
        # print("last elem", new_dict['UP'][k + 1][0])  
        collision_updn[0].append(new_dict['UP'][k - 1])                                        
        if new_dict['UP'][k + 1][0] >= 24:                                                        
            collision_updn[1].append(new_dict['UP'][k + 1][0] - 24)                           
        else:                                                                                    
            collision_updn[1].append(new_dict['UP'][k + 1][0])            
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

    """for up end"""    

    collision_updn1 = [[], [], []] # Extracting first element of x and y

    k = 1 
    for i in range(len(new_dict["UP"]) // 4):         
            # print("length: ", len(new_dict['UP'][k + 1]))
            # print("y axis", new_dict['UP'][k + 1])
            # print("last elem", new_dict['UP'][k + 1][0])                                               
            collision_updn1[0].append(new_dict['UP'][k - 1])                                        
            if new_dict['UP'][k + 1][-1] >= 24:                                                        
                collision_updn1[1].append(new_dict['UP'][k + 1][-1] - 24)                           
            else:                                                                                    
                collision_updn1[1].append(new_dict['UP'][k + 1][-1])            
            collision_updn1[2].append(new_dict['UP'][k][-1])
            k += 4

    new_data = []
    for i in range(len(collision_updn1[0])):
        new_data.append([collision_updn1[0][i], collision_updn1[1][i], collision_updn1[2][i],])
    new_data.sort(key=lambda row: (row[2], row[1]))

    data1 = new_data.copy()

    new_data0 = [data1[i][0] for i in range(len(new_data))]
    new_data1 = [data1[i][1] for i in range(len(new_data))]
    new_data2 = [data1[i][2] for i in range(len(new_data))]
    new_data = [new_data0, new_data1, new_data2]

    collision_updn1 = new_data.copy()

    return collision_updn, collision_updn1    #start, end

def extract_dn_elem(new_dict):
    """Extracting first element of array  """

    """for dn end"""
    collision_updn_for_last = [[], [], []] # Extracting first element of x and y

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

    collision_updn_for_last = new_data.copy()   #down end

    """for dn start"""
    collision_updn_for_last1 = [[], [], []] # Extracting first element of x and y

    k = 1 
    for i in range(len(new_dict["DN"]) // 4):
            collision_updn_for_last1[0].append(new_dict['DN'][k - 1])
            if new_dict['DN'][k + 1][0] >= 24: 
                collision_updn_for_last1[1].append(new_dict['DN'][k + 1][0] - 24)
            else: 
                collision_updn_for_last1[1].append(new_dict['DN'][k + 1][0])
                
            collision_updn_for_last1[2].append(new_dict['DN'][k][0])
            k += 4

    new_data = []
    for i in range(len(collision_updn_for_last1[0])):
        new_data.append([collision_updn_for_last1[0][i], collision_updn_for_last1[1][i], collision_updn_for_last1[2][i]])
    new_data.sort(key=lambda row: (row[2], row[1]))

    data1 = new_data.copy()

    new_data0 = [data1[i][0] for i in range(len(new_data))]
    new_data1 = [data1[i][1] for i in range(len(new_data))]
    new_data2 = [data1[i][2] for i in range(len(new_data))]
    new_data = [new_data0, new_data1, new_data2]

    collision_updn_for_last1 = new_data.copy()   # down start

    return collision_updn_for_last1, collision_updn_for_last       #start, end


def merging_up_fist_and_dn_last_element(collision_up, collision_dn):

    collision_merged = [[], [], []]
    for i in range(len(collision_dn)):
        collision_merged[i] = collision_up[i] + collision_dn[i]

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

def merging_dn_fist_and_up_last_element( collision_up1, collision_dn1):

    collision_merged1 = [[], [], []]
    for i in range(len(collision_dn1)):
        collision_merged1[i] = collision_up1[i] + collision_dn1[i]

    new_data = []
    for i in range(len(collision_merged1[0])):
        new_data.append([collision_merged1[0][i], collision_merged1[1][i], collision_merged1[2][i]])
    new_data.sort(key=lambda row: (row[2], row[1]))

    data1 = new_data.copy()

    new_data0 = [data1[i][0] for i in range(len(new_data))]
    new_data1 = [data1[i][1] for i in range(len(new_data))]
    new_data2 = [data1[i][2] for i in range(len(new_data))]
    new_data = [new_data0, new_data1, new_data2]

    collision_merged1 = new_data.copy()

    return collision_merged1

def extract_current_axes_ue_ds(x, y):
    if (0 <= x < 8 and 0 <= y <= 29 ) :
        # print("condition triggered for label")
        inx = 0;iny = 0  
    elif (24 <= x <= 32 and 0 <= y <= 29):
        # print("condition triggered for label MINUSING")
        inx = 0;iny = 0
    # for 0, 1
    elif (8 <= x < 16 and 0 <= y <= 29) :
        # print("condition triggered for label")
        inx = 0;iny = 1
    # for 0, 2
    elif (16 <= x <= 24 and 0 <= y <= 29) :
        # print("condition triggered for label")
        inx = 0;iny = 2
    # for 1, 0
    elif (0 <= x < 8 and 29 < y <= 49) :
        # print("condition triggered for label")
        inx = 1;iny = 0
    elif (24 <= x <= 32 and 29 < y <= 49):
        # print("condition triggered for label MINUSING")
        inx = 1;iny = 0
    # for 1, 1
    elif (8 <= x < 16 and 29 < y <= 49) :
        # print("condition triggered for label")
        inx = 1;iny = 1
    # for 1, 2
    elif (16 <= x <= 24 and 29 < y <= 49) :
        # print("condition triggered for label")
        inx = 1;iny = 2
    # for 2, 0
    elif (0 <= x < 8 and 49 < y <= 63) :
        # print("condition triggered for label")
        inx = 2;iny = 0
    elif (24 <= x <= 32 and 49 < y <= 63):
        # print("condition triggered for label MINUSING")
        inx = 2;iny = 0
    # for 2, 1
    elif (8 <= x < 16 and 49 < y <= 63) :
        # print("condition triggered for label")
        inx = 2;iny = 1
    # for 2, 2
    elif (16 <= x <= 24 and 49 < y <= 63) :
        # print("condition triggered for label")
        inx = 2;iny = 2 

    if inx == 0:
        return 0.48
    elif inx == 1:
        return 0.18
    elif inx == 2:
        return 0.18
    

def extract_current_axes_us_de(x, y):
    if (0 <= x < 8 and 0 <= y <= 29 ) :
        # print("condition triggered for label")
        inx = 0;iny = 0  
    elif (24 <= x <= 32 and 0 <= y <= 29):
        # print("condition triggered for label MINUSING")
        inx = 0;iny = 0
    # for 0, 1
    elif (8 <= x < 16 and 0 <= y <= 29) :
        # print("condition triggered for label")
        inx = 0;iny = 1
    # for 0, 2
    elif (16 <= x <= 24 and 0 <= y <= 29) :
        # print("condition triggered for label")
        inx = 0;iny = 2
    # for 1, 0
    elif (0 <= x < 8 and 29 < y <= 49) :
        # print("condition triggered for label")
        inx = 1;iny = 0
    elif (24 <= x <= 32 and 29 < y <= 49):
        # print("condition triggered for label MINUSING")
        inx = 1;iny = 0
    # for 1, 1
    elif (8 <= x < 16 and 29 < y <= 49) :
        # print("condition triggered for label")
        inx = 1;iny = 1
    # for 1, 2
    elif (16 <= x <= 24 and 29 < y <= 49) :
        # print("condition triggered for label")
        inx = 1;iny = 2
    # for 2, 0
    elif (0 <= x < 8 and 49 < y <= 63) :
        # print("condition triggered for label")
        inx = 2;iny = 0
    elif (24 <= x <= 32 and 49 < y <= 63):
        # print("condition triggered for label MINUSING")
        inx = 2;iny = 0
    # for 2, 1
    elif (8 <= x < 16 and 49 < y <= 63) :
        # print("condition triggered for label")
        inx = 2;iny = 1
    # for 2, 2
    elif (16 <= x <= 24 and 49 < y <= 63) :
        # print("condition triggered for label")
        inx = 2;iny = 2 

    if inx == 0:
        return 0.48
    elif inx == 1 or inx == 2:
        return 0.18



def add_arrow_labels(x, y):
    inx, iny = 0, 0   #NOTE: not necessary
    # for 0, 0
    if (0 <= x < 8 and 0 <= y <= 29 ) :
        # print("condition triggered for label")
        inx = 0;iny = 0  
    elif (24 <= x <= 32 and 0 <= y <= 29):
        # print("condition triggered for label MINUSING")
        inx = 0;iny = 0
    # for 0, 1
    elif (8 <= x < 16 and 0 <= y <= 29) :
        # print("condition triggered for label")
        inx = 0;iny = 1
    # for 0, 2
    elif (16 <= x <= 24 and 0 <= y <= 29) :
        # print("condition triggered for label")
        inx = 0;iny = 2
    # for 1, 0
    elif (0 <= x < 8 and 29 < y <= 49) :
        # print("condition triggered for label")
        inx = 1;iny = 0
    elif (24 <= x <= 32 and 29 < y <= 49):
        # print("condition triggered for label MINUSING")
        inx = 1;iny = 0
    # for 1, 1
    elif (8 <= x < 16 and 29 < y <= 49) :
        # print("condition triggered for label")
        inx = 1;iny = 1
    # for 1, 2
    elif (16 <= x <= 24 and 29 < y <= 49) :
        # print("condition triggered for label")
        inx = 1;iny = 2
    # for 2, 0
    elif (0 <= x < 8 and 49 < y <= 63) :
        # print("condition triggered for label")
        inx = 2;iny = 0
    elif (24 <= x <= 32 and 49 < y <= 63):
        # print("condition triggered for label MINUSING")
        inx = 2;iny = 0
    # for 2, 1
    elif (8 <= x < 16 and 49 < y <= 63) :
        # print("condition triggered for label")
        inx = 2;iny = 1
    # for 2, 2
    elif (16 <= x <= 24 and 49 < y <= 63) :
        # print("condition triggered for label")
        inx = 2;iny = 2 
    return inx, iny, x, y


def intersection(station_dict, axes, trains_dict, artist_list):
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
            # print("arr",arr)
            for i in range(len(arr[0])):
                # print(arr[0][i],target)
                if arr[0][i] == target:
                    x,y =  arr[1][i], target
            return x,y
        
        
        # find the 10 if not then look for 9 and 11
        tenth_x, tenth_y = find(station_dict[updn][index],station_dict[updn][index+1],y_target)
        # print(tenth_x, tenth_y)
        if tenth_x == None:
            ele_x,ele_y = find(station_dict[updn][index],station_dict[updn][index+1],below_intercept_station)
            # print(ele_x,ele_y)
            if ele_x == None:
                return False
                # no intersection
            else:
                nin_x,nin_y = find(station_dict[updn][index],above_intercept_station)
                # print(nin_x,nin_y) 
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
        # print("The x-value for y = 18 virar is:", x_target)
        return x_target, y_target

    def add_arrow_labels_intercept(x, y):
        # selection of graph for inx and iny
        inx, iny = 0, 0   #NOTE: not necessary
        # for 0, 0
        if (0 <= x < 8 and 0 <= y <= 29 ) :
        # print("condition triggered for label")
            inx = 0;iny = 0  
        elif (24 <= x <= 32 and 0 <= y <= 29):
            # print("condition triggered for label MINUSING")
            inx = 0;iny = 0
        # for 0, 1
        elif (8 <= x < 16 and 0 <= y <= 29) :
            # print("condition triggered for label")
            inx = 0;iny = 1
        # for 0, 2
        elif (16 <= x <= 24 and 0 <= y <= 29) :
            # print("condition triggered for label")
            inx = 0;iny = 2
        # for 1, 0
        elif (0 <= x < 8 and 29 < y <= 49) :
            # print("condition triggered for label")
            inx = 1;iny = 0
        elif (24 <= x <= 32 and 29 < y <= 49):
            # print("condition triggered for label MINUSING")
            inx = 1;iny = 0
        # for 1, 1
        elif (8 <= x < 16 and 29 < y <= 49) :
            # print("condition triggered for label")
            inx = 1;iny = 1
        # for 1, 2
        elif (16 <= x <= 24 and 29 < y <= 49) :
            # print("condition triggered for label")
            inx = 1;iny = 2
        # for 2, 0
        elif (0 <= x < 8 and 49 < y <= 63) :
            # print("condition triggered for label")
            inx = 2;iny = 0
        elif (24 <= x <= 32 and 49 < y <= 63):
            # print("condition triggered for label MINUSING")
            inx = 2;iny = 0
        # for 2, 1
        elif (8 <= x < 16 and 49 < y <= 63) :
            # print("condition triggered for label")
            inx = 2;iny = 1
        # for 2, 2
        elif (16 <= x <= 24 and 49 < y <= 63) :
            # print("condition triggered for label")
            inx = 2;iny = 2 
        return inx, iny, x, y
    # have to make for every train which is going up
    # put this intersection point in bottom 
    # send the array to arpit of intersection for labels and arrow
    # print("station_dict",station_dict)
    # VR 18
    def intercept_pts(updn):
        # drawing fucntion for intersecting points
        inter_plot_arr = []
        # print(len(station_dict))
        # updn = "UP"
        
        if updn == "UP":
            y_target = 49
        elif updn == "DN":
            y_target = 30
        # try:
        arr_index = []
        for i in range(0,len(station_dict[updn]),2):
            # print(i)
            # trains_dict[updn][]
            # print("station_dict",station_dict[updn][i])
            inter_arr = intercept_selection_pts(y_target,i, updn)
            # print("inter_arr",inter_arr)
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
                
        # print(len(inter_plot_arr),len(arr_index)) 
        # print(arr_index)      
        # print(trains_dict)
        print(len(trains_dict["UP"]))
        for i in range(len(inter_plot_arr)):
            inx, iny,_,_ = add_arrow_labels_intercept(inter_plot_arr[i][0],inter_plot_arr[i][1])
            # print("inx",inx, iny)
            # axes[inx][iny].plot(inter_plot_arr[i][0],inter_plot_arr[i][1], 'o-') # have to automate for all the
            # print("arr_index[i]//2",arr_index[i],arr_index[i]//2)
            artist_list.append(axes[inx][iny].text(inter_plot_arr[i][0], inter_plot_arr[i][1] + 1, trains_dict[updn][arr_index[i]//2], rotation = 'vertical', fontsize=8))  # NOTE: INSIDE IF
            # if inx == 1 and iny==0:
                # print("intersection train",inx,iny,trains_dict[updn][i])
            artist_list.append(axes[inx][iny].arrow(inter_plot_arr[i][0], inter_plot_arr[i][1], 0, 0.5, head_width = 0, width = 0.005, clip_on = False))
        # except:arr[i][1], 0, 0.5, head_width = 0, width = 0.005, clip_on = False)   
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
