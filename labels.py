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

# def extract_up_elem(new_dict):
def extract_up_elem(new_dict,upInter):
    """
    new_dict:
    return
    upStart: list of all up trains ([[labels]],[x],[y],[up]])
    upEnd: list of all up trains ([[labels]],[x],[y],[up]])
    """

    """for up start"""
    upStart = [[], [], [], []] # Extracting first element of x and y

    k = 1 
    for i in range(len(new_dict["UP"]) // 4):    
        upStart[0].append(new_dict['UP'][k - 1])                   #append label                                
        if new_dict['UP'][k + 1][0] >= 24:                                                        
            upStart[1].append(new_dict['UP'][k + 1][0] - 24)       #append x                       
        else:                                                                                    
            upStart[1].append(new_dict['UP'][k + 1][0])            #append x    
        upStart[2].append(new_dict['UP'][k][0])                    #append y3
        upStart[3].append(new_dict['UP'][k + 2])                   #append keys
        k += 4

    new_data = []
    for i in range(len(upStart[0])):
        new_data.append([upStart[0][i], upStart[1][i], upStart[2][i], upStart[3][i]])
    new_data.sort(key=lambda row: (row[2], row[1]))

    data1 = new_data.copy()

    new_data0 = [data1[i][0] for i in range(len(new_data))]
    new_data1 = [data1[i][1] for i in range(len(new_data))]
    new_data2 = [data1[i][2] for i in range(len(new_data))]
    new_data3 = [data1[i][3] for i in range(len(new_data))]
    new_data = [new_data0, new_data1, new_data2, new_data3]

    upStart = new_data.copy()

    """for up end"""    
    upEnd = [[], [], [], []] # Extracting first element of x and y

    k = 1 
    for i in range(len(new_dict["UP"]) // 4):                                                      
            upEnd[0].append(new_dict['UP'][k - 1])                   #append label                              
            if new_dict['UP'][k + 1][-1] >= 24:                                                        
                upEnd[1].append(new_dict['UP'][k + 1][-1] - 24)      #append x                     
            else:                                                                                    
                upEnd[1].append(new_dict['UP'][k + 1][-1])           #append x  
            upEnd[2].append(new_dict['UP'][k][-1])                   #append y
            upEnd[3].append(new_dict['UP'][k + 2])               #append keys
            k += 4

    new_data = []
    for i in range(len(upEnd[0])):
        new_data.append([upEnd[0][i], upEnd[1][i], upEnd[2][i],upEnd[3][i]])
    new_data.sort(key=lambda row: (row[2], row[1]))

    data1 = new_data.copy()

    new_data0 = [data1[i][0] for i in range(len(new_data))]
    new_data1 = [data1[i][1] for i in range(len(new_data))]
    new_data2 = [data1[i][2] for i in range(len(new_data))]
    new_data3 = [data1[i][3] for i in range(len(new_data))]
    new_data = [new_data0, new_data1, new_data2, new_data3]

    upEnd = new_data.copy()
    # ##print("upstart",upStart)
    # ##print(len(upStart[0]))
    # ##print(len(upInter[0]))
    # upStart = upStart + upInter

    # remove the train where the label and x is same
    # have to change the arrows direction and labels
    # remove it from upEnd and put it in upStart
    # convert the array into string
    # ##print("downStart",upEnd[0])
    # ##print("Dninter",upInter[0])
    j=0
    # to make all the values in string
    ##print("before removing upEnd", upEnd)
    ##print("before removing upStart", upStart)
    upEnd[0] = list(map(str, upEnd[0]))

    while j < len(upInter[0]):
        ##print("up inter",str(upInter[0][j]))
        if str(upInter[0][j]) in upEnd[0]:
            ind = upEnd[0].index(str(upInter[0][j]))
            # ##print(str(upInter[0][j]))
            # ##print(ind)
            # ##print(upEnd[0])
            # ##print(upEnd[1])
            # ##print(len(upEnd[0]))
            # ##print(len(upEnd[1]))
            if upInter[1][j] > 24:
                upInter[1][j] = upInter[1][j] - 24
            # ##print("dsaf",upInter[1][j],upInter[2][j])
            # ##print(upEnd[1][ind],upEnd[2][ind])
            if upInter[1][j] == upEnd[1][ind] and upInter[2][j] == upEnd[2][ind]:
                # ##print(str(upInter[0][j]))
                # drop that index
                # ##print("drop 1",upInter[0].pop(j))
                # ##print(upInter[1].pop(j))
                # ##print(upInter[2].pop(j))
                # ##print(upInter[3].pop(j))
                upEnd[0].pop(ind)
                upEnd[1].pop(ind)
                upEnd[2].pop(ind)
                upEnd[3].pop(ind)


                j-=1
        j+=1
    
    # append the intersection values
    for i in range(len(upInter)):
        for j in range(len(upInter[0])):
            if i==0 or i==3:
                upStart[i].append(str(upInter[i][j]))
            elif i==1 or i==2:
                upStart[i].append(upInter[i][j])

    # ##print("After downStart",upEnd[0])
    # ##print("After dninter",upInter[0])
    # ##print(upStart)
    # ##print(len(upStart[0]))
    # do only testing merge to plot
    return upStart, upEnd    #start, end

def extract_dn_elem(new_dict,dnInter):
    """
    return
    dnStart: list of all up trains ([[labels]],[x],[y],[up])
    dnEnd: list of all up trains ([[labels]],[x],[y],[up])
    """
    """for dn end"""
    dnEnd = [[], [], [], []] # Extracting first element of x and y
    k = 1 
    for i in range(len(new_dict["DN"]) // 4):

        dnEnd[0].append(new_dict['DN'][k - 1])                   #append label    
        if new_dict['DN'][k + 1][-1] >= 24: 
            dnEnd[1].append(new_dict['DN'][k + 1][-1] - 24)      #append x
        else: 
            dnEnd[1].append(new_dict['DN'][k + 1][-1])           #append x
        dnEnd[2].append(new_dict['DN'][k][-1])                   #append y
        dnEnd[3].append(new_dict['DN'][k + 2])                   #append keys
        k += 4

    new_data = []
    for i in range(len(dnEnd[0])):
        new_data.append([dnEnd[0][i], dnEnd[1][i], dnEnd[2][i], dnEnd[3][i]])
    new_data.sort(key=lambda row: (row[2], row[1]))

    data1 = new_data.copy()

    new_data0 = [data1[i][0] for i in range(len(new_data))]
    new_data1 = [data1[i][1] for i in range(len(new_data))]
    new_data2 = [data1[i][2] for i in range(len(new_data))]
    new_data3 = [data1[i][3] for i in range(len(new_data))]
    new_data = [new_data0, new_data1, new_data2, new_data3]

    dnEnd = new_data.copy()   #down end

    """for dn start"""
    dnStart = [[], [], [], []] # Extracting first element of x and y

    k = 1 
    for i in range(len(new_dict["DN"]) // 4):
        dnStart[0].append(new_dict['DN'][k - 1])                #append label  
        if new_dict['DN'][k + 1][0] >= 24: 
            dnStart[1].append(new_dict['DN'][k + 1][0] - 24)    #append x
        else: 
            dnStart[1].append(new_dict['DN'][k + 1][0])         #append x
        dnStart[2].append(new_dict['DN'][k][0])                 #append y
        dnStart[3].append(new_dict['DN'][k + 2])                #append y
        k += 4

    new_data = []
    for i in range(len(dnStart[0])):
        new_data.append([dnStart[0][i], dnStart[1][i], dnStart[2][i], dnStart[3][i]])
    new_data.sort(key=lambda row: (row[2], row[1]))

    data1 = new_data.copy()

    new_data0 = [data1[i][0] for i in range(len(new_data))]
    new_data1 = [data1[i][1] for i in range(len(new_data))]
    new_data2 = [data1[i][2] for i in range(len(new_data))]
    new_data3 = [data1[i][3] for i in range(len(new_data))]
    new_data = [new_data0, new_data1, new_data2, new_data3]

    dnStart = new_data.copy() 
    # Make a set out of it
    # both list are merging here and have to check whether the list contains the number or not
    # can do by separating the list of creating a algorithm to check
    # using sets for as there is list 2d have to use sets on 2d list
    # sequence of deleting the number so if the train is already there in list then dont put as it is starting and ending from that station
    # Algorithm to check whether the train is in list or not 
    # if i not in list:



    
    # ##print("dnInter",dnInter)
    j = 0
    # ##print("downStart",dnStart[0])
    # ##print("dninter",dnInter[0])

    # to make all the values in string
    dnEnd[0] = list(map(str, dnEnd[0]))
    # ##print("before removing dnStart", dnStart)
    # ##print("before removing dnEnd", dnEnd)

    # removes the number
    while j < len(dnInter[0]):
        # ##print("dn_inter",str(dnInter[0][j]))
        if str(dnInter[0][j]) in dnEnd[0]:
            ind = dnEnd[0].index(str(dnInter[0][j]))
            # ###print(ind)
            if dnInter[1][j] > 24:
                dnInter[1][j] = dnInter[1][j] - 24
            # ###print("dsaf",dnInter[1][j],dnInter[2][j])
            # ###print(dnStart[1][ind],dnStart[2][ind])
            ###print(dnInter[1][j],dnEnd[1][ind])
            ###print(dnInter[2][j],dnEnd[2][ind])
            if dnInter[1][j] == dnEnd[1][ind] and dnInter[2][j] == dnEnd[2][ind]:
                # ###print(str(dnInter[0][j]))
                # drop that index
                dnEnd[0].pop(ind)
                dnEnd[1].pop(ind)
                dnEnd[2].pop(ind)
                dnEnd[3].pop(ind)
                j-=1
        j+=1
    
    
    for i in range(len(dnInter)):
        for j in range(len(dnInter[0])):
            if i==0 or i==3:
                dnEnd[i].append(str(dnInter[i][j]))
            elif i==1 or i==2:
                dnEnd[i].append(dnInter[i][j])
    # ###print("After downStart",dnStart[0])
    # ###print("After dninter",dnInter[0])
    # ###print("in the function dnEnd", dnEnd)
    # ###print(dnEnd)
    # ###print(len(dnEnd[0]))
    # ###print(len(dnEnd[1]))
    # ###print(len(dnEnd[2]))
    # ###print(len(dnEnd[3]))

    return dnStart, dnEnd     


def merge_elements(collision_up, collision_dn):

    collision_merged = [[], [], [], []]
    for i in range(len(collision_dn)):
        collision_merged[i] = collision_up[i] + collision_dn[i]

    new_data = []
    for i in range(len(collision_merged[0])):
        new_data.append([collision_merged[0][i], collision_merged[1][i], collision_merged[2][i], collision_merged[3][i]])
    new_data.sort(key=lambda row: (row[2], row[1]))

    data1 = new_data.copy()

    new_data0 = [data1[i][0] for i in range(len(new_data))]
    new_data1 = [data1[i][1] for i in range(len(new_data))]
    new_data2 = [data1[i][2] for i in range(len(new_data))]
    new_data3 = [data1[i][3] for i in range(len(new_data))]
    new_data = [new_data0, new_data1, new_data2, new_data3]

    collision_merged = new_data.copy()

    return collision_merged

def extract_current_axes_ue_ds(x, y):
    first_axes_flag = False
    second_axes_flag = False
    if (0 <= x < 8 and 0 <= y <= 29 ) :
        # ###print("condition triggered for label")
        inx = 0;iny = 0;first_axes_flag = True
    elif (24 <= x <= 32 and 0 <= y <= 29):
        # ###print("condition triggered for label MINUSING")
        inx = 0;iny = 0;first_axes_flag = True
    # for 0, 1
    elif (8 <= x < 16 and 0 <= y <= 29) :
        # ###print("condition triggered for label")
        inx = 0;iny = 1;first_axes_flag = True
    # for 0, 2
    elif (16 <= x <= 24 and 0 <= y <= 29) :
        # ###print("condition triggered for label")
        inx = 0;iny = 2;first_axes_flag = True

    # for 1, 0
    elif (0 <= x < 8 and 29 < y <= 49) :
        # ###print("condition triggered for label")
        inx = 1;iny = 0;second_axes_flag = True
    elif (24 <= x <= 32 and 29 < y <= 49):
        # ###print("condition triggered for label MINUSING")
        inx = 1;iny = 0;second_axes_flag = True
    # for 1, 1
    elif (8 <= x < 16 and 29 < y <= 49) :
        # ###print("condition triggered for label")
        inx = 1;iny = 1;second_axes_flag = True
    # for 1, 2
    elif (16 <= x <= 24 and 29 < y <= 49) :
        # ###print("condition triggered for label")
        inx = 1;iny = 2;second_axes_flag = True

    # for 2, 0
    elif (0 <= x < 8 and 49 < y <= 63) :
        # ###print("condition triggered for label")
        inx = 2;iny = 0
    elif (24 <= x <= 32 and 49 < y <= 63):
        # ##print("condition triggered for label MINUSING")
        inx = 2;iny = 0
    # for 2, 1
    elif (8 <= x < 16 and 49 < y <= 63) :
        # ##print("condition triggered for label")
        inx = 2;iny = 1
    # for 2, 2
    elif (16 <= x <= 24 and 49 < y <= 63) :
        # ##print("condition triggered for label")
        inx = 2;iny = 2 

    if inx == 0:
        return 0.65, 0.18, 0.26,first_axes_flag,second_axes_flag, inx
    elif inx == 1:
        return 0.6, 0.14, 0.26,first_axes_flag, second_axes_flag, inx
    elif inx == 2:
        return 0.6, 0.14, 0.15,first_axes_flag,second_axes_flag, inx

def extract_current_axes_ue_ds_st_bsl(x, y):
    first_axes_flag = False
    second_axes_flag = False
    if (0 <= x < 8 and 0 <= y <= 25 ) :
        # ###print("condition triggered for label")
        inx = 0;iny = 0;first_axes_flag = True
    elif (24 <= x <= 32 and 0 <= y <= 25):
        # ###print("condition triggered for label MINUSING")
        inx = 0;iny = 0;first_axes_flag = True
    # for 0, 1
    elif (8 <= x < 16 and 0 <= y <= 25) :
        # ###print("condition triggered for label")
        inx = 0;iny = 1;first_axes_flag = True
    # for 0, 2
    elif (16 <= x <= 24 and 0 <= y <= 25) :
        # ###print("condition triggered for label")
        inx = 0;iny = 2;first_axes_flag = True

    # for 1, 0
    elif (0 <= x < 8 and 25 < y <= 46) :
        # ###print("condition triggered for label")
        inx = 1;iny = 0;second_axes_flag = True
    elif (24 <= x <= 32 and 25 < y <= 46):
        # ###print("condition triggered for label MINUSING")
        inx = 1;iny = 0;second_axes_flag = True
    # for 1, 1
    elif (8 <= x < 16 and 25 < y <= 46) :
        # ###print("condition triggered for label")
        inx = 1;iny = 1;second_axes_flag = True
    # for 1, 2
    elif (16 <= x <= 24 and 25 < y <= 46) :
        # ###print("condition triggered for label")
        inx = 1;iny = 2;second_axes_flag = True


    #arrow_plot_buffer, arrow_label_buffer, slash_buffer,first_axes_flag, second_axes_flag, inx
    if inx == 0:
        return 0.65, 0.13, 0.13,first_axes_flag,second_axes_flag, inx # done 
    elif inx == 1:
        return 0.6, 0.20, 0.13,first_axes_flag, second_axes_flag, inx # issue of intersection

# Have to add condition to label for both the axes 1st and 2nd same 
# Can give a flag as it has to #print twice in 2 different plots
# need to identify which axes and time zone it belongs to 
# flag first triggers then make the x as 1 and flag second triggers tehn make x as 2
def extract_current_axes_us_de(x, y):
    first_axes_flag = False
    second_axes_flag = False
    
    if (0 <= x < 8 and 0 <= y <= 29 ) :
        # ##print("condition triggered for label")
        inx = 0;iny = 0; first_axes_flag = True
    elif (24 <= x <= 32 and 0 <= y <= 29):
        # ##print("condition triggered for label MINUSING")
        inx = 0;iny = 0; first_axes_flag = True
    # for 0, 1
    elif (8 <= x < 16 and 0 <= y <= 29) :
        # ##print("condition triggered for label")
        inx = 0;iny = 1; first_axes_flag = True
    # for 0, 2
    elif (16 <= x <= 24 and 0 <= y <= 29) :
        # ##print("condition triggered for label")
        inx = 0;iny = 2; first_axes_flag = True

    # for 1, 0
    elif (0 <= x < 8 and 29 < y <= 49) :
        # ##print("condition triggered for label")
        inx = 1;iny = 0; second_axes_flag = True
    elif (24 <= x <= 32 and 29 < y <= 49):
        # ##print("condition triggered for label MINUSING")
        inx = 1;iny = 0; second_axes_flag = True
    # for 1, 1
    elif (8 <= x < 16 and 29 < y <= 49) :
        # ##print("condition triggered for label")
        inx = 1;iny = 1; second_axes_flag = True
    # for 1, 2
    elif (16 <= x <= 24 and 29 < y <= 49) :
        # ##print("condition triggered for label")
        inx = 1;iny = 2; second_axes_flag = True


    # for 2, 0
    elif (0 <= x < 8 and 49 < y <= 63) :
        # ##print("condition triggered for label")
        inx = 2;iny = 0
    elif (24 <= x <= 32 and 49 < y <= 63):
        # ##print("condition triggered for label MINUSING")
        inx = 2;iny = 0
    # for 2, 1
    elif (8 <= x < 16 and 49 < y <= 63) :
        # ##print("condition triggered for label")
        inx = 2;iny = 1
    # for 2, 2
    elif (16 <= x <= 24 and 49 < y <= 63) :
        # ##print("condition triggered for label")
        inx = 2;iny = 2 

    if inx == 0:
        return 0.6, 0.42, 0.30, first_axes_flag, second_axes_flag, inx
    elif inx == 1:
        return 0.6, 0.33, 0.22, first_axes_flag, second_axes_flag, inx
    elif inx == 2:
        return 0.6, 0.26, 0.15, first_axes_flag, second_axes_flag, inx
    
def extract_current_axes_us_de_st_bsl(x, y):
    first_axes_flag = False
    second_axes_flag = False
    
    if (0 <= x < 8 and 0 <= y <= 25 ) :
        # ##print("condition triggered for label")
        inx = 0;iny = 0; first_axes_flag = True
    elif (24 <= x <= 32 and 0 <= y <= 25):
        # ##print("condition triggered for label MINUSING")
        inx = 0;iny = 0; first_axes_flag = True
    # for 0, 1
    elif (8 <= x < 16 and 0 <= y <= 25) :
        # ##print("condition triggered for label")
        inx = 0;iny = 1; first_axes_flag = True
    # for 0, 2
    elif (16 <= x <= 24 and 0 <= y <= 25) :
        # ##print("condition triggered for label")
        inx = 0;iny = 2; first_axes_flag = True

    # for 1, 0
    elif (0 <= x < 8 and 25 < y <= 46) :
        # ##print("condition triggered for label")
        inx = 1;iny = 0; second_axes_flag = True
    elif (24 <= x <= 32 and 25 < y <= 46):
        # ##print("condition triggered for label MINUSING")
        inx = 1;iny = 0; second_axes_flag = True
    # for 1, 1
    elif (8 <= x < 16 and 25 < y <= 46) :
        # ##print("condition triggered for label")
        inx = 1;iny = 1; second_axes_flag = True
    # for 1, 2
    elif (16 <= x <= 24 and 25 < y <= 46) :
        # ##print("condition triggered for label")
        inx = 1;iny = 2; second_axes_flag = True


    #arrow_plot_buffer, arrow_label_buffer, slash_buffer,first_axes_flag, second_axes_flag, inx
    if inx == 0:
        return 0.6, 0.26, 0.16, first_axes_flag, second_axes_flag, inx # done
    elif inx == 1:
        return 0.6, 0.24, 0.14, first_axes_flag, second_axes_flag, inx # done

    
def add_arrow_labels(x, y):
    inx, iny = 0, 0   #NOTE: not necessary

    # for 0, 0
    if (0 <= x < 8 and 0 <= y <= 29 ):
        # ##print("condition triggered for label")
        inx = 0;iny = 0;arrow_first_axes_flag = True  
    elif (24 <= x <= 32 and 0 <= y <= 29):
        # ##print("condition triggered for label MINUSING")
        inx = 0;iny = 0;arrow_first_axes_flag = True
    # for 0, 1
    elif (8 <= x < 16 and 0 <= y <= 29):
        # ##print("condition triggered for label")
        inx = 0;iny = 1;arrow_first_axes_flag = True
    # for 0, 2
    elif (16 <= x <= 24 and 0 <= y <= 29):
        # ##print("condition triggered for label")
        inx = 0;iny = 2;arrow_first_axes_flag = True


    # for 1, 0
    elif (0 <= x < 8 and 29 < y <= 49):
        # ##print("condition triggered for label")
        inx = 1;iny = 0;arrow_second_axes_flag = True
    elif (24 <= x <= 32 and 29 < y <= 49):
        # ##print("condition triggered for label MINUSING")
        inx = 1;iny = 0;arrow_second_axes_flag = True
    # for 1, 1
    elif (8 <= x < 16 and 29 < y <= 49):
        # ##print("condition triggered for label")
        inx = 1;iny = 1;arrow_second_axes_flag = True
    # for 1, 2
    elif (16 <= x <= 24 and 29 < y <= 49):
        # ##print("condition triggered for label")
        inx = 1;iny = 2;arrow_second_axes_flag = True


    # for 2, 0
    elif (0 <= x < 8 and 49 < y <= 63):
        # ##print("condition triggered for label")
        inx = 2;iny = 0
    elif (24 <= x <= 32 and 49 < y <= 63):
        # ##print("condition triggered for label MINUSING")
        inx = 2;iny = 0
    # for 2, 1
    elif (8 <= x < 16 and 49 < y <= 63) :
        # ##print("condition triggered for label")
        inx = 2;iny = 1
    # for 2, 2
    elif (16 <= x <= 24 and 49 < y <= 63) :
        # ##print("condition triggered for label")
        inx = 2;iny = 2 
    return inx, iny, x, y#, arrow_first_axes_flag, arrow_second_axes_flag

def add_arrow_labels_st_bsl(x, y):
    inx, iny = 0, 0   #NOTE: not necessary

    # for 0, 0
    if (0 <= x < 8 and 0 <= y <= 25 ):
        # ##print("condition triggered for label")
        inx = 0;iny = 0;arrow_first_axes_flag = True  
    elif (24 <= x <= 32 and 0 <= y <= 25):
        # ##print("condition triggered for label MINUSING")
        inx = 0;iny = 0;arrow_first_axes_flag = True
    # for 0, 1
    elif (8 <= x < 16 and 0 <= y <= 25):
        # ##print("condition triggered for label")
        inx = 0;iny = 1;arrow_first_axes_flag = True
    # for 0, 2
    elif (16 <= x <= 24 and 0 <= y <= 25):
        # ##print("condition triggered for label")
        inx = 0;iny = 2;arrow_first_axes_flag = True


    # for 1, 0
    elif (0 <= x < 8 and 25 < y <= 46):
        # ##print("condition triggered for label")
        inx = 1;iny = 0;arrow_second_axes_flag = True
    elif (24 <= x <= 32 and 25 < y <= 46):
        # ##print("condition triggered for label MINUSING")
        inx = 1;iny = 0;arrow_second_axes_flag = True
    # for 1, 1
    elif (8 <= x < 16 and 25 < y <= 46):
        # ##print("condition triggered for label")
        inx = 1;iny = 1;arrow_second_axes_flag = True
    # for 1, 2
    elif (16 <= x <= 24 and 25 < y <= 46):
        # ##print("condition triggered for label")
        inx = 1;iny = 2;arrow_second_axes_flag = True


    