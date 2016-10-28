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

# quit()

# Define paths to NC files
#===========================================================================================
# Precip and elevation (Land Sea Mask)
# nc_trmm = Dataset(in_path+file_trmm,'r')                               # [latitude, longitude][201x400]



# ==========================================================================================
# Extract lat/lon/rr from ASCII/dat file 
gauges = np.genfromtxt("/usr/people/stepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_year2000-06-10.dat",
                        delimiter=',', 
                        dtype=[('lat', np.float32), ('lon', np.float32), ('rr', np.float32)], 
                        usecols=(2, 3, 0))

# Print imported gauge data from ASCII files`
#
# print 'lon is: ', gauges['lon']
print
# print 'lat is: ', gauges['lat']
print
# print 'rr is: ', gauges['rr']
# ==========================================================================================


# Create a raster of gauges data to be on the same grid as TRMM: [latitude, longitude][201x400]
#
rri, lati, loni = np.histogram2d(gauges['lat'], gauges['lon'], 
                  bins=(201, 400), weights=gauges['rr'], 
                  normed=False)
counts, _, _ = np.histogram2d(gauges['lat'], gauges['lon'], bins=(201,400))

rri = np.ma.masked_equal(rri, 0)

# For large number of points:
rri = rri / counts
rri = np.ma.masked_invalid(rri)

# print 'rri is: ', rri

# quit()

# Blending part

saca_blend = trmm_precip + rri

# print 'saca blend is: ', saca_blend

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
plt.savefig('plots/Gauges_raster_scatter_non_interp_20000610.png', 
            bbox_inches='tight', 
            optimize=True,
            quality=85,
            dpi=300)

# plt.close(fig)

quit()

# ==========================================================================================



