import netCDF4 as cdf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import julian as jd

buoys = pd.read_csv('ASSETS/boyas.csv')['BUOYS']

for buoy in buoys:
        
    file = 'TZ/HIST/CDF/t' + buoy + '_dy.cdf'
    data_cdf = cdf.Dataset(file)

    depth = np.array(data_cdf['depth'])
    depth = [str(int(i)) for i in depth]

    tz = np.array(data_cdf['T_20']).T[0][0].T
    tz[ tz == 1e+35] = np.NaN

    time = np.array(data_cdf['time'])
    timeMD = np.array(list(map(lambda x : (jd.from_jd(x)).strftime('%m/%d'), time)))

    data_df = pd.DataFrame(tz)
    data_df.columns = depth

    data_df['time'] = timeMD

    data_df = data_df.groupby(['time']).mean().reset_index()

    data_df.to_csv('TZ/HIST/CSV/hist_tz_' + buoy + '.csv', index=False)