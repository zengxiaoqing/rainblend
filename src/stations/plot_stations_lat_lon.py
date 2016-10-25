# import csv

# with open('../../ascii_out/saca_stations_query_series_rr_year1947.dat', 'rt') as f:
#   reader = csv.reader(f, delimiter=' ', skipinitialspace=True)

#   lineData = list()

#   cols = next(reader)
#   print(cols)


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

gauges = np.genfromtxt("/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_year2015.dat")
                        # delimiter=',', 
                        # dtype=[('lat', np.float32), ('lon', np.float32)], 
                        # usecols=(3, 4))

fig = plt.figure()


themap = Basemap(projection='gall',
              llcrnrlon = -15,              # lower-left corner longitude
              llcrnrlat = 28,               # lower-left corner latitude
              urcrnrlon = 45,               # upper-right corner longitude
              urcrnrlat = 73,               # upper-right corner latitude
              resolution = 'l',
              area_thresh = 100000.0,
              )


themap.drawcoastlines()
themap.drawcountries()
themap.fillcontinents(color = 'gainsboro')
themap.drawmapboundary(fill_color='steelblue')



x, y = themap(airports['lon'], airports['lat'])
themap.plot(x, y, 
            'o',                    # marker shape
            color='Indigo',         # marker colour
            markersize=4            # marker size
            )

plt.show()

