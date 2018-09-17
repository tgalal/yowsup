from yowsup.common.http.warequest import WARequest
from yowsup.common.http.waresponseparser import JSONResponseParser
import socket
import ssl
import os
import hashlib
import sys
from time import sleep
import threading
import logging
from yowsup.common.tools import MimeTools

logger = logging.getLogger(__name__)


class MediaUploader(WARequest, threading.Thread):
    def __init__(self, jid, accountJid, sourcePath, uploadUrl, resumeOffset=0, successClbk=None, errorClbk=None, progressCallback=None, asynchronous=True):
        WARequest.__init__(self)

        self.asynchronous = asynchronous
        self.jid = jid
        self.accountJid = accountJid
        self.sourcePath = sourcePath
        self.uploadUrl = uploadUrl
        self.resumeOffset = resumeOffset

        self.successCallback = successClbk
        self.errorCallback = errorClbk
        self.progressCallback = progressCallback

        self.pvars = ["name", "type", "size", "url", "error",
                      "mimetype", "filehash", "width", "height"]

        self.setParser(JSONResponseParser())

        self.sock = socket.socket()

    def start(self):
        if self.asynchronous:
            threading.Thread.__init__(self)
            super(MediaUploader, self).start()
        else:
            self.run()

    def run(self):

        sourcePath = self.sourcePath
        uploadUrl = self.uploadUrl
        _host = uploadUrl.replace("https://", "")

        self.url = _host[:_host.index('/')]

        try:
            filename = os.path.basename(sourcePath)
            filetype = MimeTools.getMIME(filename)
            filesize = os.path.getsize(sourcePath)

            self.sock.connect((self.url, self.port))
            ssl_sock = ssl.wrap_socket(self.sock)

            m = hashlib.md5()
            m.update(filename.encode())
            crypto = m.hexdigest() + os.path.splitext(filename)[1]

            boundary = "zzXXzzYYzzXXzzQQ"  # "-------" + m.hexdigest() #"zzXXzzYYzzXXzzQQ"
            contentLength = 0

            hBAOS = "--" + boundary + "\r\n"
            hBAOS += "Content-Disposition: form-data; name=\"to\"\r\n\r\n"
            hBAOS += self.jid + "\r\n"
            hBAOS += "--" + boundary + "\r\n"
            hBAOS += "Content-Disposition: form-data; name=\"from\"\r\n\r\n"
            hBAOS += self.accountJid.replace("@whatsapp.net", "") + "\r\n"

            hBAOS += "--" + boundary + "\r\n"
            hBAOS += "Content-Disposition: form-data; name=\"file\"; filename=\"" + crypto + "\"\r\n"
            hBAOS += "Content-Type: " + filetype + "\r\n\r\n"

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
            f = open(sourcePath, 'rb')
            stream = f.read()
            f.close()
            status = 0
            lastEmit = 0

            while totalsent < int(filesize):
                ssl_sock.write(stream[:buf])
                status = totalsent * 100 / filesize
                if lastEmit != status and status != 100 and filesize > 12288:
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
                    self.successCallback(sourcePath, self.jid, result["url"])
            else:
                logger.exception("uploadUrl: %s, result of uploading media has no url" % uploadUrl)
                if self.errorCallback:
                    self.errorCallback(sourcePath, self.jid, uploadUrl)

        except:
            logger.exception("Error occured at transfer %s" % sys.exc_info()[1])
            if self.errorCallback:
                self.errorCallback(sourcePath, self.jid, uploadUrl)
