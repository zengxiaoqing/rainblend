
# Imported scatter code, version 2.0
# ================================================================

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import string
import matplotlib
import matplotlib.cm as cm
import scipy.interpolate
# np.set_printoptions(threshold='nan')  # print full array
from matplotlib.mlab import griddata
 

gauges = np.genfromtxt("/usr/people/stepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_year2000-06-10.dat",
                        delimiter=',', 
                        dtype=[('lat', np.float32), ('lon', np.float32), ('rr', np.float32)], 
                        usecols=(2, 3, 0))

# Make lat & lon easier to use down the line:
lat = gauges['lat']
lon = gauges['lon']
rr = gauges['rr']

# Imported data from ASCII files

# print 'lon is: ', gauges['lon']
# print
# print 'lat is: ', gauges['lat']
# print
# print 'rr is: ', gauges['rr']


print 'lon shape is: ', lon.shape
print
print 'lat shape is: ', lat.shape
print
print 'rr shape is: ', rr.shape

# quit()


# New interpolation:
numcols, numrows = 30, 30
xi = np.linspace(lon.min(), lon.max(), numcols)
yi = np.linspace(lat.min(), lat.max(), numrows)
xi, yi = np.meshgrid(xi, yi)

# print 'xi is: ', xi

# quit()

x, y, z = lon, lat, rr
# zi = griddata(x, y, rr, xi, yi,s interp='linear')
zi = griddata(x, y, rr, xi, yi)

#-- Display the results
fig, ax = plt.subplots()
im = ax.contourf(xi, yi, zi)
ax.scatter(lon, lat, c=rr, s=100,
           vmin=zi.min(), vmax=zi.max())
fig.colorbar(im)

plt.show()

quit()

#-- Now let's grid your data.
# First we'll make a regular grid to interpolate onto. This is equivalent to
# your call to `mgrid`, but it's broken down a bit to make it easier to
# understand. The "30j" in mgrid refers to 30 rows or columns.
numcols, numrows = 30, 30
xi = np.linspace(data.Lon.min(), data.Lon.max(), numcols)
yi = np.linspace(data.Lat.min(), data.Lat.max(), numrows)
xi, yi = np.meshgrid(xi, yi)

#-- Interpolate at the points in xi, yi
# "griddata" expects "raw" numpy arrays, so we'll pass in
# data.x.values instead of just the pandas series data.x
x, y, z = data.Lon.values, data.Lat.values, data.Z.values
zi = griddata(x, y, z, xi, yi)

#-- Display the results
fig, ax = plt.subplots()
im = ax.contourf(xi, yi, zi)
ax.scatter(data.Lon, data.Lat, c=data.Z, s=100,
           vmin=zi.min(), vmax=zi.max())
fig.colorbar(im)

plt.show()






















# Thin plate spline part:
interp = scipy.interpolate.Rbf(gauges['lon'], gauges['lat'], gauges['rr'], function='linear')

lati,loni=np.mgrid[0:1:100j, 0:1:100j]
# lati,loni=np.mgrid[gauges['lon'], gauges['lat']]

# numcols, numrows = 400, 201 
numcols, numrows = 3838, 3838
# loni = np.linspace(gauges['lon'].min(), gauges['lon'].max(), numcols)
# lati = np.linspace(gauges['lat'].min(), gauges['lat'].max(), numrows)
xi, yi = np.meshgrid(lati, loni)

# print 'xi is:', xi
# print
# print 'yi is:', yi

print 'xi dimension is:', xi.shape
print
print 'yi dimension is:', yi.shape

print

# print 'minimum lon', gauges['lon'].min()
# print 'maximum lon', gauges['lon'].max()
# print
# print 'minimum lat', gauges['lat'].min()
# print 'maximum lat', gauges['lat'].max()
# print

# minimum lon 95.283
# maximum lon 177.45

# minimum lat -20.0
# maximum lat 22.35


# quit()

# x, y, z = data.Lon, data.Lat, data.Z

rri=interp(loni, lati)


# interp = scipy.interpolate.Rbf(x, y, z, function='thin_plate')
# yi, xi = np.mgrid[0:1:100j, 0:1:100j]
# zi = interp(xi, yi)

# quit()

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
            resolution = 'c',
            # area_thresh = 100.0,
            )


# x1,y1=m(gauges['lon'],gauges['lat'])

x1,y1=m(loni, lati)

m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='gainsboro', zorder=0)
m.drawmapboundary(fill_color='steelblue')



# #Finally, the scatter plot.
# ax = plt.gca()
# rr_scat_plot=m.scatter(x1,y1,s=500,c=gauges['rr'],marker="o",cmap=cm.cool,alpha=0.7)
# # plt.title("Flickr Geotagging Counts with Basemap")
# # plt.show()
# plt.clim(0.0,10.0)
# # plt.clim(-999,-999)
# # plt.clim(-1,1)

# Interpolated plot:
ax = plt.gca()
rr_scat_plot=m.scatter(loni,lati,s=500,c=rri,marker="o",cmap=cm.cool,alpha=0.7)
# im = ax.imshow(zi, extent=[0, 1, 1, 0], cmap='gist_earth')
# plt.title("Flickr Geotagging Counts with Basemap")
# plt.show()
plt.clim(0.0,10.0)



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
plt.show()


# # Save as PNG
# plt.savefig('plots/Precip_scatter_non_interp_20000610.png', 
#             bbox_inches='tight', 
#             optimize=True,
#             quality=85,
#             dpi=300)

# plt.close(fig)



# x, y = themap(gauges['lon'], gauges['lat'])
# themap.plot(x, y, 
#             'o',                    # marker shape
#             color='Red',         # marker colour
#             markersize=3            # marker size
#             )

