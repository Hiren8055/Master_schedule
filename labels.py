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
    for i in range(len(new_dict["UP"]) // 4):         
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
    # for 0, 0
    if (0 <= x < 8 and 0 <= y <= 11 ) :
        # print("condition triggered for label")
        inx = 0;iny = 0  
    elif (24 <= x <= 32 and 0 <= y <= 11):
        # print("condition triggered for label MINUSING")
        inx = 0;iny = 0
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
        inx = 2;iny = 0
    # for 2, 1
    elif (8 <= x < 16 and 31 < y <= 45) :
        # print("condition triggered for label")
        inx = 2;iny = 1
    # for 2, 2
    elif (16 <= x <= 24 and 31 < y <= 45) :
        # print("condition triggered for label")
        inx = 2;iny = 2 

    if inx == 0:
        return 0.07
    elif inx == 1 or inx == 2:
        return 0.14
    

def extract_current_axes_us_de(x, y):
    # for 0, 0
    if (0 <= x < 8 and 0 <= y <= 11 ) :
        # print("condition triggered for label")
        inx = 0;iny = 0  
    elif (24 <= x <= 32 and 0 <= y <= 11):
        # print("condition triggered for label MINUSING")
        inx = 0;iny = 0
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
        inx = 2;iny = 0
    # for 2, 1
    elif (8 <= x < 16 and 31 < y <= 45) :
        # print("condition triggered for label")
        inx = 2;iny = 1
    # for 2, 2
    elif (16 <= x <= 24 and 31 < y <= 45) :
        # print("condition triggered for label")
        inx = 2;iny = 2 

    if inx == 0:
        return 0.07
    elif inx == 1 or inx == 2:
        return 0.08




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


