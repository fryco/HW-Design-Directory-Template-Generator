################################################################
## IMPORTANT! If you modify this file, please copy&paste it    #
## to variable 'backMeUpScript' in HwDirectoryTreeGenerator.py.#
## Without this step any changes WILL NOT BE PRESENT!          #
##                                                             #
## NOTE: to keep desired behaviour in target script you have   #
## to pay attention and double all backslashes ('\\' instead   #
## of '\') before you copy this script to dedicated variable!  #
## Also keep version updated to easy changes tracking.         #
################################################################
__version__ = '1.1'
import os
import zipfile
import time
import datetime

## Put here correct revision number. It should be the same
## as directory name
revision = "V1I1"

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
    timestamp = time.time()
    zfTimestamp  = \
    datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d_%H%M%S')
    bckTimestamp = \
    datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S %d.%m.%Y')
    zfName = zfTimestamp+'_'+revision+'.zip'        
    zf = zipfile.ZipFile(zfName, "w")
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
