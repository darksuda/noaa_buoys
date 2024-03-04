import netCDF4 as cdf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import julian as jd

buoys = pd.read_csv('ASSETS/boyas.csv')['BUOYS']

for buoy in buoys:
        
    file = 'HDIN/HIST/CDF/dyn' + buoy + '_dy.cdf'
    data_cdf = cdf.Dataset(file)

    hdin = np.array(data_cdf['DYN_13']).T[0][0][0]
    hdin[ hdin == 1e+35] = np.NaN

    time = np.array(data_cdf['time'])
    timeMD = np.array(list(map(lambda x : (jd.from_jd(x)).strftime('%m/%d'), time)))

    data_df = pd.DataFrame({'time': timeMD, 'hdin': hdin})
    data_df = data_df.groupby(['time']).mean().reset_index()
    
    data_df.to_csv('HDIN/HIST/CSV/hist_hdin_' + buoy + '.csv', index=False)


