import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta


buoys = ['0n110w', '8n125w', '0n140w', '0n170w', '0n165e', '0n156e', '0n147e']
#buoys = ['0n147e']


months_tickslabels = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
years = [1991, 1992, 1993, 1997, 1998, 2015, 2016, 2017]

for buoy in buoys:
    file = 'uadcp_' + buoy + '.csv'
    data = pd.read_csv(file)
    for year in years:
        try:
            data_year = data[data['year'] == year]
            depths = data_year.columns[4:]
            data_content = data_year[depths].T
            depths = [int(float(i)) for i in depths]
            dates_str = data_year['date_str']


            data_init = data_year.iloc[0]
            data_end = data_year.iloc[-1]

            date_arange = np.arange(datetime(year-1 ,12 ,31), datetime(year+1 ,1 ,1), timedelta(days=1)).astype(datetime)
            date_arange = [str(i)[:10].replace('-', '/') for i in date_arange]
            a = np.empty(len(date_arange))
            a[:] = np.nan

            fig, ax = plt.subplots(figsize = (16, 9))

            ax.plot(date_arange, a)
            ax.set_xbound(str(year)+'/01/01', str(year )+'/12/31')

            plot = ax.contourf(dates_str, depths, data_content, levels = np.arange(-200, 200 + 1, 25), cmap='coolwarm')
            plot2 = ax.contour(dates_str, depths, data_content, colors = 'black', linewidths = 0.2, levels = np.arange(-200, 200 + 1, 20), alpha = 0.75)
            plot2 = ax.contour(dates_str, depths, data_content, colors = 'black', linewidths = 0.75, levels = [20])
            plot2 = ax.contour(dates_str, depths, data_content, colors = 'red', linewidths = 0.75, levels = [100], linestyles = 'dotted')

            ax.invert_yaxis()
            months_ticks = [str(year) + '/01/01', str(year) + '/02/01', str(year) + '/03/01', str(year) + '/04/01', str(year) + '/05/01', str(year) + '/06/01', str(year) + '/07/01', str(year) + '/08/01', str(year) + '/09/01', str(year) + '/10/01', str(year) + '/11/01', str(year) + '/12/01']
            ax.set_xticks(months_ticks, months_tickslabels)
            ax.set_ybound(0, 250)
            ax.set_ylabel('Profundidad (m)')
            ax.set_xlabel('Meses')

            ax.set_title('Velocidad de corriente zonal\n' + buoy + ' ' + str(year))
            plt.colorbar(plot, label = 'Velocidad (cm/s)', ticks = np.arange(-200, 200 + 1, 20))
            
            #plt.show()
            plt.savefig('img/uadcp_' + buoy + '_' + str(year))
            plt.close()
            print('Plot for buoy ' + buoy + ' in year ' + str(year) + ' created')
        except:
            print('error en la boya ' + buoy + ' con el año ' + str(year))
