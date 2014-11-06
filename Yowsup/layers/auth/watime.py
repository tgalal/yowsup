import time,datetime,re
try:
    from dateutil import tz
except ImportError:
    from .dateutil import tz

class WATime():
    def parseIso(self,iso):
        d=datetime.datetime(*map(int, re.split('[^\d]', iso)[:-1]))
        return d
        
    def utcToLocal(self,dt):
        utc = tz.gettz('UTC');
        local = tz.tzlocal()
        dtUtc =  dt.replace(tzinfo=utc);
        
        return dtUtc.astimezone(local)

    def utcTimestamp(self):
        #utc = tz.gettz('UTC')
        utcNow = datetime.datetime.utcnow()
        return self.datetimeToTimestamp(utcNow)
    
    def datetimeToTimestamp(self,dt):
        return time.mktime(dt.timetuple());