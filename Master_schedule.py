# TODO
# - Clear dots in pdf (30 dots) 
# - Resolve graph_plotting
# - check for specific time domain plots.
# 1. Excel sheet to numpy array. 
# 2. Conversion 0.99 to 0.59  5/3 ratio.
# 3. Numpy array to visualization.
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedFormatter


# TODO: HAVE TO PERFORM IT FOR ALL THE COLUMNS IN SHEETS "DOWN"
# HAVE TO ACCESS ANOTHER SHEET NAMED "UP"
def excel_to_pandas(filename):
    df_dict = pd.read_excel(filename, sheet_name=['DN', 'UP'])
    down_up = dict()
    for key, df in df_dict.items():
        df = df.iloc[2:]
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
        list_2d = []
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
            column_df = column_df[column_df.astype(str).str.contains(r'\d', na=False)]
            column_df = pd.DataFrame(column_df)
            row_indices = column_df.index.tolist()
            datapoints = column_df.iloc[:, 0].tolist()

            # Create the 2-dimensional list
            list_2d = list_2d + [row_indices, datapoints]
        down_up[key] = list_2d
        down_up[key + key] = df.index

    y_axis = list(dict.fromkeys(down_up['DNDN'].values.tolist()))
    down_up.pop("DNDN")
    down_up.pop("UPUP")
    return down_up,y_axis
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
                    rescaled_value = after_decimal * 3/5

                    time_in_hours = int(time_in_hours) + rescaled_value

                    # Update the value in the dictionary
                    value[i][j] = str(round(time_in_hours, 2))

                value[i] = [float(num) for num in value[i]]   
    return station_dict

def plot_trains(station_dict,y_axis):
    plt.figure(figsize=(20,12))
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            for j in range(len(arr_2d[i])):
                arr_2d[i][j] = y_axis.index(arr_2d[i][j])
    print(station_dict)
    for key, arr_2d in station_dict.items():
        for i in range(0, len(arr_2d), 2):
            plt.plot(arr_2d[i+1], arr_2d[i], color='red')
    plt.minorticks_on()
    xa = np.linspace(0, 24, 720)
    for i in range(len(y_axis)):
        y_index = y_axis[i]
        ya = [y_index]*len(xa)
        plt.plot(xa, ya, color='blue',linewidth=1, linestyle=(0, (1, 1.15)))
    plt.gca().xaxis.grid(True, which = 'major', linestyle='-', color = 'black')
    plt.gca().xaxis.grid(True, which = 'minor', linestyle='-')
    plt.gca().xaxis.set_minor_locator(MultipleLocator(10/60))
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],[0, 1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33], y_axis)
    plt.tick_params(axis='x', which='minor', labelbottom=True)
    plt.tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 24
    minor_labels.insert(0,"")
#     minor_labels.insert(0,"")
#     minor_labels.insert(0,"")
    formatter = FixedFormatter(minor_labels)
    plt.gca().xaxis.set_minor_formatter(formatter)
    plt.tick_params(axis='x', which='minor', labelsize=6)
    plt.xlim(0, 24)
    plt.ylim(0, 33)
    plt.savefig("myImagePDF.pdf", format="pdf")
    plt.show()
down_up, y_labes =  excel_to_pandas("HIREN.xlsx")
down_up = conversion(down_up)
plot_trains(down_up, y_labes)