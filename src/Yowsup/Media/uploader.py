from ..Common.Http.warequest import WARequest
from ..Common.Http.waresponseparser import JSONResponseParser
import socket, ssl, mimetypes, os, hashlib, sys
from time import sleep

class MediaUploader(WARequest):
    def __init__(self, jid, accountJid, successClbk = None, errorClbk = None, progressCallback = None):
        super(MediaUploader, self).__init__()

        #self.url = "mms819.whatsapp.net"
        
        self.jid = jid;
        self.accountJid = accountJid;

        self.successCallback = successClbk
        self.errorCallback = errorClbk
        self.progressCallback = progressCallback
        
        self.pvars = ["name", "type", "size", "url", "error", "mimetype", "filehash", "width", "height"]
        
        self.setParser(JSONResponseParser())
        
        self.sock = socket.socket();
        
    def upload(self, sourcePath, uploadUrl):
        
        _host = uploadUrl.replace("https://","")

        self.url = _host[:_host.index('/')]
        
        
        try:
            filename = os.path.basename(sourcePath)
            filetype = mimetypes.guess_type(filename)[0]
            filesize = os.path.getsize(sourcePath)
    
            self.sock.connect((self.url, self.port));
            ssl_sock = ssl.wrap_socket(self.sock)
    
            m = hashlib.md5()
            m.update(filename.encode())
            crypto = m.hexdigest() + os.path.splitext(filename)[1]
    
            boundary = "zzXXzzYYzzXXzzQQ"#"-------" + m.hexdigest() #"zzXXzzYYzzXXzzQQ"
            contentLength = 0

            hBAOS = "--" + boundary + "\r\n"
            hBAOS += "Content-Disposition: form-data; name=\"to\"\r\n\r\n"
            hBAOS += self.jid + "\r\n"
            hBAOS += "--" + boundary + "\r\n"
            hBAOS += "Content-Disposition: form-data; name=\"from\"\r\n\r\n"
            hBAOS += self.accountJid.replace("@whatsapp.net","") + "\r\n"
    
            hBAOS += "--" + boundary + "\r\n"
            hBAOS += "Content-Disposition: form-data; name=\"file\"; filename=\"" + crypto + "\"\r\n"
            hBAOS  += "Content-Type: " + filetype + "\r\n\r\n"
    
            fBAOS = "\r\n--" + boundary + "--\r\n"
            
            contentLength += len(hBAOS)
            contentLength += len(fBAOS)
            contentLength += filesize
    
            #POST = "POST https://mms.whatsapp.net/client/iphone/upload.php HTTP/1.1\r\n"
            POST = "POST %s\r\n" % uploadUrl
            POST += "Content-Type: multipart/form-data; boundary=" + boundary + "\r\n"
            POST += "Host: %s\r\n" % self.url
            POST += "User-Agent: %s\r\n" % self.getUserAgent()
            POST += "Content-Length: " + str(contentLength) + "\r\n\r\n"
            
            self._d(POST)
            self._d("sending REQUEST ")
            self._d(hBAOS)
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
                if lastEmit!=status and status!=100 and filesize>12288:
                    if self.progressCallback:
                        self.progressCallback(int(status))
                lastEmit = status
                stream = stream[buf:]
                totalsent = totalsent + buf
    
            ssl_sock.write(bytearray(fBAOS.encode()))
    
            sleep(1)
            self._d("Reading response...")
            data = ssl_sock.recv(8192)
            data += ssl_sock.recv(8192)
            data += ssl_sock.recv(8192)
            data += ssl_sock.recv(8192)
            data += ssl_sock.recv(8192)
            data += ssl_sock.recv(8192)
            data += ssl_sock.recv(8192)
            self._d(data)
            
            if self.progressCallback:
                self.progressCallback(100)
                
            
            lines = data.decode().splitlines()
            
            
            result = None

            for l in lines:
                if l.startswith("{"):
                    result = self.parser.parse(l, self.pvars)
                    break
            
            if not result:
                raise Exception("json data not found")
            

            self._d(result)
            
            if result["url"] is not None:
                if self.successCallback:
                    self.successCallback(result["url"])
            else:
                self.errorCallback()

        except:
            print("Error occured at transfer %s"%sys.exc_info()[1])
            if self.errorCallback:
                self.errorCallback();
