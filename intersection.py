import numpy as np
def intersection(self, station_dict, trains_dict):
    # "Input with train array and output plot intersection at particular y"
    # have to use conversion function in between to convert the time and axis domain
    # have to only give the intersection in mid subplot with index 1
    
    # intercept_station = 10
    axes = self.axes
    artist_list = self.artist_list
    def intercept_selection_pts(y_target,index,updn):
        '''function selects the for labels 
        It has condition for for not having point at that station it will find by line intersection at that station by select the 2 station above and below
        using 2 lines intersection method 
        '''

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
        if tenth_x == None or tenth_y == None:
            ele_x,ele_y = find(station_dict[updn][index],station_dict[updn][index+1],below_intercept_station)
            # print(ele_x,ele_y)
            if ele_x == None or ele_y == None:
                return False
                # no intersection
            else:
                print(station_dict[updn][index])
                nin_x,nin_y = find(station_dict[updn][index],station_dict[updn][index+1],above_intercept_station)
                # print(nin_x,nin_y) 
                if nin_x == None or nin_y == None:
                    return False
                else:
                    return [[nin_x,ele_x],[nin_y,ele_y]]
        else:
            return [tenth_x, tenth_y]

        # if station_dict[updn][index].index(intercept_station):
        #     intercept_index = station_dict[updn][index].index(intercept_station)
        # print(station_dict[updn][index+1][intercept_index])
        # have to select the index of 10 or not then go for below 10 and above 10 ie is 11
        # find 10 in list and get the index 


    def intercept(y_target, x ,y):
        '''finds the intercept of line'''
        # find the points for intersection
        print("intercept",y_target,x,y)
        x_target = np.interp(y_target,x,y)
        # print("The x-value for y = 18 virar is:", x_target)
        return x_target, y_target

    def add_arrow_labels_intercept(x, y):
        # can optimize by loop or funciton
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
        '''drawing intersection points it gives the point of intersection and then '''
        inter_plot_arr = []
        # print(len(station_dict))
        # updn = "UP"
        
        if updn == "UP":
            y_target = 49
        elif updn == "DN":
            y_target = 30
        # try:
        '''first loop is for find the point'''
        arr_index = []
        
        # create a loop for both the index or invert it 

        for i in range(0,len(station_dict[updn]),2):
            # print(i)
            # trains_dict[updn][]
            # print("station_dict",station_dict[updn][i])
            inter_arr = intercept_selection_pts(y_target,i, updn)
            
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
        
        if updn == "DN":
            y_target = 49
        elif updn == "UP":
            y_target = 30

        for i in range(0,len(station_dict[updn]),2):
            # print(i)
            # trains_dict[updn][]
            # print("station_dict",station_dict[updn][i])
            inter_arr = intercept_selection_pts(y_target,i, updn)
            
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

        stations_for_intersection = [29,50]        
        for j in range(len(stations_for_intersection)):
            y_target = stations_for_intersection[j]
            for i in range(0,len(station_dict[updn]),2):
                # print(i)
                # trains_dict[updn][]
                # print("station_dict",station_dict[updn][i])
                inter_arr = intercept_selection_pts(y_target,i, updn)
                
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
        # print(len(trains_dict["UP"]))
        '''second loop is for drawing the points stored in inter_plot_arr'''                
        # need to dicrimate up and below arrow
        bufy = 1.8
        for i in range(len(inter_plot_arr)):
            inx, iny,_,_ = add_arrow_labels_intercept(inter_plot_arr[i][0],inter_plot_arr[i][1])
            # print("inx",inx, iny)
            # axes[inx][iny].plot(inter_plot_arr[i][0],inter_plot_arr[i][1], 'o-') # have to automate for all the
            # print("arr_index[i]//2",arr_index[i],arr_index[i]//2)
            artist_list.append(axes[inx][iny].text(inter_plot_arr[i][0], inter_plot_arr[i][1] + bufy, trains_dict[updn][arr_index[i]//2], rotation = 'vertical', fontsize=8, picker=True))  # NOTE: INSIDE IF
            print(inter_plot_arr[i][0], inter_plot_arr[i][1] + bufy, trains_dict[updn][arr_index[i]//2],end="\n")
            # if inx == 1 and iny==0:
                # print("intersection train",inx,iny,trains_dict[updn][i])
            artist_list.append(axes[inx][iny].arrow(inter_plot_arr[i][0], inter_plot_arr[i][1], 0, 0.5, head_width = 0, width = 0.005, clip_on = False))
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

# solve the 24 issue 
# add labels for both the side