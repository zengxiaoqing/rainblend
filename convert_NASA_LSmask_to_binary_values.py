# Python script to convert NASA's TRMM Land Sea mask into binary file with 1=Land, 0=sea

# ==========================================
# Author: I.Stepanov (igor.stepanov@knmi.nl)
# 16.08.2016 @KNMI
# ==========================================

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


in_path_lsmsk_TRMM="/nobackup/users/stepanov/TRMM_data/Land_Sea_Mask/"

out_path="/nobackup/users/stepanov/TRMM_data/Land_Sea_Mask/"


# Files
#===========================================================================================

# Precip TRMM
# file_name='3B42_daily.2014_georef_SACA.nc'    

# Land Sea Maks TRMM specific
file_lsm_TRMM='TMPA_mask_georef_SACA_match_TRMM_grid.nc'


# Precip and elevation (Land Sea Mask)
# nc_trmm        = Dataset(in_path+file_name,'r')                  # [latitude, longitude][201x400]
nc_lsmask_trmm = Dataset(in_path_lsmsk_TRMM+file_lsm_TRMM,'r')   # [lat,lon][201x400]

trmm_lsmask = nc_lsmask_trmm.variables['landseamask'][:,:] # [time, latitude, longitude]   

print trmm_lsmask

quit()