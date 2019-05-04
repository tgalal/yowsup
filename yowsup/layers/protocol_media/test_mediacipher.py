from yowsup.layers.protocol_media.mediacipher import MediaCipher
import base64
import unittest


class MediaCipherTest(unittest.TestCase):
    IMAGE = (
        b'EOnnZIBu1vTSI51IeJvaKR+8W1FqBETATI2Ikl6nVQ8=',

        b'/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8M'
        b'CgsOCwkJDRENDg8QEBEQCgwSExIQEw8QEBD/2wBDAQMDAwQDBAgEBAgQCwkLEBAQEBAQEBAQEBAQEBAQEBAQ'
        b'EBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBD/wAARCAABAAEDAREAAhEBAxEB/8QAHwAAAQUBAQEB'
        b'AQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKB'
        b'kaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1'
        b'dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl'
        b'5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcF'
        b'BAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5'
        b'OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0'
        b'tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9U6AP/9k'
        b'==',

        b'dT9YPFSz4dprkH6uiXPEVERGZVIZbGYHzwue21WoLP1RCE2wmu11M8n6ysfROPtI39DCRFQhBBEVGFCT/nfV'
        b'pt+fouIENBSXY44mR2en4HGvRR//dlM5OBLz2WuEOf01iKPazGtfacy6lnV0X5JagL4r1mKeyuSXJEV81kxj'
        b'Vd3OArpLKt13XM36PcnTd/U6DHOV6Vf982Wc1UjR7kMb5JT+HlWrvz9CCGMTX5mqBYWEr3InCFyrmaZu8DXC'
        b'60YUZCPLTHJP0hFQA1ooKQks4f3F39tzVL3dbX3io7XPQiSgHN6nuPCD0PF7dWINep+amk+ODjeQd/o2guqx'
        b'O/AngNIxfFWq3915jMQWAXeARUFw7x+9Qx93UWC/sfQ72nTqdQaH5W4vsMUKaocZcAJ7YWudKo5Y15uo3ulP'
        b'744Cyo54tvxUSV0zLC90LYCe8fJefREjreO73RlVqoynTyFHuVS7/YMnesO5lCHZJ2NpHuzpGKCU08RgCuSr'
        b'K/wh4SLXZ1nhZEYX/xY4cDO7swrA3Y3Qt0gjFzNBfUT9aABQaU+WHY8pBS/oVfJsuj2iod2fsW8UoplImoOk'
        b'bosYlMkdZSIfwBQ5kt3On2d+HPUNt7HVZWRECFj0C4IHhZCZIJw0wFmPMOiIHyzittXGb45uJA2Sd1gnRbw0'
        b'1XFuoIyvS7z0MtW0QUiD6kaJFBkpTo7hxN/HyN8xQwOkeBcKORdpeSp62iPBuRvel9I2p07it7UyYhzas+Jv'
        b'tl6i+hIz6Z5nzQEZ+zPAYxDmoy4h9GQuXUivTzU9I0/Sd4QvM3rfewGeXsNSjWI1CLVZG+4wL1TPCbQGaHEB'
        b'NF8zmpTMYV+NvCzv/2DwYuYoiUI='
    )

    def setUp(self):
        self._cipher = MediaCipher()  # type: MediaCipher

    def test_decrypt_image(self):
        media_key, media_plaintext, media_ciphertext = map(base64.b64decode, self.IMAGE)
        self.assertEqual(media_plaintext, self._cipher.decrypt_image(media_ciphertext, media_key))

    def test_encrypt_image(self):
        media_key, media_plaintext, media_ciphertext = map(base64.b64decode, self.IMAGE)
        encrypted = self._cipher.encrypt(media_plaintext, media_key, MediaCipher.INFO_IMAGE)
        self.assertEqual(media_ciphertext, encrypted)
