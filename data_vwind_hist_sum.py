import pandas as pd
import netCDF4 as cdf 
import matplotlib.pyplot as plt
import numpy as np
import julian as jd
from ASSETS.buoy import buoyname

buoys = pd.read_csv('ASSETS/boyas.csv', delimiter=',')['BUOYS']

months = ['', 'ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC', '']

for buoy in buoys:
    try:
        data_df = None
        data_hist = None
        
        data_hist = pd.read_csv('VWIND\HIST\CSV\hist_vwind_' + buoy + '.csv', delimiter=',')
        data_hist = data_hist.drop(59).reset_index() #ELIMINAR 29 DE FEBRERO DEL HISTÓRICO
        
        data_hist = data_hist.drop(['index'], axis=1)
        data_hist['time'] = np.array([int(i[:2]) for i in data_hist['time']])
        data_hist = data_hist.groupby('time').sum()

        fig, ax = plt.subplots(figsize=(12,9))

        ax.bar(data_hist.index, data_hist['vwind'])
        ax.set_xticks(np.arange(0, 14), months)
        ax.set_yticks(np.arange(-250, 250 + 1, 50))

        ax.set_title('Vientos alisios meridionales totales\n' + buoyname(buoy))
        ax.set_xlabel('Mes')
        ax.set_ylabel('Viento resultante')


        plt.figtext(0.1, 0.02, "Fuente: NOAA - GTMBA Sitemap\n(https://www.pmel.noaa.gov/tao/drupal/disdel/)", fontsize=6.5)
        plt.figtext(0.82, 0.02, "Por: Carlo Ilave", fontsize=6.5, family ='serif')


        #plt.show()
        #break
        plt.savefig('VWIND/PLOTS/HIST/vwind_' + buoy)
        plt.close()
        print('grafico creada para la boya ' + buoy)


    except Exception as err:
        print('error en la boya ' + buoy)
        print(err)