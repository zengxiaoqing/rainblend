# Make python script executable
#!/usr/bin/python


# Thin Based Spline applied to station SACA data

# Radial Base Function core:

# interp = scipy.interpolate.Rbf(x, y, z, function='thin_plate')
# yi, xi = np.mgrid[0:1:100j, 0:1:100j]
# zi = interp(xi, yi)


# ==========================================
# Author: I.Stepanov (igor.stepanov@knmi.nl)
# 28.10.2016 @KNMI
# ============================================================================================
# Updates list
#
# ============================================================================================
# To be fixed:
#
# NaN/inf issue for interpolation

# ================================================================

from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import maskoceans
import matplotlib.pyplot as plt
import numpy as np
# import string
# import matplotlib
import matplotlib.cm as cm
import scipy.interpolate
np.set_printoptions(threshold='nan')  # print full array
# from matplotlib.mlab import griddata
from netCDF4 import Dataset
from matplotlib.colors import Normalize


# TRMM bound
# ==========================================================================================
in_path = "/nobackup/users/stepanov/TRMM_data/nc/annual_files/cropped/land_only/"   # work station
# in_path = "/Users/istepanov/github/TRMM_blend/TRMM_nc/"                           # rMBP
in_path_lsmsk_TRMM = "/nobackup/users/stepanov/TRMM_data/Land_Sea_Mask/"
# ==========================================================================================


# Define paths to NC files
#===========================================================================================
# TRMM file for SACA area, Land only
file_trmm = '3B42_daily.2000_georef_SACA_land_only.nc'  # work station
# 3b42-daily.2000-georef-saca-land-only.nc            # rMBP
#
nc_trmm = Dataset(in_path+file_trmm, 'r')

# Extract the precip var & # Coordinates for TRMM: [latitude, longitude][201x400]
trmm_precip = nc_trmm.variables['r'][161, :, :]   # [time, lat, lon], 0= 01.01.2013 (python)
lons = nc_trmm.variables['longitude']
lats = nc_trmm.variables['latitude']

# Land Sea Maks TRMM specific
file_lsm_TRMM = 'TMPA_mask_georef_SACA_match_TRMM_grid.nc'
nc_lsmask_trmm = Dataset(in_path_lsmsk_TRMM+file_lsm_TRMM, 'r')
trmm_lsmask = nc_lsmask_trmm.variables['landseamask'][:, :]

# ==========================================================================================



# Import data from ASCII CSV file
# ==========================================================================================
#
#gauges = np.genfromtxt("/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_year2000-06-10.dat",
# gauges = np.genfromtxt("/usr/people/stepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_year2000-06-10.dat",
#                         delimiter=',',
#                         # dtype=[('lat', np.float32), ('lon', np.float32), ('rr', 'i2')],
#                         dtype=[('lat', float), ('lon', float), ('rr', float)],
#                         usecols=(2, 3, 0))

gauges = np.genfromtxt("/usr/people/stepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_year2000-06-10.dat",
                        delimiter=',',
                        missing_values={0:-9999.00},
                        filling_values={0:1},
                        # dtype=[('lat', np.float32), ('lon', np.float32), ('rr', 'i2')],
                        dtype=[('lat', float), ('lon', float), ('rr', float)],
                        usecols=(2, 3, 0))

# np.genfromtxt('data_table3.txt', skip_header=1,
#                                  missing_values=(-9999,-9999,-9999),
#                                  filling_values=(1,1,1))array([[ 4.83900000e-01]])



# Make lat & lon easier to use down the line:
lat = gauges['lat']
lon = gauges['lon']
rr = gauges['rr']

# df = df[df.line_race != 0]
# rr = rr[rr.rr != 0]

# df = df[df.line_race != 0]


# Filter out stations without measurements (-999.9)
# rr[rr == -9999]=0.
#
# rr[rr == -9.99900000e+3] = np.nan
# rr[rr == -9999] = np.NaN
# rr[rr == -9.99900000e+3] = 0.0
# rr = rr[~np.isnan(rr)]   # Remove nan


# All land points convert to 1
trmm_lsmask[trmm_lsmask != 100] = 1.
# All sea points convert to 0
trmm_lsmask[trmm_lsmask == 100] = 0.
# trmm_lsmask[trmm_lsmask==100]=np.nan

# ==========================================================================================

# # Now convert NaN to closest station value
# ind = np.where(~np.isnan(rr))[0]
# first, last = ind[0], ind[-1]
# rr[:first] = rr[first]
# rr[last + 1:] = rr[last]

# rr[~np.isnan(rr).any(axis=1)]

print rr
quit()

# Design figure
# ================================================================
xsize = 20
ysize = 10

fig = plt.figure(figsize=(xsize,ysize))
# fig, ax = plt.subplots(figsize=(xsize, ysize))
# ================================================================

m = Basemap(projection='gall',
            llcrnrlon=80.125,              # lower-left corner longitude
            llcrnrlat=-24.875,               # lower-left corner latitude
            urcrnrlon=179.875,               # upper-right corner longitude
            urcrnrlat=25.125,               # upper-right corner latitude
            resolution='i',
            area_thresh=100.0,
            )


# # Create regular grid from TRMM lon/lat
xi, yi = np.meshgrid(lons, lats)
xnew, ynew = m(xi, yi)

# Create grid from stations data:
xstat, ystat = m(lon, lat)


# # Interpolation
# # =============================================================================
# # Radial Basis Function

# Set up few interolation parameters, this also affects the plot title
#
# interpolation='linear'

# When doing thing plate spline, pre-step to avoid nasty negative numbers:
rr[rr == 0] = 1 # a trick to make rr*2 ln(rr) 0
interpolation = 'thin_plate'
#

# smoothing_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]
smoothing_vals = [2]
for smoothing_val in smoothing_vals:
      print 'Now smoothing with parameter set to: ', smoothing_val
# smoothing_val = 2

      # Now interpolate
      rbf = scipy.interpolate.Rbf(lon, lat, rr, function=interpolation, smooth=smoothing_val)
      rri = rbf(xi, yi)


      print rri
      # quit()


      # # Actual plotting ----------------------------------------------------------

      # Plot Interpolation
      # im = m.pcolor(xnew, ynew, rri*trmm_lsmask, cmap=cm.Blues, zorder=1)
      im = m.pcolor(xnew, ynew, rri, cmap=cm.Blues, zorder=1)
      # Plot Stations
      scat_plot = m.scatter(xstat, ystat, 50, c=rr, cmap=cm.cool, zorder=2)

      # ---------------------------------------------------------------------------

      # Color bar properties ---------------------------------------
      # Color plot
      im.set_clim(0.0, 15.0)  # affects colorbar range too

      # Scatter plot
      scat_plot.set_clim(0.0, 15.0)  # affects colorbar range too
      # ------------------------------------------------------------


      # # Range of axis
      # plt.xlim([80.125, 179.875])
      # plt.ylim([-24.875, 25.125])



      # draw coastlines, country boundaries, fill continents.
      m.drawcoastlines(linewidth=0.75)
      m.drawcountries(linewidth=0.75)
      # draw parallels
      parallels = np.arange(-40., 40, 10.)
      m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
      # draw meridians
      meridians = np.arange(80., 180., 10.)
      m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)

      # m.drawlsmask(land_color="#ddaa66",
      #              ocean_color="#7777ff",
      #              resolution='l')


      # # -- Colorbar 1 | bottom | interpolated
      cb1 = m.colorbar(im,
                       location='bottom',
                       label='Interpolated stations precip'
                       # fontsize='14'
                       )
                       # location='right'
                       # cax=position
                       # )
                       # orientation='vertical',
                       # ticks=[0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0])


      # # -- Colorbar 2 | right | stations
      cb2 = m.colorbar(scat_plot,
                       # orientation='horizontal',
                       label='Station values'
                       # fraction=0.046,
                       # pad=0.04,
                       )

      # plt.show()

      # Save as PNG
      plt.savefig('plots/Precip_stations_'+interpolation+'_spline_smoothin_eq_'+str(smoothing_val)+'_20000610.png',
                  bbox_inches='tight',
                  optimize=True,
                  quality=85,
                  dpi=300)


      plt.close(fig)

      # quit()

#Create own grid
# grid data
# numcols, numrows = 1000, 1000
# xi = np.linspace(data['projected_lon'].min(), data['projected_lon'].max(), numcols)
# yi = np.linspace(data['projected_lat'].min(), data['projected_lat'].max(), numrows)
# xi, yi = np.meshgrid(xi, yi)
# numcols, numrows = 100, 100
# xi = np.linspace(proj_lon.min(), proj_lon.max(), numcols)
# yi = np.linspace(proj_lat.min(), proj_lat.max(), numrows)
# xi, yi = np.meshgrid(xi, yi)
