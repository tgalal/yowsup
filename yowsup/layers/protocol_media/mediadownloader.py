import sys, tempfile, logging

logger = logging.getLogger(__name__)

if sys.version_info >= (3, 0):
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib import urlencode


class MediaDownloader:
    def __init__(self, successClbk=None, errorClbk=None, progressCallback=None):
        self.successCallback = successClbk
        self.errorCallback = errorClbk
        self.progressCallback = progressCallback

    def download(self, url=""):
        try:

            if not url:
                if self.url:
                    url = "https://" if self.port == 443 else "http://"
                    url = url + self.url
                    url = url + "?" + urlencode(self.params)
                    logger.debug("URL is %s" % url)
                else:
                    raise Exception("No url specified for fetching")

            u = urlopen(url)

            path = tempfile.mkstemp()[1]
            with open(path, "wb") as f:
                meta = u.info()

                if sys.version_info >= (3, 0):
                    fileSize = int(u.getheader("Content-Length"))
                else:
                    fileSize = int(meta.getheaders("Content-Length")[0])

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

            if self.successCallback:
                self.successCallback(path)
        except:
            logger.exception("Error occured at transfer")
            if self.errorCallback:
                self.errorCallback();
