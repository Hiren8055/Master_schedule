import numpy as np

def is_sorted_ascending(lst):
    """this function checkes the list is sorted in ascending or not. If yes then it is 'DN' list"""
    return lst == sorted(lst)

def add_arrow_labels(x, y):
    inx = 0   #NOTE: not necessary
    # for 0, 0
    if (0 <= x < 8 and 0 <= y <= 11 ) :
        inx =   0
    elif (24 <= x <= 32 and 0 <= y <= 11):
        x = x - 24
    # for 0, 1
    elif (8 <= x < 16 and 0 <= y <= 11) :
        inx = 1
    # for 0, 2
    elif (16 <= x <= 24 and 0 <= y <= 11) :
        inx = 2
    # for 1, 0
    elif (0 <= x < 8 and 11 < y <= 31) :
        inx = 3
    elif (24 <= x <= 32 and 11 < y <= 31):
        x = x - 24
        inx = 3
    # for 1, 1
    elif (8 <= x < 16 and 11 < y <= 31) :
        inx = 4
    # for 1, 2
    elif (16 <= x <= 24 and 11 < y <= 31) :
        inx = 5
    # for 2, 0
    elif (0 <= x < 8 and 31 < y <= 45) :
        inx = 6
    elif (24 <= x <= 32 and 31 < y <= 45):
        x = x - 24
        inx = 6
    # for 2, 1
    elif (8 <= x < 16 and 31 < y <= 45) :
        inx = 7
    # for 2, 2
    elif (16 <= x <= 24 and 31 < y <= 45) :
        inx =  8
    return inx, x, y

def collision_text_updn(collision_merged, axes):   
        """ this function takes cares in overlapping of labels"""

        """ Variables Declaration"""
        k = 1
        previous_x, previous_y= 0, 0
        label_var = ''
        y_overlap_both_up = 0
        y_buffer_both_up = 0


        for i in range(len(collision_merged[0])):
            
            label_ = collision_merged[0][i]
            x = collision_merged[1][i]
            y = collision_merged[2][i]

            if abs(x - previous_x) <= 0.03 and y == previous_y:
                label_var = '/'
                len_of_labels = len(label_)
                y_buffer_both_up = y_buffer_both_up + (0.06 * len_of_labels)
                """y_overlap_both_up is y axis for text which is different in arrows y axis that is original 'y' """
                y_overlap_both_up = y + y_buffer_both_up 
            else:
                label_var = ''
                y_buffer_both_up = 0
                y_overlap_both_up = y + y_buffer_both_up                         

            label = label_ + label_var

            # original_x = x
            inx, x, y = add_arrow_labels(x, y)
            axes[inx].text(x - 0.02, y_overlap_both_up + 0.8, label, rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
            axes[inx].arrow(x, y, 0, 0.5, width = 0.005, clip_on = False)

            previous_x, previous_y = x, y
            k += 3


############################################################################################################

def collision_text_updn1(collision_merged1, axes):   

        """ this function takes cares in overlapping of labels"""
        """ Variables Declaration"""
        k = 1

        previous_x, previous_y= 0, 0
        label_var = ''
        y_overlap_both_up = 0
        y_buffer_both_up = 0

        for i in range(len(collision_merged1[0])):
            
            label_ = collision_merged1[0][i]
            x = collision_merged1[1][i]
            y = collision_merged1[2][i]

            if abs(x - previous_x) <= 0.03 and y == previous_y:
                # print('label is overlapping')
                label_var = '/'
                len_of_labels = len(label_)
                y_buffer_both_up = y_buffer_both_up + (0.045 * len_of_labels)
                """y_overlap_both_up is y axis for text which is different in arrows y axis that is original 'y' """
                y_overlap_both_up = y - y_buffer_both_up 
            else:
                label_var = ''
                y_buffer_both_up = 0
                y_overlap_both_up = y - y_buffer_both_up                         

            label = label_var + label_

            inx, x, y = add_arrow_labels(x, y)
            axes[inx].text(x - 0.02, y_overlap_both_up - 0.55, label, rotation = 'vertical', fontsize=13)  # NOTE: INSIDE IF
            axes[inx].arrow(x, y, 0, - 0.5, width = 0.005, clip_on = False)

            previous_x, previous_y = x, y

            ###############################################################################
            k += 3
