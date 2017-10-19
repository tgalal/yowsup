from yowsup.common.http.warequest import WARequest
from yowsup.common.http.waresponseparser import JSONResponseParser
import socket, ssl, os, hashlib, sys
from time import sleep
import threading
import logging
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
        if "video" in filetype:
            return DownloadableMediaMessageProtocolEntity.VIDEO_KEY
        elif "image" in filetype:
            return DownloadableMediaMessageProtocolEntity.IMAGE_KEY
        elif "audio" in filetype:
            return DownloadableMediaMessageProtocolEntity.AUDIO_KEY
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
        _host = uploadUrl.replace("https://","")

        self.url = _host[:_host.index('/')]


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

            self.sock.connect((self.url, self.port))
            ssl_sock = ssl.wrap_socket(self.sock)

            m = hashlib.md5()
            m.update(filename.encode())
            crypto = m.hexdigest() + os.path.splitext(filename)[1]

            boundary = "zzXXzzYYzzXXzzQQ"#"-------" + m.hexdigest() #"zzXXzzYYzzXXzzQQ"
            contentLength = 0

            digTo = hmac.new("".encode("utf-8"), self.jid.replace("@s.whatsapp.net", "@c.us").encode("utf-8"),
                             hashlib.sha256).digest()[:20]
            refTo = base64.b64encode(digTo).decode()
            digFrom = hmac.new("".encode("utf-8"), self.accountJid.replace("@s.whatsapp.net", "@c.us").encode("utf-8"),
                               hashlib.sha256).digest()[:20]
            refFrom = base64.b64encode(digFrom).decode()

            hBAOS = "--" + boundary + "\r\n"
            hBAOS += "Content-Disposition: form-data; name=\"hash\"\r\n\r\n"
            hBAOS += b64Hash.decode() + "\r\n"

            hBAOS += "--" + boundary + "\r\n"
            hBAOS += "Content-Disposition: form-data; name=\"refs\"\r\n\r\n"
            hBAOS += refFrom + "\r\n"
            hBAOS += refTo + "\r\n"

            hBAOS += "--" + boundary + "\r\n"
            hBAOS += "Content-Disposition: form-data; name=\"file\"; filename=\"" + "blob" + "\"\r\n"
            hBAOS += "Content-Type: " + "application/octet-stream" + "\r\n\r\n"

            fBAOS = "\r\n--" + boundary + "--\r\n"

            contentLength += len(hBAOS)
            contentLength += len(fBAOS)
            contentLength += filesize

            POST = "POST %s\r\n" % uploadUrl
            POST += "Content-Type: multipart/form-data; boundary=" + boundary + "\r\n"
            POST += "Host: %s\r\n" % self.url
            POST += "User-Agent: %s\r\n" % self.getUserAgent()
            POST += "Content-Length: " + str(contentLength) + "\r\n\r\n"

            ssl_sock.write(bytearray(POST.encode()))
            ssl_sock.write(bytearray(hBAOS.encode()))

            totalsent = 0
            buf = 1024
            status = 0
            lastEmit = 0

            while totalsent < int(filesize):
                ssl_sock.write(stream[:buf])
                status = totalsent * 100 / filesize
                if lastEmit!=status and status!=100 and filesize>12288:
                    if self.progressCallback:
                        self.progressCallback(self.sourcePath, self.jid, uploadUrl, int(status))
                lastEmit = status
                stream = stream[buf:]
                totalsent = totalsent + buf

            ssl_sock.write(bytearray(fBAOS.encode()))

            sleep(1)
            data = ssl_sock.recv(8192)
            data += ssl_sock.recv(8192)
            data += ssl_sock.recv(8192)
            data += ssl_sock.recv(8192)
            data += ssl_sock.recv(8192)
            data += ssl_sock.recv(8192)
            data += ssl_sock.recv(8192)

            if self.progressCallback:
                self.progressCallback(self.sourcePath, self.jid, uploadUrl, 100)


            lines = data.decode().splitlines()


            result = None

            for l in lines:
                if l.startswith("{"):
                    result = self.parser.parse(l, self.pvars)
                    break

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
