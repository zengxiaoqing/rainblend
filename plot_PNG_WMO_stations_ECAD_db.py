# Make python script executable
#!/usr/bin/python

# Script produces markers of 42 existing weather stations on Papua New Guinea

# ==========================================
# Author: I.Stepanov (igor.stepanov@knmi.nl)
# 06.06.2016 @KNMI
# ============================================================================================
# Updates list
# 06.06.2016. Script created
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
            lat_0=-6.0, lon_0=147,                  # center: lat_0=0.125, lon_0=130
            llcrnrlon=139.0, llcrnrlat=-12.0,
            urcrnrlon=165.0, urcrnrlat=0.5,
            fix_aspect=True,
            resolution='f')

# Borders for Papua New Guinea (approximate for now)

# East: 8.23.18.4.S 165.11.08.7.E
# West: 5.50.46.7.S 139.47.10.4.E

# North: 0.05'58.7"S 149.32'31.5"E
# South: 12.26'14.3"S 151.49'38.0"E


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

# Plot markers from 42 existing stations

# 1
# -----------------------------------------------------
lon, lat = 149.383, -9.96
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Agaun') #,%5.1fW,%3.1fN)
# -----------------------------------------------------

# 2
# -----------------------------------------------------
lon, lat = 145.9, -6.316667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Aiyura')
# -----------------------------------------------------

# 3
# -----------------------------------------------------
lon, lat = 142.816667, -4.216667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Ambunti')
# -----------------------------------------------------

# 4
# -----------------------------------------------------
lon, lat = 146.983333, -2.016667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'BIPI')
# -----------------------------------------------------

# 5
# -----------------------------------------------------
lon, lat = 146.65, -7.2
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Bulolo')
# -----------------------------------------------------

# 6
# -----------------------------------------------------
lon, lat = 150.4, -5.483333
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Dami')
# -----------------------------------------------------

# 7
# -----------------------------------------------------
lon, lat = 143.2, -9.083333
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Daru W.O.')
# -----------------------------------------------------

# 8
# -----------------------------------------------------
lon, lat = 143.883333, -6.65
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Erave')
# -----------------------------------------------------

# 9
# -----------------------------------------------------
lon, lat = 153.666667, -4.016667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Feni')
# -----------------------------------------------------

# 10
# -----------------------------------------------------
lon, lat = 145.383333, -6.066667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Goroka ATS')
# -----------------------------------------------------

# 11
# -----------------------------------------------------
lon, lat = 141.183333, -3.9
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Green river')
# -----------------------------------------------------


# 12
# -----------------------------------------------------
lon, lat = 150.333333, -10.316667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Gurney W.O.')
# -----------------------------------------------------

# 13
# -----------------------------------------------------
lon, lat = 150.4, -5.466667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt-20000,'Hoskins W.O.')
# -----------------------------------------------------

# 14
# -----------------------------------------------------
lon, lat = 154.233333, -11.316667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Jinjo')
# -----------------------------------------------------

# 15
# -----------------------------------------------------
lon, lat = 150.816667, -2.566667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Kavieng W.O.')
# -----------------------------------------------------

# 16
# -----------------------------------------------------
lon, lat = 145.766667, -7.95
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Kerema')
# -----------------------------------------------------

# 17
# -----------------------------------------------------
lon, lat = 141.183333, -6.083333
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Kiunga W.O.')
# -----------------------------------------------------

# 18
# -----------------------------------------------------
lon, lat = 144.6, -5.483333
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Koinambe')
# -----------------------------------------------------


# 19
# -----------------------------------------------------
lon, lat = 144.966667, -6.016667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Kundiawa')
# -----------------------------------------------------

# 20
# -----------------------------------------------------
lon, lat = 151, -10.05
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Kurada')
# -----------------------------------------------------


# 21
# -----------------------------------------------------
lon, lat = 143.3, -6.366667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Lake Kutubu')
# -----------------------------------------------------


# 22
# -----------------------------------------------------
lon, lat = 147.383333, -2.416667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Lobrum')
# -----------------------------------------------------


# 23
# -----------------------------------------------------
lon, lat = 145.8, -5.216667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'ro')
plt.text(xpt+10000,ypt+10000,'Madang W.O.')
# -----------------------------------------------------


# 24
# -----------------------------------------------------
lon, lat = 143.666667, -6.166667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Mendi')
# -----------------------------------------------------


# 125
# -----------------------------------------------------
lon, lat = 152.833333, -10.683333
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Misima W.O.')
# -----------------------------------------------------


# 26
# -----------------------------------------------------
lon, lat = 147.416667, -2.05
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Momote W.O.')
# -----------------------------------------------------


# 27
# -----------------------------------------------------
lon, lat = 144.3, -5.833333
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Mt Hagen Ats')
# -----------------------------------------------------


# 28
# -----------------------------------------------------
lon, lat = 146.716667, -6.566667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Nadzab W.O.')
# -----------------------------------------------------

# 29
# -----------------------------------------------------
lon, lat = 152.45, -3.666667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Namatanai')
# -----------------------------------------------------

# 30
# -----------------------------------------------------
lon, lat = 153.266667, -11.3
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Nimowa')
# -----------------------------------------------------

# 31
# -----------------------------------------------------
lon, lat = 154.666667, -3.316667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Nuguria')
# -----------------------------------------------------

# 32
# -----------------------------------------------------
lon, lat = 140.333333, -5.783333
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Orobiga')
# -----------------------------------------------------

# 33
# -----------------------------------------------------
lon, lat = 147.216667, -9.383333
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'ro')
plt.text(xpt+10000,ypt+10000,'Port Moresby')
# -----------------------------------------------------

# 34
# -----------------------------------------------------
lon, lat = 148.633333, -9.583333
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Safia')
# -----------------------------------------------------

# 35
# -----------------------------------------------------
lon, lat = 150.783333, -9.666667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Salamo')
# -----------------------------------------------------

# 36
# -----------------------------------------------------
lon, lat = 144.083333, -4.083333
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Saramandi')
# -----------------------------------------------------

# 37
# -----------------------------------------------------
lon, lat = 150.666667, -10.616667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Sideia')
# -----------------------------------------------------

# 38
# -----------------------------------------------------
lon, lat = 152.366667, -4.333333
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Tokua W.O.')
# -----------------------------------------------------


# 39
# -----------------------------------------------------
lon, lat = 149.316667, -9.083333
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Tufi')
# -----------------------------------------------------

# 40
# -----------------------------------------------------
lon, lat = 150.95, -6.166667
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Uvol')
# -----------------------------------------------------

# 41
# -----------------------------------------------------
lon, lat = 141.316667, -2.7
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Vanimo')
# -----------------------------------------------------

# 42
# -----------------------------------------------------
lon, lat = 143.666667, -3.583333
xpt,ypt=m(lon,lat)
lonpt,latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')
plt.text(xpt+10000,ypt+10000,'Wewak W.O.')
# -----------------------------------------------------




# Updated LS Mask by NASA

#cs = m.pcolor(x_mask,y_mask,trmm_lsmask)
#cs= m.pcolormesh(x_mask,y_mask,trmm_lsmask)
#cs =m.contourf(x_mask,y_mask,trmm_lsmask,clevs_wat_perc) 

# Add colorbar 
#cbar =m.colorbar(cs) # 

# Add title 
#plt.title('TRMM (NASA) percentage of water [Land Sea Mask]', size=26) 

# Save plot
savefig('plots/PNG_WMO_stations_db_plot.png',optimize=True,quality=85,dpi=300)


#plt.show()

quit()