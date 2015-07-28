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
projectName = 'TelebulbleMator'

if not projectName:
    projectName = os.path.relpath(".","..")
    
# Most work will be done with KiCAD EDA so it will be default value of
# 'toolName'. If you are using different software, please put its name
# here.
toolName = 'KiCAD'


dirTemplateFilename = "DirectoryTemplate.txt"
fileContainer = []

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
##                fileContainer.append(lastPath+slash+structure[idx][2])
                __CreateDummyFile(lastPath+slash+structure[idx][2])
            elif structure[idx][1] == lastDepth:
##                fileContainer.append(__UpdatePath(lastPath,1)+structure[idx][2])
                __CreateDummyFile(__UpdatePath(lastPath,1)+structure[idx][2])
            else:
                print "Error in file!"
            idx += 1
        else:
            print "Generic error!!!!!!!!!!!!!!"
        if idx>=len(structure):
            break

                 
##############
dirTemplate = __ReadFile(dirTemplateFilename)

structure = ParseDirTemplate(dirTemplate)
PersonalizeProject(structure)
CreatePaths(structure)

for line in structure:
    print line

for line in fileContainer:
    print line

