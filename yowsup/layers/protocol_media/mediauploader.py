from yowsup.common.http.warequest import WARequest
from yowsup.common.http.waresponseparser import JSONResponseParser
import socket, ssl, os, hashlib, sys
from time import sleep
import threading
import logging
import requests
from yowsup.common.tools import MimeTools
import base64
import hmac
from Crypto.Cipher import AES
import binascii
from axolotl.kdf.hkdfv3 import HKDFv3
from axolotl.sessioncipher import pad
from axolotl.util.byteutil import ByteUtil
from .protocolentities.message_media_downloadable import DownloadableMediaMessageProtocolEntity 
logger = logging.getLogger(__name__)

class MediaUploader(WARequest, threading.Thread):
    def __init__(self, jid, accountJid, sourcePath, uploadUrl, resumeOffset = 0, successClbk = None, errorClbk = None, progressCallback = None, async = True):
        WARequest.__init__(self)

        self.async = async
        self.jid = jid
        self.accountJid = accountJid
        self.sourcePath = sourcePath
        self.uploadUrl = uploadUrl
        self.resumeOffset = resumeOffset

        self.successCallback = successClbk
        self.errorCallback = errorClbk
        self.progressCallback = progressCallback

        self.pvars = ["name", "type", "size", "url", "error", "mimetype", "filehash", "width", "height"]

        self.setParser(JSONResponseParser())

        self.sock = socket.socket()

    def start(self):
        if self.async:
            threading.Thread.__init__(self)
            super(MediaUploader, self).start()
        else:
            self.run()

    def pad(self,s):
        # return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        y = (16 - len(s) % 16) * chr(16 - len(s) % 16)
        a = s + y.encode()
        return a

    def getKey(self, filetype):
        print("FILE TYPE")
        print(filetype)
        if "video" in filetype:
            return DownloadableMediaMessageProtocolEntity.VIDEO_KEY
        elif "image" in filetype:
            return DownloadableMediaMessageProtocolEntity.IMAGE_KEY
        elif "audio" in filetype:
            return DownloadableMediaMessageProtocolEntity.AUDIO_KEY
        elif "application" in filetype:
            return DownloadableMediaMessageProtocolEntity.DOCUMENT_KEY
        elif "text" in filetype:
            return DownloadableMediaMessageProtocolEntity.DOCUMENT_KEY
        raise Exception ("FILE TYPE NOT SUPPORTED")
        
        

    def encryptMedia(self,img, refkey,filetype):
        key = self.getKey(filetype)
        derivative = HKDFv3().deriveSecrets(binascii.unhexlify(refkey),
                                            binascii.unhexlify(key), 112)
        parts = ByteUtil.split(derivative, 16, 32)
        iv = parts[0]
        cipherKey = parts[1]
        macKey=derivative[48:80]

        mac = hmac.new(macKey,digestmod=hashlib.sha256)
        mac.update(iv)

        cipher = AES.new(key=cipherKey, mode=AES.MODE_CBC, IV=iv)
        imgEnc = cipher.encrypt(self.pad(img))

        mac.update(imgEnc)
        hash = mac.digest()
        hashKey = ByteUtil.trim(mac.digest(), 10)

        finalEnc =  imgEnc + hashKey

        return finalEnc

    def run(self):

        sourcePath = self.sourcePath
        uploadUrl = self.uploadUrl

        try:
            filename = os.path.basename(sourcePath)
            filetype = MimeTools.getMIME(filename)
            f = open(sourcePath, 'rb')
            stream = f.read()
            f.close()
            refkey = binascii.hexlify(os.urandom(32))
            stream=self.encryptMedia(stream,refkey,filetype)
            fenc = open(sourcePath+".enc", 'wb')  # bahtiar
            fenc.write(stream)
            fenc.seek(0, 2)
            filesize=fenc.tell()
            fenc.close()
            os.remove(sourcePath+".enc")
            filesize2=len(stream)

            sha1 = hashlib.sha256()
            sha1.update(stream)
            b64Hash = base64.b64encode(sha1.digest())

            file_enc_sha256 = hashlib.sha256(stream).hexdigest()

            m = hashlib.md5()
            m.update(filename.encode())
            crypto = m.hexdigest() + os.path.splitext(filename)[1]

            digTo = hmac.new("".encode("utf-8"), self.jid.replace("@s.whatsapp.net", "@c.us").encode("utf-8"),
                             hashlib.sha256).digest()[:20]

            refTo = base64.b64encode(digTo).decode()

            digFrom = hmac.new("".encode("utf-8"), self.accountJid.replace("@s.whatsapp.net", "@c.us").encode("utf-8"),
                               hashlib.sha256).digest()[:20]
            refFrom = base64.b64encode(digFrom).decode()

            hBAOS = "------zzXXzzYYzzXXzzQQ\r\n"
            hBAOS += "Content-Disposition: form-data; name=\"hash\"\r\n\r\n"
            hBAOS += b64Hash.decode() + "\r\n"
            hBAOS += "------zzXXzzYYzzXXzzQQ\r\n"
            hBAOS += "Content-Disposition: form-data; name=\"refs\"\r\n\r\n"
            hBAOS += refTo + "\r\n"
            hBAOS += refFrom + "\r\n"
            hBAOS += "------zzXXzzYYzzXXzzQQ\r\n"
            hBAOS += "Content-Disposition: form-data; name=\"file\"; filename=\"" + "blob" + "\"\r\n"
            hBAOS += "Content-Type: " + "application/octet-stream" + "\r\n\r\n"

            fBAOS = "\r\n------zzXXzzYYzzXXzzQQ--"

            contentLength = len(hBAOS) + len(fBAOS) + len(stream)

            headers = {
                "content-length": contentLength,
                "user-agent": self.getUserAgent(),
                "content-type": "multipart/form-data; boundary=----zzXXzzYYzzXXzzQQ"}

            data = bytearray(hBAOS, 'utf-8') + stream + bytearray(fBAOS, 'utf-8')

            response = requests.post(uploadUrl, data=data, headers=headers)

            result = None

            if response.text.startswith("{"):
               result = self.parser.parse(response.text, self.pvars)

            if not result:
                raise Exception("json data not found")

            if result["url"] is not None:
                if self.successCallback:
                    # self.successCallback(sourcePath, self.jid, result["url"])
                    result["mediaKey"]=refkey
                    result["file_enc_sha256"]=file_enc_sha256
                    self.successCallback(sourcePath, self.jid, result)
            else:
                logger.exception("uploadUrl: %s, result of uploading media has no url" % uploadUrl)
                if self.errorCallback:
                    self.errorCallback(sourcePath, self.jid, uploadUrl)

        except:
            logger.exception("Error occured at transfer %s"%sys.exc_info()[1])
            if self.errorCallback:
                self.errorCallback(sourcePath, self.jid, uploadUrl)