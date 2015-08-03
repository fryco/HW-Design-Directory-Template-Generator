__version__ = '2.0'
import os
import errno
from sys import platform as _platform
import re

# Backslash alignment between different OSes
if _platform == "linux" or _platform == "linux2":
   # Linux
    slash = '/'
elif _platform == "win32":
   # Windows
    slash = '\\'

# Project client name.
clientName = 'MalyGrubyBenek'

# If 'projectName' will be empty, script will fetch current directory
# name and uses it as project name.
projectName = 'TeleboobleMator'

if not projectName:
    projectName = os.path.relpath(".","..")
    
# Most work will be done with KiCAD EDA so it will be default value of
# 'toolName'. If you are using different software, please put its name
# here.
toolName = 'KiCAD'


dirTemplateFilename = "DirectoryTemplate.txt"
fileContainer = []
fileContent   = []

def __CreateDir(dirName):
    try:
        os.makedirs(dirName)
##        print "###\n### Directory %s has been created" \
##        % dirName
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        else:
            pass
##            print "###\n### BE CAREFUL! Directory %s already exists.\n###" \
##            % dirName
            
def __SaveFile(string, fname):
    with open(fname, "w") as textFile:
        textFile.write(string)

def __CreateFile(string, fname, overwrite=False):
    if overwrite:
        __SaveFile(string, fname)
    else:
        if not os.path.exists(fname):
            __SaveFile(string, fname)

def __CreateDummyFile(fname, overwrite=False):
    if overwrite:
        __SaveFile("", fname)
    else:
        if not os.path.exists(fname):
            __SaveFile("", fname)            
                
def __ReadFile(filename):
    with open(filename, "r") as textFile:
        result = list(textFile)        
    return result

def ParseDirTemplate(template):
    rootPattern    = r'(\\---)'
    dirPattern     = r'(.\+---)'
    lastDirPattern = r'(.\\---)'
    filePattern    = r'(.#---)'    

    rdPat  = re.compile(rootPattern)
    dPat   = re.compile(dirPattern)
    ldPat  = re.compile(lastDirPattern)
    fPat   = re.compile(filePattern)
    
    structure = []
    parent = "root"

    for line in dirTemplate:
        if rdPat.match(line):
            result = line.rfind("\\")
            structure.append(["root", result,line[result+4:].rstrip("\n")])
        elif dPat.search(line):
            result = line.rfind("+")         
            structure.append(["dir", result/4, line[result+4:].rstrip("\n")])
        elif ldPat.search(line):
            result = line.rfind("\\")         
            structure.append(["dir", result/4, line[result+4:].rstrip("\n")])            
        elif fPat.search(line):
            result = line.rfind("#")         
            structure.append(["file", result/4, line[result+4:].rstrip("\n")])
        else:
            print "Incorrect syntax or empty line!!"
    return structure      
    
def __DebugPrint(structure,i):
    print "### "+str(i)+"\nMode:  "+structure[i][0]+"\nDepth: "+str(structure[i][1])+"\nName:  "+structure[i][2]

def __UpdatePath(oldPath, depthLevel):
    result = ""
    tmpPath = oldPath.split(slash)
    for i in range(0,depthLevel,1):
        del tmpPath[-1]

    for elem in tmpPath:
        result += elem+slash
    return result

def CreatePaths(structure):
    lastDepth     = -1
    lastMode      = ""
    lastPath      = ""
    currentPath   = ""
    previousDir   = ""
    idx           = 0
    rootPath = os.getcwd()+slash
    
    for line in structure:
        if structure[idx][0] == "root":
            lastMode  = structure[idx][0]
            lastDepth = structure[idx][1]
            lastPath  = rootPath+structure[idx][2]
            lastDir   = structure[idx][2]
            __CreateDir(lastPath)
            idx +=1
        elif structure[idx][0] == "dir":
            if lastMode == "root" and lastDepth < structure[idx][1]:
                lastMode  = structure[idx][0]
                lastDepth = structure[idx][1]
                lastPath  = lastPath+slash+structure[idx][2]
                lastDir   = structure[idx][2]
                __CreateDir(lastPath)
            elif lastMode == "dir" and lastDepth < structure[idx][1]:
                lastMode  = structure[idx][0]
                lastDepth = structure[idx][1]
                lastPath  = lastPath+slash+structure[idx][2]
                lastDir   = structure[idx][2]
                __CreateDir(lastPath)
            elif lastMode == "dir" and lastDepth == structure[idx][1]:
                lastMode  = structure[idx][0]
                lastDepth = structure[idx][1]
                lastPath  = __UpdatePath(lastPath, 1)+structure[idx][2]
                lastDir   = structure[idx][2]
                __CreateDir(lastPath)
            elif lastMode == "dir" and lastDepth > structure[idx][1]:
                lastMode  = structure[idx][0]
                depthDiff = lastDepth - structure[idx][1]
                lastDepth = structure[idx][1]             
                newPath   = __UpdatePath(str(lastPath), depthDiff+1)+structure[idx][2]
                lastPath  = newPath
                lastDir   = structure[idx][2]
                __CreateDir(lastPath)             
            else:
                print "Error!"

            idx += 1           
        elif structure[idx][0] == "file":
            if structure[idx][1] > lastDepth:
                fileContainer.append(lastPath+slash+structure[idx][2])
            elif structure[idx][1] == lastDepth:
                fileContainer.append(__UpdatePath(lastPath,1)+structure[idx][2])
            else:
                print "Error in file!"
            idx += 1
        else:
            print "Generic error!!!!!!!!!!!!!!"
        if idx>=len(structure):
            break
        
def PersonalizeProject(structure):
    idx  = 0
    
    for line in structure:
        if structure[idx][2] == "_ProjectName":
            structure[idx][2] = projectName
        if structure[idx][2] == "_ClientName":
            structure[idx][2] = clientName
        if structure[idx][2].find("EDATool"):
            structure[idx][2] = structure[idx][2].replace("EDATool", toolName)
        idx += 1  

def FillTextFiles(fContainer, fContent):
    idx = 0

    for path in fContainer:
        __CreateFile(fContent[idx], path)

        
##############        
projectNameReadMe = \
"""Design Files - place this directory on a server with regular backup.
Release Files - place this directory on a server with regular backup. Once released, NEVER CHANGE THESE FILES and DO NOT WORK IN THIS DIRECTORY!
Work - place this directory on your computer.
"""
fileContent.append(projectNameReadMe)

edaToolIntegratedLibrary = \
"""Place for """+toolName+""" Library files
"""
fileContent.append(edaToolIntegratedLibrary)

model3D = \
"""Place STEP files of 3D models here.
"""
fileContent.append(model3D)

edaToolTemplates = \
"""Place for """+toolName+""" templates, e.g for BOMs
"""
fileContent.append(edaToolTemplates)

designFilesProjectName = \
"""Examples of other directory names:
V1I1A - only BOM changes
V1I2 - pin compatible with V1I1, no big changes
V2I1 - not compatible with V1


This is also place for backups. Pack V1I1 Directory, add date and possibly a note:
V1I1 2011 01 10
V1I1 2011 02 21 Schematic Checked
"""
fileContent.append(designFilesProjectName)

backupInfo = \
"""Directory where BackMeUp.py is saving backups.
"""
fileContent.append(backupInfo)

backMeUpScript = \
"""__version__ = '1.3'
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
    slash = "\\\\"
    
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
    timestamp = time.time()
    zfTimestamp  = \\
    datetime.datetime.fromtimestamp(timestamp).strftime("%Y%m%d_%H%M%S")
    bckTimestamp = \\
    datetime.datetime.fromtimestamp(timestamp).strftime("%H:%M:%S %d.%m.%Y")
    zfName = zfTimestamp+'_'+revision+'.zip'
    os.chdir("."+slash+"Backup")
    zf = zipfile.ZipFile(zfName, "w")
    os.chdir("..")
    for dirname, subdirs, files in os.walk(revision):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    with open(backupInfoFile, "a") as f:
        f.write("\\n\\nTimestamp: "+bckTimestamp)
    zf.write(backupInfoFile)
    zf.close()
    open(backupInfoFile, 'w').close()
    print "Backup is done. Zip file:", zfName
else:
    print "Backup info is empty! \\
    \\nPlease add description to backupInfo.txt and re-run this script again!"

print "Press any key to continue..."
raw_input()

"""
fileContent.append(backMeUpScript)

docs = \
"""Copy all created documents (doc, xls, pdf) directly here, or create new subfolders e.g. Manual, ...
"""
fileContent.append(docs)

viIi = \
"""Place here """+toolName+""" Design Files
After release, keep record about any required changes in TODO directory.
"""
fileContent.append(viIi)

viIiFw = \
"""All the files needed for CPLD, EEPROMs, uController, BIOS, ...
"""
fileContent.append(viIiFw)

viIiTodo = \
"""Here describe all the things which have to be improved or done in the next revision.

Schematic:


PCB:


Production:


Firmware:
"""
fileContent.append(viIiTodo)

#For VxIx
fileContent.append(viIi)
fileContent.append(viIiFw)
fileContent.append(viIiTodo)

releaseWrn = \
"""ONCE RELEASED: 
- NEVER EVER CHAGE THE FILES IN THESE DIRECTORIES!
- NEVER WORK IN THESE DIRECTOTRIES (do not open files directly from these folders)

WHEN YOU START A NEW BOARD ISSUE, ALWAYS COPY AND USE FILES FROM THESE RELEASE DIRECTORIES AS STARTING POINT 
AND THEN READ TODO file at!
"""
fileContent.append(releaseWrn)

info = \
"""Use same naming for folders as in ! """+toolName+""" Source Files
"""
fileContent.append(info)

## RELEASE for V1I1
releasedModel3D = \
"""Place following files here:

3D step file
3D pdf

"""
fileContent.append(releasedModel3D)

releasedBrdAsm = \
"""Place following files here:

- Mechanical Drawing (Board dimensions, holes position, ..)
- TOP and BOTTOM Assembly Drawing (Component position with Reference Designator)
- TOP and BOTTOM VIEW (shows board outline, assembly layer, TOP + BOTTOM layers)
- Bill of Materials (grouped by component type)
- Component reference BOM (each component on one line: Designator, Description, Manufacturer 1,
  Manufacturer, Part Number 1, Package / Case, Supplier 1, Supplier Part Number 1)
- Pick and Place
- TOP and BOTTOM Layer + TOP and BOTTOM Paste Gerber Files (for stencil - if panel is done in a PCB house, ask them later for the top/bottom layers and paste for the panel)
- PDF 3D Model

"""
fileContent.append(releasedBrdAsm)

releasedFrm = \
"""All the files needed for CPLD, EEPROMs, uController, BIOS, ...

Start file name with component designator - the one where the file needs to be stored e.g:
U5 - AMI BIOS 0ABVQ018
U15 - Ethernet EEPROM 82574 
"""
fileContent.append(releasedFrm)

releasedPcbManufacturing = \
"""Place PCB stackup information here.
"""
fileContent.append(releasedPcbManufacturing)

releasedGerberOut = \
"""Place here gerber files.
"""
fileContent.append(releasedGerberOut)

releasedDiffLayers = \
"""Highlight differential pairs and Take screenshots of each layer. Examples of naming screenshots:

DIFF100-L1.jpg
DIFF100-L3.jpg
DIFF90-L1.jpg
...

Why? If manufacturer can not find a particular DIFF pair on one of the layers, they will contact you. 
By providing them these screenshots, they can check it by themselves.

"""
fileContent.append(releasedDiffLayers)

releasedDrill = \
"""Place here drill files and documents which explain it (e.g. for HDI PCB you can put here pdf showing drills for each layer pair)
"""
fileContent.append(releasedDrill)

releasedSch = \
"""Update Schematic Cover Page to RELEASED DD-MMM-YYYY
Place here PDF version of schematic, if possible one for each BOM variant.
"""
fileContent.append(releasedSch)

releasedSrc = \
"""Place here zip file of source files, e.g copy and pack here directory from:\n"""+\
"."+slash+projectName+clientName+slash+"Design Files"+slash+clientName+slash+\
projectName+slash+"VxIx"+slash+\
"\nwhere VxIx is the latest project version ready to release."
fileContent.append(releasedSrc)
## RELEASE for VxIx
fileContent.append(releasedModel3D)
fileContent.append(releasedBrdAsm)
fileContent.append(releasedFrm)
fileContent.append(releasedPcbManufacturing)
fileContent.append(releasedGerberOut)
fileContent.append(releasedDiffLayers)
fileContent.append(releasedDrill)
fileContent.append(releasedSch)
fileContent.append(releasedSrc)

## WORK for V1I1
similarProducts = \
"""Create a directory with Competition Company name and place all documents about their similar produtcs there.
"""
fileContent.append(similarProducts)

datasheets = \
"""For components with one datasheet only, these can be place directly here.

For components with more then one datasheet, create a directory, e.g:
Intel
Ethernet
"""
fileContent.append(datasheets)

designGuides = \
"""Place all design guide, schematic / layout check documents, length & power calculators here.
"""
fileContent.append(designGuides)

devBrds = \
"""Create a directory with Board name and copy there all the files from manufacturer.
"""
fileContent.append(devBrds)

errata = \
"""Place all the errate files here.
"""
fileContent.append(errata)

software = \
"""Place here all software related files: Apllications, Drivers, Tools, ...
"""
fileContent.append(software)
## WORK for VxIx
fileContent.append(similarProducts)
fileContent.append(datasheets)
fileContent.append(designGuides)
fileContent.append(devBrds)
fileContent.append(errata)
fileContent.append(software)

##
## MAIN
##

dirTemplate = __ReadFile(dirTemplateFilename)
structure = ParseDirTemplate(dirTemplate)
PersonalizeProject(structure)
CreatePaths(structure)

##for line in structure:
##    print line
print len(fileContent)
for idx, line in enumerate(fileContainer):
    __SaveFile(fileContent[idx],line)


