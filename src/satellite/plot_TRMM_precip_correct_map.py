# Make python script executable
#!/usr/bin/python

# pylint: disable=C0103
# pylint: disable-msg=C0103

# Script produces TRMM precip filtered using update (Zhong) Land Sea mask

# ==========================================
# Author: I.Stepanov (igor.stepanov@knmi.nl)
# 22.04.2016 @KNMI
# ============================================================================================
# Updates list
# 22.04.2016. Script created as a derivative of plotting TRMM Land Sea Mask
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
np.set_printoptions(threshold='nan')  # print full array


# Define some paths
# ==========================================================================================

in_path = "/nobackup/users/stepanov/TRMM_data/nc/annual_files/cropped/"
in_path_rr_SACA = "/nobackup/users/stepanov/SACA/final/"
in_path_lsmsk_TRMM = "/nobackup/users/stepanov/TRMM_data/Land_Sea_Mask/"


# Files
#===========================================================================================

# Precip TRMM
#
#file_name='3B42_daily.2013_georef_SACA.nc' 
file_name = '3B42_daily.2000_georef_SACA.nc' 
# ncks -d latitude,-24.875,25.125 -d longitude,80.125,179.875 3B42_daily.2015.12.29.7.nc
# 3B42_daily.2015.12.29.7_georef_SACA.nc

# Precip SACA rr
file_r_SACA = 'rr_0.25deg_regular.nc'

# Land Sea Maks TRMM update by  Zhong Liu, Ph.D. Zhong.Liu-1@nasa.gov, remapped as NN to TRMM r
file_lsm_TRMM_cdo_to_SACA_coords = 'TMPA_land_sea_mask_georef_SACA.nc'
#ncks -d lat,-24.875,25.125 -d lon,80.125,179.875 TMPA_land_sea_mask.nc
# TMPA_land_sea_mask_georef_SACA.nc

#===========================================================================================


# Full file paths
#===========================================================================================
file_pr = [in_path+file_name]  
file_rr_SACA = [in_path_rr_SACA+file_r_SACA]  
file_lsmask_TRMM_cdo_to_SACA = [in_path_lsmsk_TRMM+file_lsm_TRMM_cdo_to_SACA_coords]


# Review imported file paths in log
print "Location of TRMM precipitation file is: ", file_pr
print
print
print "Location of SACA precip file is: ", file_rr_SACA
print
print
print "Location of TRMM land-sea mask file is: ", file_lsmask_TRMM_cdo_to_SACA
print
print
#===========================================================================================


# Define paths to NC files
#===========================================================================================

# Precip and elevation (Land Sea Mask)
nc_trmm = Dataset(in_path+file_name, 'r')
# [latitude, longitude][201x400]
nc_SACA_rr = Dataset(in_path_rr_SACA+file_r_SACA, 'r')
# [longitude, latitude][400x201]
nc_lsmask_trmm = Dataset(in_path_lsmsk_TRMM+file_lsm_TRMM_cdo_to_SACA_coords)
# new LS maks by Zhong Liu


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
# =======================================================================================


# Extract the actual variable
# For TRMM data go from 1-365 in ncview, but python counts 0-364
#

# INDIVIDUAL DAY
#
# =======================================================================================
# trmm_precip        = nc_trmm.variables['r'][89,:,:]
# [time, lat, lon], 0= 01.01.2013 (python). 90 is 31st March ideally.
trmm_precip = nc_trmm.variables['r'][161, :, :]
# [time, lat, lon], 0= 01.01.2013 (python). 161 is 31st March ideally.
saca_precip = nc_SACA_rr.variables['rr'][11688, :, :]
# 11688 = 01.Jan.2013. (python)
trmm_lsmask = nc_lsmask_trmm.variables['landseamask'][:, :]
# [landseamask, latitude, longitude]
# =======================================================================================

# 1-12418 in ncview, but python counts 0-12417

# Accumulated period
# =======================================================================================
# Import entire year of precip data now
trmm_precip_array = nc_trmm.variables['r'][0-364, :, :]
# [time, lat, lon], 0= 01.01.2013 (python)
trmm_precip_array_2 = nc_trmm.variables['r'][:, :, :]
# =======================================================================================

print
#print 'precip array 2013', trmm_precip_array
print
#print 'precip array 2013_2', trmm_precip_array_2
print
#print 'precip array 2013_2 - precip array 2013', trmm_precip_array_2-trmm_precip_array


#quit()


# Data pre-processing
#===========================================================================================


# Pre-process TRMM land sea mask
#==================================
# # Define fill_value
# fill_value=-999.9

# # All land points convert to 1
# trmm_lsmask[trmm_lsmask!=100]=1.

# # All sea points convert to fill_value (-999.9)
# trmm_lsmask[trmm_lsmask==100]=fill_value

# # New mask should now be: 1=land, fill_value=sea

# # Multiply with TRMM data when plotting

# # SPrint new TRMM mask (1,fill_value only!)
# print 'TRMM land sea mask',trmm_lsmask
# print

# Do the same with new TRMM land sea mask (cdo remapnn to SACA coordinates)


# Pre-process SACA land sea mask
#==================================

# # All land points convert to 1
# trmm_lsmask_cdo[trmm_lsmask_cdo!=100]=1.

# # All sea points convert to fill_value (-999.9)
# trmm_lsmask_cdo[trmm_lsmask_cdo==100]=fill_value

# # New mask should now be: 1=land, fill_value=sea

# # Multiply with TRMM data when plotting

# # SPrint new TRMM mask (1,fill_value only!)
# print 'TRMM land sea mask CDO to SACA',trmm_lsmask_cdo
# print


# Design FIGURE
# ================================================================

xsize = 20
ysize = 10

fig = plt.figure(figsize=(xsize, ysize))


# Map projection
# ================================================================

# Experimental to match coast line better with TRMM orography
m = Basemap(projection='gall',
            # lat_0=0.125, lon_0=130,
            llcrnrlon=80.125, llcrnrlat=-24.875,
            urcrnrlon=179.875, urcrnrlat=25.125,
            # fix_aspect=True,
            area_thresh=100.0,
            resolution='i')


m.drawcoastlines(linewidth=0.75)
m.drawcountries(linewidth=0.75)
# draw parallels.
parallels = np.arange(-40., 40, 10.)
m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
# draw meridians
meridians = np.arange(80., 180., 10.)
m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)


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


# Make grid for TRMM data
# ny = trmm_precip.shape[0]
# nx = trmm_precip.shape[1]
# lons, lats = m.makegrid(nx, ny)                     # get lat/lons of ny by nx evenly spaced grid.
# x, y = m(lons, lats)                                # compute map proj coordinates.

# Alternative grid
lonst, latst = np.meshgrid(lons, lats)
x, y = m(lonst, latst)


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

# # Alternative SACA NaN removal
# #
# # where_are_NaNs = isnan(saca_precip)
# # saca_precip[where_are_NaNs] = 0


# print 'SACA LS mask is: ', saca_precip
# print


# clevs_saca_oro=(0.0,1.0)

# #cs = m.contourf(x_saca,y_saca,saca_precip,clevs_saca_oro,cmap=cm.s3pcpn)
# #cs = m.contourf(x_saca,y_saca,trmm_lsmask-(saca_precip*0.0+5.0),cmap=cm.s3pcpn)
# cs = m.contourf(x_saca,y_saca,trmm_lsmask-saca_precip,cmap=cm.s3pcpn)
# cs = m.contourf(x_saca,y_saca,trmm_lsmask-(saca_precip*0.0+5.0),clevs,cmap=cm.s3pcpn)

# cbar = m.colorbar(cs)
# plt.title('TRMM min SACA [precip] Land Sea Mask (01. January 2014)', size=26)
# savefig('plots/Land_sea_mask_TRMM_min_SACA_precip.png',optimize=True,quality=85,dpi=900)



#SACA LS mask
# ===============
# cs = m.contourf(x_saca,y_saca,saca_precip*0.0+5.0,clevs,cmap=cm.s3pcpn)
# cbar = m.colorbar(cs)
# plt.title('SACA precip Land Sea Mask (01. January 2013)', size=26)
# savefig('plots/Land_sea_mask_SACA_precip.png',optimize=True,quality=85,dpi=900)


# TRMM LS mask
# Process TRMM_LS_maks so that only land points are used
#
trmm_lsmask[trmm_lsmask==100.0]=np.NaN

# clevs_oro=[0.0,5.0,10.0]

# cs = m.contourf(x,y,trmm_lsmask,clevs_oro)
# cs = m.contourf(x,y,trmm_lsmask,clevs,cmap=cm.s3pcpn)
# Add colorbar
# cbar = m.colorbar(cs)
# Add title
# plt.title('TRMM (NASA) land-sea mask for precip (01. January 2013))', size=26)
# Set label
# savefig('plots/Land_sea_mask_TRMM_precip.png',optimize=True,quality=85,dpi=900)


# TRMM LS mask, when CDO remapped to SACA
# Process TRMM_LS_maks so that only land points have values
#
# trmm_lsmask_cdo[trmm_lsmask_cdo==100.0]=np.NaN


# Updated LS Mask by NASA
#cs = m.pcolor(x,y,trmm_lsmask_update)
#cs= m.pcolormesh(x,y,trmm_lsmask_update)
#cs =m.contourf(x_mask,y_mask,trmm_lsmask,clevs_wat_perc) 

# Update TRMM precip using new LS mask that is correct (Zhong, NASA)
# ---------------------------------------------------------------------------------------

# Without LS mask
# cs =m.contourf(x,y,trmm_precip,clevs_precip,cmap=cm.s3pcpn)

# With LS mask
# cs =m.contourf(x,y,trmm_precip*trmm_lsmask,clevs_precip,cmap=cm.s3pcpn)


# Used last time
# clevs_precip_white_zero_SACA = [-0.5,0,0.1,0.5,2.5,5,7.5,10,15,20,30,40,50,100]
# New clevel upgrade
# clevs_precip_white_zero_SACA = [0,0.1,0.5,2.5,5,7.5,10,15,20,30,40,50,100]#,200,250]
# From original color map
clevs_precip_white_zero_SACA = [0.01, 0.1, 0.25, 0.50, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0,
                                6.0]

cs = m.contourf(x, y, trmm_precip*trmm_lsmask,
                clevs_precip_white_zero_SACA,
                cmap=precip_colormap)

# cs =m.contourf(x,y,trmm_precip*trmm_lsmask,
                # clevs_precip_white_zero,
                # cmap=plt.cm.jet,
                # ticks=[0,1,2.5,7.5,10,15,30,50,100,150])

# Heavy rain, sum over a year
#
# cs = m.contourf(x,y,trmm_precip_array*trmm_lsmask,clevs_precip_med_heavy)
# cs = m.contourf(x,y,trmm_precip_array*trmm_lsmask,clevs_precip)    # entire year
# cs = m.pcolormesh(x,y,trmm_precip_array+100.0*trmm_lsmask)
# ---------------------------------------------------------------------------------------


# Add colorbar 
# cbar =m.colorbar(cs,ticks=[0,0.1,0.5,2.5,5.0,7.5,10,15,20,30,40,50,100]) # 
cbar = m.colorbar(cs)
# Colorbar units
cbar.set_label('Rainfall [mm]', fontsize=16)

# Title 
#
# plt.title('TRMM precipitation | w/ Land Sea Mask | 31.03.2000', size=26) 
plt.title('TRMM precipitation | w/ Land Sea Mask | 10.06.2010', size=20) 



# Save plot as PNG
# ------------------------------------------------------------------------------------

# With LS mask one day
#
# savefig('plots/Precip_TRMM_from_LS_mask_update_contourf_new_lat_0_correct_grid_w_LS_mask_'
#         'IN_10062010_white_zero_mm_min_one day.png',
#         bbox_inches='tight',
#         optimize=True,
#         quality=85,
#         dpi=300)

plt.show()

quit()
