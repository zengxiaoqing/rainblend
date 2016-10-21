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

# Resolution on 'i' (intermediate) makes good enough coastline. 
# Use 'f' (full) for showing off
m = Basemap(projection='merc',                      # SACA gridded data set coordinates
	        lat_0=0, lon_0=130,
	        llcrnrlon=80.125, llcrnrlat=-24.875,
	        urcrnrlon=179.875, urcrnrlat=25.125,
	        resolution='i')


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

# Precip bins to be used for plots
clevs = [0,1,2.5,5,7.5,10,15,20,30,40,50,70,100,150]#,200,250]#,300,400,500,600,750]


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
ny = trmm_precip.shape[0]; nx = trmm_precip.shape[1]
lons, lats = m.makegrid(nx, ny) # get lat/lons of ny by nx evenly spaced grid.
x, y = m(lons, lats) # compute map proj coordinates.

# Make grid for SACA data
ny_saca = saca_precip.shape[0]; nx_saca = saca_precip.shape[1]
lons_saca, lats_saca = m.makegrid(nx_saca, ny_saca) # get lat/lons of ny by nx evenly space grid.
x_saca, y_saca = m(lons_saca, lats_saca) # compute map proj coordinates.


# Actual plotting and rendering
# ================================================================


# Plot TRMM
# ===============
# cs = m.contourf(x,y,trmm_precip*trmm_lsmask,clevs,cmap=cm.s3pcpn)
# # Add colorbar
# cbar = m.colorbar(cs)
# # Add title
# plt.title('Date: 01. January 2014 TRMM precip (NASA land-sea mask)', size=26)
# # Set label
# savefig('plots/compare_plot_trmm_precip.png',optimize=True,quality=85,dpi=900)


# Plot SACA 
# ===============
# cs = m.contourf(x_saca,y_saca,saca_precip,clevs,cmap=cm.s3pcpn)
# #Add colorbar
# cbar = m.colorbar(cs)
# #Add title
# plt.title('Date: 01. January 2014 SACA precip', size=26)
# #Set label
# savefig('plots/compare_plot_SACA_precip.png',optimize=True,quality=85,dpi=900)


# Plot TRMM Else way (-+SACA)
# ===============
# cs = m.contourf(x,y,trmm_precip-saca_precip+saca_precip ,clevs,cmap=cm.s3pcpn)
# #Add colorbar
# cbar = m.colorbar(cs)
# #Add title
# plt.title('Date: 01. January 2014 TRMM precip (SACA land-sea mask)', size=26)
# #Set label
# savefig('plots/compare_plot_trmm_precip_min_saca_plus_saca.png',optimize=True,quality=85,dpi=900)


# Plot TRMM Else way (-+SACA)
# ===============

# cs = m.contourf(x,y,polygon_data)
# #Add colorbar
# #cbar = m.colorbar(cs)
# #Add title
# plt.title('Date: 01. January 2014 TRMM grid points (SACA land-sea mask)', size=26)
# #Set label
# savefig('plots/grid_points_plot_trmm_precip_min_saca_plus_saca.png',optimize=True,quality=85,dpi=900)



# Plot grid points only
# ===============
# Function in python to create array from data grid points

# Adapted getPolygon function for SACA or TRMM data

def getPolygon(x,y):
 
    lon_bd = np.concatenate((x[:,0],y[-1,:],x[::-1,-1], y[0,::-1] ))
    lat_bd = np.concatenate((x[:,0],y[-1,:],x[::-1,-1], y[0,::-1] ))
 
    """ Save the polygon as array to plot later"""
    polygon_data=np.empty((2,len(lon_bd)))
    for k in xrange(len(lon_bd)):
        polygon_data[0,k]=lon_bd[k]
        polygon_data[1,k]=lat_bd[k]
 
    return polygon_data


def drawGridBoundaries(ax,map,polygon_data):
    print "Plotting grid boundaries"
    polygon_data_xy=[]
    for i in xrange(len(polygon_data[0,:])):
        myx,myy=map(polygon_data[0,i],polygon_data[1,i])
        vertices=[myx,myy]
        polygon_data_xy.append(vertices)
 
    polygon_data_xy=np.asarray(polygon_data_xy)
    patch = Polygon(array(polygon_data_xy), facecolor='none',
        edgecolor=(.9, .3, .3, 1), linewidth=4)
    ax.add_patch(patch)

# cs = m.contourf(x,y)

# Custom way to unify all TRMM data and plot as markers

#clevs_grid = [0,50.0]                                       # this one

#trmm_grid = trmm_precip-saca_precip+saca_precip*0.0+1.0
#trmm_grid = trmm_precip*trmm_lsmask#-saca_precip#*0.0+1.0   # this one
#trmm_grid = saca_precip*0.0+1.0#-saca_precip#*0.0+1.0
#trmm_grid = trmm_lsmask*0.0+1.0#-saca_precip#*0.0+1.0

#trmm_grid = trmm_precip*trmm_lsmask-saca_precip

#print 'trmm_grid is now: ', trmm_grid

#cs = m.contourf(x,y,trmm_grid,clevs_grid,cmap=cm.s3pcpn)
#cs = m.contourf(x,y,trmm_grid,clevs_grid,cmap=cm.unicolor)  # this one
#cs = m.pcolor(x,y,trmm_grid,clevs,cmap=cm.s3pcpn)
# Add colorbar
#cbar = m.colorbar(cs)                                       # this one


#plt.show()