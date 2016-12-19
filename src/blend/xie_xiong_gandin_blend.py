# -*- coding: utf-8 -*-
# pylint: disable=C0103

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
import numpy.ma as ma


print "I am pi from py: ", math.pi
print "And I am e from py: ", math.e


# Product function
# def prod(iterable):
#     """Iteration for calculating sums"""
#     return reduce(operator.mul, iterable, 1)

def square(n):
    """Square function"""
    return n**2


# TRMM bound
# ==========================================================================================
in_path = "/nobackup/users/stepanov/TRMM_data/nc/annual_files/cropped/land_only/"  # worksttion
# in_path = "/Users/istepanov/github/TRMM_blend/TRMM_nc/"                          # rMBP
in_path_lsmsk_TRMM = "/nobackup/users/stepanov/TRMM_data/Land_Sea_Mask/"
# ==========================================================================================


# Define paths to NC files
# ===========================================================================================
# TRMM file for SACA area, Land only
file_trmm = '3B42_daily.2000_georef_SACA_land_only.nc'       # work station
# file_trmm = '3b42-daily.2000-georef-saca-land-only.nc'     # rMBP
#
nc_trmm = Dataset(in_path + file_trmm, 'r')

# Extract the precip var &                        # TRMM: [latitude, longitude][201x400]
trmm_precip = nc_trmm.variables['r'][161, :, :]   # [time, lat, lon], 0= 01.01.2013 (python)
lons = nc_trmm.variables['longitude']
lats = nc_trmm.variables['latitude']

# OLD part where manual filtering so sea points was still needed. Now nc files
# pre filtered for sea points. Remove completely later.
# 
# Land Sea Maks TRMM specific
file_lsm_TRMM = 'TMPA_mask_georef_SACA_match_TRMM_grid.nc'
nc_lsmask_trmm = Dataset(in_path_lsmsk_TRMM + file_lsm_TRMM, 'r')
trmm_lsmask = nc_lsmask_trmm.variables['landseamask'][:, :]

# ============================================================================================

# Import data from ASCII CSV file
# ============================================================================================
#
gauges = np.genfromtxt("/usr/people/stepanov/github/TRMM_blend/ascii_out/"+
                       "saca_stations_query_series_rr_blended_derived_year2000-06-10.dat",
                       delimiter=',',
                       dtype=[('lat', float), ('lon', float), ('rr', float)],
                       usecols=(2, 3, 0),
                       missing_values=-9999,
                       usemask=True
                      )

# Make lat & lon easier to use down the line:
lat = gauges['lat']
lon = gauges['lon']
rr = gauges['rr']


# Land Sea mask from NASA ------------------
#
# All land points convert to 1
trmm_lsmask[trmm_lsmask != 100] = 1.
# All sea points convert to 0
# trmm_lsmask[trmm_lsmask == 100] = 0.0
# trmm_lsmask[trmm_lsmask == 100] = 9999
# trmm_lsmask[trmm_lsmask == 100] = np.NaN
trmm_lsmask[trmm_lsmask == 100] = None

# ------------------------------------------


# Design figure
# ==============================================================
xsize = 20
ysize = 10

fig = plt.figure(figsize=(xsize, ysize))
# fig, ax = plt.subplots(figsize=(xsize, ysize))

# Adjust margins
fig.subplots_adjust(left=0.04, right=0.96, top=0.98, bottom=0.02)
# ==============================================================

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

# Create GRID from STATIONS data:
xstat, ystat = m(lon, lat)

# Interpolation
# ==============================================================
# Radial Basis Function

# interpolation = 'linear'
# interpolation = 'thin_plate'
# interpolation = 'cubic'
# interpolation = 'multiquadric'
interpolation = 'inverse'          # Inverse of multiquadric

# Comment line below to TURN drizzle ON ------------------------
# drizzle = 'OFF'       # Trick to make rr*2 ln(rr) = 0
drizzle = 'ON'          # Keep rain in range 0-1mm in the spline


# Switch for 0-1MM/DAY range filtering to do log smoothing:
# ---------------------------------------------------------
if drizzle == 'OFF':
    rr[rr <= 1.0] = 1.0     # Trick to make rr*2 ln(rr) = 0
# elif drizzle == 'ON':
    # rr == rr
# ---------------------------------------------------------

# Thin Plate spline input is pre and post-processed in this way:
# 1. Square root the data
# 2. TPS run
# 3. Square the data

rr = np.sqrt(rr)

# Lists of interpolation parameters ----------------------------
# epsilon_list = [1]                # Factor for gaussian or multiquadratics funcs only
epsilon_list = [1, 10, 100]       # 100 does not work for smoothing above 4
# epsilon_list = ['automatic']
smoothing_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 40, 50, 100]
# smoothing_vals = [1]
# smoothing_vals = ['automatic']  # This usually picks zero
# ---------------------------------------------------------

# Loop through EPSILON and SMOOTHING lists
#
for epsilon_val in epsilon_list:

    for smoothing_val in smoothing_vals:
        print 'Now smoothing with parameter set to: ', smoothing_val
        print 'Now setting epsilon parameter to: ', epsilon_val

        # Interpolate with prescribed smoothing parameter
        rbf = scipy.interpolate.Rbf(lon, lat, rr,
                                    function=interpolation,
                                    smooth=smoothing_val,
                                    epsilon=epsilon_val
                                   )

        rri = rbf(xi, yi)

        # Now square all processed precip back (normalize precip matrix too)
        rri = square(rri)

        # print 'Interpolated station precip is: ', rri

    # Apply TRMM Land-Sea mask to the rain gauge station analysis:
        rri_analysis = rri * trmm_lsmask
    # Remove NaN values from analysis (no need to  with trmm mask later any more)
        rri_final = ma.array(rri_analysis, mask=np.isnan(rri_analysis))


# Intellective objective analysis --------------------------------------------------

# Deriving weights =========================
# ---> Optimal weight matrix via Kalnay manual, Xie paper and Ganding book

    # Fixed Optimum Interpolation weight
        Wght_static = 4.75

    # Geospatial calibration of station data to TRMM grid (weights free)

        # F0 = G0 + (Fi - Gi)
        # RRo = trmm_precip + Wght_static * (rri - trmm_precip)

        # print 'Blended precip is: ', RRo

# ==========================================

    # Dynamic Optimum Interpolation weight
    # Most important is to quantify 3 errors here
    # ------------------------------------------------------------------------------

    # Satellite retrieval error (calibrated to stations in China)
        Sig_f = 2.93 + 9.845 * trmm_precip

    # Rain gauge error est: ----------------
        # params:

    # temp
        N_g0 = 5                                # Temporarily
        N_g1 = 7                                # Temporarily
        N_g2 = 9                                # Temporarily

        N_eg = N_g0 + N_g1 / 8. + N_g2 / 32.    # Number of equivalent gauges
        N_eg_stat = 20                          # Number of equivalent gauges
        h0 = 60.0                               # E-folding distance
        h = 100.0                               # Temporarily

        Mij_o = 1  # i=j
        Mij_o = 0  # i!=j                       # convert later to IF statement

    # Rain gauge error:
        Sig_o = 0.15 + 4.09 * rri_analysis / (N_eg_stat)

    # Satellite error correlation at two separated grid boxes
        Mij_f = -0.025 + 1.196*(math.e**-h / h0)
        Mi_o = Mij_o                            # Temporarily
        Mi_f = Mij_f                            # Temporarily

    # Combined params:
        lambda_i = Sig_o / Sig_f
        lambda_j = Sig_o / Sig_f  # to change

        # Equation to solve for dynamic weights:
        # Mki_f = sum(Mi_f + Mi_o * lambda_i * lambda_j) * W_kj  # W_kj is the weight to derive
        # W_kj = Mij_f / sum(Mi_f + Mi_o * lambda_i * lambda_j)   # With sum
        W_kj = Mij_f / (Mi_f + Mi_o * lambda_i * lambda_j)     # Without sum

        Wght_dyn = W_kj
# ---------------------------------------------------------------------------------------

    # Geospatial calibration of station data to TRMM grid (weights free)

        # F0 = G0 + (Fi - Gi)
        # RRo = trmm_precip + Wght_dyn * (rri_analysis - trmm_precip)  # Before isnan removal
        RRo = trmm_precip + Wght_dyn * (rri_final - trmm_precip)       # After isnan removal
        # RRo = trmm_precip + Wght_static * (rri_final - trmm_precip)

        # print 'Blended precip is: ', RRo

# ---------------------------------------------------------------------------------------

    # Control of derived arguments in dynamic weights derivation
        # -------------------------------
        log_file_1 = open('logs/Sig_o_xie_blended_spline_smoothin_eq_'
                          + interpolation
                          + '_spline_smoothin_eq_' + str(smoothing_val)
                          + '_epsilon_' + str(epsilon_val) + '.log', 'w+')
        log_file_2 = open('logs/Sig_f_xie_blended_spline_smoothin_eq_'
                          + interpolation
                          + '_spline_smoothin_eq_' + str(smoothing_val)
                          + '_epsilon_' + str(epsilon_val) + '.log', 'w+')
        log_file_3 = open('logs/Lambda_i_xie_blended_spline_smoothin_eq_'
                          + interpolation
                          + '_spline_smoothin_eq_' + str(smoothing_val)
                          + '_epsilon_' + str(epsilon_val) + '.log', 'w+')
        log_file_4 = open('logs/Lambda_j_xie_blended_spline_smoothin_eq_'
                          + interpolation
                          + '_spline_smoothin_eq_' + str(smoothing_val)
                          + '_epsilon_' + str(epsilon_val) + '.log', 'w+')
        log_file_5 = open('logs/Weights_final_xie_blended_spline_smoothin_eq_'
                          + interpolation
                          + '_spline_smoothin_eq_' + str(smoothing_val)
                          + '_epsilon_' + str(epsilon_val) + '.log', 'w+')
        log_file_6 = open('logs/Mij_f_xie_blended_spline_smoothin_eq_'
                          + interpolation
                          + '_spline_smoothin_eq_' + str(smoothing_val)
                          + '_epsilon_' + str(epsilon_val) + '.log', 'w+')

        # Gridded fields
        log_file_7 = open('logs/Trmm_precip_spline_smoothin_eq_'
                          + interpolation
                          + '_spline_smoothin_eq_' + str(smoothing_val)
                          + '_epsilon_' + str(epsilon_val) + '.log', 'w+')
        log_file_8 = open('logs/rg_anal_precip_spline_smoothin_eq_'
                          + interpolation
                          + '_spline_smoothin_eq_' + str(smoothing_val)
                          + '_epsilon_' + str(epsilon_val) + '.log', 'w+')
        log_file_9 = open('logs/blended_precip_spline_smoothin_eq_'
                          + interpolation
                          + '_spline_smoothin_eq_' + str(smoothing_val)
                          + '_epsilon_' + str(epsilon_val) + '.log', 'w+')

    # Write derived parameres into files:
        # -------------------------------
        print >>log_file_1, 'This is Sig_o coefficient:', Sig_o
        print >>log_file_2, 'This is Sig_f coefficient:', Sig_f
        print >>log_file_3, 'This is lambda_i coefficient:', lambda_i
        print >>log_file_4, 'This is lambda_j coefficient:', lambda_j
        print >>log_file_5, 'This is final weight coefficient:', Wght_dyn
        print >>log_file_6, 'This is Mij_f weight coefficient:', Mij_f
        # Gridded fields
        print >>log_file_7, 'TRMM precip is: ', trmm_precip
        print >>log_file_8, 'Raingauge precip w/o NaNs is: ', rri_final
        print >>log_file_9, 'Blended precip is: ', RRo


        # quit()

# ==========================================

# Plotting -----------------------------------------------------------------------------------

    # Plot Interpolated fiedld (analysis)
        # im = m.pcolor(xnew, ynew, rri*trmm_lsmask, cmap=cm.Blues, zorder=1)
        # im = m.pcolor(xnew, ynew, RRo, cmap=cm.Blues, zorder=1)                # Blue cmap
        # im = m.pcolor(xnew, ynew, RRo, cmap=cm.rainbow_r, zorder=1)            # Stations cmap
        # im = m.pcolor(xnew, ynew, trmm_precip, cmap=cm.rainbow_r, zorder=1)    # Pure TRMM
        # im = m.pcolor(xnew, ynew, 100*Sig_o, cmap=cm.rainbow_r, zorder=1)   
        # im = m.pcolor(xnew, ynew, rri_analysis, cmap=cm.rainbow_r, zorder=1)  
        # im = m.pcolor(xnew, ynew, rri, cmap=cm.rainbow_r, zorder=1)  
        # im = m.pcolor(xnew, ynew, rri*trmm_lsmask, cmap=cm.rainbow_r, zorder=1) 
        # im = m.pcolor(xnew, ynew, trmm_lsmask, cmap=cm.rainbow_r, zorder=1)  
        # im = m.pcolor(xnew, ynew, rri_final, cmap=cm.rainbow_r, zorder=1)      # Final rg anal
        im = m.pcolor(xnew, ynew, RRo, cmap=cm.rainbow_r, zorder=1)        # Blend

        # Plot Stations
        # scat_plot = m.scatter(xstat, ystat, 50, c=rr, cmap=cm.cool, zorder=2)
        scat_plot = m.scatter(xstat, ystat, 50, c=rr, cmap=cm.Blues, zorder=2)
    # --------------------------------------------------------------------

# Color bar properties
    # Color plot
        im.set_clim(0.0, 5.0)  # affects colorbar range too

    # Scatter plot
        scat_plot.set_clim(0.0, 10.0)
    # --------------------------------------------------------------------

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


# -- Colorbar 1 | bottom | interpolated
        cb1 = m.colorbar(im,
                         location='bottom',
                         label='Interpolated stations precip'
                         # fontsize='14'
                         # location='right'
                         # cax=position
                         # orientation='vertical',
                         # ticks=[0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0,
                         # 35.0, 40.0, 45.0, 50.0, 55.0, 60.0])
                        )

# -- Colorbar 2 | right | stations
        cb2 = m.colorbar(scat_plot,
                         label='Station values'
                         # orientation='horizontal',
                         # fraction=0.046,
                         # pad=0.04,
                        )

        # plt.show()

# Save as PNG

        plt.savefig('plots/Precip_blend_dynamic_weight_' + interpolation + 
                    '_spline_smoothin_eq_' + str(smoothing_val) + '_epsilon_' +
                    str(epsilon_val) + '_drizzle_' +
                    drizzle + '_20000610.png',
                    bbox_inches='tight',
                    optimize=True,
                    quality=85,
                    dpi=300)

        # plt.savefig('plots/test_gridd_errors.png',
        #             # bbox_inches='tight',
        #             optimize=True,
        #             quality=85,
        #             dpi=300)
    # --------------------------------------------------------------------

quit()
