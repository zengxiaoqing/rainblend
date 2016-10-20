# Make python script executable
#!/usr/bin/python

# Location of this script:
# /Users/istepanov/github/TRMM_blend/query_data_SACA_series_rr.py

# What script does?
# Makes MySQL queries from didah database and selects stations in SACA region

# ==========================================
# Author: I.Stepanov (igor.stepanov@knmi.nl)
# 19.10.2016 @KNMI
# ============================================================================================
# Updates list
# 
# ============================================================================================


import datetime
import mysql.connector
import os
from astropy.io import ascii


# Open file which will store query output:
f1=open('/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr.dat', 'w+')


cnx = mysql.connector.connect(user='igor', database='didah', host='localhost', password='adelante')
cursor = cnx.cursor()


# Bash query
query = ("SELECT name, lat, lon FROM wmostations,series_rr "
         "WHERE lat BETWEEN %s AND %s "
         "AND lon BETWEEN %s AND %s")


# Database lat/lon units from db are in seconds. Divide by 3600. to convert decimal degrees.
#
lat_min = -89550  # -24.875
lat_max = 90450   # 25.125

lon_min = 288450  # 80.125
lon_max = 647550  # 179.875


# Lat condition only
# cursor.execute(query, (lat_min, lat_max))
# Lat & Lon condition
cursor.execute(query, (lat_min, lat_max,lon_min,lon_max))


#==============================================================================
# Loop over station name, latitude & longitude
for (name, lat, lon) in cursor:

  print("{}, {}, {}".format(
    name, lat/3600., lat/3600.))
  
  # Feed output array into a variable  
  stations = str("{}".format(
  	name))


# Print names of stations
  # print "Stations are: ", stations
  # ascii.write(stations, 'values.csv', format='csv', fast_writer=False)  
  
  # WRITE to FILE
  f1.write("{}, {}, {}\n".format(name, lat/3600., lon/3600.))
#==============================================================================


f1.close()  # Close file

cursor.close()
cnx.close()


# END

