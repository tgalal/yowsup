from axolotl.kdf.hkdfv3 import HKDFv3
from axolotl.util.byteutil import ByteUtil

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii
import hmac
import hashlib


class MediaCipher(object):
    INFO_IMAGE = binascii.unhexlify(b'576861747341707020496d616765204b657973')
    INFO_AUDIO = binascii.unhexlify("576861747341707020417564696f204b657973")
    INFO_VIDEO = binascii.unhexlify("576861747341707020566964656f204b657973")
    INFO_DOCUM = binascii.unhexlify("576861747341707020446f63756d656e74204b657973")

    def encrypt_image(self, plaintext, ref_key):
        return self.encrypt(plaintext, ref_key, self.INFO_IMAGE)

    def encrypt_audio(self, ciphertext, ref_key):
        return self.encrypt(ciphertext, ref_key, self.INFO_AUDIO)

    def encrypt_video(self, ciphertext, ref_key):
        return self.encrypt(ciphertext, ref_key, self.INFO_VIDEO)

    def encrypt_document(self, ciphertext, ref_key):
        return self.encrypt(ciphertext, ref_key, self.INFO_DOCUM)

    def decrypt_image(self, ciphertext, ref_key):
        return self.decrypt(ciphertext, ref_key, self.INFO_IMAGE)

    def decrypt_audio(self, ciphertext, ref_key):
        return self.decrypt(ciphertext, ref_key, self.INFO_AUDIO)

    def decrypt_video(self, ciphertext, ref_key):
        return self.decrypt(ciphertext, ref_key, self.INFO_VIDEO)

    def decrypt_document(self, ciphertext, ref_key):
        return self.decrypt(ciphertext, ref_key, self.INFO_DOCUM)

    def encrypt(self, plaintext, ref_key, media_info):
        derived = HKDFv3().deriveSecrets(ref_key, media_info, 112)
        parts = ByteUtil.split(derived, 16, 32)
        iv = parts[0]
        key = parts[1]
        mac_key = derived[48:80]

        cipher_encryptor = Cipher(
            algorithms.AES(key), modes.CBC(iv), backend=default_backend()
        ).encryptor()
        ciphertext = cipher_encryptor.update(plaintext) + cipher_encryptor.finalize()

        mac = hmac.new(mac_key, digestmod=hashlib.sha256)
        mac.update(iv)
        mac.update(ciphertext)

        return ciphertext + mac.digest()[:10]

    def decrypt(self, ciphertext, ref_key, media_info):
        derived = HKDFv3().deriveSecrets(ref_key, media_info, 112)
        parts = ByteUtil.split(derived, 16, 32)
        iv = parts[0]
        key = parts[1]
        mac_key = derived[48:80]
        media_ciphertext = ciphertext[:-10]
        mac_value = ciphertext[-10:]

        mac = hmac.new(mac_key, digestmod=hashlib.sha256)
        mac.update(iv)
        mac.update(media_ciphertext)

        if mac_value != mac.digest()[:10]:
            raise ValueError("Invalid MAC")

        cipher_decryptor = Cipher(
            algorithms.AES(key), modes.CBC(iv), backend=default_backend()
        ).decryptor()

        return cipher_decryptor.update(media_ciphertext) + cipher_decryptor.finalize()
