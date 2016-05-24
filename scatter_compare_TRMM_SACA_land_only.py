# Make python script executable
#!/usr/bin/python

# Script produces scatter plot fot variable
# rainfall estimates from TRMM, produyct 3B42 daily from NASA
# vs
# SACA precipitation

# ==========================================
# Author: I.Stepanov (igor.stepanov@knmi.nl)
# 01.04.2016 @KNMI
# ============================================================================================
# Updates list
# 01.04.2016. Script created as a derivative of plotting TRMM data on land only
# ============================================================================================


# Load python modules
import netCDF4
import pylab as pl
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from pylab import *
import math as m
from mpl_toolkits.basemap import Basemap, cm


# Define some paths
# ==========================================================================================

#in_path="/Users/istepanov/PostDoc/EOBS_data"         # local MBP
#in_path="/usr/people/stepanov/EOBS_data/"            # home folder
in_path="/nobackup/users/stepanov/TRMM_data/nc/annual_files/cropped/"
in_path_lsmsk_TRMM="/nobackup/users/stepanov/TRMM_data/Land_Sea_Mask/"
in_path_rr_SACA="/nobackup/users/stepanov/SACA/final/"


# Files
#===========================================================================================

# Precip TRMM
file_name='3B42_daily.2014_georef_SACA.nc'    
# ncks -d latitude,-24.875,25.125 -d longitude,80.125,179.875 3B42_daily.2015.12.29.7.nc 3B42_daily.2015.12.29.7_georef_SACA.nc

# Precip SACA rr
file_r_SACA='rr_0.25deg_regular.nc'

# Land Sea Maks TRMM specific
file_lsm_TRMM='TMPA_mask_georef_SACA_match_TRMM_grid.nc'
#ncks -d lat,-24.875,25.250 -d lon,80.125,179.875 TMPA_mask.nc TMPA_mask_georef_SACA_match_TRMM_grid.nc

#===========================================================================================


# Full file paths
#===========================================================================================

file_pr = [in_path+file_name]  
file_lsmask_TRMM = [in_path_lsmsk_TRMM+file_lsm_TRMM]
file_rr_SACA = [in_path_rr_SACA+file_r_SACA]  


# Review imported file paths in log
print "Location of TRMM precipitation file is: ",file_pr
print
print
print "Location of SACA precip file is: ",file_rr_SACA
print
print
print "Location of TRMM land-sea mask file is: ",file_lsmask_TRMM
print
print


# Precip and elevation (Land Sea Mask)
nc_trmm        = Dataset(in_path+file_name,'r')                  # [latitude, longitude][201x400]
nc_lsmask_trmm = Dataset(in_path_lsmsk_TRMM+file_lsm_TRMM,'r')   # [lat,lon][201x400]
nc_SACA_rr     = Dataset(in_path_rr_SACA+file_r_SACA,'r')        # [longitude, latitude][400x201]

# Coordinates for TRMM
lons = nc_trmm.variables['longitude']
lats = nc_trmm.variables['latitude']

# Coordinates for SACA
lons_saca = nc_SACA_rr.variables['longitude']
lats_saca = nc_SACA_rr.variables['latitude']
#===========================================================================================


# Extract the actual variable
# For TRMM data go from 1-365 in ncview, but python counts 0-364
trmm_precip = nc_trmm.variables['r'][0,:,:]                # [time, lat, lon], 0= 01.01.2014 (python)
trmm_lsmask = nc_lsmask_trmm.variables['landseamask'][:,:] # [time, latitude, longitude]   
saca_precip = nc_SACA_rr.variables['rr'][12053,:,:]        # 12053 = 01.Jan.2014. (python)
# 1-12418 in ncview, but python counts 0-12417


# Some data pre-processing
#===========================================================================================

fill_value=-999.9

# Python replacing syntax
# arr[arr > 255] = x

# All land points convert to 1
trmm_lsmask[trmm_lsmask!=100]=1.

# All sea points convert to 0
trmm_lsmask[trmm_lsmask==100]=fill_value

# New mask should now be: 1=land, 0=sea
# Multiply woth TRMM data when plotting

print 'TRMM land sea mask',trmm_lsmask
print
print "TRMM precip is: ", trmm_precip
print


# Design figure
# ================================================================

xsize=20
ysize=12

fig = plt.figure(figsize=(xsize,ysize))


# Map projection
# ================================================================




# Actual plotting and rendering
# ================================================================

# Plot TRMM
#cs = m.contourf(x,y,trmm_precip*trmm_lsmask,clevs,cmap=cm.s3pcpn)

# Plot SACA 
#cs = m.contourf(x_saca,y_saca,saca_precip,clevs,cmap=cm.s3pcpn)

# Quantititave comparison head2head

#ss = plt.scatter(trmm_precip*trmm_lsmask,saca_precip)
ss = plt.scatter(trmm_precip,saca_precip)

# Add colorbar
#cbar = m.colorbar(cs)
# Set label
#savefig('plots/compare_plot_SACA_precip.png',optimize=True,quality=85,dpi=900)cbar.set_label('mm')

#savefig('plots/trmm_precip_SACA_area.png',optimize=True,quality=85,dpi=900)
#savefig('plots/compare_plot_trmm_VS_SACA_precip.png',optimize=True,quality=85,dpi=900)
#savefig('plots/compare_plot_trmm_precip.png',optimize=True,quality=85,dpi=900)
#savefig('plots/compare_plot_SACA_precip.png',optimize=True,quality=85,dpi=900)
#savefig('plots/scatter_plot_SACA_vs_TRMM_precip.png',optimize=True,quality=85,dpi=900)

plt.show()