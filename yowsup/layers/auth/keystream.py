import hashlib, hmac, sys
from struct import pack
from operator import xor
from itertools import starmap

class RC4:
    def __init__(self, key, drop):
        self.s = []
        self.i = 0;
        self.j = 0;

        self.s = [0] * 256

        for i in range(0, len(self.s)):
            self.s[i] = i

        for i in range(0, len(self.s)):
            self.j = (self.j + self.s[i] + key[i % len(key)]) % 256
            RC4.swap(self.s, i, self.j)

        self.j = 0;
        self.cipher(bytearray(drop), 0, drop)


    def cipher(self, data, offset, length):
        while True:
            num = length
            length = num - 1

            if num == 0: break

            self.i = (self.i+1) % 256
            self.j = (self.j + self.s[self.i]) % 256

            RC4.swap(self.s, self.i, self.j)

            num2 = offset
            offset = num2 + 1

            data[num2] = (data[num2] ^ self.s[(self.s[self.i] + self.s[self.j]) % 256])

    @staticmethod
    def swap(arr, i, j):
        tmp = arr[i]
        arr[i] = arr[j]
        arr[j] = tmp


class KeyStream:

    def __init__(self, key, macKey):
        self.key = key if sys.version_info < (3, 0) else bytes(key)
        self.rc4 = RC4(self.key, 0x300)
        self.macKey = str(macKey) if sys.version_info < (3, 0) else bytes(macKey)
        self.seq = 0

    def computeMac(self, bytes_buffer, int_offset, int_length):
        mac = hmac.new(self.macKey, None, hashlib.sha1)
        updateData = bytes_buffer[int_offset:] + bytearray([self.seq >> 24, self.seq >> 16, self.seq >> 8, self.seq])

        try:
            mac.update(updateData)
        except TypeError: #python3 support
            mac.update(bytes(updateData))

        self.seq += 1
        return bytearray(mac.digest())

    def decodeMessage(self, bufdata, macOffset, offset, length):
        buf = bufdata[:-4]
        hashed = bufdata[-4:]
        numArray = self.computeMac(buf, 0, len(buf))

        num = 0
        while num < 4:
            if numArray[macOffset + num] == hashed[num]:
                num += 1
            else:
                raise Exception("INVALID MAC")

        self.rc4.cipher(buf, 0, len(buf))

        return buf

    def encodeMessage(self, buf, macOffset, offset, length):
        self.rc4.cipher(buf, offset, length)
        mac = self.computeMac(buf, offset, length)
        output = buf[0:macOffset] + mac[0:4] + buf[macOffset+4:]
        return output

    @staticmethod
    def generateKeys(password, nonce):
        resultBytes = []

        for i in range(1, 5):
            currNonce = nonce + bytearray([i])
            resultBytes.append(KeyStream.pbkdf2(password, currNonce, 2, 20))

        return resultBytes

    @staticmethod
    def pbkdf2( password, salt, itercount, keylen, hashfn = hashlib.sha1 ):
        def pbkdf2_F( h, salt, itercount, blocknum ):
            def prf( h, data ):
                hm = h.copy()
                try:
                    hm.update(bytearray(data))
                except TypeError: #python 3 support
                    hm.update(bytes(data))

                d = hm.digest()
                return bytearray(d)

            U = prf( h, salt + pack('>i',blocknum ) )
            T = U

            for i in range(2, itercount + 1):
                U = prf( h, U )
                T = starmap(xor, zip(T, U))
            return T

        digest_size = hashfn().digest_size
        l = int(keylen / digest_size)
        if keylen % digest_size != 0:
            l += 1
        
        h = hmac.new(bytes(password), None, hashfn )

        T = bytearray()
        for i in range(1, l+1):
            tmp = pbkdf2_F( h, salt, itercount, i )
            T.extend(tmp)
        
        return T[0: keylen]