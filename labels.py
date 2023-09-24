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
    # print("upstart",upStart)
    # print(len(upStart[0]))
    # print(len(upInter[0]))
    # upStart = upStart + upInter
    for i in range(len(upInter)):
        for j in range(len(upInter[0])):
            if i==0 or i==3:
                upStart[i].append(str(upInter[i][j]))
            elif i==1 or i==2:
                upStart[i].append(upInter[i][j])

    # print(upStart)
    # print(len(upStart[0]))
    # do only testing merge to plot
    return upStart, upEnd    #start, end

def extract_dn_elem(new_dict,dnInter):
    """
    return
    dnStart: list of all up trains ([[labels]],[x],[y],[up])
    dnEnd: list of all up trains ([[labels]],[x],[y],[up])"""
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

    for i in range(len(dnInter)):
        for j in range(len(dnInter[0])):
            if i==0 or i==3:
                dnEnd[i].append(str(dnInter[i][j]))
            elif i==1 or i==2:
                dnEnd[i].append(dnInter[i][j])

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
        return 0.6, 0.9, 0.33
    elif inx == 1:
        return 0.6, 0.7, 0.16
    elif inx == 2:
        return 0.6, 0.7, 0.09
    

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
        return 0.6, 2.2, 0.4
    elif inx == 1:
        return 0.6, 1.8, 0.28
    elif inx == 2:
        return 0.6, 1.3, 0.18
    

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

