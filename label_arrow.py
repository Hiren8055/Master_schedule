import uuid
from labels import extract_current_axes_ue_ds, extract_current_axes_us_de, add_arrow_labels
# Have to make the an array with slashing and original position
def round_tenths(input_float: float) -> int:
    return int(round(input_float/10))
def built_dict(dict_name, text_label,train_x,train_y):
    key_name = str(uuid.uuid4())
    # print(key_name)
    text_label.set_gid(key_name)
    dict_name[key_name] = [train_x, train_y]
    return text_label

def upEnd_dnStart_label(canvas, axes, express_flag, artist_list, upEnd_dnStart):
    """ this function plot arrow and labels for up-end and down-start"""
    canvas.flush_events()
    k = 1
    previous_x, previous_y= 0, 0
    label_var = ''
    final_y = 0
    y_buffer = 0
    arrow_label_buffer = 0
    label_counter = 0
    label_counter1 = 0
    label_counter2 = 0

    drag_dict_ueds ={}
    for i in range(len(upEnd_dnStart[0])):
        canvas.flush_events()
        label_ = upEnd_dnStart[0][i]    
        x = upEnd_dnStart[1][i]
        y = upEnd_dnStart[2][i]
        key = upEnd_dnStart[3][i]
        len_of_labels = len(label_)

        arrow_plot_buffer, arrow_label_buffer, slash_buffer,first_axes_flag, second_axes_flag = extract_current_axes_ue_ds(x, y)
        if abs(x - previous_x) <= 0.03 and y == previous_y:
            label_var = '/'
            y_buffer = y_buffer + (slash_buffer * len_of_labels) 
            final_y = y - y_buffer 
            label_counter += 1
        else:
            label_counter = 0
            # if the buffer value doesn't satisfy then directly print the label
            label_var = ''
            y_buffer = 0
            # it is the buffer used for placing the labels
            y_buffer = arrow_label_buffer * len_of_labels 
            # final_y is used as final y for labels
            final_y = y - y_buffer                         
        
        label = label_var + label_

        inx, iny, x, y= add_arrow_labels(x, y)

        # logic is to plot text and arrow after 24
        if x > 24:
            dup_x = x - 24
        else:
            dup_x = x

        # have to change the plot of intersection at vr in axes zero plot and still keep the plot of first axes same
# what was the differentiating factor in change that is done
#  up start and dn end in zero row
# up end and dn start in first row
# change the 

        if first_axes_flag and y == 29:
            #checking if label counter > 5 then further label plotting will be ignored
            if label_counter > 5:
                pass
            else:
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_ueds, text_label,x,y)
                artist_list.append(text_label)  # NOTE: INSIDE IF
                if key == 'UP':
                    artist_list.append(axes[inx][iny].arrow(dup_x, y, 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer, 0, 0.5, width = 0.005, clip_on = False))
            # to plot vr labels on 2nd axes

            if express_flag:
                arrow_plot_buffer_inx1, arrow_label_buffer_inx1, slash_buffer_inx1,first_axes_flag, second_axes_flag = extract_current_axes_ue_ds(x, y+2)
                if abs(x - previous_x) <= 0.03 and y == previous_y:
                    label_var = '/'
                    y_buffer_inx1  = y_buffer_inx1  + (slash_buffer_inx1 * len_of_labels) 
                    final_y_inx1 = y + y_buffer_inx1  
                    label_counter += 1
                else:
                    # print(type(label))
                    # if label == "12283":
                    #     print("Arrow label triggered 12267 j")
                    #     print(arrow_label_buffer_inx1)
                    label_counter = 0
                    label_var = ''
                    y_buffer_inx1  = 0
                    y_buffer_inx1  = arrow_label_buffer_inx1 * len_of_labels
                    final_y_inx1 = y + y_buffer_inx1                          

                label = label_ + label_var
                inx = 1
                if label_counter1 > 5:
                    pass
                else:
                    text_label = axes[inx][iny].text(dup_x - 0.02, final_y_inx1, label, rotation = 'vertical', fontsize=8, picker=True)
                    text_label = built_dict(drag_dict_ueds, text_label,x,y)
                    artist_list.append(text_label)  # NOTE: INSIDE IF
                    if key == 'UP': #UP
                        artist_list.append(axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer_inx1, 0, -0.5, width = 0.005, clip_on = False))
                    else:
                        artist_list.append(axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))

        elif second_axes_flag and y==49 :
            if label_counter > 5:
                pass
            else:
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_ueds, text_label,x,y)
                artist_list.append(text_label)  # NOTE: INSIDE IF
                if key == 'UP':
                    artist_list.append(axes[inx][iny].arrow(dup_x, y, 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer, 0, 0.5, width = 0.005, clip_on = False))

            # to plot vr labels on 2nd axes 
            arrow_plot_buffer_inx2, arrow_label_buffer_inx2, slash_buffer_inx2,first_axes_flag, second_axes_flag = extract_current_axes_ue_ds(x, y+2)
            if abs(x - previous_x) <= 0.03 and y == previous_y:
                label_var = '/'
                y_buffer_inx2 = y_buffer_inx2 + (slash_buffer_inx2 * len_of_labels) 
                final_y_inx2 = y + y_buffer_inx2 
                label_counter2 += 1
            else:
                print("Arrow label triggered inx2")
                print(arrow_label_buffer_inx2)
                label_counter2 = 0
                label_var = ''
                y_buffer_inx2 = 0
                y_buffer_inx2 = arrow_label_buffer_inx2 * len_of_labels
                final_y_inx2 = y + y_buffer_inx2                         

            
            label = label_ + label_var
            inx = 2
            if label_counter2 > 5:
                pass
            else:
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y_inx2, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_ueds, text_label,x,y)
                artist_list.append(text_label)  # NOTE: INSIDE IF
                # if key == 'UP':
                #     artist_list.append(axes[inx][iny].arrow(dup_x, y , 0, -0.5, width = 0.005, clip_on = False))
                # else:
                #     artist_list.append(axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer_inx2, 0, 0.5, width = 0.005, clip_on = False))

                if key == 'UP': #UP
                        artist_list.append(axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer_inx2, 0, -0.5, width = 0.005, clip_on = False))
                else:
                        artist_list.append(axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))

        elif (first_axes_flag and y != 29) or (second_axes_flag and y!= 49)or not (first_axes_flag and second_axes_flag):
            if label_counter > 5:
                pass
            else:
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_ueds, text_label,x,y)
                artist_list.append(text_label)  # NOTE: INSIDE IF
                if key == 'UP':
                    artist_list.append(axes[inx][iny].arrow(dup_x, y , 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer, 0, 0.5, width = 0.005, clip_on = False))
        else:
            # add except here
            print("ue and ds dead end")
        previous_x, previous_y = x, y
        k += 3
    print("drag_dict_ueds",drag_dict_ueds)
    return drag_dict_ueds

def upStart_dnEnd_label(canvas, axes, express_flag, artist_list, upStart_dnEnd):   
    """ this function plot arrow and labels for up-start and down-end"""
    canvas.flush_events()
    k = 1
    previous_x, previous_y= 0, 0
    label_var = ''
    final_y = 0
    y_buffer = 0
    canvas.flush_events()
    label_counter = 0
    label_counter1 = 0
    label_counter2 = 0
    drag_dict_usde = {}
    for i in range(len(upStart_dnEnd[0])):
        label_ = upStart_dnEnd[0][i]
        x = upStart_dnEnd[1][i]
        y = upStart_dnEnd[2][i]
        key = upStart_dnEnd[3][i]
        len_of_labels = len(label_)

        arrow_plot_buffer, arrow_label_buffer, slash_buffer, first_axes_flag, second_axes_flag = extract_current_axes_us_de(x, y)
        if abs(x - previous_x) <= 0.03 and y == previous_y:
            label_var = '/'
            y_buffer = y_buffer + (slash_buffer * len_of_labels) 
            final_y = y + y_buffer 
            label_counter += 1
        else:
            label_counter = 0
            label_var = ''
            y_buffer = 0
            y_buffer = arrow_label_buffer * len_of_labels
            final_y = y + y_buffer                         

        label = label_ + label_var
        inx, iny, x, y = add_arrow_labels(x, y)
        canvas.flush_events()
        if x > 24:
            dup_x = x - 24
        else:
            dup_x = x
        
        if first_axes_flag or y == 29:
            #checking if label counter > 5 then further label plotting will be ignored
            if label_counter > 5:
                pass
            else:
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_usde, text_label,x,y)           
                artist_list.append(text_label)  # NOTE: INSIDE IF
                if key == 'UP': #UP
                    artist_list.append(axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer, 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))
            
            # to plot vr labels on 2nd axes 
            if express_flag:
                arrow_plot_buffer_inx1, arrow_label_buffer_inx1, slash_buffer_inx1, first_axes_flag, second_axes_flag = extract_current_axes_us_de(x, y+2)
                
                # arrow_label_buffer_inx1 = arrow_label_buffer_inx1 - 
                # if abs(x - previous_x) <= 0.03 and y == previous_y:
                #     label_var = '/'
                #     y_buffer_inx1 = y_buffer_inx1 + (slash_buffer_inx1 * len_of_labels) 
                #     final_y_inx1 = y + y_buffer_inx1 
                #     label_counter1 += 1
                # else:
                #     label_counter1 = 0
                #     label_var = ''
                #     y_buffer_inx1 = 0
                #     y_buffer_inx1 = arrow_label_buffer_inx1 * len_of_labels
                #     final_y_inx1 = y + y_buffer_inx1                         

                # label = label_ + label_var
                if abs(x - previous_x) <= 0.03 and y == previous_y:
                    label_var = '/'
                    y_buffer_inx1 = y_buffer_inx1 + (slash_buffer_inx1 * len_of_labels) 
                    final_y_inx1 = y - y_buffer_inx1 
                    label_counter1 += 1
                else:
                    print("arrow_label_buffer_inx1 before",arrow_label_buffer_inx1)
                    arrow_label_buffer_inx1 = arrow_label_buffer_inx1 - 0.20
                    print("arrow_label_buffer_inx1",arrow_label_buffer_inx1)
                    # print("arrow_label_buffer_inx1 before",arrow_label_buffer_inx1)
                    # arrow_label_buffer_inx1 = arrow_label_buffer_inx1 - 0.27
                    # print("arrow_label_buffer_inx1",arrow_label_buffer_inx1)
                    label_counter1 = 0
                    # if the buffer value doesn't satisfy then directly print the label
                    label_var = ''
                    y_buffer_inx1 = 0
                    # it is the buffer used for placing the labels
                    y_buffer_inx1 = arrow_label_buffer_inx1 * len_of_labels 
                    # final_y is used as final y for labels
                    final_y_inx1 = y - y_buffer_inx1   
                label = label_var + label_
                inx = 1
                if label_counter1 > 5:
                    pass
                else:
                    text_label = axes[inx][iny].text(dup_x - 0.02, final_y_inx1, label, rotation = 'vertical', fontsize=8, picker=True)
                    # print("arrow_label_buffer_inx1 before",arrow_label_buffer_inx1)
                    # arrow_label_buffer_inx1 = arrow_label_buffer_inx1 - 0.27
                    # print("arrow_label_buffer_inx1",arrow_label_buffer_inx1)                
                    text_label = built_dict(drag_dict_usde, text_label,x,y)
                    artist_list.append(text_label)  # NOTE: INSIDE IF
                    if key == 'UP':
                        artist_list.append(axes[inx][iny].arrow(dup_x, y , 0, -0.5, width = 0.005, clip_on = False))
                    else:
                        artist_list.append(axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer_inx1, 0, 0.5, width = 0.005, clip_on = False))
                    

        elif second_axes_flag and y == 49:
            if label_counter > 5:
                pass
            else:
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_usde, text_label,x,y)
                artist_list.append(text_label)  # NOTE: INSIDE IF
                if key == 'UP': #UP
                    artist_list.append(axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer, 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))


            arrow_plot_buffer_inx2, arrow_label_buffer_inx2, slash_buffer_inx2, first_axes_flag, second_axes_flag = extract_current_axes_us_de(x, y+2)
            
            if abs(x - previous_x) <= 0.03 and y == previous_y:
                label_var = '/'
                y_buffer_inx2 = y_buffer_inx2 + (slash_buffer_inx2 * len_of_labels) 
                final_y_inx2 = y - y_buffer_inx2 
                label_counter2 += 1
            else:
                arrow_label_buffer_inx2 = arrow_label_buffer_inx2 - 0.14
                label_counter2 = 0
                # if the buffer value doesn't satisfy then directly print the label
                label_var = ''
                y_buffer_inx2 = 0
                # it is the buffer used for placing the labels
                y_buffer_inx2 = arrow_label_buffer_inx2 * len_of_labels 
                # final_y is used as final y for labels
                final_y_inx2 = y - y_buffer_inx2                         

            label = label_var + label_
            # to plot vr labels on 2nd axes 
            inx = 2
            if label_counter2 > 5:
                pass
            else:            
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y_inx2, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_usde, text_label,x,y)
                artist_list.append(text_label)  # NOTE: INSIDE IF
                if key == 'UP':
                    artist_list.append(axes[inx][iny].arrow(dup_x, y , 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer_inx2, 0, 0.5, width = 0.005, clip_on = False))

        # should not be in first and should not b1
        elif (first_axes_flag and y != 29) or (second_axes_flag and y!= 49) or not (first_axes_flag and second_axes_flag):
            if label_counter > 5:
                pass
            else:
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_usde, text_label,x,y)
                artist_list.append(text_label)  # NOTE: INSIDE IF
                if key == 'UP': #UP
                    artist_list.append(axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer, 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))
        else:
            #put except here
            print("Dead End")
        previous_x, previous_y = x, y
        k += 3
    print("drag_dict_usde",drag_dict_usde)
    return drag_dict_usde
