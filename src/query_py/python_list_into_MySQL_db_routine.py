import datetime
import mysql.connector
import os
from astropy.io import ascii



for n in range(0,75):
  cursor.execute("SELECT row FROM table WHERE column = %s ORDER BY column ASC", (n))
  result = cursor.fetchall()
  List = list()
  for t in result:
    List.append(int(t[0]))
  List = ",".join(map(str,List))
  ListUpdate = cursor.execute("UPDATE table SET column = %s WHERE column = %s", (str(List),n))

