import time,datetime,re, hashlib
from dateutil import tz
import os
from .constants import YowConstants
import codecs, sys
import logging
import tempfile
import base64
import hashlib
import json

logger = logging.getLogger(__name__)

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
    def generateIdentity():
        return os.urandom(20)

    @staticmethod
    def getFileHashForUpload(filePath):
        sha1 = hashlib.sha256()
        f = open(filePath, 'rb')
        try:
            sha1.update(f.read())
        finally:
            f.close()
        b64Hash = base64.b64encode(sha1.digest())
        return b64Hash if type(b64Hash) is str else b64Hash.decode()

class StorageTools:
    @staticmethod
    def constructPath(*path):
        path = os.path.join(*path)
        fullPath = os.path.expanduser(os.path.join(YowConstants.PATH_STORAGE, path))
        if not os.path.exists(os.path.dirname(fullPath)):
            os.makedirs(os.path.dirname(fullPath))
        return fullPath

    @staticmethod
    def getStorageForPhone(phone):
        return StorageTools.constructPath(phone + '/')

    @staticmethod
    def writeIdentity(phone, identity):
        path = StorageTools.getStorageForPhone(phone)
        with open(os.path.join(path, "id"), 'wb') as idFile:
            idFile.write(identity)

    @staticmethod
    def getIdentity(phone):
        path = StorageTools.getStorageForPhone(phone)
        out = None
        idPath = os.path.join(path, "id")
        if os.path.isfile(idPath):
            with open(idPath, 'rb') as idFile:
                out = idFile.read()
        return out

    @staticmethod
    def writeNonce(phone, nonce):
        path = StorageTools.getStorageForPhone(phone)
        with open(os.path.join(path, "nonce"), 'wb') as idFile:
            idFile.write(nonce.encode("latin-1") if sys.version_info >= (3,0) else nonce)

    @staticmethod
    def getNonce(phone):
        path = StorageTools.getStorageForPhone(phone)
        out = None
        noncePath = os.path.join(path, "nonce")
        if os.path.isfile(noncePath):
            with open(noncePath, 'rb') as idFile:
                out = idFile.read()
        return out

class TimeTools:
    @staticmethod
    def parseIso(iso):
        d=datetime.datetime(*map(int, re.split('[^\d]', iso)[:-1]))
        return d
    
    @staticmethod 
    def utcToLocal(dt):
        utc = tz.gettz('UTC')
        local = tz.tzlocal()
        dtUtc =  dt.replace(tzinfo=utc)
        
        return dtUtc.astimezone(local)

    @staticmethod
    def utcTimestamp():
        #utc = tz.gettz('UTC')
        utcNow = datetime.datetime.utcnow()
        return TimeTools.datetimeToTimestamp(utcNow)

    @staticmethod
    def datetimeToTimestamp(dt):
        return time.mktime(dt.timetuple())


class ModuleTools:
    @staticmethod
    def INSTALLED_PIL():
        try:
            import PIL
            return True
        except ImportError:
            return False

    @staticmethod
    def which(file):
        for path in os.environ["PATH"].split(":"):
            if os.path.exists(path + "/" + file):
                    return path + "/" + file
        return None

class ImageTools:

    @staticmethod
    def scaleImage(infile, outfile, imageFormat, width, height):
        if ModuleTools.INSTALLED_PIL():
            from PIL import Image
            im = Image.open(infile)
            im.thumbnail((width, height))
            im.save(outfile, imageFormat)
            return True
        else:
            logger.warn("Python PIL library not installed")
            return False


    @staticmethod
    def getImageDimensions(imageFile):
        if ModuleTools.INSTALLED_PIL():
            from PIL import Image
            im = Image.open(imageFile)
            return im.size
        else:
            logger.warn("Python PIL library not installed")

    @staticmethod
    def generatePreviewFromImage(image):
        fd, path = tempfile.mkstemp()
        fileObj = os.fdopen(fd, "rb+")
        preview = None
        if ImageTools.scaleImage(image, fileObj, "JPEG", YowConstants.PREVIEW_WIDTH, YowConstants.PREVIEW_HEIGHT):
            fileObj.seek(0)
            preview = fileObj.read()
        fileObj.close()
        return preview


class VideoTools:

    @staticmethod
    def getVideoFormat(video):
        if not os.path.isfile(video):
            return None

        if not ModuleTools.which('avprobe'):
            logger.warn("libav-tools not installed (only on linux)")
            return None

        if not os.path.isfile(video + '.info'):
            os.system('avprobe -of json -show_streams -show_format ' + video + ' > ' + video + '.info')

        if os.path.isfile(video + '.info'):
            with open(video + '.info', 'rb') as infoFile:
                return json.loads(infoFile.read())
        else:
            return None


    @staticmethod
    def generatePreviewFromVideo(video):
        if not os.path.isfile(video):
            return None

        if os.path.isfile(video + '.jpg'):
            with open(video + '.jpg', 'rb') as vidFile:
                return vidFile.read()

        if not ModuleTools.which('avconv'):
            logger.warn("libav not installed (only on linux)")
            return None

        #logger.debug('avconv -y -i ' + video + ' -vframes 1 ' + video + '.jpg')
        logger.debug(os.system('avconv -y -i ' + video + ' -vframes 1 ' + video + '.jpg'))

        if os.path.isfile(video + '.jpg'):
            with open(video + '.jpg', 'rb') as vidFile:
                return vidFile.read()
        else:
            logger.warn("Can't find preview video output file")
            return None

