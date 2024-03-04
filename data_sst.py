import pandas as pd
import netCDF4 as cdf 
import matplotlib.pyplot as plt
import numpy as np
import julian as jd
from ASSETS.buoy import buoyname

buoys = pd.read_csv('ASSETS/boyas.csv', delimiter=',')['BUOYS']
year = '2023'

time_numbers = ['01/01', '02/01', '03/01', '04/01', '05/01', '06/01', '07/01', '08/01', '09/01', '10/01', '11/01', '12/01']
months = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']

for buoy in buoys:
    try:
        data_hist = pd.read_csv('sst\HIST\CSV\hist_sst_' + buoy + '.csv', delimiter=',')
        data_hist = data_hist.drop(59).reset_index() #ELIMINAR 29 DE FEBRERO DEL HISTÓRICO

        file = 'SST/DATA/' + year + '/sst' + buoy + '_dy.cdf'
        data_cdf = cdf.Dataset(file)

        sst = np.array(data_cdf['T_25']).T[0][0][0]
        sst[ sst == 1e+35] = np.NaN

        time = np.array(data_cdf['time'])
        timeMD = np.array(list(map(lambda x : (jd.from_jd(x)).strftime('%m/%d'), time)))

        data_df = pd.DataFrame({'time': timeMD, 'sst': sst})
        data_df = data_df.groupby(['time']).mean().reset_index()
        data_df['anom'] = data_df['sst'] - data_hist['sst']

        if int(year) % 4 == 0:
            index29 = data_df[data_df['time'] == '02/29'].index
            data_df = data_df.drop(index29).reset_index()

        data_hist['nan'] = np.empty(365)
        data_hist['nan'][:] = np.nan

        fig, ax = plt.subplots(2, figsize=(12,9))

        ax[0].plot(data_hist['time'], data_hist['sst'], color = '#5b02a8', label='histórico')
        ax[0].bar(data_df['time'], data_df['sst'], color = '#a4f542', label=year)

        ax[1].plot(data_hist['time'], data_hist['nan'])
        ax[1].bar(data_df[data_df['anom']>0]['time'] ,data_df[data_df['anom']>0]['anom'] , color='red')
        ax[1].bar(data_df[data_df['anom']<=0]['time'] ,data_df[data_df['anom']<=0]['anom'] , color='blue')
        ax[1].axhline(y=0, color='#a2a4a6', linestyle='dashed')

        ax[0].set_ybound(15, 35)
        ax[1].set_ybound(-10, 10)
        ax[1].set_yticks(np.arange(-10, 11, 2))

        for i in ax:
            i.set_xbound('01/01', '12/31')
            i.set_xticks(time_numbers, months)

        ax[0].set_title('Temperatura superficial\n' + buoyname(buoy) + ' - ' + year)
        ax[0].set_ylabel('Temperatura (°C)')
        ax[1].set_xlabel('Mes')
        ax[1].set_ylabel('Anomalía (m)')

        ax[0].legend()
        ax[1].grid()

        plt.savefig('SST/PLOTS/' + year + '/sst_' + buoy + '_' + year)
        #plt.show()
        plt.close()
        #break


    except Exception as err:
        print('error en la boya ' + buoy)
        print(err)