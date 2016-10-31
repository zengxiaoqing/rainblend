# Make python script executable
#!/usr/bin/python


# Blending script for TRMM and SE Asia rain gauges using Gandin OI method


# ==========================================
# Author: I.Stepanov (igor.stepanov@knmi.nl)
# 28.10.2016 @KNMI
# ============================================================================================
# Updates list
# 
# ============================================================================================


# ================================================================

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(threshold='nan')  # print full array
import string
import matplotlib
import matplotlib.cm as cm
from netCDF4 import Dataset
import scipy.interpolate
 
# Define some paths - TRMM related
# ==========================================================================================
in_path="/nobackup/users/stepanov/TRMM_data/nc/annual_files/cropped/land_only/"
# ==========================================================================================

# TRMM file for SACA area, Land only
file_trmm='3B42_daily.2000_georef_SACA_land_only.nc' 

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

# quit()

# Define paths to NC files
#===========================================================================================
# Precip and elevation (Land Sea Mask)
# nc_trmm = Dataset(in_path+file_trmm,'r')                               # [latitude, longitude][201x400]


# Thin plate spline part:

rbfi = scipy.interpolate.Rbf(lons, lats, trmm_precip)  # radial basis function interpolator instance
trmm_precip_i = rbfi(lons, lats)   # interpolated values

# rbfi = Rbf(x, y, z, d)  # radial basis function interpolator instance
# di = rbfi(xi, yi, zi)   # interpolated values

# interp = scipy.interpolate.Rbf(lats, lons, trmm_precip, function='linear')
quit()

# lati,loni=np.mgrid[0:1:100j, 0:1:100j]
# lati,loni=np.mgrid[gauges['lon'], gauges['lat']]

numcols, numrows = 400, 201 
loni = np.linspace(gauges['lon'].min(), gauges['lon'].max(), numcols)
lati = np.linspace(gauges['lat'].min(), gauges['lat'].max(), numrows)
xi, yi = np.meshgrid(lati, loni)

# print 'xi is:', xi
# print
# print 'yi is:', yi

print 'xi dimension is:', xi.shape
print
print 'yi dimension is:', yi.shape

# quit()

# x, y, z = data.Lon, data.Lat, data.Z

rri=interp(loni, lati)

quit()

# Design figure
# ================================================================
xsize=20
ysize=10

fig = plt.figure(figsize=(xsize,ysize))


# m = Basemap(projection='gall',
#             llcrnrlon = 80.125,              # lower-left corner longitude
#             llcrnrlat = -24.875,               # lower-left corner latitude
#             urcrnrlon = 179.875,               # upper-right corner longitude
#             urcrnrlat = 25.125,               # upper-right corner latitude
#             resolution = 'i',
#             # area_thresh = 100.0,
#             )


# x1,y1=m(gauges['lon'],gauges['lat'])


# m.drawcoastlines()
# m.drawcountries()
# m.fillcontinents(color='gainsboro', zorder=0)
# m.drawmapboundary(fill_color='steelblue')
# ================================================================

# fig, ax = plt.subplots()
ax = plt.gca()
ax.pcolormesh(loni, lati, rri, edgecolors='green', facecolor='white', vmin=0, vmax=10)
# quadmesh.set_clim(vmin=0, vmax=5)

# Plot the actual scatters
scat = ax.scatter(gauges['lon'], gauges['lat'], c=gauges['rr'], s=50, zorder=4)
# scat = ax.scatter(gauges['lon'], gauges['lat'], c=saca_blend, s=50, zorder=4)

# Colorbar
cb=fig.colorbar(scat)
cb.set_label('[mm/day]', fontsize=22)
cb.set_clim(0.0,10.0)
# plt.clim(0.0,10.0)
ax.margins(0.05)

# Sample

# pcm = ax[1].pcolormesh(X, Y, Z1, cmap='RdBu_r', vmin=-np.max(Z1))
# fig.colorbar(pcm, ax=ax[1], extend='both')
# fig.show()
# End of sample


# Save as PNG
# plt.savefig('plots/Gauges_raster_scatter_non_interp_20000610.png', 
#             bbox_inches='tight', 
#             optimize=True,
#             quality=85,
#             dpi=300)

# plt.close(fig)

quit()

# ==========================================================================================



