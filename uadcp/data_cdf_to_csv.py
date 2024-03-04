import netCDF4 as cdf 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt  
import julian as jd

buoys = ['0n110w', '8n125w', '0n140w', '0n170w', '0n165e', '0n156e', '0n147e']

for buoy in buoys:

    file = 'datos/adcp' + buoy + '_dy.cdf'
    data = cdf.Dataset(file)
    time = np.array(data['time'])
    depth = np.array(data['depth'])

    time_cvrtd = []
    years = []
    months = []
    days = []
    date_str = []

    for i in time:
        date = jd.from_jd(i).strftime("%Y/%m/%d")
        years.append(int(date[:4]))
        months.append(int(date[5:7]))
        days.append(int(date[8:]))
        date_str.append(date)

    uc = np.array(data['u_1205']).T[0][0].T
    uc[uc == 1e+35] = np.nan
    data_df = pd.DataFrame(uc, columns=depth)

    data_df.insert(loc=0,
            column='year',
            value=years)
    data_df.insert(loc=1,
            column='month',
            value=months)
    data_df.insert(loc=2,
            column='day',
            value=days)
    data_df.insert(loc=3,
            column='date_str',
            value=date_str)

    data_df.to_csv('uadcp_' + buoy + '.csv', index=False)

    print('dataframe ' + buoy + ' created')