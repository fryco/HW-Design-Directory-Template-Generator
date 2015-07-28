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

def __CreateDir(dirName):
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
            
def __SaveFile(string, fname):
    with open(fname, "w") as textFile:
        textFile.write(string)

def __CreateFile(string, overwrite=False,fname="read_me.txt"):
    if overwrite:
        SaveFile(string, fname)
    else:
        if not os.path.exists(fname):
            SaveFile(string, fname)
                
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

def __DebugPrintE(structure,i, mode):
    print mode+' '+str(i)+"\nMode:  "+structure[i][0]+"\nDepth: "+str(structure[i][1])+"\nName:  "+structure[i][2]

def __UpdatePath(oldPath, depthLevel):
    result = ""
    tmpPath = oldPath.split(slash)
    for i in range(0,depthLevel,1):
        del tmpPath[-1]

    for elem in tmpPath:
        result += elem+slash
    return result

def __GoUp(height):
    for level in xrange(0,height,1):
        os.chdir("..")

def __GoDown(directory):
    os.chdir(os.getcwd()+slash+directory)
    
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
            print lastPath
            
            idx +=1
        elif structure[idx][0] == "dir":
            if lastMode == "root" and lastDepth < structure[idx][1]:
                lastMode  = structure[idx][0]
                lastDepth = structure[idx][1]
                lastPath  = lastPath+slash+structure[idx][2]
                lastDir   = structure[idx][2]
                print lastPath
            elif lastMode == "dir" and lastDepth < structure[idx][1]:
                lastMode  = structure[idx][0]
                lastDepth = structure[idx][1]
                lastPath  = lastPath+slash+structure[idx][2]
                lastDir   = structure[idx][2]
                print lastPath
            elif lastMode == "dir" and lastDepth == structure[idx][1]:
                lastMode  = structure[idx][0]
                lastDepth = structure[idx][1]
                lastPath  = __UpdatePath(lastPath, 1)+structure[idx][2]
                lastDir   = structure[idx][2]
                print lastPath
            elif lastMode == "dir" and lastDepth > structure[idx][1]:
                lastMode  = structure[idx][0]
                depthDiff = lastDepth - structure[idx][1]
                lastDepth = structure[idx][1]             
                newPath   = __UpdatePath(str(lastPath), depthDiff+1)+structure[idx][2]
                lastPath  = newPath
                lastDir   = structure[idx][2]
                print lastPath                  
            else:
                print "Error!"

            idx += 1           
        elif structure[idx][0] == "file":
            print "file"+str(idx)              

            idx += 1
        else:
            print "Generic error!!!!!!!!!!!!!!"
        if idx>=len(structure):
            break

                 
##############
dirTemplate = __ReadFile(dirTemplateFilename)

structure = ParseDirTemplate(dirTemplate)
##print len(structure)
CreatePaths(structure)

##for line in structure:
##    print line
##


