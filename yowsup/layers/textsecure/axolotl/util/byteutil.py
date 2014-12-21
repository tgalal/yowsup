class ByteUtil:

    @staticmethod
    def combine(*args):
        baos = bytearray()
        for a in args:
            if type(a) in (list, bytearray, str):
                baos.extend(a)
            else:
                baos.append(a)

        return baos

    # @staticmethod
    # def xsplit(inp, firstLength, secondLength, thirdLength = None):
    #     parts = []
    #     parts.append(inp[:firstLength])
    #     parts.append(inp[len(parts[0]): secondLength + 1])
    #     if thirdLength:
    #         parts.append(inp[len(parts[1]): thirdLength + 1])
    #     return parts

    @staticmethod
    def split(inp, firstLength, secondLength, thirdLength = None):
        parts = []
        parts.append(inp[:firstLength])
        parts.append(inp[firstLength:firstLength + secondLength])
        if thirdLength is not None:
            parts.append(inp[firstLength + secondLength: firstLength + secondLength + thirdLength])

        return parts


    @staticmethod
    def trim(inp, length):
        return inp[:length]

    @staticmethod
    def intsToByteHighAndLow(highValue, lowValue):
        highValue = ord(highValue) if type(highValue) is str else highValue
        lowValue = ord(lowValue) if type(lowValue) is str else lowValue
        return ((highValue << 4 | lowValue) & 0xFF) % 256

    @staticmethod
    def highBitsToInt(value):
        bit = ord(value) if type(value) is str else value
        return (bit & 0xFF) >> 4



    @staticmethod
    def intToByteArray(_bytes, offset, value):
        _bytes[offset + 3] = value % 256
        _bytes[offset + 2] = (value >> 8) % 256
        _bytes[offset + 1] = (value >> 16) % 256
        _bytes[offset] = (value >> 24) % 256

        return 4
