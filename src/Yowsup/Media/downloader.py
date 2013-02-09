from ..Common.Http.warequest import WARequest
from urllib2 import urlopen
#from urllib.request import urlopen
import tempfile, sys

class MediaDownloader(WARequest):
    def __init__(self, successClbk = None, errorClbk = None, progressCallback = None):
        self.successCallback = successClbk
        self.errorCallback = errorClbk
        self.progressCallback = progressCallback
        

    def download(self, url):
        try:
            u = urlopen(url)
            
            path = tempfile.mkstemp()[1]
            f = open(path, "wb")
            meta = u.info()
            fileSize = int(meta.getheaders("Content-Length")[0])
            #fileSize = int(u.getheader("Content-Length"))

            fileSizeDl = 0
            blockSz = 8192
            lastEmit = 0
            while True:
                buf = u.read(blockSz)
                
                if not buf:
                    break

                fileSizeDl += len(buf)
                f.write(buf)
                status = (fileSizeDl * 100 / fileSize)
            
                if self.progressCallback and lastEmit != status:
                    self.progressCallback(int(status))
                    lastEmit = status;

            self.successCallback(path)
        except:
            print("Error occured at transfer %s"%sys.exc_info()[1])
            if self.errorCallback:
                self.errorCallback();