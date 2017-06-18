import time
import re
from Bio.PDB import *
import os
import subprocess
import warnings
import xml.etree.cElementTree as XMLParser

def testParsingTimeAndSaveToXml(files, saveDirectory, outputName, filesDirectory="", PERMISSIVE=1, filesZipped=False, _7zipLocation="", deleteFileAfterError=False):

    listOfWarnings = []

    def convert_size(size_bytes):
        if size_bytes == 0:
            return 0
        s = int(round(size_bytes / 1024))
        return s

    xmlTree = XMLParser.Element("data")
    xmlErrors = XMLParser.Element("errors")

    def customwarn(message, category, filename, lineno, file=None, line=None):
        warningString = warnings.formatwarning(message, category, filename, lineno)
        strintArray = re.sub(r'.*:\s', '', warningString).strip().split("\n")
        if strintArray[len(strintArray) - 1][-1:] == ')':
            strintArray[len(strintArray) - 1] = strintArray[len(strintArray) - 1][:-1].strip()
        listOfWarnings.append(strintArray)

    warnings.showwarning = customwarn

    for file in files:
        #overriding warning method to pass warnings to file
        listOfWarnings = []

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
            structureName = file[len(file) - 11:-7]
            file = file[len(file) - 14:-3]
        else:
            print(filesDirectory + file, saveDirectory)
            structureName = file[len(file) - 8:-4]

        print(structureName)
        print("file ",file )
        structureHandler = XMLParser.SubElement(xmlTree, "structure", name=str(structureName))

        print('structure', structureName) # filename
        parser = PDBParser(PERMISSIVE=PERMISSIVE)
        try:
            t1 = time.time()
            if filesZipped:
                structure = parser.get_structure('PHA-L', saveDirectory + file)
            else:
                parser.get_structure('PHA-L', filesDirectory + file)
            fileSize = convert_size(os.path.getsize(saveDirectory + file))

            XMLParser.SubElement(structureHandler, "file_size", name="KB").text = str(fileSize)

            print('pathsize in KB', convert_size(os.path.getsize(saveDirectory + file)))
            #print(insertEntryName(structure, cnx))

            print(int(round((time.time() - t1) * 1000)), 'ms') # time in ticks
            parsingTime = int(round((time.time() - t1) * 1000))
            XMLParser.SubElement(structureHandler, "parsing_time", name="seconds").text = str(parsingTime)

            if len(listOfWarnings) != 0:
                warningHandler = XMLParser.SubElement(structureHandler, "warnings")
                for item in listOfWarnings:
                    XMLParser.SubElement(warningHandler, "warning", name=item[1]).text = item[0]

            print ('warning: ', listOfWarnings)
            if os.path.exists(saveDirectory + file) and filesZipped:
                os.remove(saveDirectory + file)
        except:
            print ("error while parsing")
            XMLParser.SubElement(xmlErrors, "structure").text = structureName

            if deleteFileAfterError and os.path.exists(saveDirectory + file) and filesZipped:
                os.remove(saveDirectory + file)



    permText = "PermFalse" if PERMISSIVE == 0 else "PermTrue"
    XMLParser.ElementTree(xmlTree).write(saveDirectory + outputName + permText + ".xml")
    XMLParser.ElementTree(xmlErrors).write(saveDirectory + outputName + permText + "Errors.xml")


