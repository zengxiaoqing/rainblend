from datetime import datetime

currentdate = datetime.date(2006,1,1)
enddate = datetime.date(2006,1,19)
while currentdate <= enddate:
   print currentdate
   currentdate += datetime.timedelta(days=1)