import time,datetime,re, hashlib
import calendar
from dateutil import tz
import os
from .constants import YowConstants
import codecs, sys
import logging
import tempfile
import base64
import hashlib
import os.path, mimetypes
from .optionalmodules import PILOptionalModule, FFVideoOptionalModule
from preview_generator.manager import PreviewManager
import urllib.request
from PIL import Image
import os
import math

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
    @staticmethod
    def getFileHashForUpload2(filePath):
        sha1 = hashlib.sha256()
        f = open(filePath, 'rb')
        try:
            hash = hashlib.sha256(f.read()).hexdigest()
        finally:
            f.close()
        return hash

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
        utcNow = datetime.datetime.utcnow()
        return calendar.timegm(utcNow.timetuple())

    @staticmethod
    def datetimeToTimestamp(dt):
        return time.mktime(dt.timetuple())

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

class AudioTools:
    @staticmethod
    def getAudioProperties(audioFile):
        if ".ogg" in audioFile or ".mp3" in audioFile:
            import audioread
            with audioread.audio_open(audioFile) as f:
                return f.duration
        raise Exception("Unsupported/extension file type for: " + audioFile);

class DocumentTools:
    @staticmethod
    def getDocumentProperties(documentFile):
        if '.pdf' in documentFile:
           from PyPDF2 import PdfFileReader
           pdf = PdfFileReader(open(documentFile, 'rb'))
           return pdf.getNumPages()
        return 0

    @staticmethod
    def generatePreviewFromDocument(documentFile):
        preview = None

        manager = PreviewManager('/tmp/cache/', create_folder=True)
        path = manager.get_jpeg_preview(documentFile, height=YowConstants.PREVIEW_DOCUMENT_HEIGHT, width=YowConstants.PREVIEW_DOCUMENT_WIDTH)
        image = open(path, "rb+")
        preview = image.read()
        image.close()
        os.remove(path)
        return preview

class MapTools:
    @staticmethod
    def generatePreviewFromLatLong(latitute, longitude):
        preview = None
        try:
            # Get the high resolution image
            self.getXY(latitute, longitude, YowConstants.MAP_ZOOM)
            preview = self.generateImage()
        except IOError:
            logger.warning("Could not generate the image - try adjusting the zoom level and checking your coordinates")
        else:
            # Save the image to disk
            #img.save("high_resolution_image.png")
            logger.warning("The map has successfully been created")

        #preview = b'\377\330\377\340\000\020JFIF\000\001\001\000\000\001\000\001\000\000\377\333\000C\000\006\004\005\006\005\004\006\006\005\006\007\007\006\010\n\020\n\n\t\t\n\024\016\017\014\020\027\024\030\030\027\024\026\026\032\035%\037\032\033#\034\026\026 , #&\')*)\031\037-0-(0%()(\377\333\000C\001\007\007\007\n\010\n\023\n\n\023(\032\026\032((((((((((((((((((((((((((((((((((((((((((((((((((\377\300\000\021\010\000d\000d\003\001\"\000\002\021\001\003\021\001\377\304\000\037\000\000\001\005\001\001\001\001\001\001\000\000\000\000\000\000\000\000\001\002\003\004\005\006\007\010\t\n\013\377\304\000\265\020\000\002\001\003\003\002\004\003\005\005\004\004\000\000\001}\001\002\003\000\004\021\005\022!1A\006\023Qa\007\"q\0242\201\221\241\010#B\261\301\025R\321\360$3br\202\t\n\026\027\030\031\032%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\203\204\205\206\207\210\211\212\222\223\224\225\226\227\230\231\232\242\243\244\245\246\247\250\251\252\262\263\264\265\266\267\270\271\272\302\303\304\305\306\307\310\311\312\322\323\324\325\326\327\330\331\332\341\342\343\344\345\346\347\350\351\352\361\362\363\364\365\366\367\370\371\372\377\304\000\037\001\000\003\001\001\001\001\001\001\001\001\001\000\000\000\000\000\000\001\002\003\004\005\006\007\010\t\n\013\377\304\000\265\021\000\002\001\002\004\004\003\004\007\005\004\004\000\001\002w\000\001\002\003\021\004\005!1\006\022AQ\007aq\023\"2\201\010\024B\221\241\261\301\t#3R\360\025br\321\n\026$4\341%\361\027\030\031\032&\'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\202\203\204\205\206\207\210\211\212\222\223\224\225\226\227\230\231\232\242\243\244\245\246\247\250\251\252\262\263\264\265\266\267\270\271\272\302\303\304\305\306\307\310\311\312\322\323\324\325\326\327\330\331\332\342\343\344\345\346\347\350\351\352\362\363\364\365\366\367\370\371\372\377\332\000\014\003\001\000\002\021\003\021\000?\000\367\360H \216\010\253W\203\314\362\347A\376\260r\007\367\207Z\236\337Kv\301\235\266\217A\311\2558 \216\004\333\030\300\316y\347\232\000\307\267\323\246\227\005\207\226\276\247\257\345ZV\366\020\303\203\267{z\265K=\314P\017\3368\007\323\275gO\252;dB\273G\251\344\320\006\254\216\221\256\347`\243\324\232\250o\325\326_\263\215\314\213\270g\200k\026I\036F\334\354X\372\223N\266\227\311\235\037\260<\217Q@\016\236\346Y\377\000\3269#\320p*\032\226\352/*wA\367z\203\352;TT\000U\233\337\237\313\234\177\313E\347\375\341\301\252\325f\017\336\332M\027t\375\342\377\000Z\000\255R\332K\344\\#\366\007\237\245EJ\252X\200\240\222{\n\000\352\007#\212*\275\200\220Z\242\312\245Xq\317\245\024\000\313\213\370a\310\335\275\275\026\263\345\324\246v\0330\212\016p;\325\032(\002\305\352\0016\364\373\222\r\343\361\252\365j?\337Y\274\177\307\027\316\277N\365V\200\n\245\252jv\332lj\327,w>BF\203,\370\364\037\324\3602*\355y\237\215o\'\217V\325\244\215|\311\240\214,)\353\210\303\001\370\263\032\306\265Og\033\243\273/\302,U^I=\022\271\332\017\026\330\316!K\210\256mJ\374\236d\301vc<d\253\034}N\007\275lW\315\337\017<M\254\352\367\267\261j\353\272\004\\\206\362\202ml\343o\277\031\374\253\350\037\002\333\334^\370n\315\333\356\215\361\2537\367U\331G\327\200*(\325\224\244\343#\2470\300\323\243J5\251^\315\333_\353\310\320\253:zHn\021\243B\300\0347\246;\326\225\276\233\014|\311\231\033\337\247\345W@\n\000P\000\035\205t\236A\235\036\224\241\311\221\311\\\360\007\245^\206\030\341\030\215\002\375*J\202\340\\7\020\264h=NI\240\t\362=h\254\207\323\'v,\362\253\037RM\024\001\233E\024P\004\226\322\3713+\365\000\362=Gz[\250\274\231\331G+\325O\250\244\202\t\'lD\205\275\373\n\327K\005h\342\027\007s \307\007\250\364\240\014dF\221\266\242\226>\200W\'\361\033\303\323\305f5\250\324\003\020\021\334 \344\354\317\017\370\023\317\261\366\257Q\2164\215v\306\241G\260\250\257\226\336KYa\273\332`\225\n:\267FR0G\345Y\324\246\252E\305\2358<L\260\265\243V=?#\347\335\022\316}kV\266\323\255I\022N\330/\214\371j9f?A\371\234\016\365\364\016\237g\016\237c\005\245\252\354\202\004\021\240\366\003\037\235yg\302\213S\246\\ks\310\253,\361LlRC\330!\313\037\243e\177\357\232\364+mNA)\363\376d>\203\356\326\030:\\\220\346{\263\323\317q\236\336\277\263\207\303\037\315\232\027\027\260\302Hf\313\017\341^j\204\232\254\205\277v\212\027\337\232]Y\355r\205\344\t#\214\243c\345ol\326n\017\241\256\263\3037\264\373\277\264\243n\0002\236\202\242\273\277ky\314f F2\016z\325\r2o*\351r~V\371M^\326a\335\022\312:\247\007\351@\020\377\000k?\374\362_\316\212\315\242\200&KY^V\215\020\222\247\004\366\374\353J\333KE\301\234\357?\335\035+@\000\243\000\000\005U\270\277\206,\200\333\333\321\177\306\200-*\252(U\000\001\330SL\210$\t\274o?\303\236k\026\343P\232\\\205>Z\372/_\316\253\300\314\263+\251\371\201\316M\000jjwS@\312\261\200\252\303\357u5\220\356\316\305\235\213\023\334\3235\ry\365\0376-#N\222\340\303\037\236e\271&\004e\347\356dnc\301\035\000\351\3174\252\351\"$\221\034\307\"\207C\354FE\000Aii\005\247\235\366x\302y\3224\322rN\347=O?J\261E\024%a\266\333\273\027lR\354K\240\315\022\222@\007\004g\275jZ\231X\233yIf\333\230\356\024p\353\357\357YUn\302\361\255\233\r\223\021\352==\350\020\267\020e\330\000\026a\311Q\321\275\305jZ\310.\255>~I\033X{\322\334\304\263\302Yq\234d0\252\366\0222\344L\273X\235\244\364\311\354h\003&h\314R\274m\325N(\255\313\233(\347\223{d\034c\212(\003\036\342\356i\363\275\360\277\335\034\n\202\237<~T\316\237\3358\246P\001@$\034\203\203E\024\000\3504{]N\372\346MDM9\330\242\022\035\243T\214\365A\265\271%\201-\236\271Q\332\245\275\200[\316cU\013\030\003`\003\000/`?\225U\236[\210`2Y\227\363U\320\266\305\014\346=\343xPz\235\271\251f\325$\324o\326\030mc\205#\033\237\355R\205\231\227\276\330\207?\213c\350h\001\264QJ\212\316\330E,}\000\315\000%\025i,d$\tYc\366\352\337\220\251f\216\332\320`\2034\336\207\240\372\320\005\235\032b\360\264m\316\316\237J\255so\034S\267\2356\0279T^N?\245:\302\362F\272Eb\0263\300U\030\002\227[\217\022G\'\250\301\240\007.\252\025B\210\230\201\300%\2714V]\024\001=\351\335u!\3655\005\024P\200(\240\014\234\016MYKG\300i\230D\247\373\335O\320P\005t;]O\241\315f\306\242\326{{I\305\230\002\340\335\254\261\0267\023\374\304\200AP\252I;r[\234\020\007<ti\014p\256\355\201\177\333\237\372-bx\226(g\214\\\211\256w\250X\\#\210\204\273\235B\006l\035\252\254s\270\014\216H4\001{J\236\322\365\345\362U\344)\265\200f\013\224#!\210\352;\214\036\340\212\2755\304Q\026U\220\262\347\204\210m\037\211\254\233v\232\003.\231 \200\013H\243q\366b\333\000b\300+\006$\356\371I\311<\346\237@\026\036\362B\n\306\004J{\'\004\375MW\242\212\000Tb\216\254:\251\310\255+\353\250n\222hP\376\366\022\033\036\240\216\243\363\254\300\t \000I=\205X\266\263H\265\010<\330\360\323\304\353\363u\014;\376T\320\025\350\240\202\t\007\250\242\220\005Me\022\315:\243\222\001\364\242\212\000\321E\021^\210!\001\0063\270\014\261\374MG\250\334\274S\225\214*\234}\375\2777\347E\024\001\232\314\314IbI=\311\246\220\254\254\216\252\350\300\253+\014\206\007\250#\270\242\212\000\3200[i~\032\270k\013Kx\025b2\371q\306\025K\001\234\2201\351Xz%\343\352\032-\215\344\312\213,\360\207`\203\013\236zQE\000]\251\254\342Y\256\025\034\220\017\245\024P\005\233\311\r\244\206+p\2501\313\001\363\037\306\244\322cY\3674\243sF\373\224\222x$b\212(\002\225\362\205\273\224\016\233\215\024Q@\037\377\331'
        return preview


    def getXY(self, latitude, longitude, zoom):
        """
        Generates an X,Y tile coordinate based on the latitude, longitude
        and zoom level
        Returns:    An X,Y tile coordinate
        """

        tile_size = 256

        # Use a left shift to get the power of 2
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles
        numTiles = 1 << zoom

        # Find the x_point given the longitude
        point_x = (tile_size / 2 + longitude * tile_size / 360.0) * numTiles // tile_size

        # Convert the latitude to radians and take the sine
        sin_y = math.sin(latitude * (math.pi / 180.0))

        # Calulate the y coorindate
        point_y = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(
            tile_size / (2 * math.pi))) * numTiles // tile_size

        return int(point_x), int(point_y)


    def generateImage(self, **kwargs):
        """
        Generates an image by stitching a number of google map tiles together.

        Args:
            start_x:        The top-left x-tile coordinate
            start_y:        The top-left y-tile coordinate
            tile_width:     The number of tiles wide the image should be -
                            defaults to 5
            tile_height:    The number of tiles high the image should be -
                            defaults to 5
        Returns:
            A high-resolution Goole Map image.
        """

        start_x = kwargs.get('start_x', None)
        start_y = kwargs.get('start_y', None)
        tile_width = kwargs.get('tile_width', 5)
        tile_height = kwargs.get('tile_height', 5)

        # Check that we have x and y tile coordinates
        if start_x == None or start_y == None:
            start_x, start_y = self.getXY()

        # Determine the size of the image
        width, height = 256 * tile_width, 256 * tile_height

        # Create a new image of the size require
        map_img = Image.new('RGB', (width, height))

        for x in range(0, tile_width):
            for y in range(0, tile_height):
                url = 'https://mt0.google.com/vt?x=' + str(start_x + x) + '&y=' + str(start_y + y) + '&z=' + str(
                    self._zoom)

            current_tile = str(x) + '-' + str(y)
            urllib.request.urlretrieve(url, current_tile)

            im = Image.open(current_tile)
            map_img.paste(im, (x * 256, y * 256))

            os.remove(current_tile)

        return map_img


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

    @staticmethod
    def getExtension(mimeType):
        mimeType = mimetypes.guess_extension(mimeType)
        if mimeType is None:
            raise Exception("Unsupported/unrecognized file type for: " + mimeType);
        return mimeType

class VideoTools:
    @staticmethod
    def getVideoProperties(videoFile):
        if sys.version_info <= (3, 0): 
            with FFVideoOptionalModule() as imp:
                VideoStream = imp("VideoStream")
                s = VideoStream(videoFile)
                return s.width, s.height, s.bitrate, s.duration #, s.codec_name
        else:
            import av
            container = av.open(videoFile)
            for i,frame in enumerate(container.decode(video=0)):
                break
            return frame.width, frame.height, container.bit_rate, container.duration/av.time_base

    @staticmethod
    def generatePreviewFromVideo(videoFile):
        if sys.version_info <= (3, 0):
            with FFVideoOptionalModule() as imp:
                VideoStream = imp("VideoStream")
                fd, path = tempfile.mkstemp('.jpg')
                stream = VideoStream(videoFile)
                stream.get_frame_at_sec(0).image().save(path)
                preview = ImageTools.generatePreviewFromImage(path)
                os.remove(path)
                return preview
        else:
            #install av lib using pip3 install av
            import av
            container = av.open(videoFile)
            for i, frame in enumerate(container.decode(video=0)):
                fd, path = tempfile.mkstemp('.jpg')
                frame.to_image().save(path)
                preview = ImageTools.generatePreviewFromImage(path)
                os.remove(path)
                return preview
