from hkdf import HKDF

class HKDFv3(HKDF):
    def getIterationStartOffset(self):
        return 1