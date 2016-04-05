from yowsup.layers import YowLayer
from yowsup.structs import ProtocolTreeNode
from .mediadownloader import MediaDownloader
import shutil, os, logging
logger = logging.getLogger(__name__)


class YowMediaPictureLayer(YowLayer):
    def send(self, data):
        self.toLower(data)

    def receive(self, node):
        if ProtocolTreeNode.tagEquals(node, "message") and node.getAttributeValue("type") == "media":
            self.downloadMedia(node.getChild("media").getAttributeValue("url"))
        else:
            self.toUpper(node)

    def downloadMedia(self, url):
        logger.debug("Downloading %s" % url)
        downloader = MediaDownloader(self.onSuccess, self.onError, self.onProgress)
        downloader.download(url)

    def onError(self):
        logger.error("Error download file")

    def onSuccess(self, path):
        outPath = "/tmp/yowfiles/%s.jpg" % os.path.basename(path)
        shutil.copyfile(path, outPath)
        logger.debug("Picture downloaded to %s" % outPath)

    def onProgress(self, progress):
        logger.debug("Download progress %s" % progress)
