import time,datetime,re
try:
    from dateutil import tz
except ImportError:
    from Yowsup.libs.dateutil import tz

class TimeTools:
    @staticmethod
    def parseIso(iso):
        d=datetime.datetime(*map(int, re.split('[^\d]', iso)[:-1]))
        return d
    
    @staticmethod 
    def utcToLocal(dt):
        utc = tz.gettz('UTC');
        local = tz.tzlocal()
        dtUtc =  dt.replace(tzinfo=utc);
        
        return dtUtc.astimezone(local)

    @staticmethod
    def utcTimestamp():
        #utc = tz.gettz('UTC')
        utcNow = datetime.datetime.utcnow()
        return TimeTools.datetimeToTimestamp(utcNow)
    
    @staticmethod
    def datetimeToTimestamp(dt):
        return time.mktime(dt.timetuple());