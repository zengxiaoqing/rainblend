# import csv

# with open('../../ascii_out/saca_stations_query_series_rr_year1947.dat', 'rt') as f:
#   reader = csv.reader(f, delimiter=' ', skipinitialspace=True)

#   lineData = list()

#   cols = next(reader)
#   print(cols)


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


# gauges = np.genfromtxt("/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_year2015.dat")
gauges = np.genfromtxt("/usr/people/stepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_year2000-06-10.dat",
                        delimiter=',', 
                        dtype=[('lat', np.float32), ('lon', np.float32)], 
                        usecols=(2, 3))

# Design figure
# ================================================================

xsize=20
ysize=10

fig = plt.figure(figsize=(xsize,ysize))
# ================================================================


themap = Basemap(projection='gall',
              llcrnrlon = 80.125,              # lower-left corner longitude
              llcrnrlat = -24.875,               # lower-left corner latitude
              urcrnrlon = 179.875,               # upper-right corner longitude
              urcrnrlat = 25.125,               # upper-right corner latitude
              resolution = 'f',
              area_thresh = 0.1,
              )

# area_thresh:	coastline or lake with an area smaller than area_thresh in 
# km^2 will not be plotted. Default 10000,1000,100,10,1 for resolution c, l, i, h, f.


themap.drawcoastlines()
themap.drawcountries()
themap.fillcontinents(color = 'gainsboro')
themap.drawmapboundary(fill_color='steelblue')



x, y = themap(gauges['lon'], gauges['lat'])
themap.plot(x, y, 
            'o',                    # marker shape
            color='Red',         # marker colour
            markersize=3            # marker size
            )

# plt.show()

# Save plot


plt.savefig('plots/Stations_location_20110610.png',bbox_inches='tight',optimize=True,quality=85,dpi=300)


plt.close(fig)