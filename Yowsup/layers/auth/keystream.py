import hashlib, hmac, sys
from struct import pack
from operator import xor
from itertools import starmap



def _bytearray(data):

      if type(data) == str:
            return data
      elif type(data) == list:
            tmp = [chr(x) if type(x) == int else x for x in data]
            return "".join(tmp)
      elif type(data) == int:
            tmp = ""
            return [0] * data

      return ""

class RC4:
    def __init__(self, key, drop):
        self.s = []
        self.i = 0;
        self.j = 0;

        self.s = [0] * 256

        for i in range(0, len(self.s)):
            self.s[i] = i

        for i in range(0, len(self.s)):
            self.j = (self.j + self.s[i] + ord(key[i % len(key)])) % 256
            RC4.swap(self.s, i, self.j)
        self.j = 0;
        self.cipher(_bytearray(drop), 0, drop)


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

            data[num2] = ord(data[num2]) if type(data[num2]) == str else data[num2]
            data[num2] = (data[num2] ^ self.s[(self.s[self.i] + self.s[self.j]) % 256])

    @staticmethod
    def swap(arr, i, j):
        tmp = arr[i]
        arr[i] = arr[j]
        arr[j] = tmp


if sys.version_info >= (3, 0):
  buffer = lambda x: bytes(x, 'iso-8859-1') if type(x) is str else bytes(x)
  _bytearray = lambda x: [0]*x if type(x) is int else x

class KeyStream:

    def __init__(self, key, macKey):
        self.key = key if sys.version_info < (3, 0) else bytes(key, 'iso-8859-1')
        self.rc4 = RC4(self.key, 0x300)
        self.macKey = macKey if sys.version_info < (3, 0) else bytes(macKey, 'iso-8859-1')
        self.seq = 0

    def computeMac(self, bytes_buffer, int_offset, int_length):
        mac = hmac.new(self.macKey, None, hashlib.sha1)
        mac.update(buffer(_bytearray(bytes_buffer[int_offset:])))

        numArray = "%s%s%s%s" % (chr(self.seq >> 24), chr(self.seq >> 16), chr(self.seq >> 8), chr(self.seq))

        mac.update(buffer(_bytearray(numArray)))

        self.seq += 1
        return mac.digest()

    def decodeMessage(self, bufdata, macOffset, offset, length):
        buf = bufdata[:-4]
        hashed = bufdata[-4:]
        numArray = self.computeMac(buf, 0, len(buf))

        numArray = [ord(x) for x in numArray.decode('iso-8859-1')];

        num = 0
        while num < 4:
            if numArray[macOffset + num] == hashed[num]:
                num += 1
            else:
                raise Exception("INVALID MAC")

        self.rc4.cipher(buf, 0, len(buf))

        return [x for x in buf]

    def encodeMessage(self, buf, macOffset, offset, length):
        self.rc4.cipher(buf, offset, length)
        hashed = self.computeMac(buf, offset, length)

        numArray = [ord(x) for x in hashed.decode('iso-8859-1')]

        output = buf[0:macOffset] + numArray[0:4] + buf[macOffset+4:]

        return [x for x in output]

    @staticmethod
    def generateKeys(password, nonce):
        _bytes = [0] * 4
        numArray = [1,2,3,4]

        if sys.version >= (3, 0):
            nonce = nonce.encode('iso-8859-1')

        for j in range(0, len(numArray)):
            noncex = nonce + chr(numArray[j])
            _bytes[j] = KeyStream.pbkdf2(password, noncex, 2, 20)

        return _bytes

    @staticmethod
    def pbkdf2( password, salt, itercount, keylen, hashfn = hashlib.sha1 ):
        def pbkdf2_F( h, salt, itercount, blocknum ):
            def prf( h, data ):
                hm = h.copy()
                hm.update( buffer(_bytearray(data)) )
                d = hm.digest()
                return [ord(i) for i in d.decode('iso-8859-1')]

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

        h = hmac.new( password, None, hashfn )

        T = []
        for i in range(1, l+1):
            tmp = pbkdf2_F( h, salt, itercount, i )
            T.extend(tmp)
        T = [chr(i) for i in T]
        return "".join(T[0: keylen])