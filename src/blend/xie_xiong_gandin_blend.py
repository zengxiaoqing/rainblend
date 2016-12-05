# -*- coding: utf-8 -*-

# Make python script executable
#!/usr/bin/python

# xie_xiong_gandin_blend.py

# Optimal Interpolation from Gandin 1965 (Xie and Xiong 2011)
# is applied to TRMM v.7 gridded precipitation dataset to merge
# with the SACA database station data .

# Paper:
# A conceptual model for constructing high‐resolution gauge‐satellite merged precipitation analyses
# P Xie, AY Xiong
# Journal of Geophysical Research: Atmospheres 116 (D21)
# NOOA


# ==========================================
# Author: I.Stepanov (igor.stepanov@knmi.nl)
# 11.11.2016 @KNMI
# ============================================================================================
# Updates list
#
# Code edited through DIVA user guide for approximations
# ============================================================================================
# To be fixed:
#
# Define and calculate W_ki
# ================================================================

from mpl_toolkits.basemap import Basemap
# from mpl_toolkits.basemap import maskoceans
import matplotlib.pyplot as plt
import numpy as np
# import matplotlib
import matplotlib.cm as cm
import scipy.interpolate
np.set_printoptions(threshold='nan')  # print full array
from netCDF4 import Dataset
# from matplotlib.colors import Normalize
# from math import sqrt
import math

print math.pi


# Product function
def prod(iterable):
    return reduce(operator.mul, iterable, 1)


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
gauges = np.genfromtxt("/usr/people/stepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_year2000-06-10.dat",
                        delimiter=',',
                        dtype=[('lat', float), ('lon', float), ('rr', float)],
                        usecols=(2, 3, 0),
                        missing_values=-9999,
                        usemask=True)


# Make lat & lon easier to use down the line:
lat = gauges['lat']
lon = gauges['lon']
rr = gauges['rr']


# All land points convert to 1
trmm_lsmask[trmm_lsmask != 100] = 1.
# All sea points convert to 0
trmm_lsmask[trmm_lsmask == 100] = 0.
# trmm_lsmask[trmm_lsmask==100]=np.nan

# ==========================================================================================

# print rr
# quit()


# Design figure
# ================================================================
xsize = 20
ysize = 10

fig = plt.figure(figsize=(xsize,ysize))
# fig, ax = plt.subplots(figsize=(xsize, ysize))
# ================================================================

# # Interpolation
# # =============================================================================
# # Radial Basis Function


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


# Set up few interolation parameters, this also affects the plot title
#
# interpolation='linear'
# interpolation = 'thin_plate'
interpolation = 'cubic'

# Comment line below to TURN drizzle ON
# drizzle = 'OFF'       # Trick to make rr*2 ln(rr) = 0
drizzle = 'ON'        # Keep rain in range 0-1mm in the spline


# Switch for 0-1mm/day range filtering to do log smoothing:
# ----------------------------------------------------------
if drizzle == 'OFF':
    rr[rr <= 1.0] = 1.0        # Trick to make rr*2 ln(rr) = 0
elif drizzle == 'ON':
    rr == rr
# ----------------------------------------------------------


# For Thin Plate spline input data is pre and post-processed:
# 1. Square root the data
# 2. TPS run
# 3. Square the data

rr = np.sqrt(rr)

epsilon_list = [1] # From 1 - million
  

smoothing_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 40, 50, 100]
# smoothing_vals = ['automatic']

for epsilon_val in epsilon_list:
#  print 'Now setting epsilon parameter to: ', epsilon_val

    for smoothing_val in smoothing_vals:
        print 'Now smoothing with parameter set to: ', smoothing_val
        print 'Now setting epsilon parameter to: ', epsilon_val

        # # Now interpolate with prescribed smoothing parameter (lambda)
        rbf = scipy.interpolate.Rbf(lon, lat, rr,
                                    function=interpolation,
                                    smooth=smoothing_val,
                                    epsilon=epsilon_val)
        # Interpolate with automatic smoothing parameter selection
        # rbf = scipy.interpolate.Rbf(lon, lat, rr, function=interpolation)

        rri = rbf(xi, yi)

        # Now square all processed precip back (normalize precip matrix too)
        rri = rri*rri

        print 'Interpolated station precip is: ', rri
        

        # Intellective objective analysis ----------------------------------------------------------

        # Deriving weights ======================
        # Optimal weight matrix via Kalnay
        Wght_static = 4.75
        Wght_dyn = 


        # =======================================


        # Adjust geospatial calibration of station data to TRMM grid (weights free)

        # F0 = G0 + (Fi - Gi)

        # RRo = trmm_precip + (rr - trmm_precip*factor)
        RRo = trmm_precip + Wght_static * (rri - trmm_precip)

        print 'Blended precip is: ', RRo


        # Actual plotting ----------------------------------------------------------

        # Plot Interpolation
        # im = m.pcolor(xnew, ynew, rri*trmm_lsmask, cmap=cm.Blues, zorder=1)
        # im = m.pcolor(xnew, ynew, RRo, cmap=cm.Blues, zorder=1)  # Blue cmap
        im = m.pcolor(xnew, ynew, RRo, cmap=cm.rainbow_r, zorder=1)    # Stations cmap
        # Plot Stations
        # scat_plot = m.scatter(xstat, ystat, 50, c=rr, cmap=cm.cool, zorder=2)  # old pink cmap
        scat_plot = m.scatter(xstat, ystat, 50, c=rr, cmap=cm.Blues, zorder=2)  # blue red contrast

        # ---------------------------------------------------------------------------

        # Color bar properties ---------------------------------------
        # Color plot
        # im.set_clim(0.0, 150.0)  # affects colorbar range too
        im.set_clim(0.0, 30.0)  # affects colorbar range too

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
                         # ticks=[0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0,
                                  # 35.0, 40.0, 45.0, 50.0, 55.0, 60.0])


        # # -- Colorbar 2 | right | stations
        cb2 = m.colorbar(scat_plot,
                         # orientation='horizontal',
                         label='Station values'
                         # fraction=0.046,
                         # pad=0.04,
                        )

        # plt.show()

        # Save as PNG
        plt.savefig('plots/Precip_blend_'+interpolation+'_spline_smoothin_eq_'+
                    str(smoothing_val)+'_epsilon_'+
                    str(epsilon_val)+'_drizzle_'+
                    drizzle+'_20000610.png',
                    bbox_inches='tight',
                    optimize=True,
                    quality=85,
                    dpi=300)

quit()




# Weights:
# Determined by minimizing the analysis error variance

# Wki is define by solving the linear equation group:
mu_ki_f = sum(mu_ij_f + mu_ij_o * lambda_i * lambda_j) * W_kj   # i = 1, 2, ..., n.

# mu_ij_f is the first guess (observation) error correlation at two grid boxes i and j
#
# mu_ki_f is the first guess error correlation between the target grid box k and the 
# observation grid box i, respectively.

# mu_ij_o = 1 for i == j
# mu_ij_o = 0 for i != j
# After W_ki is determined from previous step, the analyzed values A_k can be defined 
# from the first guess and observation through the eq below.

# Translated into TRMM42B v7.0 imported above, we have:

# mu_ki_f = sum(mu_ij_f + )

# Final expression: plugging weights into blended precip values
Ak = Fk + np.sum(Wki(Oi - Fi))

# Eq B
Ek = (A_k - T_k)^2  # T_k is truth at grid point (k), should be ensemble process

# ERROR variance for resulting Ak =======================================================
#
# Express the truth (T_k) as the sum of the first guess (F_k) and the first guess error 
# sigma_k_f, error variance (E_k)^2  defined in eq B:

# E_k_sqr = (E_k)**2
E_k_sqr = (sigma_k_f)**2 * (1 - sum(W_ki * mu_ki_f))
# =======================================================================================


# =======================================================================================
# Py version of DIVA and Xie and Xiong 2011




quit()


# Leave ploting for later ------------------------------------------------------------------

# # Design figure
# # ================================================================
# xsize = 20
# ysize = 10

# fig = plt.figure(figsize=(xsize,ysize))
# # fig, ax = plt.subplots(figsize=(xsize, ysize))
# # ================================================================

# m = Basemap(projection='gall',
#             llcrnrlon=80.125,              # lower-left corner longitude
#             llcrnrlat=-24.875,               # lower-left corner latitude
#             urcrnrlon=179.875,               # upper-right corner longitude
#             urcrnrlat=25.125,               # upper-right corner latitude
#             resolution='i',
#             area_thresh=100.0,
#             )


# # # Create regular grid from TRMM lon/lat
# xi, yi = np.meshgrid(lons, lats)
# xnew, ynew = m(xi, yi)

# # Create grid from stations data:
# xstat, ystat = m(lon, lat)


# # # Interpolation
# # # =============================================================================
# # # Radial Basis Function

# # Set up few interolation parameters, this also affects the plot title
# #
# # interpolation='linear'
# interpolation = 'thin_plate'
# # interpolation = 'cubic'

# # Comment line below to TURN drizzle ON
# # drizzle = 'OFF'       # Trick to make rr*2 ln(rr) = 0
# drizzle = 'ON'        # Keep rain in range 0-1mm in the spline


# # Switch for 0-1mm/day range filtering to do log smoothing:
# # ----------------------------------------------------------
# if drizzle == 'OFF':
#     rr[rr <= 1.0] = 1.0        # Trick to make rr*2 ln(rr) = 0
# elif drizzle == 'ON':
#     rr == rr
# # ----------------------------------------------------------


# # For Thin Plate spline input data is pre and post-processed:
# # 1. Square root the data
# # 2. TPS run
# # 3. Square the data

# rr = np.sqrt(rr)


# smoothing_vals = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 40, 50, 100]
# # smoothing_vals = ['automatic']


# for smoothing_val in smoothing_vals:
#       print 'Now smoothing with parameter set to: ', smoothing_val

#       # # Now interpolate with prescribed smoothing parameter (lambda)
#       rbf = scipy.interpolate.Rbf(lon, lat, rr, function=interpolation, smooth=smoothing_val)
#       # Interpolate with automatic smoothing parameter selection
#       # rbf = scipy.interpolate.Rbf(lon, lat, rr, function=interpolation)

#       rri = rbf(xi, yi)

#       # Now square all processed precip back (normalize precip matrix too)
#       rri=rri*rri

#       print rri
#       # quit()

#       # Actual plotting ----------------------------------------------------------

#       # Plot Interpolation
#       # im = m.pcolor(xnew, ynew, rri*trmm_lsmask, cmap=cm.Blues, zorder=1)
#       im = m.pcolor(xnew, ynew, rri, cmap=cm.Blues, zorder=1)
#       # Plot Stations
#       scat_plot = m.scatter(xstat, ystat, 50, c=rr, cmap=cm.cool, zorder=2)

#       # ---------------------------------------------------------------------------

#       # Color bar properties ---------------------------------------
#       # Color plot
#       im.set_clim(0.0, 15.0)  # affects colorbar range too

#       # Scatter plot
#       scat_plot.set_clim(0.0, 15.0)  # affects colorbar range too
#       # ------------------------------------------------------------


#       # # Range of axis
#       # plt.xlim([80.125, 179.875])
#       # plt.ylim([-24.875, 25.125])


#       # draw coastlines, country boundaries, fill continents.
#       m.drawcoastlines(linewidth=0.75)
#       m.drawcountries(linewidth=0.75)
#       # draw parallels
#       parallels = np.arange(-40., 40, 10.)
#       m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
#       # draw meridians
#       meridians = np.arange(80., 180., 10.)
#       m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)

#       # m.drawlsmask(land_color="#ddaa66",
#       #              ocean_color="#7777ff",
#       #              resolution='l')


#       # # -- Colorbar 1 | bottom | interpolated
#       cb1 = m.colorbar(im,
#                        location='bottom',
#                        label='Interpolated stations precip'
#                        # fontsize='14'
#                        )
#                        # location='right'
#                        # cax=position
#                        # )
#                        # orientation='vertical',
#                        # ticks=[0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0])


#       # # -- Colorbar 2 | right | stations
#       cb2 = m.colorbar(scat_plot,
#                        # orientation='horizontal',
#                        label='Station values'
#                        # fraction=0.046,
#                        # pad=0.04,
#                        )

      # plt.show()


      # plt.close(fig)

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
