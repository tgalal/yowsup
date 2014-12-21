import hkdf
class HKDFv2(hkdf.HKDF):
    def getIterationStartOffset(self):
        return 0