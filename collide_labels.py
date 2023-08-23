import numpy as np

def is_sorted_ascending(lst):
    """this function checkes the list is sorted in ascending or not. If yes then it is 'DN' list"""
    return lst == sorted(lst)

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

def collision_text_updn(collision_merged, axes):   
    # def collision_text_updn(collision_updn,  new_dict):   
        """ this function takes cares in overlapping of labels"""

        """ Variables Declaration"""
        k = 1
        last_y = 0

        previous_x, previous_y= 0, 0
        label_var = ''
        y_overlap_both_up = 0
        y_buffer_both_up = 0
        original_x = 0

        for i in range(len(collision_merged[0])):
            
            label_ = collision_merged[0][i]
            x = collision_merged[1][i]
            y = collision_merged[2][i]

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

            """ This is for 'DOWN' """
            # if key == 'DN':       
            #     c = 0 
                # """Label for end"""
                # inx, iny, x, y = add_arrow_labels(x, y)
                # axes[inx][iny].text(x, y - 0.7, label_, rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
                # axes[inx][iny].arrow(x, y, 0, -0.5, width = 0.005, clip_on = False)

                # """Label for End"""
                # inx, iny, x_last, y_last = add_arrow_labels(x_last, y_last)
                # axes[inx][iny].text(x_last, y_last + 1, label_, rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
                # axes[inx][iny].arrow(x_last, y_last, 0, 0.5, head_width = 0, width = 0.005, clip_on = False) 

            # else:
            #     """ This is for 'UP' """
            #     c = 1
            #     if start_end == 'start':

            print(previous_x, x, previous_y, y)
            if abs(x - previous_x) <= 0.01 and y == previous_y:
                print('label is overlapping')
                label_var = '/'
                len_of_labels = len(label_)
                y_buffer_both_up = y_buffer_both_up + (0.06 * len_of_labels) + 0.12
                """y_overlap_both_up is y axis for text which is different in arrows y axis that is original 'y' """
                y_overlap_both_up = y + y_buffer_both_up 
            else:
                print('label is NOT overlapping')
                label_var = ''
                y_buffer_both_up = 0
                y_overlap_both_up = y + y_buffer_both_up                         

            # label = new_dict['UPDN'][k - 1] + label_var
            label = label_ + label_var

            original_x = x
            inx, iny, x, y = add_arrow_labels(x, y)
            axes[inx][iny].text(x, y_overlap_both_up + 0.9, label, rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
            axes[inx][iny].arrow(x, y, 0, 0.5, width = 0.005, clip_on = False)

            previous_x, previous_y = original_x, y


            ###############################################################################
            k += 3
