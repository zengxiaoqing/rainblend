
# Imported scatter code, version 2.0
# ================================================================

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import string
import matplotlib
import matplotlib.cm as cm
 

gauges = np.genfromtxt("/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_year2000-06-10.dat",
                        delimiter=',', 
                        dtype=[('lat', np.float32), ('lon', np.float32), ('rr', np.float32)], 
                        usecols=(2, 3, 0))

# Imported data from ASCII files

print 'lon is: ', gauges['lon']
print
print 'lat is: ', gauges['lat']
print
print 'rr is: ', gauges['rr']


# Design figure
# ================================================================
xsize=20
ysize=10

fig = plt.figure(figsize=(xsize,ysize))
# ================================================================


m = Basemap(projection='gall',
            llcrnrlon = 80.125,              # lower-left corner longitude
            llcrnrlat = -24.875,               # lower-left corner latitude
            urcrnrlon = 179.875,               # upper-right corner longitude
            urcrnrlat = 25.125,               # upper-right corner latitude
            resolution = 'i',
            # area_thresh = 100.0,
            )


x1,y1=m(gauges['lon'],gauges['lat'])


m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='gainsboro', zorder=0)
m.drawmapboundary(fill_color='steelblue')

# # doubling width of markers
# x = [0,2,4,6,8,10]
# y = [0]*len(x)
# s = [20*4**n for n in range(len(x))]

# doubling area of markers
# x = [0,2,4,6,8,10]
# y = [0]*len(x)
# s = [20*2**n for n in range(len(x))]


#Finally, the scatter plot.
ax = plt.gca()
rr_scat_plot=m.scatter(x1,y1,s=500,c=gauges['rr'],marker="o",cmap=cm.cool,alpha=0.7)
# plt.title("Flickr Geotagging Counts with Basemap")
# plt.show()
plt.clim(0.0,10.0)
# plt.clim(-999,-999)
# plt.clim(-1,1)


cb = fig.colorbar(rr_scat_plot, orientation='vertical',fraction=0.046, pad=0.04)
cb.set_label('[mm/day]', fontsize=22)
# Amp up the font size on colorbar
ax = cb.ax
text = ax.xaxis.label
font = matplotlib.font_manager.FontProperties(style='italic', size=16)
text.set_font_properties(font)
# Up the colorbar ticks
cb.ax.tick_params(labelsize=16) 

# plt.colorbar()


# Save as PNG
plt.savefig('plots/Precip_scatter_non_interp_20000610.png', 
            bbox_inches='tight', 
            optimize=True,
            quality=85,
            dpi=300)

plt.close(fig)


# x, y = themap(gauges['lon'], gauges['lat'])
# themap.plot(x, y, 
#             'o',                    # marker shape
#             color='Red',         # marker colour
#             markersize=3            # marker size
#             )

