# Make python script executable
#!/usr/bin/python

# Script produces TRMM Land Sea Mask plot

# ==========================================
# Author: I.Stepanov (igor.stepanov@knmi.nl)
# 01.04.2016 @KNMI
# ============================================================================================
# Updates list
# 01.04.2016. Script created as a derivative of plotting TRMM data on land only
# 22.04.2016. Corrected the latitudinal shift caused by the negative lat values rounding
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

#in_path="/usr/people/stepanov/EOBS_data/"            # home folder
in_path="/nobackup/users/stepanov/TRMM_data/nc/annual_files/cropped/"
in_path_lsmsk_TRMM="/nobackup/users/stepanov/TRMM_data/Land_Sea_Mask/"
in_path_rr_SACA="/nobackup/users/stepanov/SACA/final/"


# Files
#===========================================================================================

# Precipitation
# =====================
# Precip TRMM
file_name='3B42_daily.2013_georef_SACA.nc'    
# ncks -d latitude,-24.875,25.125 -d longitude,80.125,179.875 3B42_daily.2015.12.29.7.nc 3B42_daily.2015.12.29.7_georef_SACA.nc

# Precip SACA rr
file_r_SACA='rr_0.25deg_regular.nc'

# Land Sea Maks TRMM update by  Zhong Liu, Ph.D. Zhong.Liu-1@nasa.gov, remapped as NN to TRMM r
file_lsm_TRMM_cdo_to_SACA_coords='TMPA_land_sea_mask_georef_SACA.nc'
#ncks -d lat,-24.875,25.125 -d lon,80.125,179.875 TMPA_land_sea_mask.nc TMPA_land_sea_mask_georef_SACA.nc

# =====================

#===========================================================================================


# Full file paths
#===========================================================================================
file_pr = [in_path+file_name]  
file_rr_SACA = [in_path_rr_SACA+file_r_SACA]  
file_lsmask_TRMM_cdo_to_SACA = [in_path_lsmsk_TRMM+file_lsm_TRMM_cdo_to_SACA_coords]


# Review imported file paths in log
print "Location of TRMM precipitation file is: ",file_pr
print
print
print "Location of SACA precip file is: ",file_rr_SACA
print
print
print "Location of TRMM land-sea mask file is: ",file_lsmask_TRMM_cdo_to_SACA
print
print
#===========================================================================================


# Define paths to NC files
#===========================================================================================

# Precip and elevation (Land Sea Mask)
nc_trmm        = Dataset(in_path+file_name,'r')                               # [latitude, longitude][201x400]
nc_SACA_rr     = Dataset(in_path_rr_SACA+file_r_SACA,'r')                     # [longitude, latitude][400x201]
nc_lsmask_trmm = Dataset(in_path_lsmsk_TRMM+file_lsm_TRMM_cdo_to_SACA_coords) # new LS maks by Zhong Liu


# Coordinates for TRMM
lons = nc_trmm.variables['longitude']
lats = nc_trmm.variables['latitude']

# Coordinates for SACA
lons_saca = nc_SACA_rr.variables['longitude']
lats_saca = nc_SACA_rr.variables['latitude']

# Coordinates for LS mask
lons_ls_mask = nc_lsmask_trmm.variables['lon'][:]
lats_ls_mask = nc_lsmask_trmm.variables['lat'][:]

print 'lats_ls_mask', lats_ls_mask
#===========================================================================================


# Extract the actual variable
# For TRMM data go from 1-365 in ncview, but python counts 0-364

trmm_precip        = nc_trmm.variables['r'][0,:,:]                        # [time, lat, lon], 0= 01.01.2013 (python)
saca_precip        = nc_SACA_rr.variables['rr'][11688,:,:]                # 11688 = 01.Jan.2013. (python)
trmm_lsmask        = nc_lsmask_trmm.variables['landseamask'][:,:]         # [landseamask, latitude, longitude]   

# 1-12418 in ncview, but python counts 0-12417


# Data pre-processing
#===========================================================================================



# Design figure
# ================================================================

xsize=20
ysize=12

fig = plt.figure(figsize=(xsize,ysize))


# Map projection
# ================================================================

# Experimental to match coast line better with TRMM orography
m = Basemap(projection='merc',                       # SACA gridded data set coordinates
            lat_0=0.125, lon_0=130,                  # center: lat_0=0.125, lon_0=130
            llcrnrlon=80.125, llcrnrlat=-24.875,
            urcrnrlon=179.875, urcrnrlat=25.125,
            fix_aspect=True,
            resolution='i')


# Precip bins to be used for precip
clevs = [0,1,2.5,5,7.5,10,15,20,30,40,50,70,100,150]


# More map configuration
# draw coastlines, country boundaries
m.drawcoastlines(linewidth=0.25)
m.drawcountries(linewidth=0.25)
# draw parallels.
parallels = np.arange(-40.,40,10.)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
# draw meridians
meridians = np.arange(80.,180.,10.)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)


# Make grid for TRMM data
ny = trmm_precip.shape[0]
nx = trmm_precip.shape[1]
lons, lats = m.makegrid(nx, ny)                     # get lat/lons of ny by nx evenly spaced grid.
x, y = m(lons, lats)                                # compute map proj coordinates.

# Make grid for SACA data
ny_saca = saca_precip.shape[0]
nx_saca = saca_precip.shape[1]
lons_saca, lats_saca = m.makegrid(nx_saca, ny_saca) 
x_saca, y_saca = m(lons_saca, lats_saca) 

# Make grid for TRMM Land Sea mask (updated)
lons_mask, lats_mask = np.meshgrid(lons_ls_mask, lats_ls_mask)
x_mask, y_mask = m(lons_mask, lats_mask)


print 'lons_mask', lons_mask
print 'lats_mask', lats_mask
print

# ================================================================


# Actual plotting and rendering
# ================================================================
# Plot WATER PERCENTAGE for the cropped DOMAIN


# Plotting levels
clevs_wat_perc=[0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90,100.0]
#clevs_wat_perc=np.arange(0.0,100.0,10.0)

# Updated LS Mask by NASA
#cs = m.pcolor(x_mask,y_mask,trmm_lsmask)
cs= m.pcolormesh(x_mask,y_mask,trmm_lsmask)
#cs =m.contourf(x_mask,y_mask,trmm_lsmask,clevs_wat_perc) 

# Add colorbar 
cbar =m.colorbar(cs) # 

# Add title 
plt.title('TRMM (NASA) percentage of water [Land Sea Mask]', size=26) 

# Save plot

# LS Mask update
#savefig('plots/Water_percentage_TRMM_from_LS_mask_update_contourf_new_lat_0_correct_grid.png',optimize=True,quality=85,dpi=600)
#savefig('plots/Water_percentage_TRMM_from_LS_mask_update_pcolor_new_lat_0_correct_grid.png',optimize=True,quality=85,dpi=600)
savefig('plots/Water_percentage_TRMM_from_LS_mask_update_pcolormesh_new_lat_0_correct_grid.png',optimize=True,quality=85,dpi=600)


#plt.show()

quit()