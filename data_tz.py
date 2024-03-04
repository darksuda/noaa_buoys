import netCDF4 as cdf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import julian as jd
from ASSETS.buoy import buoyname

buoys = pd.read_csv('ASSETS/boyas.csv')['BUOYS']
year = '2015'

time_numbers = ['01/01', '02/01', '03/01', '04/01', '05/01', '06/01', '07/01', '08/01', '09/01', '10/01', '11/01', '12/01']
months = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']

for buoy in buoys:

    try:
        data_hist = pd.read_csv('TZ\HIST\CSV\hist_tz_' + buoy + '.csv', delimiter=',')
        data_hist = data_hist.drop(59).reset_index() #ELIMINAR 29 DE FEBRERO DEL HISTÓRICO

        file = 'TZ/DATA/' + year + '/t' + buoy + '_dy.cdf'
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

        fig, ax = plt.subplots(3, figsize=(12, 9))

        plt.figtext(0.05, 0.02, "Fuente: NOAA - GTMBA Sitemap\n(https://www.pmel.noaa.gov/tao/drupal/disdel/)", fontsize=6.5)
        plt.figtext(0.78, 0.02, "Por: Carlo Ilave", fontsize=6.5, family ='serif')

        ax[0].plot(data_hist['time'], data_hist['nan'])
        plot_h = ax[0].contourf(data_hist['time'], [int(i) for i in data_hist.columns[2:-1]] , data_hist[data_hist.columns[2:-1]].T, levels=np.arange(10, 32.1, 1), cmap='rainbow')
        plot_hc1 = ax[0].contour(plot_h, levels = np.arange(20, 33, 2), colors = 'black', linewidths = 0.5)
        plot_hc2 = ax[0].contour(plot_h, levels = [10, 15], colors = 'black', linewidths = 0.5)
        plot_h3 = ax[0].contour(plot_h, levels = [20], colors = 'red', linewidths = 1)
        ax[0].clabel(plot_hc1, levels = np.arange(20, 33, 2), colors = 'black')
        ax[0].clabel(plot_hc2, levels = [10, 15], colors = 'black')

        ax[1].plot(data_hist['time'], data_hist['nan'])
        plot_year = ax[1].contourf(data_df['time'], [int(i) for i in data_df.columns[2:]] , data_df[data_df.columns[2:]].T, levels=np.arange(10, 32.1, 0.2), cmap='rainbow')
        plot_yc1 = ax[1].contour(plot_year, levels = np.arange(20, 33, 1), colors = 'black', linewidths = 0.5)
        ax[1].contour(plot_year, levels = [10, 15], colors = 'black', linewidths = 0.5)
        ax[1].contour(plot_year, levels = [20], colors = 'red', linewidths = 1)
        ax[1].clabel(plot_yc1, levels = np.arange(20, 33, 1), colors = 'black')

        ax[2].plot(data_hist['time'], data_hist['nan'])
        plot_anom = ax[2].contourf(data_anom['time'], [int(i) for i in data_anom.columns[2:]] , data_anom[data_anom.columns[2:]].T, levels=np.arange(-8, 8.1, 0.1), cmap='RdYlBu_r')
        plto_anom_c = ax[2].contour(plot_anom, levels = np.arange(-8, 8.1, 1), colors = 'black', linewidths = 0.5)
        ax[2].clabel(plto_anom_c, levels = np.arange(-8, 8.1, 1), colors = 'black')
        

        for i in ax:
            i.set_ybound(0, 300)
            i.set_xbound('01/01', '12/31')
            i.set_xticks(time_numbers, months)
            i.invert_yaxis()
        ax[2].set_xlabel('Mes')

        ax[0].set_title('Histórico')
        ax[1].set_title('Temperatura ' + year )
        ax[2].set_title('Anomalías ' + year )

        ax[0].set_ylabel('Profundidad (m)')
        ax[1].set_ylabel('Profundidad (m)')
        ax[2].set_ylabel('Profundidad (m)')

        plt.colorbar(plot_h, ticks = np.arange(10, 33, 2), label = 'Temperatura (°C)')
        plt.colorbar(plot_year, ticks = np.arange(10, 33, 2), label = 'Temperatura (°C)')
        plt.colorbar(plot_anom, ticks = np.arange(-8, 8.1, 1), label = 'Temperatura (°C)')

        plt.suptitle('Temperatura subsuperficial\n' + buoyname(buoy) + ' - ' + year, x=0.43)
        fig.tight_layout(pad=5.0)
        plt.savefig('TZ/PLOTS/' + year + '/tz_' + buoy + '_' + year)
        #plt.show()
        plt.close()
        #break
    
    


    except:
        pass