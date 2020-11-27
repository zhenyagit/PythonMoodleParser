import datetime
import datetime as dt
import pytz

dtime = dt.datetime.now(pytz.timezone('Antarctica/Davis'))
time = dt.datetime.now()
print(dtime)
print(time)