__version__ = '1.4'
import os
import zipfile
import time
import datetime
from sys import platform as _platform

## Put here correct revision number. It should be the same
## as directory name
revision = "V1I1"

# Backslash alignment between different OSes
if _platform == "linux" or _platform == "linux2":
   # Linux
    slash = "/"
elif _platform == "win32":
   # Windows
    slash = "\\"
    
## Put brief description about what have been done in
## this revision in backupInfo.txt and/or update TODO
## info in dedicated directory. If file will be empty
## you will be asked to fill it.
backupInfoFile = "backupInfo.txt"

if not os.path.exists(backupInfoFile):
    open(backupInfoFile, 'a').close()
    
with open(backupInfoFile, 'rb+') as f: 
    backupInfo = f.readlines() 
    
if backupInfo:
    if not os.path.exists("Backup"):
        os.makedirs("Backup")
    prjName = os.path.basename(os.getcwd())
    timestamp = time.time()
    zfTimestamp  = \
    datetime.datetime.fromtimestamp(timestamp).strftime("%Y%m%d_%H%M%S")
    bckTimestamp = \
    datetime.datetime.fromtimestamp(timestamp).strftime("%H:%M:%S %d.%m.%Y")
    zfName = prjName+'_'+revision+'_'+zfTimestamp+'.zip'
    os.chdir("."+slash+"Backup")
    zf = zipfile.ZipFile(zfName, "w")
    os.chdir("..")
    for dirname, subdirs, files in os.walk(revision):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    with open(backupInfoFile, "a") as f:
        f.write("\n\nTimestamp: "+bckTimestamp)
    zf.write(backupInfoFile)
    zf.close()
    open(backupInfoFile, 'w').close()
    print "Backup is done. Zip file:", zfName
else:
    print "Backup info is empty! \
    \nPlease add description to backupInfo.txt and re-run this script again!"

print "Press any key to continue..."
raw_input()

