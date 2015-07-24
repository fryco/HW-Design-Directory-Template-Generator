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
clientName = '_ClientName'

# If 'projectName' will be empty, script will fetch current directory
# name and uses it as project name.
projectName = '_ProjectName'

if not projectName:
    projectName = os.path.relpath(".","..")
    
# Most work will be done with KiCAD EDA so it will be default value of
# 'toolName'. If you are using different software, please put its name
# here.
toolName = '_ToolName'

# If you want to create root directory named as projectName you have
# to set this flag to True. It depends on user needs:
#    - if user is using Git or SVN it is better to use False. After
#      creating repository user should copy script into repo dir and run it.
#    - if user is not using any control version system it is better to put
#      script in dedicated directory with all HW projects, set flag to True
#      and perform manual setup before script will be run. In this case
#      user can do manual version control and backup with BackMeUp.py script.
projectNameAsRootDir = False

dirTemplateFilename = "DirectoryTemplate.txt"

def CreateDir(dirName):
    try:
        os.makedirs(dirName)
        print "###\n### Directory %s has been created" \
        % dirName
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        else:
            print "###\n### BE CAREFUL! Directory %s already exists.\n###" \
            % dirName
            
def SaveFile(string, fname):
    with open(fname, "w") as textFile:
        textFile.write(string)

def CreateFile(string, overwrite=False,fname="read_me.txt"):
    if overwrite:
        SaveFile(string, fname)
    else:
        if not os.path.exists(fname):
            SaveFile(string, fname)
                
def ReadFile(filename):
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
    
    for line in dirTemplate:
        if rdPat.match(line):
            result = line.rfind("\\")
            structure.append(("root", result,line[result+4:].rstrip("\n")))
        elif dPat.search(line):
            result = line.rfind("+")         
            structure.append(("ndir", result/4, line[result+4:].rstrip("\n")))
        elif ldPat.search(line):
            result = line.rfind("\\")         
            structure.append(("ldir", result/4, line[result+4:].rstrip("\n")))
        elif fPat.search(line):
            result = line.rfind("#")         
            structure.append(("file", result/4, line[result+4:].rstrip("\n")))
        else:
            print "Incorrect syntax or empty line!!"
    return structure

def GoUp(height):
    for level in xrange(0,height,1):
        os.chdir("..")

def GoDown(directory):
    os.chdir(os.getcwd()+slash+directory)
        
def DebugPrint(structure,i):
    print "Mode: "+structure[i][0]+" Depth: "+str(structure[i][1])+" Name: "+structure[i][2]  

def CreateDirectoryTree(structure):
    i = 0
    currrentMode = ""    
    currentDepth = 0
    print len(structure)
    for i in xrange(0,len(structure),1):
        if structure[i][0] == "root":
            currentMode  = structure[i][0]            
            currentDepth = structure[i][1]
            CreateDir(structure[i][2])
            GoDown(structure[i][2])
            DebugPrint(structure,i)
        elif structure[i][0] == "ndir":
            if currentDepth - structure[i][1] < 0:
                currentMode  = structure[i][0]            
                currentDepth = structure[i][1]
                CreateDir(structure[i][2])
                GoDown(structure[i][2])                
                DebugPrint(structure,i)                
            elif currentDepth == structure[i][1]:
                 currentMode  = structure[i][0]
                 CreateDir(structure[i][2])
                 DebugPrint(structure,i)
            elif currentDepth > structure[i][1]:
                 GoUp(currentDepth - structure[i][1])
                 currentMode  = structure[i][0]            
                 currentDepth = structure[i][1]
                 CreateDir(structure[i][2])
                 GoDown(structure[i][2])                                 
                 DebugPrint(structure,i)
        elif structure[i][0] == "ldir":
                pass
        elif structure[i][0] == "file":
                pass
        else:
            print "ERROR!"
            
##############
dirTemplate = ReadFile(dirTemplateFilename)
structure = ParseDirTemplate(dirTemplate)

for line in structure:
    print line


