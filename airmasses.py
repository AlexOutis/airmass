import numpy as np
import matplotlib.pyplot as plt
import csv
import math
from scipy.optimize import curve_fit
filename = 'lcurvePoints.csv'
fields = []
rows = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        rows.append(row)

def timeconv(string):
    temp = string
    hh, mm, ss = list(map(float, temp.split(':')))
    if (hh < 12): hh += 24
    return hh + mm/60 + ss/3600

def func(x, a, b, c, d):
    return a / np.cos(b * x + d) + c

x, y, z, mag = [np.empty(0) for i in range(4)]

for row in rows:
    rowstr = row[0]
    x1, y1, z1, rat  = rowstr.split()
    x1 = timeconv(x1); y1 = float(y1)
    x = np.append(x, x1); y = np.append(y, y1)

x -= x[0]
y /= y[0]
dm = -2.5 * np.log10(y)

param, pcov = curve_fit(func, x, dm, bounds=([0.025, 0.15, -0.4, -1.6], [0.2, 0.4, -0.2, -1.1]))
xnew = np.linspace(x[0], x[len(x) - 1], 300)
ans = (param[0]/np.cos(param[1] *xnew + param[3])) + param[2]


plt.axvline(x=-param[3]/param[1], color = 'black', linestyle= '--')
plt.scatter(x, dm)
plt.plot(xnew, ans, label =f'extinction: {round(param[0], 2)}')
plt.ylabel('Relative magnitude of standard star')
plt.xlabel('Time in hours')
plt.legend()
plt.show()
