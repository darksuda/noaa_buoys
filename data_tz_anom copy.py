import netCDF4 as cdf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import julian as jd
from ASSETS.buoy import buoyname

buoys = pd.read_csv('ASSETS/boyas.csv')['BUOYS']
buoys = ['0n165e']
year = '1996'

time_numbers = ['01/01', '02/01', '03/01', '04/01', '05/01', '06/01', '07/01', '08/01', '09/01', '10/01', '11/01', '12/01']
months = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']

for buoy in buoys:

    try:
        data_hist = pd.read_csv('TZ\HIST\CSV\hist_tz_' + buoy + '.csv', delimiter=',')
        data_hist = data_hist.drop(59).reset_index() #ELIMINAR 29 DE FEBRERO DEL HISTÓRICO

        file = 'TZ/DATA/' + year + '/t'+ buoy+'_5day.cdf'
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

        if int(year) % 4 == 0:
            index29 = data_df[data_df['time'] == '02/29'].index
            data_df = data_df.drop(index29).reset_index()

        data_anom = pd.DataFrame()
        data_anom['time'] = data_df['time']

    
        for d in depth:
            data_anom[d] = data_df[d] - data_hist[d]

        data_hist['nan'] = np.empty(365)
        data_hist['nan'][:] = np.nan

        
        data_anom = data_anom.drop(index = data_anom.index[-1]).reset_index()
        fig, ax = plt.subplots(1, figsize=(8, 6.5))

        plt.figtext(0.05, 0.02, "Fuente: NOAA - GTMBA Sitemap\n(https://www.pmel.noaa.gov/tao/drupal/disdel/)", fontsize=6.5)
        plt.figtext(0.78, 0.02, "Por: Carlo Ilave", fontsize=6.5, family ='serif')

        
        ax.plot(data_hist['time'], data_hist['nan'])
        plot_anom = ax.contourf(data_anom['time'], [int(i) for i in data_anom.columns[2:]] , data_anom[data_anom.columns[2:]].T, levels=np.arange(-7.5, 7.6, 0.1), cmap='RdYlBu_r')
        #plto_anom_c = ax.contour(plot_anom, levels = [-2, -1, 0, 1, 2], colors = 'black', linewidths = 0.5)
        plto_anom_c = ax.contour(plot_anom, levels = np.arange(-7, 7.6, 1), colors = 'black', linewidths = 0.5)
        ax.clabel(plto_anom_c, levels = np.arange(-7, 7.6, 1), colors = 'black')

        ax.set_ybound(0, 300)
        ax.set_xbound('01/01', '12/31')
        ax.set_xticks(time_numbers, months)
        ax.invert_yaxis()
        ax.set_xlabel('Mes')
        ax.set_title('Anomalía subsuperficial\n' + buoyname(buoy) + ' - ' + year, x=0.43)
        ax.set_ylabel('Profundidad (m)')

        plt.colorbar(plot_anom, ticks = np.arange(-6.5, 6.6, 1), label = 'Temperatura (°C)')

        fig.tight_layout(pad=5.0)
        plt.show()
        break
        #plt.savefig('TZ/PLOTS/' + year + '/tz_anom_' + buoy + '_' + year+'_2')
        #plt.close()
    
    except:
        print('error')