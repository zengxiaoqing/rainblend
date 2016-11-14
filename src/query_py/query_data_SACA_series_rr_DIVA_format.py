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
# Query data only for DIVA interface: lat | lon | rr
# ============================================================================================


import datetime
import mysql.connector
import os
import numpy as np
# from astropy.io import ascii


class NumpyMySQLConverter(mysql.connector.conversion.MySQLConverter):
    """ A mysql.connector Converter that handles Numpy types """

    def _float32_to_mysql(self, value):
        return float(value)

    def _float64_to_mysql(self, value):
        return str(value)

    def _int32_to_mysql(self, value):
        return int(value)

    def _int64_to_mysql(self, value):
        return str(value)

config = {
    'user'    : 'igor',
    'host'    : 'localhost',
    'password': 'adelante',
    'database': 'didah'
}


cnx = mysql.connector.connect(**config)
cnx.set_converter_class(NumpyMySQLConverter)


# Open file which will store query output:
# f1=open('/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_wmostations.dat', 'w+')
# f2=open('/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr.dat', 'w+')


# cnx = mysql.connector.connect(user='igor', database='didah', host='localhost', password='adelante')
cursor = cnx.cursor()


# Parameters


# Datetime construction
# -----------------------------------------------------------------------
datetest=str(datetime.date(2008, 11, 22))

print
print 'new date should be in format 2008-11-22: ', datetest


# year_list=['1947%', '1948%', '1949%', '1950%']
# year_list=['1951%', '1952%', '1953%', '1954%', '1955%', '1956%', '1957%', '1958%', '1959%', '1960%']
# year_list=['1961%', '1962%', '1963%', '1964%', '1965%', '1966%', '1967%', '1968%', '1969%', '1970%']
# year_list=['1971%', '1972%', '1973%', '1974%', '1975%', '1976%', '1977%', '1978%', '1979%', '1980%']
# year_list=['1981%', '1982%', '1983%', '1984%', '1985%', '1986%', '1987%', '1988%', '1989%', '1990%']
# year_list=['1991%', '1992%', '1993%', '1994%', '1995%', '1996%', '1997%', '1998%', '1999%', '2000%']
# year_list=['2001%', '2002%', '2003%', '2004%', '2005%', '2006%', '2007%', '2008%', '2009%', '2010%']
# year_list=['2011%', '2012%', '2013%', '2014%', '2015%', '2016%']

# Individual year:
# year_list=['2000%']

# Single day
year_list=['2000-06-10']


# Loop for every year in database
# =====================================================
# for year in year_list_arange:
# for year in year_list:
for year in year_list:

  # f3=open('/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_year'
  #         +(str(year)[0:4])+'.dat', 'w+')

  # f3=open('/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_year'
  #         +(str(year)[0:4])+'.dat', 'w+')

  f3=open('/Users/istepanov/github/TRMM_blend/ascii_out/saca_stations_query_series_rr_blended_derived_DIVA_year'
          +(str(year))+'.dat', 'w+')


  # Bash queries
  #==============================================================================
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
  
  # # series_rr
  # # rr with lat and lon and date
  # query = ("SELECT rr, ser_date, lat, lon  FROM series_rr,series,stations "
  #          # "WHERE ser_date LIKE '1947%' AND "
  #          # "WHERE ser_date LIKE '%%%s%%' AND "
  #          # "WHERE ser_date LIKE %s AND "
  #          "WHERE ser_date LIKE %s "
  #          "AND lat BETWEEN %s AND %s "
  #          "AND lon BETWEEN %s AND %s "
  #          "AND series_rr.ser_id=series.ser_id "
  #          "AND series.sta_id=stations.sta_id")



  # series_rr_blended_mixed
  # rr with lat and lon and date
  query = ("SELECT series_rr_blended_mixed.rr AS rr, "
                  "series_rr_blended_mixed.ser_date AS ser_date, "
                  "stations.lat AS lat, "
                  "stations.lon AS lon, "
                  "stations.elev AS elev, "
                  "stations.wmocode AS wmocode, "
                  "stations.coun_id AS coun_id "
           "FROM series_rr_blended_mixed, stations "
                  "WHERE series_rr_blended_mixed.ser_date LIKE %s "
                  "AND series_rr_blended_mixed.sta_id=stations.sta_id "
                  "AND stations.lat BETWEEN %s AND %s "
                  "AND stations.lon BETWEEN %s AND %s")



  # # Richard extracting metadata from "series_blended_mixed_derived"
  # "SELECT series_blended_mixed_derived.sta_id AS id, "
  #         stations.name AS station, 
  #         country.name AS country, 
  #         stations.lat/3600 AS lat,
  #         stations.lon/3600 AS lon, 
  #         elev/10.0 AS elev 
  #           FROM series_blended_mixed_derived,stations,country  
  #             WHERE series_blended_mixed_derived.syn_kind='tx' AND
  #             series_blended_mixed_derived.sta_id=stations.sta_id AND
  #             stations.coun_id=country.coun_id""



  # Database lat/lon units from db are in seconds. Divide by 3600. to convert decimal degrees.
  #
  # SACA coordinates
  lat_min = -89550  # -24.875
  lat_max = 90450   # 25.125

  lon_min = 288450  # 80.125
  lon_max = 647550  # 179.875


  # Lat & Lon condition
  cursor.execute(query, (year, lat_min, lat_max, lon_min, lon_max))  # worked for myslq


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
  for (rr, ser_date, lat, lon, elev, wmocode, coun_id) in cursor:
    
    lat=lat/3600.          # Convert to decimals
    lon=lon/3600.

    if rr != -9999:
      rr=rr/10.            # To be confirmed!

    elev=elev/10.0  

    print("{}, {}, {}, {}, {}, {}".format(
      ("%8.2f" % rr), ("%12s" % ser_date), ("%8.3f" % lat), ("%8.3f" % lon), 
      ("%8.3f" % elev), ("%4s" % coun_id)))


    # Print names of stations
    # print "Stations are: ", stations
    # ascii.write(stations, 'values.csv', format='csv', fast_writer=False)  
  
    # WRITE to FILE
    # f3.write("{}, {}, {}, {}\n".format(rr, ser_date, lat/3600., lon/3600.))
    # f3.write("{}, {}, {}, {}\n".format(("%8.2f" % rr), ser_date, ("%8.3f" % lat), ("%8.3f" % lon)))

    # f3.write("{}, {}, {}, {}, {}\n".format(
    #   ("%8.2f" % rr), ("%12s" % ser_date), 
    #   ("%8.3f" % lat), ("%8.3f" % lon), 
    #   ("%8.3f" % elev)))

# Query data only for DIVA interface: lon | lat | rr
    f3.write("{}, {}, {}\n".format(
      ("%8.3f" % lon),
      ("%8.3f" % lat),
      ("%8.2f" % rr)))
  #==============================================================================


# f1.close()  # Close file
# f2.close()  # Close file
f3.close()      # Close file

cursor.close()
cnx.close()     # disconnect from database


quit()

# END

