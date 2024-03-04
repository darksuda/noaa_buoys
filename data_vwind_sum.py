import pandas as pd
import netCDF4 as cdf 
import matplotlib.pyplot as plt
import numpy as np
import julian as jd
from ASSETS.buoy import buoyname

buoys = pd.read_csv('ASSETS/boyas.csv', delimiter=',')['BUOYS']
year = '2023'

months = ['', 'ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC','']

for buoy in buoys:
    try:
        data_df = None
        data_hist = None
        
        data_hist = pd.read_csv('VWIND\HIST\CSV\hist_vwind_' + buoy + '.csv', delimiter=',')
        data_hist = data_hist.drop(59).reset_index() #ELIMINAR 29 DE FEBRERO DEL HISTÓRICO
        
        file = 'VWIND/DATA/' + year + '/w' + buoy + '_dy.cdf'
        data_cdf = cdf.Dataset(file)

        uwind = np.array(data_cdf['WV_423']).T[0][0][0]
        uwind[ uwind == 1e+35] = np.NaN

        time = np.array(data_cdf['time'])
        timeMD = np.array(list(map(lambda x : (jd.from_jd(x)).strftime('%m/%d'), time)))

        data_df = pd.DataFrame({'time': timeMD, 'vwind': uwind})
        data_df = data_df.groupby(['time']).mean().reset_index()
        data_df['anom'] = data_df['vwind'] - data_hist['vwind']

        if int(year) % 4 == 0:
            index29 = data_df[data_df['time'] == '02/29'].index
            data_df = data_df.drop(index29).reset_index()

        data_hist['nan'] = np.empty(365)
        data_hist['nan'][:] = np.nan

        data_df['time'] = np.array([int(i[:2]) for i in data_df['time']])

        data_df = data_df.groupby('time').sum()

        fig, ax = plt.subplots( figsize=(12,9))
        
        ax.bar(data_df.index, data_df['vwind'])
        ax.set_xticks(np.arange(0, 14), months)
        ax.set_yticks(np.arange(-250, 250 + 1, 50))
        ax.set_xlabel('Mes')
        ax.set_ylabel('Viento resultante')

        ax.set_title('Vientos alisios meridionales totales\n' + buoyname(buoy) + ' - ' + year)
        
        plt.figtext(0.1, 0.02, "Fuente: NOAA - GTMBA Sitemap\n(https://www.pmel.noaa.gov/tao/drupal/disdel/)", fontsize=6.5)
        plt.figtext(0.82, 0.02, "Por: Carlo Ilave", fontsize=6.5, family ='serif')

        #plt.show()
        #break
        plt.savefig('VWIND/PLOTS/' + year + '/vwind_' + buoy + '_' + year + '_sum')
        plt.close()
        print('grafico creada para la boya ' + buoy)
        
    except Exception as err:
        print('error en la boya ' + buoy)
        print(err)