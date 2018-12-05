import sys
import base64
import zipfile
import hashlib

if len(sys.argv) < 2:
    print("Usage: python dexMD5.py <WhatsApp.apk>")
    exit()
else:
    apkFile = sys.argv[1]
try:
    zipFile = zipfile.ZipFile(apkFile,'r')
    classesDexFile = zipFile.read('classes.dex')
    hash = hashlib.md5()
    hash.update(classesDexFile)

    version = classesDexFile.decode("utf-8", errors = 'ignore').partition('App: ')[-1].partition(',')[0]

    print("Version: " + version)
    print("ClassesDex: " + base64.b64encode(hash.digest()).decode("utf-8"));
except Exception as e:
    print(sys.argv[1] + " not found.")
