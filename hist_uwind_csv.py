import netCDF4 as cdf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import julian as jd

buoys = pd.read_csv('ASSETS/boyas.csv')['BUOYS']

for buoy in buoys:
        
    data_df = None
    file = 'uwind/HIST/CDF/w' + buoy + '_dy.cdf'
    data_cdf = cdf.Dataset(file)

    uwind = np.array(data_cdf['WU_422']).T[0][0][0]
    uwind[ uwind == 1e+35] = np.NaN

    time = np.array(data_cdf['time'])
    timeMD = np.array(list(map(lambda x : (jd.from_jd(x)).strftime('%m/%d'), time)))

    data_df = pd.DataFrame({'time': timeMD, 'uwind': uwind})
    data_df = data_df.groupby(['time']).mean().reset_index()

    data_df.to_csv('UWIND/HIST/CSV/hist_uwind_' + buoy + '.csv', index=False)
    #print(data_df)

