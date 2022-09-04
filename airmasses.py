import numpy as np
import math
import matplotlib.pyplot as plt
import sys
import csv
from scipy.optimize import curve_fit
filename = 'lcurvePoints.csv'
fields = []
rows = []
t0 = 0

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
        
    

i = 0
x = []
y = []
z = []
mag = []
for row in rows:
   # print(row)
    rowstr = row[0]
    x0, y0, z0, rat  = rowstr.split()
    x0 = timeconv(x0)
    y0 = float(y0)
    z0 = float(z0)
    rat = float(rat)
    x.append(x0), y.append(y0)
    #print(type(x0))
    rat = z0 / y0
    mag0 = -2.5 * math.log10(rat)
    mag.append(mag0)

x00 = x[0]
for i in range(len(x)):
    x[i] -= x00
y00 = y[0]
dm = []
for i in range(len(y)):
    y[i] /= y00
    dm.append(-2.5 * math.log10(y[i]))
#print(x)
#print(dm)
xnew = np.linspace(x[0], x[len(x) - 1], 300)

param, pcov = curve_fit(func, x, dm, bounds=([0.025, 0.15, -0.4, -1.6], [0.2, 0.4, -0.2, -1.1]))

ans = (param[0]/np.cos(param[1] *xnew + param[3])) + param[2]
plt.axvline(x=-param[3]/param[1], color = 'black', linestyle= '--')
plt.scatter(x, dm)
plt.plot(xnew, ans, label =f'extinction: {round(param[0], 2)}')
plt.ylabel('Relative magnitude of standard star')
plt.xlabel('Time in hours')
plt.legend()
plt.show()

