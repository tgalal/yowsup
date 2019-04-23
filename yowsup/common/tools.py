import os
from .constants import YowConstants
import codecs, sys
import logging
import tempfile
import base64
import hashlib
import os.path, mimetypes
import uuid
from consonance.structs.keypair import KeyPair
from appdirs import user_config_dir

from .optionalmodules import PILOptionalModule, FFVideoOptionalModule

logger = logging.getLogger(__name__)

class Jid:
    @staticmethod
    def normalize(number):
        if '@' in number:
            return number
        elif "-" in number:
            return "%s@%s" % (number, YowConstants.WHATSAPP_GROUP_SERVER)
        return "%s@%s" % (number, YowConstants.WHATSAPP_SERVER)

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

    @classmethod
    def generatePhoneId(cls):
        """
        :return:
        :rtype: str
        """
        return str(cls.generateUUID())

    @classmethod
    def generateDeviceId(cls):
        """
        :return:
        :rtype: bytes
        """
        return cls.generateUUID().bytes

    @classmethod
    def generateUUID(cls):
        """
        :return:
        :rtype: uuid.UUID
        """
        return uuid.uuid4()

    @classmethod
    def generateKeyPair(cls):
        """
        :return:
        :rtype: KeyPair
        """
        return KeyPair.generate()

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
    NAME_CONFIG = "config.json"

    @staticmethod
    def constructPath(*path):
        path = os.path.join(*path)
        fullPath = os.path.join(user_config_dir(YowConstants.YOWSUP), path)
        if not os.path.exists(os.path.dirname(fullPath)):
            os.makedirs(os.path.dirname(fullPath))
        return fullPath

    @staticmethod
    def getStorageForPhone(phone):
        if type(phone) is not str:
            phone = str(phone)
        return StorageTools.constructPath(phone + '/')

    @staticmethod
    def writePhoneData(phone, name, val):
        logger.debug("writePhoneData(phone=%s, name=%s, val=[omitted])" % (phone, name))
        path = os.path.join(StorageTools.getStorageForPhone(phone), name)
        logger.debug("Writing %s" % path)

        with open(path, 'w' if type(val) is str else 'wb') as attrFile:
            attrFile.write(val)

    @staticmethod
    def readPhoneData(phone, name, default=None):
        logger.debug("readPhoneData(phone=%s, name=%s)" % (phone, name))
        path = StorageTools.getStorageForPhone(phone)
        dataFilePath = os.path.join(path, name)
        if os.path.isfile(dataFilePath):
            logger.debug("Reading %s" % dataFilePath)
            with open(dataFilePath, 'rb') as attrFile:
                return attrFile.read()
        else:
            logger.debug("%s does not exist" % dataFilePath)

        return default

    @classmethod
    def writeIdentity(cls, phone, identity):
        cls.writePhoneData(phone, 'id', identity)

    @classmethod
    def getIdentity(cls, phone):
        return cls.readPhoneData(phone, 'id')

    @classmethod
    def writePhoneConfig(cls, phone, config):
        cls.writePhoneData(phone, cls.NAME_CONFIG, config)

    @classmethod
    def readPhoneConfig(cls, phone, config):
        return cls.readPhoneData(phone, cls.NAME_CONFIG)


class ImageTools:
    @staticmethod
    def scaleImage(infile, outfile, imageFormat, width, height):
        with PILOptionalModule() as imp:
            Image = imp("Image")
            im = Image.open(infile)
            #Convert P mode images
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.thumbnail((width, height))
            im.save(outfile, imageFormat)
            return True
        return False

    @staticmethod
    def getImageDimensions(imageFile):
        with PILOptionalModule() as imp:
            Image = imp("Image")
            im = Image.open(imageFile)
            return im.size

    @staticmethod
    def generatePreviewFromImage(image):
        fd, path = tempfile.mkstemp()

        preview = None
        if ImageTools.scaleImage(image, path, "JPEG", YowConstants.PREVIEW_WIDTH, YowConstants.PREVIEW_HEIGHT):
            fileObj = os.fdopen(fd, "rb+")
            fileObj.seek(0)
            preview = fileObj.read()
            fileObj.close()
        os.remove(path)
        return preview

class MimeTools:
    MIME_FILE = os.path.join(os.path.dirname(__file__), 'mime.types')
    mimetypes.init() # Load default mime.types
    try:
        mimetypes.init([MIME_FILE]) # Append whatsapp mime.types
    except exception as e:
        logger.warning("Mime types supported can't be read. System mimes will be used. Cause: " + e.message)

    @staticmethod
    def getMIME(filepath):
        mimeType = mimetypes.guess_type(filepath)[0]
        if mimeType is None:
            raise Exception("Unsupported/unrecognized file type for: "+filepath);
        return mimeType

class VideoTools:
    @staticmethod
    def getVideoProperties(videoFile):
        with FFVideoOptionalModule() as imp:
            VideoStream = imp("VideoStream")
            s = VideoStream(videoFile)
            return s.width, s.height, s.bitrate, s.duration #, s.codec_name

    @staticmethod
    def generatePreviewFromVideo(videoFile):
        with FFVideoOptionalModule() as imp:
            VideoStream = imp("VideoStream")
            fd, path = tempfile.mkstemp('.jpg')
            stream = VideoStream(videoFile)
            stream.get_frame_at_sec(0).image().save(path)
            preview = ImageTools.generatePreviewFromImage(path)
            os.remove(path)
            return preview
