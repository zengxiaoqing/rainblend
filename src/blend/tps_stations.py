
# Imported scatter code, version 2.0
# ================================================================

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import string
import matplotlib
import matplotlib.cm as cm
import scipy.interpolate
np.set_printoptions(threshold='nan')  # print full array
from matplotlib.mlab import griddata
from netCDF4 import Dataset

# Define some paths - TRMM related
# ==========================================================================================
# in_path="/nobackup/users/stepanov/TRMM_data/nc/annual_files/cropped/land_only/"
in_path="/Users/istepanov/github/TRMM_blend/TRMM_nc/"
# ==========================================================================================

# TRMM file for SACA area, Land only
file_trmm='3b42-daily.2000-georef-saca-land-only.nc' 
# 3b42-daily.2000-georef-saca-land-only.nc

# file_pr = [in_path+file_trmm]  


# # Review imported file paths in log
# print "Location of TRMM precipitation file is: ",file_pr
# print

# Define paths to NC files
#===========================================================================================

# Precip and elevation (Land Sea Mask)
nc_trmm = Dataset(in_path+file_trmm,'r')   # [latitude, longitude][201x400]

# Extract the actual variable
# For TRMM data go from 1-365 in ncview, but python counts 0-364
trmm_precip = nc_trmm.variables['r'][161,:,:]   # [time, lat, lon], 0= 01.01.2013 (python)

print 'trmm data is: ', trmm_precip

# Coordinates for TRMM
lons = nc_trmm.variables['longitude']
lats = nc_trmm.variables['latitude']

# Import data from ASCII CSV file 
#
gauges = np.genfromtxt("/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_year2000-06-10.dat",
# gauges = np.genfromtxt("/usr/people/stepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_year2000-06-10.dat",
                        delimiter=',', 
                        dtype=[('lat', np.float32), ('lon', np.float32), ('rr', np.float32)], 
                        usecols=(2, 3, 0))


# Make lat & lon easier to use down the line:
lat = gauges['lat']
lon = gauges['lon']
rr = gauges['rr']

# Filter out stations without measurements (-999.9)
# rr[rr == -9.99900000e+3] = np.nan
rr[rr == -9.99900000e+3] = 0.0


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


# print 'rr is:', rr

# quit()


# -- New interpolation (gridding):
numcols, numrows = 110, 110
# xi = np.linspace(lon.min(), lon.max(), numcols)
# yi = np.linspace(lat.min(), lat.max(), numrows)

# Now create grid matching SACA
# xi = np.linspace(90, 190, numcols)
# yi = np.linspace(-24.875, 24.875, numrows)

xi = lons
yi = lats

xi, yi = np.meshgrid(xi, yi)


# quit()

x, y, z = lon, lat, rr
# zi = griddata(x, y, rr, xi, yi)  # works IS


# use RBF
# rbf = scipy.interpolate.Rbf(x, y, z, epsilon=2)
# rbf = scipy.interpolate.Rbf(x, y, z, function='thin-plate')
rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
ZI = rbf(xi, yi)

# plot the result
# n = plt.normalize(-2., 2.)
# plt.subplot(1, 1, 1)
# plt.pcolor(xi, yi, ZI, cmap=cm.jet)

fig, ax = plt.subplots()
im = ax.contourf(xi, yi, ZI)
plt.scatter(x, y, 50, z, cmap=cm.jet)

# Range of axis 
plt.xlim([90,190])
plt.ylim([-25,25])

# # -- Display the results
# fig, ax = plt.subplots()
# im = ax.contourf(xi, yi, zi)
# ax.scatter(lon, lat, c=rr, s=100, vmin=0.0, vmax=10.0)

# # -- Colorbar
fig.colorbar(im)

# # cbar=fig.colorbar(im, ticks=[0.0,5.0,10.0])
# # cbar.set_clim(0.0, 10.0)
# # plt.clim(0,10)


# plt.show()

# Save as PNG
plt.savefig('plots/Precip_TPspline_20000610.png', 
            bbox_inches='tight', 
            optimize=True,
            quality=85,
            dpi=300)

plt.close(fig)

quit()



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

