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


# ================================================================

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import string
import matplotlib
import matplotlib.cm as cm
import scipy.interpolate
# np.set_printoptions(threshold='nan')  # print full array
from matplotlib.mlab import griddata
from netCDF4 import Dataset
from matplotlib.colors import Normalize


# TRMM bound
# ==========================================================================================
in_path="/nobackup/users/stepanov/TRMM_data/nc/annual_files/cropped/land_only/"   # work station
# in_path="/Users/istepanov/github/TRMM_blend/TRMM_nc/"                           # rMBP
# ==========================================================================================


# Define paths to NC files
#===========================================================================================
# TRMM file for SACA area, Land only
file_trmm='3B42_daily.2000_georef_SACA_land_only.nc'  # work station
# 3b42-daily.2000-georef-saca-land-only.nc            # rMBP


# Precip and elevation
nc_trmm = Dataset(in_path+file_trmm,'r')   

# Extract the precip var
trmm_precip = nc_trmm.variables['r'][161,:,:]   # [time, lat, lon], 0= 01.01.2013 (python)


# Coordinates for TRMM: [latitude, longitude][201x400]
lons = nc_trmm.variables['longitude'] 
lats = nc_trmm.variables['latitude']
# ==========================================================================================



# Import data from ASCII CSV file 
# ==========================================================================================
#
#gauges = np.genfromtxt("/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_year2000-06-10.dat",
gauges = np.genfromtxt("/usr/people/stepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_year2000-06-10.dat",
                        delimiter=',', 
                        dtype=[('lat', np.float32), ('lon', np.float32), ('rr', np.float32)], 
                        usecols=(2, 3, 0))


# Make lat & lon easier to use down the line:
lat = gauges['lat']
lon = gauges['lon']
rr  = gauges['rr']

norm = Normalize()


# Filter out stations without measurements (-999.9)
# rr[rr == -9.99900000e+3] = np.nan
rr[rr == -9.99900000e+3] = 0.0
# ==========================================================================================



# Design figure
# ================================================================
xsize=20
ysize=10

# fig = plt.figure(figsize=(xsize,ysize))
fig, ax = plt.subplots(figsize=(xsize,ysize),dpi=100)
# ================================================================

m = Basemap(projection='gall',
            llcrnrlon = 80.125,              # lower-left corner longitude
            llcrnrlat = -24.875,               # lower-left corner latitude
            urcrnrlon = 179.875,               # upper-right corner longitude
            urcrnrlat = 25.125,               # upper-right corner latitude
            resolution = 'c',
            # area_thresh = 100.0,
            )


# # Create regular grid from TRMM lon/lat
xi, yi = np.meshgrid(lons, lats)
xnew, ynew = m(xi,yi)

# Alternative grid
lonst, latst = np.meshgrid(lons, lats)
x_trmm, y_trmm = m(lonst, latst)

# # Dealing witg NaNs
# vals = ~np.isnan(rr)

# # Interpolation
# # =============================================================================
# # Radial Basis Function
# rbf = scipy.interpolate.Rbf(lon, lat, rr, function='thin_plate', smooth=5)
# rri = rbf(xi, yi)


m.drawcoastlines(zorder=3)
m.drawcountries()
m.fillcontinents(color='gainsboro', zorder=1)
m.drawmapboundary(fill_color='steelblue')


# # Actual plotting
# im = ax.pcolor(xi, yi, rri, zorder=1)
# # im = ax.pcolor(xi, yi, trmm_precip, zorder=1)  # ok
# # im = ax.contourf(xnew, ynew, trmm_precip, zorder=1)
# plt.scatter(lon, lat, 50, rr, cmap=cm.cool, zorder=2)  # works

# im.set_clim(0.0,150.0)  # affects colorbar range too


# Range of axis 
plt.xlim([80.125,179.875])
plt.ylim([-24.875,25.125])





# New snippet to overlay basemap
# transform lon / lat coordinates to map projection
# data['projected_lon'], data['projected_lat'] = m(*(data.Lon.values, data.Lat.values))
proj_lon, proj_lat = m(lon, lat)

# grid data
# numcols, numrows = 1000, 1000
# xi = np.linspace(data['projected_lon'].min(), data['projected_lon'].max(), numcols)
# yi = np.linspace(data['projected_lat'].min(), data['projected_lat'].max(), numrows)
# xi, yi = np.meshgrid(xi, yi)
numcols, numrows = 100, 100
xi = np.linspace(proj_lon.min(), proj_lon.max(), numcols)
yi = np.linspace(proj_lat.min(), proj_lat.max(), numrows)
xi, yi = np.meshgrid(xi, yi)

# quit()

# interpolate
# x, y, z = data['projected_lon'].values, data['projected_lat'].values, data.Z.values
# zi = griddata(x, y, z, xi, yi)
rbf = scipy.interpolate.Rbf(proj_lon, proj_lat, rr, function='thin_plate', smooth=5)
rri = rbf(xi, yi)

# draw map details
m.drawmapboundary(fill_color = 'white')
m.fillcontinents(color='#C0C0C0', lake_color='#7093DB')
m.drawcountries(
    linewidth=.75, linestyle='solid', color='#000073',
    antialiased=True,
    ax=ax, zorder=3)


# define map extent
lllon = -24.875
lllat = 80.125
urlon = 179.875
urlat = 25.125

m.drawparallels(
    np.arange(lllat, urlat, 2.),
    color = 'black', linewidth = 0.5,
    labels=[True, False, False, False])
m.drawmeridians(
    np.arange(lllon, urlon, 2.),
    color = '0.25', linewidth = 0.5,
    labels=[False, False, False, True])

# contour plot
con = m.contourf(xi, yi, rri, zorder=4, alpha=0.6, cmap='RdPu')
# scatter plot
m.scatter(
    proj_lon,
    proj_lat,
    color='#545454',
    edgecolor='#ffffff',
    alpha=.75,
    s=50 * norm(rr),
    cmap='RdPu',
    ax=ax,
    vmin=rri.min(), vmax=rri.max(), zorder=4)
















# # -- Colorbar
# fig.colorbar(im)
cb = plt.colorbar(con)
# cb.set_clim(0.0,10.0)

# # cbar=fig.colorbar(im, ticks=[0.0,5.0,10.0])
# # cbar.set_clim(0.0, 10.0)
# # plt.clim(0,10)

plt.show()

# # Save as PNG
# plt.savefig('plots/Precip_TPspline_20000610.png', 
#             bbox_inches='tight', 
#             optimize=True,
#             quality=85,
#             dpi=30)


# plt.close(fig)

quit()

