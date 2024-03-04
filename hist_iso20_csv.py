import netCDF4 as cdf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import julian as jd

buoys = pd.read_csv('ASSETS/boyas.csv')['BUOYS']

for buoy in buoys:
        
    file = 'ISO20/HIST/CDF/iso' + buoy + '_dy.cdf'
    data_cdf = cdf.Dataset(file)

    iso20 = np.array(data_cdf['ISO_6']).T[0][0][0]
    iso20[ iso20 == 1e+35] = np.NaN

    time = np.array(data_cdf['time'])
    timeMD = np.array(list(map(lambda x : (jd.from_jd(x)).strftime('%m/%d'), time)))

    data_df = pd.DataFrame({'time': timeMD, 'iso20': iso20})
    data_df = data_df.groupby(['time']).mean().reset_index()

    data_df.to_csv('ISO20/HIST/CSV/hist_iso20_' + buoy + '.csv', index=False)
    #print(data_df)
