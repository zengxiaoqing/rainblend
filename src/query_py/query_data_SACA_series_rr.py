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
# f3=open('/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_year2015.dat', 'w+')


cnx = mysql.connector.connect(user='igor', database='didah', host='localhost', password='adelante')
cursor = cnx.cursor()

# Parameters

year_list=[1947, 1948, 1949, 1950,
           1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960,
           1961, 1962, 1963, 1964, 1966, 1966, 1967, 1968, 1969, 1970,
           1971, 1972, 1973, 1974, 1977, 1977, 1977, 1978, 1979, 1980,
           1981, 1982, 1983, 1984, 1988, 1986, 1987, 1988, 1989, 1990,
           1991, 1992, 1993, 1994, 1999, 1996, 1997, 1998, 1999, 2000,
           2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
           2011, 2012, 2013, 2014, 2015, 2016]


for year in year_list:

  f3=open('/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_year'
          +str(year)+'.dat', 'w+')

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
           # "WHERE ser_date LIKE '1947%' AND "
           "WHERE ser_date LIKE %s AND "
           "lat BETWEEN %s AND %s "
           "AND lon BETWEEN %s AND %s "
           "AND series_rr.ser_id=series.ser_id "
           "AND series.sta_id=stations.sta_id")


# >>> filenames=['file1', 'file2']
# >>> query = "SELECT version,name FROM data2.files WHERE name IN ('%s')" % "','".join(filenames)
# >>> print query
# SELECT version,name FROM data2.files WHERE name IN ('file1','file2')
# >>>


  # Database lat/lon units from db are in seconds. Divide by 3600. to convert decimal degrees.
  #
  # SACA coordinates
  lat_min = -89550  # -24.875
  lat_max = 90450   # 25.125

  lon_min = 288450  # 80.125
  lon_max = 647550  # 179.875

  # years=year
  years=tuple(year_list)


  # # Test coordinates
  # lat_min = 35550  # -24.875
  # lat_max = 90450   # 25.125

  # lon_min = 358450  # 80.125
  # lon_max = 647550  # 179.875



  # This defines which %s are going to be taken, and the order.
  # Lat condition only
  # cursor.execute(query, (lat_min, lat_max))
  # Lat & Lon condition
  cursor.execute(query, (lat_min, lat_max, lon_min, lon_max, years))


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
    
    lat=lat/3600.  # Convert to decimals
    lon=lon/3600.
    rr=rr/10.  # To be checked!

    print("{}, {}, {}, {}".format(
      ("%8.2f" % rr), ser_date, ("%8.3f" % lat), ("%8.3f" % lon)))

    
    # # Feed output array into a variable  
    # stations = str("{}".format(
    # 	name))


  # Print names of stations
    # print "Stations are: ", stations
    # ascii.write(stations, 'values.csv', format='csv', fast_writer=False)  
    
    # WRITE to FILE
    # f1.write("{}, {}, {}\n".format(name, lat/3600., lon/3600.))

    # WRITE to FILE
    # f3.write("{}, {}, {}, {}\n".format(rr, ser_date, lat/3600., lon/3600.))
    f3.write("{}, {}, {}, {}\n".format(("%8.2f" % rr), ser_date, ("%8.3f" % lat), ("%8.3f" % lon)))
  #==============================================================================


# f1.close()  # Close file
# f2.close()  # Close file
f3.close()  # Close file

cursor.close()
cnx.close()     # disconnect from database


# END

