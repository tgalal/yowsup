from yowsup.layers.protocol_media.mediacipher import MediaCipher
from yowsup.layers.protocol_media.protocolentities \
    import ImageDownloadableMediaMessageProtocolEntity, AudioDownloadableMediaMessageProtocolEntity,\
    VideoDownloadableMediaMessageProtocolEntity, DocumentDownloadableMediaMessageProtocolEntity, \
    ContactMediaMessageProtocolEntity, DownloadableMediaMessageProtocolEntity

import threading
from tqdm import tqdm
import requests
import logging
import math
import sys
import os
import base64

if sys.version_info >= (3, 0):
    from queue import Queue
else:
    from Queue import Queue

logger = logging.getLogger(__name__)


class SinkWorker(threading.Thread):
    def __init__(self, storage_dir):
        super(SinkWorker, self).__init__()
        self.daemon = True
        self._storage_dir = storage_dir
        self._jobs = Queue()
        self._media_cipher = MediaCipher()

    def enqueue(self, media_message_protocolentity):
        self._jobs.put(media_message_protocolentity)

    def _create_progress_iterator(self, iterable, niterations, desc):
        return tqdm(
                    iterable, total=niterations, unit='KB', dynamic_ncols=True,
                    unit_scale=True, leave=True, desc=desc, ascii=True)

    def _download(self, url):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        logger.debug("%s total size is %s, downloading" % (url, total_size))
        block_size = 1024
        wrote = 0
        enc_data = b""

        for data in self._create_progress_iterator(
                response.iter_content(block_size), math.ceil(total_size // block_size) + 1, "Download       ",
        ):
            wrote = wrote + len(data)
            enc_data = enc_data + data

        if total_size != 0 and wrote != total_size:
            logger.error("Something went wrong")
            return None

        return enc_data

    def _decrypt(self, ciphertext, ref_key, media_info):
        length_kb = int(math.ceil(len(ciphertext) / 1024))
        progress = self._create_progress_iterator(range(length_kb), length_kb, "Decrypt        ")
        try:
            plaintext = self._media_cipher.decrypt(ciphertext, ref_key, media_info)
            progress.update(length_kb)
            return plaintext
        except Exception as e:
            progress.set_description("Decrypt Error  ")
            logger.error(e)

        return None

    def _write(self, data, filename):
        length_kb = int(math.ceil(len(data) / 1024))
        progress = self._create_progress_iterator(range(length_kb), length_kb, "Write          ")
        try:
            with open(filename, 'wb') as f:
                f.write(data)
            progress.update(length_kb)
            return filename
        except Exception as e:
            progress.set_description("Write error    ")
            logger.error(e)

        return None

    def _create_unique_filepath(self, filepath):
        file_dir = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        result_filename = filename
        dissected = os.path.splitext(filename)
        count = 0
        while os.path.exists(os.path.join(file_dir, result_filename)):
            count += 1
            result_filename = "%s_%d%s" % (dissected[0], count, dissected[1])

        return os.path.join(file_dir, result_filename)

    def run(self):
        logger.debug(
            "SinkWorker started, storage_dir=%s" % self._storage_dir
        )
        while True:
            media_message_protocolentity = self._jobs.get()
            if media_message_protocolentity is None:
                sys.exit(0)
            if isinstance(media_message_protocolentity, DownloadableMediaMessageProtocolEntity):
                logger.info(
                    "Processing [url=%s, media_key=%s]" %
                    (media_message_protocolentity.url, base64.b64encode(media_message_protocolentity.media_key))
                )
            else:
                logger.info("Processing %s" % media_message_protocolentity.media_type)

            filedata = None
            fileext = None
            if isinstance(media_message_protocolentity, ImageDownloadableMediaMessageProtocolEntity):
                media_info = MediaCipher.INFO_IMAGE
                filename = "image"
            elif isinstance(media_message_protocolentity, AudioDownloadableMediaMessageProtocolEntity):
                media_info = MediaCipher.INFO_AUDIO
                filename = "ptt" if media_message_protocolentity.ptt else "audio"
            elif isinstance(media_message_protocolentity, VideoDownloadableMediaMessageProtocolEntity):
                media_info = MediaCipher.INFO_VIDEO
                filename = "video"
            elif isinstance(media_message_protocolentity, DocumentDownloadableMediaMessageProtocolEntity):
                media_info = MediaCipher.INFO_DOCUM
                filename = media_message_protocolentity.file_name
            elif isinstance(media_message_protocolentity, ContactMediaMessageProtocolEntity):
                filename = media_message_protocolentity.display_name
                filedata = media_message_protocolentity.vcard
                fileext = "vcard"
            else:
                logger.error("Unsupported Media type: %s" % media_message_protocolentity.__class__)
                sys.exit(1)

            if filedata is None:
                enc_data = self._download(media_message_protocolentity.url)
                if enc_data is None:
                    logger.error("Download failed")
                    sys.exit(1)

                filedata = self._decrypt(enc_data, media_message_protocolentity.media_key, media_info)
                if filedata is None:
                    logger.error("Decrypt failed")
                    sys.exit(1)

            if not isinstance(media_message_protocolentity, DocumentDownloadableMediaMessageProtocolEntity):
                if fileext is None:
                    fileext = media_message_protocolentity.mimetype.split('/')[1].split(';')[0]
                filename_full = "%s.%s" % (filename, fileext)
            else:
                filename_full = filename
            filepath = self._create_unique_filepath(os.path.join(self._storage_dir, filename_full))
            if self._write(filedata, filepath):
                logger.info("Wrote %s" % filepath)
            else:
                sys.exit(1)
