import uuid
from labels import extract_current_axes_ue_ds, extract_current_axes_us_de, add_arrow_labels
# Have to make the an array with slashing and original position

def built_dict(dict_name, text_label,train_x,train_y):
    key_name = str(uuid.uuid4())
    # #print(key_name)
    text_label.set_gid(key_name)
    dict_name[key_name] = [train_x, train_y]
    return text_label

def condition_for_text_buffer(label, len_of_labels, arrow_label_buffer, slash_buffer, inx, flag_ueds):
    """should take input len of labels and return variable constant based on len of label"""
    # if len_of_labels <= 5:
    #     #print("entered in below 5")
    #     if inx == 0:
    #         arrow_label_buffer = 0.55
    #     elif  inx == 1:
    #         arrow_label_buffer = 0.42
    #     elif inx == 2:
    #         arrow_label_buffer = 0.27
    #     # ueds
    #     elif inx == 0:
    #         arrow_label_buffer = 0.18
    #     elif  inx == 1:
    #         arrow_label_buffer = 0.16
    #     elif  inx == 2:
    #         arrow_label_buffer = 0.14
    #     # else:
    #     #     #print("no arrow_label_buffer exists") 
    if 5 <len_of_labels <=7:
        # #print("entered in 5 and 7")
        # #print(label,inx,len_of_labels)
        # usde add
        if flag_ueds == False:
            if inx == 0:
                arrow_label_buffer = arrow_label_buffer - 0.04
                slash_buffer = slash_buffer - 0.010
            elif  inx == 1:
                arrow_label_buffer = arrow_label_buffer - 0.05
                slash_buffer = slash_buffer - 0.03
            elif  inx == 2:
                arrow_label_buffer = arrow_label_buffer - 0.04
                slash_buffer = slash_buffer - 0.01
        else:               
            # ueds 
            if inx == 0:
                arrow_label_buffer = arrow_label_buffer - 0.08
                slash_buffer = slash_buffer + 0.01
            elif inx == 1: 
                arrow_label_buffer = arrow_label_buffer - 0.02
                slash_buffer = slash_buffer - 0.05
            elif inx == 2: #DONE
                arrow_label_buffer = arrow_label_buffer - 0.03
                slash_buffer = slash_buffer - 0.01
            # else:
            #     #print("no arrow_label_buffer exists")

    elif 7 < len_of_labels <= 10:
        #print(" entered in 7 and 10")
        #print(label,inx,len_of_labels, flag_ueds)
        # TODO: there is problem regarding up start in intersection from virar
        if flag_ueds == False:
            # set for all inx so have to change the remark len to more then 7 
            # Check what ueds flag is
            if inx == 0: 
                arrow_label_buffer = arrow_label_buffer - 0.08
                slash_buffer = slash_buffer - 0.02
            elif  inx == 1:
                arrow_label_buffer = arrow_label_buffer - 0.02
                slash_buffer = slash_buffer - 0.02
            elif  inx == 2: 
                arrow_label_buffer = arrow_label_buffer - 0.025
                slash_buffer = slash_buffer - 0.005
        else:
            # ueds
            if inx == 0:
                arrow_label_buffer = arrow_label_buffer + 0.01
                slash_buffer = slash_buffer + 0.03
            elif inx == 1:
                arrow_label_buffer = arrow_label_buffer - 0.02
                slash_buffer = slash_buffer - 0.03
            elif inx == 2: 
                arrow_label_buffer = arrow_label_buffer - 0.05
                slash_buffer = slash_buffer - 0.00
            # else:
            #     #print("no arrow_label_buffer exists")

    elif 10 < len_of_labels <= 15:
        # #print(" entered in 10 and 12")
        if flag_ueds == False:
            if label == 'grup 2 mo 16124':
                pass
                #print("yes done it again for")
            if inx == 0:
                arrow_label_buffer = arrow_label_buffer - 0.09
                slash_buffer = slash_buffer - 0.025
            elif  inx == 1:
                arrow_label_buffer = arrow_label_buffer - 0.06
                slash_buffer = slash_buffer - 0.025
            elif  inx == 2:   #DONE
                arrow_label_buffer = arrow_label_buffer - 0.05
                slash_buffer = slash_buffer - 0.005
        else:
            # ueds
            if inx == 0:
                arrow_label_buffer = arrow_label_buffer - 0.05
                slash_buffer = slash_buffer + 0.01
            elif  inx == 1:
                arrow_label_buffer = arrow_label_buffer -0.05
                slash_buffer = slash_buffer - 0.03
            elif  inx == 2:
                arrow_label_buffer = arrow_label_buffer -0.07
                slash_buffer = slash_buffer - 0.00
            # else:
            #     #print("no arrow_label_buffer exists")

    elif 15 < len_of_labels:
        if flag_ueds == False:
            if inx == 0: 
                arrow_label_buffer = arrow_label_buffer - 0.11
                slash_buffer = slash_buffer - 0.03
            elif inx == 1: 
                arrow_label_buffer = arrow_label_buffer - 0.10
                slash_buffer = slash_buffer - 0.03
            elif inx == 2: 
                arrow_label_buffer = arrow_label_buffer - 0.09
                slash_buffer = slash_buffer - 0.01
        else:
            # ueds
            if inx == 0: 
                arrow_label_buffer = arrow_label_buffer - 0.14
                slash_buffer = slash_buffer + 0.00
            elif inx == 1: 
                arrow_label_buffer = arrow_label_buffer - 0.10
                slash_buffer = slash_buffer - 0.03
            elif inx == 2: 
                arrow_label_buffer = arrow_label_buffer - 0.10
                slash_buffer = slash_buffer - 0.015            # else:
            #     #print("no arrow_label_buffer exists")
    # else:
    #     # #print("Problem in len of labels for the label: ", label)
    #     if label[:3] == 'nan':
    #         #print("nan label is found with inx: ", inx, "and label name: ", label)

    return arrow_label_buffer, slash_buffer
    # return arrow_label_buffer


def upEnd_dnStart_label(canvas, axes, express_flag, artist_list, upEnd_dnStart):
    """ this function plot arrow and labels for up-end and down-start"""
    canvas.flush_events()
    k = 1
    previous_x, previous_y,previous_len_of_labels= 0, 0,0
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

        arrow_plot_buffer, arrow_label_buffer, slash_buffer,first_axes_flag, second_axes_flag, inx = extract_current_axes_ue_ds(x, y)
        arrow_label_buffer, slash_buffer = condition_for_text_buffer(label_, len_of_labels, arrow_label_buffer, slash_buffer, inx, True)        
        # arrow_label_buffer = condition_for_text_buffer(label_, len_of_labels, arrow_label_buffer, inx, True)        
        if x == 8 or x == 16 or x == 24:
            x = x - 0.01
        if abs(x - previous_x) <= 0.03 and y == previous_y:
            label_var = '/'
            # previous len
            y_buffer = y_buffer + (slash_buffer * (previous_len_of_labels + 1)) 
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
            if label_counter > 3:
                pass
            else:
                #print("ueds first first", label)
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_ueds, text_label,x,y)
                artist_list.append(text_label)  # NOTE: INSIDE IF
                #print("first first axes ",label)

                if key == 'UP':
                    artist_list.append(axes[inx][iny].arrow(dup_x, y, 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer, 0, 0.5, width = 0.005, clip_on = False))
            # to plot vr labels on 2nd axes

            if express_flag:
                arrow_plot_buffer_inx1, arrow_label_buffer_inx1, slash_buffer_inx1,first_axes_flag, second_axes_flag, _ = extract_current_axes_ue_ds(x, y+2)
                if abs(x - previous_x) <= 0.03 and y == previous_y:
                    label_var = '/'
                    y_buffer_inx1  = y_buffer_inx1  + (slash_buffer_inx1 * (len_of_labels + 1)) 
                    final_y_inx1 = y + y_buffer_inx1  
                    label_counter += 1
                else:
                    # #print(type(label))
                    # if label == "12283":
                    #     #print("Arrow label triggered 12267 j")
                    #     #print(arrow_label_buffer_inx1)
                    label_counter = 0
                    label_var = ''
                    y_buffer_inx1  = 0
                    y_buffer_inx1  = arrow_label_buffer_inx1 * len_of_labels
                    final_y_inx1 = y + y_buffer_inx1                          

                label = label_ + label_var
                inx = 1
                if label_counter > 3:
                    pass
                else:
                    #print("ueds unique", label)
                    text_label = axes[inx][iny].text(dup_x - 0.02, final_y_inx1, label, rotation = 'vertical', fontsize=8, picker=True)
                    text_label = built_dict(drag_dict_ueds, text_label,x,y)
                    artist_list.append(text_label)  # NOTE: INSIDE IF
                    #print("first second axes ",label)

                    if key == 'UP': #UP
                        artist_list.append(axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer_inx1, 0, -0.5, width = 0.005, clip_on = False))
                    else:
                        artist_list.append(axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))

        elif second_axes_flag and y==49 :
            if label_counter > 3:
                pass
            else:
                #print("first second axes ",label)
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_ueds, text_label,x,y)
                artist_list.append(text_label)  # NOTE: INSIDE IF
                if key == 'UP':
                    artist_list.append(axes[inx][iny].arrow(dup_x, y, 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer, 0, 0.5, width = 0.005, clip_on = False))

            # to plot vr labels on 2nd axes 
            arrow_plot_buffer_inx2, arrow_label_buffer_inx2, slash_buffer_inx2,first_axes_flag, second_axes_flag, _ = extract_current_axes_ue_ds(x, y+2)
            if abs(x - previous_x) <= 0.03 and y == previous_y:
                label_var = '/'
                y_buffer_inx2 = y_buffer_inx2 + (slash_buffer_inx2 * (len_of_labels + 1)) 
                final_y_inx2 = y + y_buffer_inx2 
                label_counter += 1
            else:
                # #print("Arrow label triggered inx2")
                # #print(arrow_label_buffer_inx2)
                label_counter = 0
                label_var = ''
                y_buffer_inx2 = 0
                y_buffer_inx2 = arrow_label_buffer_inx2 * len_of_labels
                final_y_inx2 = y + y_buffer_inx2                         

            
            label = label_ + label_var
            inx = 2
            if label_counter > 3:
                pass
            else:
                #print("second second axes ",label)
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

        elif (first_axes_flag and y != 29) or (second_axes_flag and y!= 49) or not (first_axes_flag and second_axes_flag):
            if label_counter > 3:
                pass
            else:
                #print("last elif",label)
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_ueds, text_label,x,y)
                artist_list.append(text_label)  # NOTE: INSIDE IF
                if key == 'UP':
                    artist_list.append(axes[inx][iny].arrow(dup_x, y , 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer, 0, 0.5, width = 0.005, clip_on = False))
        else:
            pass
            # add except here
            #print("ue and ds dead end")
        previous_x, previous_y, previous_len_of_labels = x, y, len_of_labels
        k += 3
    # #print("drag_dict_ueds",drag_dict_ueds)
    return drag_dict_ueds

def upStart_dnEnd_label(canvas, axes, express_flag, artist_list, upStart_dnEnd):   
    """ this function plot arrow and labels for up-start and down-end"""
    canvas.flush_events()
    k = 1
    previous_x, previous_y, previous_len_of_labels= 0, 0,0
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

        arrow_plot_buffer, arrow_label_buffer, slash_buffer, first_axes_flag, second_axes_flag, inx = extract_current_axes_us_de(x, y)
        arrow_label_buffer, slash_buffer = condition_for_text_buffer(label_, len_of_labels, arrow_label_buffer, slash_buffer, inx, False)        
        # arrow_label_buffer = condition_for_text_buffer(label_, len_of_labels, arrow_label_buffer, inx, False)        
        if x == 8 or x == 16 or x == 24:
            x = x - 0.01
        if abs(x - previous_x) <= 0.03 and y == previous_y and not (x == 8 or x==16) :
            
            label_var = '/'
            y_buffer = y_buffer + (slash_buffer * (len_of_labels + 1)) 
            final_y = y + y_buffer  
            label_counter += 1
            #print("label_counter",label_counter)
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
        
        #print("ignore",label)
        if first_axes_flag or y == 29:
            #checking if label counter > 5 then further label plotting will be ignored
            if label_counter > 4:
                pass
            else:
                #print("usde unique one",label)
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_usde, text_label,x,y)           
                artist_list.append(text_label)  # NOTE: INSIDE IF
                if key == 'UP': #UP
                    artist_list.append(axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer, 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))
            
            # to plot vr labels on 2nd axes 
            if express_flag:
                arrow_plot_buffer_inx1, arrow_label_buffer_inx1, slash_buffer_inx1, first_axes_flag, second_axes_flag, inx = extract_current_axes_us_de(x, y+2)
                arrow_label_buffer_inx1, slash_buffer_inx1 = condition_for_text_buffer(label_, len_of_labels, arrow_label_buffer_inx1, slash_buffer_inx1, inx, True)        
                # arrow_label_buffer_inx1 = condition_for_text_buffer(label_, len_of_labels, arrow_label_buffer_inx1, inx, False)        

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
                if abs(x - previous_x) <= 0.03 and y == previous_y and not (x == 8 or x==16):
                    label_var = '/'
                    y_buffer_inx1 = y_buffer_inx1 + (slash_buffer_inx1 * (previous_len_of_labels + 1)) 
                    final_y_inx1 = y - y_buffer_inx1 
                    label_counter += 1
                else:
                    # #print("arrow_label_buffer_inx1 before",arrow_label_buffer_inx1)
                    arrow_label_buffer_inx1 = arrow_label_buffer_inx1 - 0.19
                    # #print("arrow_label_buffer_inx1",arrow_label_buffer_inx1)
                    # #print("arrow_label_buffer_inx1 before",arrow_label_buffer_inx1)
                    # arrow_label_buffer_inx1 = arrow_label_buffer_inx1 - 0.27
                    # #print("arrow_label_buffer_inx1",arrow_label_buffer_inx1)
                    label_counter = 0
                    # if the buffer value doesn't satisfy then directly print the label
                    label_var = ''
                    y_buffer_inx1 = 0
                    # it is the buffer used for placing the labels
                    y_buffer_inx1 = arrow_label_buffer_inx1 * len_of_labels 
                    # final_y is used as final y for labels
                    final_y_inx1 = y - y_buffer_inx1   
                label = label_var + label_
                inx = 1
                if label_counter > 4:
                    pass
                else:
                    #print("usde unique 2",label)
                    text_label = axes[inx][iny].text(dup_x - 0.02, final_y_inx1, label, rotation = 'vertical', fontsize=8, picker=True)
                    # #print("arrow_label_buffer_inx1 before",arrow_label_buffer_inx1)
                    # arrow_label_buffer_inx1 = arrow_label_buffer_inx1 - 0.27
                    # #print("arrow_label_buffer_inx1",arrow_label_buffer_inx1)                
                    text_label = built_dict(drag_dict_usde, text_label,x,y)
                    artist_list.append(text_label)  # NOTE: INSIDE IF
                    #print("usde first first", label)
                    if key == 'UP':
                        artist_list.append(axes[inx][iny].arrow(dup_x, y , 0, -0.5, width = 0.005, clip_on = False))
                    else:
                        artist_list.append(axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer_inx1, 0, 0.5, width = 0.005, clip_on = False))
                    

        elif second_axes_flag and y == 49:
            if label_counter > 4:
                pass
            else:
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_usde, text_label,x,y)
                artist_list.append(text_label)  # NOTE: INSIDE IF
                #print("usde first second", label)

                if key == 'UP': #UP
                    artist_list.append(axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer, 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))


            arrow_plot_buffer_inx2, arrow_label_buffer_inx2, slash_buffer_inx2, first_axes_flag, second_axes_flag, inx = extract_current_axes_us_de(x, y+2)
            arrow_label_buffer_inx2, slash_buffer_inx2 = condition_for_text_buffer(label_, len_of_labels, arrow_label_buffer_inx2, slash_buffer_inx2, inx, True)        
            # arrow_label_buffer_inx2 = condition_for_text_buffer(label_, len_of_labels, arrow_label_buffer_inx2, inx, False)        
            
            if abs(x - previous_x) <= 0.03 and y == previous_y and not (x == 8 or x==16):
                label_var = '/'
                y_buffer_inx2 = y_buffer_inx2 + (slash_buffer_inx2 * (previous_len_of_labels + 1)) 
                final_y_inx2 = y - y_buffer_inx2 
                label_counter += 1
                #print("label_counter2",label_counter)

            else:
                arrow_label_buffer_inx2 = arrow_label_buffer_inx2 - 0.1
                label_counter = 0
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
            if label_counter > 4:
                pass
            else:            
                #print("usde second second", label)
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y_inx2, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_usde, text_label,x,y)
                artist_list.append(text_label)  # NOTE: INSIDE IF
                if key == 'UP':
                    artist_list.append(axes[inx][iny].arrow(dup_x, y , 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y - arrow_plot_buffer_inx2, 0, 0.5, width = 0.005, clip_on = False))

        # should not be in first and should not b1
        elif (first_axes_flag and y != 29) or (second_axes_flag and y!= 49) or not (first_axes_flag and second_axes_flag):
            if label_counter > 4:
                pass
            else:
                #print("usde second second second", label)
                text_label = axes[inx][iny].text(dup_x - 0.02, final_y, label, rotation = 'vertical', fontsize=8, picker=True)
                text_label = built_dict(drag_dict_usde, text_label,x,y)
                artist_list.append(text_label)  # NOTE: INSIDE IF
                if key == 'UP': #UP
                    artist_list.append(axes[inx][iny].arrow(dup_x, y + arrow_plot_buffer, 0, -0.5, width = 0.005, clip_on = False))
                else:
                    artist_list.append(axes[inx][iny].arrow(dup_x, y, 0, 0.5, width = 0.005, clip_on = False))
        else:
            pass
            #put except here
            #print("Dead End")
        previous_x, previous_y, previous_len_of_labels = x, y,len_of_labels
        k += 3
    # #print("drag_dict_usde",drag_dict_usde)
    return drag_dict_usde
