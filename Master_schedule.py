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


def demo_plots():
    # THIS IS DEMO PLOTS WILL BE USED FOR REFERENCE
    train_timings = [2.17, 2.22, 2.29, 2.32, 2.35, 2.38, 2.44, 2.46, 2.51, 2.56, 2.59, 3.03, 3.15, 3.20]
    stations = ['ST266.78', 'ST266.78', 'UDN262.77', 'BHET257.3', 'SCH252.63', 'MRL245.63', 'NVS237.33', 'NVS237.33', 'VDH228.87', 'AML221.72', 'BIM216.41', 'DGI207.21', 'BL198.22', 'BL198.22']
    print(len(train_timings))
    print(len(stations))

    # halt with 5 mins
    train_timings_1 = [2.30, 2.35, 2.42, 2.45, 2.48, 2.51, 2.57,2.63, 3.04, 3.09, 3.12, 3.17, 3.30, 3.35]
    stations_1 = ['ST266.78', 'ST266.78', 'UDN262.77', 'BHET257.3', 'SCH252.63', 'MRL245.63', 'NVS237.33', 'NVS237.33', 'VDH228.87', 'AML221.72', 'BIM216.41', 'DGI207.21', 'BL198.22', 'BL198.22']
    print(len(train_timings_1))
    print(len(stations_1))

    # reverse train
    train_timings_2 = [5.35, 5.3, 5.17, 5.12, 5.09, 5.04, 4.60, 4.62,4.51, 4.48, 4.45, 4.42, 4.35, 4.3]
    stations_2 = ['ST266.78', 'ST266.78', 'UDN262.77', 'BHET257.3', 'SCH252.63', 'MRL245.63', 'NVS237.33','NVS237.33', 'VDH228.87', 'AML221.72', 'BIM216.41', 'DGI207.21', 'BL198.22', 'BL198.22']
    print(len(train_timings_2))
    print(len(stations_2))

    # intersection of trains
    train_timings_3 =[7.2, 7.15,
                    7.03,7.02,
                    6.59,6.57,
                    6.54,6.51,
                    6.48,6.46,
                    6.43,6.41,
                    6.35, 6.32,
                    6.29, 6.22,
                    6.17,6.15,
                    6.10,6.05,
                    5.57,5.53
                    ]
    stations_3 = ['ST266.78', 'ST266.78', 'UDN262.77','UDN262.77', 'BHET257.3','BHET257.3', 'SCH252.63','SCH252.63', 'MRL245.63','MRL245.63', 'NVS237.33', 'NVS237.33', 'VDH228.87','VDH228.87', 'AML221.72','AML221.72', 'BIM216.41','BIM216.41', 'DGI207.21','DGI207.21','BL198.22', 'BL198.22']
    print(len(train_timings_3))
    print(len(stations_3))
    plt.figure(figsize=(10,6))
    plt.plot(train_timings, stations, color='red')
    plt.plot(train_timings_1, stations_1, color='red')
    plt.plot(train_timings_2, stations_2, color='red')
    plt.plot(train_timings_3, stations_3, color='blue')

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
        df = df.set_index(first_column_series)
        list_2d = []
        for column_name in df.columns:
            column_df = df[column_name]

            # Drop null values in the column DataFrame
            column_df = column_df.dropna()
            column_df = column_df.astype(str)

            # Remove the '1900-01-01 ' prefix from the values in the column
            column_df = column_df.str.replace('1900-01-01 ', '')
            # Convert the column back to datetime type if needed
        #     column_df = pd.to_datetime(column_df)
            column_df = column_df.replace(r'[\s._-]+|^$', np.nan, regex=True)
            column_df = column_df.dropna()
            column_df = pd.DataFrame(column_df)
        #     # Create a new DataFrame for each column
        #     column_df = pd.DataFrame(df[column_name])

        #     # Drop null values in the column DataFrame
        #     column_df = column_df.dropna()

            # Do further operations with the non-null column DataFrame if needed
            # ...
            row_indices = column_df.index.tolist()
            datapoints = column_df.iloc[:, 0].tolist()

            # Create the 2-dimensional list
            list_2d = list_2d + [row_indices, datapoints]
            
            # # Print the non-null column DataFrame
            # print(f"Non-null values in '{column_name}':")
            # print(column_df)
            # print()
        # pass 3d list down and up containt all the combined 2d list made before
        down_up[key] = list_2d
    return down_up


def axes_setting():
    # this will contain all the setting of minor ticks vertical and horizontal
    # TODO : MAKE ALL THE PLOTTING PROCESS AUTOMATED
    y_labes = ['ST266.78', 'UDN262.77', 'BHET257.3', 'SCH252.63', 'MRL245.63', 'NVS237.33', 'VDH228.87', 'AML221.72', 'BIM216.41', 'DGI207.21', 'BL198.22']
    y_no = range(len(y_labes))
    plt.minorticks_on()
    xa = np.linspace(0, 8, 240)
    print(len(xa))
    # TODO : Automate according to stations and can be done with a single loop
    ya = ["BL198.22"]*len(xa)
    plt.plot(xa, ya, color='blue',linewidth=1, linestyle=(0, (1, 1.15)))
    ya = ["DGI207.21"]*len(xa)
    plt.plot(xa, ya, color='blue', linewidth=1, linestyle=(0, (1, 1.15)))
    ya = ["BIM216.41"]*len(xa)
    plt.plot(xa, ya, color='blue', linewidth=1, linestyle=(0, (1, 1.15)))
    ya = ["AML221.72"]*len(xa)
    plt.plot(xa, ya, color='blue', linewidth=1, linestyle=(0, (1, 1.15)))
    ya = ["VDH228.87"]*len(xa)
    plt.plot(xa, ya, color='blue', linewidth=1, linestyle=(0, (1, 1.15)))
    ya = ["NVS237.33"]*len(xa)
    plt.plot(xa, ya, color='blue', linewidth=1, linestyle=(0, (1, 1.15)))
    ya = ["MRL245.63"]*len(xa)
    plt.plot(xa, ya, color='blue', linewidth=1, linestyle=(0, (1, 1.15)))
    ya = ["SCH252.63"]*len(xa)
    plt.plot(xa, ya, color='blue', linewidth=1, linestyle=(0, (1, 1.15)))
    ya = ["BHET257.3"]*len(xa)
    plt.plot(xa, ya, color='blue', linewidth=1, linestyle=(0, (1, 1.15)))
    ya = ["UDN262.77"]*len(xa)
    plt.plot(xa, ya, color='blue', linewidth=1, linestyle=(0, (1, 1.15)))
    ya = ["ST266.78"]*len(xa)
    plt.plot(xa, ya, color='blue', linewidth=1, linestyle=(0, (1, 1.15)))

    # plt.yticks(y_positions, y_labels)
    plt.gca().xaxis.grid(True, which = 'major', linestyle='-', color = 'black')
    plt.gca().xaxis.grid(True, which = 'minor', linestyle='-')
    plt.gca().xaxis.set_minor_locator(MultipleLocator(10/60))
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 3, 4, 5, 6, 7, 8])

    plt.text(2.17,-2,"12902",rotation='vertical')
    plt.arrow(2.17, -1, 0, 1, width = 0.01)

    plt.text(2.30,-2,"12903",rotation='vertical')
    plt.arrow(2.30, -1, 0, 1, width = 0.01)

    plt.text(4.3,12,"12904",rotation='vertical')
    plt.arrow(4.3, 11, 0, -1, width = 0.01)

    plt.text(5.53,12,"12905",rotation='vertical')
    plt.arrow(5.53, 11, 0, -1, width = 0.01)
    plt.tick_params(axis='x', which='minor', labelbottom=True)
    plt.tick_params(labeltop=True, labelright=True)
    minor_labels = ["10", "20", "30", "40", "50"] * 8
    minor_labels.insert(0,"")
    minor_labels.insert(0,"")
    minor_labels.insert(0,"")
    formatter = FixedFormatter(minor_labels)
    plt.gca().xaxis.set_minor_formatter(formatter)
    plt.tick_params(axis='x', which='minor', labelsize=8)

def conversion(station_arrray):
    # this wil multiply with ratios for plotting
    pass
    # return converted_station_array

def trains(station_arrray):
    # This will plot trains
    converted_station_array = conversion(station_arrray)
    


def graph_plotting():
    # will act as a driver function for plotting
    axes_setting()
    demo_plots()
    plt.savefig('master_schedule.png')
    plt.show()

stations_dict = excel_to_pandas('HIREN.xlsx')
print("stations_dict",stations_dict)
trains(stations_array)
#graph_plotting function still has errors that need to be resort, can take old code for plotting.
#graph_plotting()
