
import sys, os, warnings

import time

import re
from Bio import PDB

from Bio.PDB import *
from os import listdir
from os.path import isfile, join
import os
import glob
import gzip
import tarfile
import subprocess
import mysql.connector
import warnings, sys
import math
import xml.etree.cElementTree as XMLParser

def convert_size(size_bytes):
   if size_bytes == 0:
       return 0
   s = int(round(size_bytes / 1024))
   return s


mypath = "C:/Users/Michal/AppData/Local/VirtualStore/Program Files (x86)/GnuWin32/bin"
_7zipLocation = "C:/Program Files/7-Zip/"
pathToStore = "C:/data/1"
os.chdir(mypath)
files = glob.glob('*.gz')


class WarningHackClass:
    listOfWarnings = []


def parseAndSaveToDatabase(filesDirectory, file, _7zipLocation, cnx, listOfEntries, xml, xmlErrors): #cnx is database connection
    try:
        WarningHackClass.listOfWarnings = []
        def customwarn(message, category, filename, lineno, file=None, line=None):
            warningString = warnings.formatwarning(message, category, filename, lineno)
            strintArray = re.sub(r'.*:\s', '', warningString).strip().split("\n")
            if strintArray[len(strintArray) - 1][-1:] == ')':
                strintArray[len(strintArray) - 1] = strintArray[len(strintArray) - 1][:-1].strip()
            WarningHackClass.listOfWarnings.append(strintArray)

        warnings.showwarning = customwarn

        path = "\""+ _7zipLocation+ '7z.exe' + "\" "+ 'e '+ "\""+ filesDirectory+ '/' + file + "\"" + ' -o'+ "\"" + pathToStore+ "\""
        subprocess.call(path)

        filename = file[3:-7]
        listOfEntries[filename] = {}

        structureHandler = XMLParser.SubElement(xml, "structure", name=str(file[3:-7]))

        print('filename', file[3:-7]) # filename
        t1 = time.time()
        parser = PDBParser(PERMISSIVE=0)
        try:
            structure = parser.get_structure('PHA-L', 'C:/data/1/' + file[:-2])
            fileSize = convert_size(os.path.getsize('C:/data/1/' + file[:-2]))

            XMLParser.SubElement(structureHandler, "file_size", name="KB").text = str(fileSize)

            print('pathsize in KB', convert_size(os.path.getsize('C:/data/1/' + file[:-2])))
            listOfEntries[filename]['filesize'] = convert_size(os.path.getsize('C:/data/1/' + file[:-2]))
            #print(insertEntryName(structure, cnx))

            print(int(round((time.time() - t1) * 1000)), 'ms') # time in ticks
            parsingTime = int(round((time.time() - t1) * 1000))
            listOfEntries[filename]['time'] = int(round((time.time() - t1) * 1000))
            XMLParser.SubElement(structureHandler, "parsing_time", name="seconds").text = str(parsingTime)

            if len(WarningHackClass.listOfWarnings) != 0:
                warningHandler = XMLParser.SubElement(structureHandler, "warnings")
                listOfEntries[filename]['warnings'] = []
                for item in WarningHackClass.listOfWarnings:
                    XMLParser.SubElement(warningHandler, "warning", name=item[1]).text = item[0]
                    listOfEntries[filename]['warnings'].append(item)

            print ('warning: ', WarningHackClass.listOfWarnings)
            if os.path.exists('C:/data/1/' + file[:-2]):
                os.remove('C:/data/1/' + file[:-2])
        except:
            print ("error while parsing")
            XMLParser.SubElement(xmlErrors, "structure").text = file[3:-7]
    except:
        print("unknown error")
        if os.path.exists('C:/data/1/' + file[:-2]):
            os.remove('C:/data/1/' + file[:-2])



cnx = mysql.connector.connect(user='root', password='admin',
                                  host='localhost',
                                  database='bioparser')


listOfEntries = {}

xmlTree = XMLParser.Element("data")
xmlErrors = XMLParser.Element("errors")

iterator = 0
for file in files:
    parseAndSaveToDatabase(mypath, file, _7zipLocation, cnx, listOfEntries, xmlTree, xmlErrors)
    print(iterator)
    iterator += 1

XMLParser.ElementTree(xmlTree).write("parserPermissiveFalsepython27.xml")
XMLParser.ElementTree(xmlErrors).write("errorsparserPermissiveFalsepython27.xml")