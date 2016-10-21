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
f1=open('/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_wmostations.dat', 'w+')
f2=open('/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr.dat', 'w+')
f3=open('/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_date.dat', 'w+')


cnx = mysql.connector.connect(user='igor', database='didah', host='localhost', password='adelante')
cursor = cnx.cursor()


# Bash query

# # wmostations
# query = ("SELECT name, lat, lon FROM wmostations "
#          "WHERE lat BETWEEN %s AND %s "
#          "AND lon BETWEEN %s AND %s")


# # rr with lat and lon
# query = ("SELECT rr, lat, lon  FROM series_rr,series,stations "
#          "WHERE lat BETWEEN %s AND %s "
#          "AND lon BETWEEN %s AND %s "
#          "AND series_rr.ser_id=series.ser_id "
#          "AND series.sta_id=stations.sta_id")
#          # "WHERE ser_date LIKE '%1996%'")


# rr with lat and lon and date
query = ("SELECT rr, ser_date, lat, lon  FROM series_rr,series,stations "
         "WHERE rr LIKE '%1%' AND "
         "WHERE lat BETWEEN %s AND %s "
         "AND lon BETWEEN %s AND %s "
         "AND series_rr.ser_id=series.ser_id "
         "AND series.sta_id=stations.sta_id")



# Database lat/lon units from db are in seconds. Divide by 3600. to convert decimal degrees.
#
# # SACA coordinates
# lat_min = -89550  # -24.875
# lat_max = 90450   # 25.125

# lon_min = 288450  # 80.125
# lon_max = 647550  # 179.875


# Test coordinates
lat_min = 75550  # -24.875
lat_max = 90450   # 25.125

lon_min = 358450  # 80.125
lon_max = 647550  # 179.875



# Lat condition only
# cursor.execute(query, (lat_min, lat_max))
# Lat & Lon condition
cursor.execute(query, (lat_min, lat_max,lon_min,lon_max))


#==============================================================================
# Loop over station name, latitude & longitude
# for (name, lat, lon) in cursor:

#   print("{}, {}, {}".format(
#     name, lat/3600., lat/3600.))


# # Loop over precip amount, latitude & longitude
# for (rr, lat, lon) in cursor:

#   print("{}, {}, {}".format(
#     rr, lat/3600., lat/3600.))


# Loop over precip amount, latitude & longitude and series date
for (rr, ser_date, lat, lon) in cursor:

  print("{}, {}, {}, {}".format(
    rr, ser_date, lat/3600., lat/3600.))

  
  # # Feed output array into a variable  
  # stations = str("{}".format(
  # 	name))


# Print names of stations
  # print "Stations are: ", stations
  # ascii.write(stations, 'values.csv', format='csv', fast_writer=False)  
  
  # WRITE to FILE
  # f1.write("{}, {}, {}\n".format(name, lat/3600., lon/3600.))

  # WRITE to FILE
  f3.write("{}, {}, {}, {}\n".format(rr, ser_date, lat/3600., lon/3600.))
#==============================================================================


# f1.close()  # Close file
# f2.close()  # Close file
f3.close()  # Close file

cursor.close()
cnx.close()


# END

