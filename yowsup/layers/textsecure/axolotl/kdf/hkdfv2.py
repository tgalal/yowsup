from hkdf import HKDF

class HKDFv2(HKDF):
    def getIterationStartOffset(self):
        return 0