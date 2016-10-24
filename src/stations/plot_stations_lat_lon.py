import csv

with open('../../ascii_out/saca_stations_query_series_rr_year1947.dat', 'rt') as f:
  reader = csv.reader(f, delimiter=' ', skipinitialspace=True)

  lineData = list()

  cols = next(reader)
  print(cols)


