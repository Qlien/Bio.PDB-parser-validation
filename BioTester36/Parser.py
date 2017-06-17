import time
import re
from Bio.PDB import *
import os
import glob
import subprocess
import warnings
import xml.etree.cElementTree as XMLParser
from shutil import copyfile

def parseAndSaveToDatabase(filesDirectory, files, saveDirectory, PERMISSIVE=1, filesZipped=False, _7zipLocation="", deleteFileAfterError=False): #cnx is database connection

    listOfEntries = {}

    class WarningHackClass:
        listOfWarnings = []

    def convert_size(size_bytes):
        if size_bytes == 0:
            return 0
        s = int(round(size_bytes / 1024))
        return s

    xmlTree = XMLParser.Element("data")
    xmlErrors = XMLParser.Element("errors")

    for file in files:
        try:
            #overriding warning method to pass warnings to file
            WarningHackClass.listOfWarnings = []
            def customwarn(message, category, filename, lineno, file=None, line=None):
                warningString = warnings.formatwarning(message, category, filename, lineno)
                strintArray = re.sub(r'.*:\s', '', warningString).strip().split("\n")
                if strintArray[len(strintArray) - 1][-1:] == ')':
                    strintArray[len(strintArray) - 1] = strintArray[len(strintArray) - 1][:-1].strip()
                WarningHackClass.listOfWarnings.append(strintArray)
            warnings.showwarning = customwarn

            path = ""
            structureName = ""
            #unzips file if zipped
            if filesZipped:
                if _7zipLocation == "":
                    path = '7z' + "\" " + 'e ' + "\"" + filesDirectory + file + "\"" + ' -o' + "\"" + saveDirectory
                else:
                    #trying running 7zip from path
                    path = "\""+ _7zipLocation+ '7z.exe' + "\" "+ 'e '+ "\""+ filesDirectory + file + "\"" + ' -o'+ "\"" + saveDirectory
                subprocess.call(path)
                structureName = file[3:-7]
                file = file[:-2]
            else:
                copyfile(filesDirectory + file, saveDirectory)
                structureName = file[3:-4]
            listOfEntries[structureName] = {}

            print(structureName)
            structureHandler = XMLParser.SubElement(xmlTree, "structure", name=str(structureName))

            print('filename', structureName) # filename
            parser = PDBParser(PERMISSIVE=PERMISSIVE)
            try:
                t1 = time.time()
                structure = parser.get_structure('PHA-L', saveDirectory + file)
                fileSize = convert_size(os.path.getsize(saveDirectory + file))

                XMLParser.SubElement(structureHandler, "file_size", name="KB").text = str(fileSize)

                print('pathsize in KB', convert_size(os.path.getsize(saveDirectory + file)))
                listOfEntries[structureName]['filesize'] = convert_size(os.path.getsize(saveDirectory + file))
                #print(insertEntryName(structure, cnx))

                print(int(round((time.time() - t1) * 1000)), 'ms') # time in ticks
                parsingTime = int(round((time.time() - t1) * 1000))
                listOfEntries[structureName]['time'] = int(round((time.time() - t1) * 1000))
                XMLParser.SubElement(structureHandler, "parsing_time", name="seconds").text = str(parsingTime)

                if len(WarningHackClass.listOfWarnings) != 0:
                    warningHandler = XMLParser.SubElement(structureHandler, "warnings")
                    listOfEntries[structureName]['warnings'] = []
                    for item in WarningHackClass.listOfWarnings:
                        XMLParser.SubElement(warningHandler, "warning", name=item[1]).text = item[0]
                        listOfEntries[structureName]['warnings'].append(item)

                print ('warning: ', WarningHackClass.listOfWarnings)
                if os.path.exists(saveDirectory + file):
                    os.remove(saveDirectory + file)
            except:
                print ("error while parsing")
                XMLParser.SubElement(xmlErrors, "structure").text = structureName

                if deleteFileAfterError and os.path.exists(saveDirectory + file):
                    os.remove(saveDirectory + file)
        except:
            print("unknown error")

    XMLParser.ElementTree(xmlTree).write(saveDirectory +"ParseResults.xml")
    XMLParser.ElementTree(xmlErrors).write(saveDirectory +"ParseResultsErrors.xml")


mypath = "C:/Users/Michal/AppData/Local/VirtualStore/Program Files (x86)/GnuWin32/bin/"
_7zipLocation = "C:/Program Files/7-Zip/"
pathToStore = "C:/data/new/"
os.chdir(mypath)
files = glob.glob('pdb2k*.ent.gz')

parseAndSaveToDatabase(mypath, files, pathToStore, PERMISSIVE=0, filesZipped=True, _7zipLocation=_7zipLocation, deleteFileAfterError=False)
