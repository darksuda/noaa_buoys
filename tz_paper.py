import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import netCDF4 as cdf 
import julian as jd
from datetime import datetime, timedelta

t = np.arange(datetime(2022,12,31), datetime(2025,1,1), timedelta(days=1)).astype(datetime)
t = np.array(list(map(lambda x : (x).strftime('%Y/%m/%d'), t)))


file = 't0n95w_5day_2023-2024.cdf'

nan_values = []

a = np.empty((732))
a[:] = np.nan 

data_cdf = cdf.Dataset(file)
depth = np.array(data_cdf['depth'])
depth = [int(i) for i in depth]

tz = np.array(data_cdf['T_20']).T[0][0].T
tz[ tz == 1e+35] = np.NaN

time = np.array(data_cdf['time'])
timeMD = np.array(list(map(lambda x : (jd.from_jd(x)).strftime('%Y/%m/%d'), time)))
print(timeMD)

fig, ax = plt.subplots(figsize=(12, 9))

ax.plot(t, a)
plot = ax.contourf(timeMD, depth, tz.T, cmap = 'rainbow', levels=np.arange(10, 32+ 1, 1))
plot2 = ax.contour(plot, levels=np.arange(10, 32+ 1, 1), colors = 'black', linewidths= 0.5)
ax.clabel(plot2, inline = True, fontsize= 8)
ax.set_xticks(['2023/01/01', '2023/03/01', '2023/06/01', '2023/09/01', '2023/12/01', '2024/01/01',  '2024/03/01', '2024/06/01', '2024/09/01', '2024/12/01', '2024/12/31'], ['ENE\n2023', 'MAR', 'JUN', 'SEP', 'DIC', 'ENE\n2024', 'MAR', 'JUN', 'SEP', 'DIC', ''])
#ax.set_xticks(['2024/01/01',  '2024/03/01', '2024/06/01', '2024/09/01', '2024/12/01', '2024/12/31'], ['ENE\n2024', 'MAR', 'JUN', 'SEP', 'DIC', 'ENE\n2024'])

#ax.set_xbound('2024/01/01', '2024/12/31')
ax.set_ybound(0, 300)
ax.invert_yaxis()

plt.show()