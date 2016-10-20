# Make python script executable
#!/usr/bin/python

# Where is this script?
# /Users/istepanov/github/TRMM_blend/query_data_SACA.py

# What script does?
# Makes MySQL queries from didah database and selects stations in SACA region

# ==========================================
# Author: I.Stepanov (igor.stepanov@knmi.nl)
# 01.08.2016 @KNMI (around this time)
# ============================================================================================
# Updates list
# 18.10.2016. 
# ============================================================================================


import datetime
import mysql.connector
import os
from astropy.io import ascii

# cwd = os.getcwd()


# Open file to store query output in
f1=open('/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query.dat', 'w+')


cnx = mysql.connector.connect(user='igor', database='didah', host='localhost', password='adelante')
cursor = cnx.cursor()

# This one works
# query = ("SELECT name, elev, lat FROM wmostations "
#          "WHERE lat BETWEEN %s AND %s")

# Now lets include lon too, this works!
# query = ("SELECT name, elev, lat FROM wmostations "
#          "WHERE lat BETWEEN %s AND %s "
#          "AND lon BETWEEN %s AND %s")

# Now lets include lon too, this works!
query = ("SELECT name, lat, lon FROM wmostations "
         "WHERE lat BETWEEN %s AND %s "
         "AND lon BETWEEN %s AND %s")



# query = ("SELECT name, elev, lat FROM wmostations "
#          "WHERE lat BETWEEN %s AND %s"
#          "OR WHERE lon BETWEEN %s AND %s")

# Database lat/lon units are in seconds. Divide by 3600 to convert decimal degrees
lat_min = -89550  # -24.875
lat_max = 90450   # 25.125

lon_min = 288450  # 80.125
lon_max = 647550  # 179.875

# This one works with lat only
# cursor.execute(query, (lat_min, lat_max))

cursor.execute(query, (lat_min, lat_max,lon_min,lon_max))

#cursor.execute(query, (lat_min, lat_max, lon_min, lon_max))

# This one works
#for (name, elev, lat) in cursor:
for (name, lat, lon) in cursor:
# for (name, elev, lat, lon) in cursor:
  print("{}, {}, {}".format(
  	name, lat/3600., lat/3600.))
# Feed output array into a variable  
  stations = str("{}".format(
  	name))
  # stations_list=stations.append('new_station')
  # stations.append('new_station')
  # mylists = {}

  # station1 = 'abhishek'
  # mylists[stations] = []
# Print name of stations directly as taken from the variable
  print "Stations are: ", stations
  # ascii.write(stations, 'values.csv', format='csv', fast_writer=False)  
  
  # Write to file
  # f1.write("{}, {}, {}\n".format(name, elev, lat/3600.))
  f1.write("{}, {}, {}\n".format(name, lat/3600., lon/3600.))

# print "Stations list is: ", mylists


f1.close()

cursor.close()
cnx.close()
