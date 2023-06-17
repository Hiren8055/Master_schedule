import matplotlib.pyplot as plt
import numpy as np

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






y_labes = ['ST266.78', 'UDN262.77', 'BHET257.3', 'SCH252.63', 'MRL245.63', 'NVS237.33', 'VDH228.87', 'AML221.72', 'BIM216.41', 'DGI207.21', 'BL198.22']
y_no = range(len(y_labes))

plt.figure(figsize=(10,6))

plt.plot(train_timings, stations, color='red')
plt.plot(train_timings_1, stations_1, color='red')
plt.plot(train_timings_2, stations_2, color='red')
plt.plot(train_timings_3, stations_3, color='blue')

xa = np.linspace(0, 8, 240)
print(len(xa))
ya = ["BL198.22"]*len(xa)
plt.plot(xa, ya, color='blue', linewidth=1, linestyle=':')
ya = ["DGI207.21"]*len(xa)
plt.plot(xa, ya, color='blue', linewidth=1, linestyle=':')
ya = ["BIM216.41"]*len(xa)
plt.plot(xa, ya, color='blue', linewidth=1, linestyle=':')
ya = ["AML221.72"]*len(xa)
plt.plot(xa, ya, color='blue', linewidth=1, linestyle=':')
ya = ["VDH228.87"]*len(xa)
plt.plot(xa, ya, color='blue', linewidth=1, linestyle=':')
ya = ["NVS237.33"]*len(xa)
plt.plot(xa, ya, color='blue', linewidth=1, linestyle=':')
ya = ["MRL245.63"]*len(xa)
plt.plot(xa, ya, color='blue', linewidth=1, linestyle=':')
ya = ["SCH252.63"]*len(xa)
plt.plot(xa, ya, color='blue', linewidth=1, linestyle=':')
ya = ["BHET257.3"]*len(xa)
plt.plot(xa, ya, color='blue', linewidth=1, linestyle=':')
ya = ["UDN262.77"]*len(xa)
plt.plot(xa, ya, color='blue', linewidth=1, linestyle=':')
ya = ["ST266.78"]*len(xa)
plt.plot(xa, ya, color='blue', linewidth=1, linestyle=':')

# plt.yticks(y_positions, y_labels)
plt.gca().xaxis.grid(True, linestyle='-')
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 3, 4, 5, 6, 7, 8])

plt.text(2.17,-2,"12902",rotation='vertical')
plt.arrow(2.17, -1, 0, 1, width = 0.01)

plt.text(2.30,-2,"12903",rotation='vertical')
plt.arrow(2.30, -1, 0, 1, width = 0.01)

plt.text(4.3,12,"12904",rotation='vertical')
plt.arrow(4.3, 11, 0, -1, width = 0.01)

plt.text(5.53,12,"12905",rotation='vertical')
plt.arrow(5.53, 11, 0, -1, width = 0.01)

plt.tick_params(labeltop=True, labelright=True)
plt.savefig('master_schedule.png')
# plt.xlabel("Time")
# plt.legend()
plt.show()
# plt.yticks(y_no, y_labels)


# plt.ylim(-0.5, len(y_labels) - 0.5)
# plt.xlim(0, 8)
