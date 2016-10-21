# Make python script executable
#!/usr/bin/python

# Script to plot rainfall estimates from TRMM, produyct 3B42 daily from NASA

import netCDF4
import pylab as pl
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from pylab import *
import math as m
from mpl_toolkits.basemap import Basemap, cm
#import ctypes
#import icclim
import datetime
#import icclim.util.callback as callback
#cb = callback.defaultCallback


print
print '<<Loaded modules>>'
print


# Define some paths
# ==========================================================================================

#in_path="/Users/istepanov/PostDoc/EOBS_data"         # local MBP
#in_path="/usr/people/stepanov/EOBS_data/"            # home folder
in_path="/nobackup/users/stepanov/TRMM_data/nc/annual_files/cropped/"         # nobackup
#in_path_oro_SACA="/nobackup/users/stepanov/SACA/final/"
in_path_lsmsk_TRMM="/nobackup/users/stepanov/TRMM_data/Land_Sea_Mask/"


# Files
#===========================================================================================

# Precip TRMM
file_name='3B42_daily.2015_georef_SACA.nc'    
# ncks -d latitude,-24.875,25.125 -d longitude,80.125,179.875 3B42_daily.2015.12.29.7.nc 3B42_daily.2015.12.29.7_georef_SACA.nc

# Orography SACA rr
#file_oro_SACA='new_elevs_rr.nc'

# Land Sea Maks TRMM specific
file_lsm_TRMM='TMPA_mask_georef_SACA_match_TRMM_grid.nc'



# ECA&D files
#file_pr = [in_path+'3B42_daily.2015_georef_SACA.nc']  # 
#file_pr = [in_path+'3B42_daily.2015.12.29.7.nc']  # Average temperature
#file_max_temp = [in_path+'tx_0.25deg_reg_v12.0.nc']  # Max temperature
#file_min_temp = [in_path+'tn_0.25deg_reg_v12.0.nc']  # Min temperature
#file_precip   = [in_path+'rr_0.25deg_reg_v12.0.nc']  # Precipitation


# Full file paths
file_pr = [in_path+file_name]  
#file_oro_SACA = [in_path_oro_SACA+file_oro]  
file_lsmask_TRMM = [in_path_lsmsk_TRMM+file_lsm_TRMM]


print "Location of TRMM precipitation file is: ",file_pr
print
print
#print "Location of orography file is: ",file_oro_SACA
print
print
print "Location of TRMM land-sea mask file is: ",file_lsmask_TRMM
print
print




#ncfile1 = Dataset(file_pr,'r')
ncfile1 = Dataset(in_path+file_name,'r')
nc_lsmask_trmm = Dataset(in_path_lsmsk_TRMM+file_lsm_TRMM,'r')

#ncfile2 = Dataset(in_path_lsmsk_TRMM+file_lsm_TRMM,'r')

#quit()

# Extract the actuall variable
trmm_precip = ncfile1.variables['r'][0,:,:]

trmm_lsmask = nc_lsmask_trmm.variables['landseamask'][:,:]


#trmm_lsmask = trmm_lsmask/100.
print trmm_lsmask

# Python replacing syntax
# arr[arr > 255] = x

# All land points convert to 1
trmm_lsmask[trmm_lsmask!=100]=1.

# All sea points convert to 0
trmm_lsmask[trmm_lsmask==100]=0.

# New mask should be: 1=land, 0=sea
# Multiply woth TRMM data when plotting
print trmm_lsmask

#quit()

print "TRMM precip is: ", trmm_precip
print

#quit()

lons = ncfile1.variables['longitude']
lats = ncfile1.variables['latitude']

#lsmaks=ncfile2



# m = Basemap(projection='stere',
# 	        lat_0=40, lon_0=-15,
# 	        llcrnrlon=-40, llcrnrlat=30,
# 	        urcrnrlon=10, urcrnrlat=50)


# Start making the figure
# ================================================================

xsize=20
ysize=12

fig = plt.figure(figsize=(xsize,ysize))


# Map projection
# =============================================================
# m = Basemap(projection='stere',        # Graciosa coords
# 	        lat_0=40, lon_0=-15,
# 	        llcrnrlon=-40, llcrnrlat=30,
# 	        urcrnrlon=10, urcrnrlat=50)

# Resolution on 'i' (intermediate) makes good enough coastline. 
# Use 'f' (full) for showing off
m = Basemap(projection='stere',                      # SACA gridded data set coordinates
	        lat_0=0, lon_0=130,
	        llcrnrlon=80.125, llcrnrlat=-24.875,
	        urcrnrlon=179.875, urcrnrlat=25.125,
	        resolution='i')

#x, y = m(lons,lats)
#print lons

# Colorbar with NSW Precip colors
nws_precip_colors = [
    "#04e9e7",  # 0.01 - 0.10 inches
    "#019ff4",  # 0.10 - 0.25 inches
    "#0300f4",  # 0.25 - 0.50 inches
    "#02fd02",  # 0.50 - 0.75 inches
    "#01c501",  # 0.75 - 1.00 inches
    "#008e00",  # 1.00 - 1.50 inches
    "#fdf802",  # 1.50 - 2.00 inches
    "#e5bc00",  # 2.00 - 2.50 inches
    "#fd9500",  # 2.50 - 3.00 inches
    "#fd0000",  # 3.00 - 4.00 inches
    "#d40000",  # 4.00 - 5.00 inches
    "#bc0000",  # 5.00 - 6.00 inches
    "#f800fd",  # 6.00 - 8.00 inches
    "#9854c6",  # 8.00 - 10.00 inches
    "#fdfdfd"   # 10.00+
]
precip_colormap = matplotlib.colors.ListedColormap(nws_precip_colors)

levels = [0.01, 0.1, 0.25, 0.50, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0,
          6.0, 8.0, 10., 20.0, 25.0]

#clevs = [0,1,2.5,5,7.5,10,15,20,30,40,50,70,100,150,200,250,300,400,500,600,750]
clevs = [0,1,2.5,5,7.5,10,15,20,30,40,50,70,100,150]#,200,250]#,300,400,500,600,750]

norm = matplotlib.colors.BoundaryNorm(levels, 16)


# draw coastlines, country boundaries, fill continents.
m.drawcoastlines(linewidth=0.25)
m.drawcountries(linewidth=0.25)
# draw parallels.
parallels = np.arange(-40.,40,10.)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
# draw meridians
meridians = np.arange(80.,180.,10.)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)


ny = trmm_precip.shape[0]; nx = trmm_precip.shape[1]
lons, lats = m.makegrid(nx, ny) # get lat/lons of ny by nx evenly space grid.
x, y = m(lons, lats) # compute map proj coordinates.

#print x

# Land sea mask
#topo = maskoceans(lons, lats, topoin)


#cs = m.pcolor(lons,lats,trmm_precip)
#cs = plt.contour(trmm_precip, cmap=cm.jet)

# From my old script
#m.drawlsmask(land_color='white',ocean_color='white')
#trmm_precip.mask
cs = m.contourf(x,y,trmm_precip*trmm_lsmask,clevs,cmap=cm.s3pcpn)  # works
#cs = m.pcolormesh(x,y,trmm_precip) # works but standard matlab look

#cs = m.pcolormesh(x,y,trmm_precip,norm=norm,cmap=cm.s3pcpn)

#plt.pcolormesh(trmm_precip) # WORKS

#plt.pcolor(trmm_precip)

#scatter(trmm_precip,trmm_precip+log(trmm_precip))

# Add colorbar
cbar = m.colorbar(cs)
# Set label
cbar.set_label('mm')

savefig('plots/trmm_precip_SACA_area.png',optimize=True,quality=85,dpi=900)

#plt.show()