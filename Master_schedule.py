# TODO
# - Clear dots in pdf (30 dots) 
# - Resolve graph_plotting
# - check for specific time domain plots.
# 1. Excel sheet to numpy array. 
# 2. Conversion 0.99 to 0.59  5/3 ratio.
# 3. Numpy array to visualization.
# %%
import pandas as pd
# %%
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedFormatter
from adjustText import adjust_text
import matplotlib.transforms as mtransforms
# TODO: HAVE TO PERFORM IT FOR ALL THE COLUMNS IN SHEETS "DOWN"
# HAVE TO ACCESS ANOTHER SHEET NAMED "UP"


def excel_to_pandas(filename):
    df_dict = pd.read_excel(filename, sheet_name=['DN', 'UP'], header=None)
    down_up = dict()
    dwn_upp = dict()
    for key, df in df_dict.items():
        first_filled_row_index = df.first_valid_index()
        df = df.loc[first_filled_row_index:]
        df = df[2:]
        df = df[:-3]
        df = df.iloc[::-1]
        first_non_empty_row = df.apply(lambda row: row.notnull().any(), axis=1).idxmax()
        df = df.loc[first_non_empty_row:]
        df = df.iloc[::-1]
        df = df.loc[~(df.iloc[:, 0].isna() & df.iloc[:, 0].shift().isin(["EA", "TRT"]))]
        df = df.loc[~df.iloc[:, 0].isin(["EA", "TRT"])]
        df.iloc[:, 0].fillna(method="ffill", inplace=True)
        df = df.dropna(subset=df.columns[2:], how="all")
        df = df.reset_index(drop=True)
        df = df.drop(df.columns[1], axis=1)
        df.iloc[0, 0] = np.nan
        df.columns = df.iloc[0]
        df = df.drop(0)
        first_column_series = df.iloc[:, 0]
        df = df.iloc[:, 1:]
        first_column_series = first_column_series.rename(None)
        first_column_series = first_column_series.str.strip()
        df = df.set_index(first_column_series)
        trains_list = df.columns.tolist()
        list_2d = []
        df = df.loc[:,~df.columns.duplicated()].copy()

        for column_name in df.columns:
            column_df = df[column_name]
            column_df = column_df.dropna()
            column_df = column_df.astype(str)
            column_df = column_df.str.replace('1900-01-01 ', '')
            column_df = column_df.replace(r'([\s_-]+|^$|(\.))', np.nan, regex=True)
#             column_df = column_df.dropna()
#             mask = column_df.str.contains(r'\.+')
#             column_df[mask] = np.nan
            column_df = column_df.dropna()
#             column_df = column_df[column_df != "......"]
            column_df = column_df[column_df.astype(str).str.contains(r'\d\d:\d\d:\d\d', na=False)]
            column_df = pd.DataFrame(column_df)
            row_indices = column_df.index.tolist()
            datapoints = column_df.iloc[:, 0].tolist()

            # Create the 2-dimensional list
            list_2d = list_2d + [row_indices, datapoints]
        down_up[key] = list_2d
        down_up[key + key] = df.index
        dwn_upp[key] = trains_list
    y_axis = ["CCG","BCT","DDR","BA","BDTS","ADH","BVI","BYR","BSR","NSP","VR","VTN","SAH","KLV","PLG","UOI","BOR","VGN","DRD","GVD","BRRD","UBR","SJN","BLD","KEB","VAPI","BAGD","UVD","PAD","ATUL","BL","DGI","JRS","BIM","AML","ACL","VDH","HXR","GNST","NVS","MRL","SCH","BHET","UDN","ST"]
    down_up.pop("DNDN")
    down_up.pop("UPUP")
    return down_up,y_axis, dwn_upp

def conversion(station_dict):
    # this wil multiply with ratios for plotting
    for key, value in station_dict.items():
        for i in range(len(value)):
            if i % 2 == 1:  # Check if it's an alternative column
                for j in range(len(value[i])):
                    time_string = value[i][j]
                    hours, minutes, seconds = map(int, time_string.split(':'))

                    # Convert hours, minutes, and seconds to a decimal representation of hours
                    time_in_hours = hours + (minutes / 60) + (seconds / 3600)

                    after_decimal = time_in_hours % 1
                    time_in_hours = int(time_in_hours) + after_decimal

                    # Update the value in the dictionary
                    value[i][j] = str(round(time_in_hours, 2))

                value[i] = [float(num) for num in value[i]]   
    return station_dict

def plot_trains(station_dict, y_axis, trains_dict):
    y_axis.insert(0," ")
    y_axis.insert(0,"  ")
    y_axis.insert(0,"   ")
    y_axis.insert(0,"    ")
    y_axis.append("     ")
    y_axis.append("      ")
    y_axis.append("       ")
    y_axis.append("        ")
    print(" ")
    print("Trains dictionary: ", trains_dict)
    print(" ")
# Arrow:
#     eg. axes[2].arrow(20, 25, 0, 1, width = 0.01, head_width=0.1, head_length=0.1, color = 'blue')
#     20---> x axis
#     25 --> y axis
#     1 --> size of line segment
 


   
    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 50))
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            for j in range(len(arr_2d[i])):
                arr_2d[i][j] = y_axis.index(arr_2d[i][j])
    # Subplot 1: 0-8
    axes[0].minorticks_on()

    # print('station_dict : ', station_dict)
    # xa_0 = np.linspace(0, 8, 200)
    xa_0 = np.arange(0, 8, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[0].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_0)
        axes[0].scatter(xa_0, ya, marker=',',color='blue', s=0.3)
        
    ### ARROW DowN        
    k = 1    
    for i in range(len(station_dict['DN']) // 2):    
        if 0 <= station_dict['DN'][k][0] <= 8:
            axes[0].text(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - 2.3, trains_dict['DN'][i], rotation = 'vertical', fontsize=9)
            axes[0].arrow(station_dict['DN'][k][0], station_dict['DN'][k - 1][0], 0, 1, width = 0.005)
        k += 2
    
    ### ARROW UP        
    k = 1    
    for i in range(len(station_dict['UP']) // 2):    
        if 0 <= station_dict['UP'][k][0] <= 8:
            axes[0].text(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1.3, trains_dict['UP'][i], rotation = 'vertical', fontsize=9)
            axes[0].arrow(station_dict['UP'][k][0], station_dict['UP'][k - 1][0], 0, -1, width = 0.005)
        k += 2     
    
    axes[0].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[0].xaxis.grid(True, which='minor', linestyle='-')
    axes[0].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[0].set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8])
    axes[0].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
    axes[0].set_yticks(range(len(y_axis)))
    axes[0].set_yticklabels(y_axis)
    axes[0].tick_params(axis='x', which='minor', labelbottom=True)
    axes[0].tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[0].xaxis.set_minor_formatter(formatter)
    axes[0].tick_params(axis='x', which='minor', labelsize=6)
    axes[0].set_xlim(0, 8)
    axes[0].set_ylim(0, len(y_axis))
  
    # Subplot 2: 8-16
    axes[1].minorticks_on()
    xa_1 =np.arange(8, 16, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[1].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_1)
        axes[1].scatter(xa_1, ya, marker=',',color='blue', s=0.3)
        
    ### ARROW DowN        
    k = 1    
    for i in range(len(station_dict['DN']) // 2):    
        if 8 <= station_dict['DN'][k][0] <= 16:
            axes[1].text(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - 2.3, trains_dict['DN'][i], rotation = 'vertical', fontsize=9)
            axes[1].arrow(station_dict['DN'][k][0], station_dict['DN'][k - 1][0], 0, 1, width = 0.005)
        k += 2  
        
    ### ARROW UP        
    k = 1    
    for i in range(len(station_dict['UP']) // 2):    
        if 8 <= station_dict['UP'][k][0] <= 16:
            axes[1].text(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1.3, trains_dict['UP'][i], rotation = 'vertical', fontsize=9)
            axes[1].arrow(station_dict['UP'][k][0], station_dict['UP'][k - 1][0], 0, -1, width = 0.005)
        k += 2
        
    axes[1].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[1].xaxis.grid(True, which='minor', linestyle='-')
    axes[1].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[1].set_xticks([8, 9, 10, 11, 12, 13, 14, 15, 16])
    axes[1].set_xticklabels([8, 9, 10, 11, 12, 13, 14, 15, 16])
    axes[1].set_yticks(range(len(y_axis)))
    axes[1].set_yticklabels(y_axis)
    axes[1].tick_params(axis='x', which='minor', labelbottom=True)
    axes[1].tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[1].xaxis.set_minor_formatter(formatter)
    axes[1].tick_params(axis='x', which='minor', labelsize=6)
    axes[1].set_xlim(8, 16)
    axes[1].set_ylim(0, len(y_axis))

    # Subplot 3: 16-24
    
    axes[2].minorticks_on()
    xa_2 = np.arange(16, 24, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[2].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_2)
        axes[2].scatter(xa_2, ya, marker=',',color='blue', s=0.3)

    ### ARROW DowN         
    k = 1  
    arrow_lis = []
    for i in range(len(station_dict['DN']) // 2):    
        if 16 <= station_dict['DN'][k][0] <= 24:
            arrow_lis.append(station_dict['DN'][k][0])
            count = arrow_lis.count(station_dict['DN'][k][0])
            # print(arrow_lis)
            

    ### ARROW UP   
    k = 1    
    for i in range(len(station_dict['UP']) // 2):    
        if 16 <= station_dict['UP'][k][0] <= 24:
            axes[2].text(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1.3, trains_dict['UP'][i], rotation = 'vertical', fontsize=9)
            axes[2].arrow(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1, 0, -1, width = 0.005)
        k += 2    
    
    fontsize = 7
    offset = 2.3

    k = 1
    texts = []
    i = 0
    for _ in trains_dict['DN']:
        axes[2].arrow(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - 1, 0, 1, width = 0.005)
        texts.append(axes[2].text(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - offset, trains_dict['DN'][i], rotation='vertical', fontsize=fontsize))
        
        x_positions = [station_dict['DN'][k][0], station_dict['DN'][k][0]]
        y_positions = [station_dict['DN'][k - 1][0] - offset, station_dict['DN'][k - 1][0] - offset - 0.5]        
        k += 2
        i += 1
   
    adjust_text(texts, ax=axes[2], expand=(0.5, 0.5), time_lim=1, force_text=(1,0))
    
    axes[2].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[2].xaxis.grid(True, which='minor', linestyle='-')
    axes[2].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[2].set_xticks([16, 17, 18, 19, 20, 21, 22, 23, 24])
    axes[2].set_xticklabels([16, 17, 18, 19, 20, 21, 22, 23, 24])
    axes[2].set_yticks(range(len(y_axis)))
    axes[2].set_yticklabels(y_axis)
    axes[2].tick_params(axis='x', which='minor', labelbottom=True)
    axes[2].tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[2].xaxis.set_minor_formatter(formatter)
    axes[2].tick_params(axis='x', which='minor', labelsize=6)
    axes[2].set_xlim(16, 24)
    axes[2].set_ylim(0, len(y_axis))
    
    
    # Subplot 4: 24-31
       
    axes[3].minorticks_on()
    xa_3 = np.arange(24, 32, 0.03333)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            axes[3].plot(arr_2d[i+1], arr_2d[i], color='red')
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index] * len(xa_3)
        axes[3].scatter(xa_3, ya, marker=',',color='blue', s=0.3)
        
        
    ### ARROW DowN       
    k = 1    
    for i in range(len(station_dict['DN']) // 2):    
        if 24 <= station_dict['DN'][k][0] <= 32:
            axes[3].text(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - 2.3, trains_dict['DN'][i], rotation = 'vertical', fontsize=9)
            axes[3].arrow(station_dict['DN'][k][0], station_dict['DN'][k - 1][0] - 1, 0, 1, width = 0.005)
        k += 2
        
    ### ARROW UP        
    k = 1    
    for i in range(len(station_dict['UP']) // 2):    
        if 24 <= station_dict['UP'][k][0] <= 32:
            axes[3].text(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1.3, trains_dict['UP'][i], rotation = 'vertical', fontsize=9)
            axes[3].arrow(station_dict['UP'][k][0], station_dict['UP'][k - 1][0] + 1, 0, -1, width = 0.005)
        k += 2     
        
    axes[3].xaxis.grid(True, which='major', linestyle='-', color='black')
    axes[3].xaxis.grid(True, which='minor', linestyle='-')
    axes[3].xaxis.set_minor_locator(MultipleLocator(10 / 60))
    axes[3].set_xticks([24,25,26,27,28,29,30,31,32])
    axes[3].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8])
    axes[3].set_yticks(range(len(y_axis)))
    axes[3].set_yticklabels(y_axis)
    axes[3].tick_params(axis='x', which='minor', labelbottom=True)
    axes[3].tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0, "")
    formatter = FixedFormatter(minor_labels)
    axes[3].xaxis.set_minor_formatter(formatter)
    axes[3].tick_params(axis='x', which='minor', labelsize=6)
    axes[3].set_xlim(24, 32)
    axes[3].set_ylim(0, len(y_axis))
    
    plt.tight_layout()
#     for me, ax in enumerate(axes):
#         ax.set_title(f"Subplot {me+1}")
#         # Save each subplot as a separate PDF
#         plt.savefig(f"subplot_{me+1}.pdf")
    fig.savefig(
    "frac0.pdf",
    bbox_inches=mtransforms.Bbox([[0, 0.75], [1,1]]).transformed(
        fig.transFigure - fig.dpi_scale_trans
    ),format="pdf")
    fig.savefig(
    "frac1.pdf",
    bbox_inches=mtransforms.Bbox([[0, 0.5], [1, 0.75]]).transformed(
        fig.transFigure - fig.dpi_scale_trans
    ),format="pdf")
    fig.savefig(
    "frac2.pdf",
    bbox_inches=mtransforms.Bbox([[0, 0.25], [1, 0.5]]).transformed(
        fig.transFigure - fig.dpi_scale_trans
    ),format="pdf")
    fig.savefig(
    "frac3.pdf",
    bbox_inches=mtransforms.Bbox([[0, 0], [1, 0.25]]).transformed(
        fig.transFigure - fig.dpi_scale_trans
    ),format="pdf")


    print("saved-------------------------")
    # for i, ax in enumerate(axes.flat):
    #     ax.set_title('Plot {}'.format(i+1))
    #     plt.savefig('subplot_{}.pdf'.format(i+1), format="pdf")
    #     ax.clear()
    plt.show()

def add_24_down_up(down_up):
    arr_2= down_up['DN']
    for hi in range(1, len(arr_2),2):
        arr_2[hi] = [x + 24 if x < 1 else x for x in arr_2[hi]]
    down_up['DN'] = arr_2
    arr_2 = down_up['UP']
    # Add 24 to each element  the arrayin
    for h in range(1, len(arr_2),2):
        arr_2[h] = [x + 24 if x < 23 else x for x in arr_2[h]]
    down_up['UP'] = arr_2
#     print(down_up)
    return down_up


down_up, y_labes, dwn_upp =  excel_to_pandas('HIREN.xlsx')
for key in dwn_upp:
    dwn_upp[key] = [value for value in dwn_upp[key]]



down_up = conversion(down_up)
down_up = add_24_down_up(down_up)
plot_trains(down_up, y_labes, dwn_upp)
