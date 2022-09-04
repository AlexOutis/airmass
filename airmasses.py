import numpy as np
import math
import matplotlib.pyplot as plt
import sys
import csv
#from scipy.interpolate import *
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
mag = mag
xnew = np.linspace(x[0], x[len(x) - 1], 300)
model = np.poly1d(np.polyfit(x, dm, 2))
ynew = model(xnew)
plt.plot(xnew, ynew)

#plt.axvline(x=0, color = 'black', linestyle= '--')
#plt.hlines(1.382, x[0], x[len(x) - 1], color = 'grey', linestyle = '--')
#plt.axvline(x=5.7, color = 'black', linestyle= '--')
plot = plt.scatter(x, dm)
plt.ylabel('Relative magnitude of standard star')
plt.xlabel('Time in hours')
plt.show()

