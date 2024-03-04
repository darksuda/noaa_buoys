import pandas as pd
import netCDF4 as cdf 
import matplotlib.pyplot as plt
import numpy as np
import julian as jd
from ASSETS.buoy import buoyname

buoys = pd.read_csv('ASSETS/boyas.csv', delimiter=',')['BUOYS']
buoys = ['0n165e']
year = '2022'

time_numbers = ['01/01', '02/01', '03/01', '04/01', '05/01', '06/01', '07/01', '08/01', '09/01', '10/01', '11/01', '12/01.000000000']
months = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']

wind_m_suma_d = []
wind_m_suma_a = []

for mes in np.arange(1, 13):

    for buoy in buoys:
        try:
            data_df = None
            data_hist = None
            
            data_hist = pd.read_csv('UWIND\HIST\CSV\hist_uwind_' + buoy + '.csv', delimiter=',')
            data_hist = data_hist.drop(59).reset_index() #ELIMINAR 29 DE FEBRERO DEL HISTÓRICO
            
            file = 'UWIND/DATA/' + year + '/w' + buoy + '_dy.cdf'
            data_cdf = cdf.Dataset(file)

            uwind = np.array(data_cdf['WU_422']).T[0][0][0]
            uwind[ uwind == 1e+35] = np.NaN

            time = np.array(data_cdf['time'])
            timeMD = np.array(list(map(lambda x : (jd.from_jd(x)).strftime('%m/%d'), time)))

            data_df = pd.DataFrame({'time': timeMD, 'uwind': uwind})
            data_df = data_df.groupby(['time']).mean().reset_index()
            data_df['anom'] = data_df['uwind'] - data_hist['uwind']

            if int(year) % 4 == 0:
                index29 = data_df[data_df['time'] == '02/29'].index
                data_df = data_df.drop(index29).reset_index()

            data_hist['nan'] = np.empty(365)
            data_hist['nan'][:] = np.nan

            data_df['time'] = [int(i[:2]) for i in data_df['time']]

            if 'index' in data_df.columns:
                data_df = data_df.drop('index', axis=1)

            print(data_df[data_df['time'] == mes].describe())
            print(data_df[data_df['time'] == mes].sum())
            
            print('----------------------------------------------')
            print('SUMA TOTAL: ', data_df[data_df['time'] == mes].sum()[1])
            print('NÚMERO DE DÍAS: ', data_df[data_df['time'] == mes].describe()['uwind'][0])
            print('SUMA / DIAS', data_df[data_df['time'] == mes].sum()[1] / data_df[data_df['time'] == mes].describe()['uwind'][0])
            
            wind_m_suma_d.append(data_df[data_df['time'] == mes].sum()[1])
            wind_m_suma_a.append(data_df[data_df['time'] == mes].sum()[2])


        except Exception as err:
            print('error en la boya ' + buoy)
            print(err)

print(wind_m_suma_a)
print(wind_m_suma_d)

fig, ax = plt.subplots()

ax.bar(months, wind_m_suma_a)

ax.set_title(year)
ax.set_ybound(-250, 250)
ax.set_yticks(np.arange(-250, 250 +1, 50))

plt.show()
