import time,datetime,re, hashlib
from dateutil import tz
import os
from .constants import YowConstants
import codecs, sys


class HexTools:
    decode_hex = codecs.getdecoder("hex_codec")
    @staticmethod
    def decodeHex(hexString):
        result = HexTools.decode_hex(hexString)[0]
        if sys.version_info >= (3,0):
            result = result.decode('latin-1')
        return result

class WATools:
    @staticmethod
    def processIdentity(identifier):
        try:
            identifier.index(":")
            identifier = identifier.upper()
            identifier = identifier + identifier

        except:
            identifier = identifier[::-1]

        digest = hashlib.md5(identifier.encode("utf-8"))
        return digest.hexdigest()

class StorageTools:
    @staticmethod
    def constructPath(*path):
        path = os.path.join(*path)
        fullPath = os.path.expanduser(os.path.join(YowConstants.PATH_STORAGE, path))
        if not os.path.exists(os.path.dirname(fullPath)):
            os.makedirs(os.path.dirname(fullPath))
        return fullPath


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