
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


iterator = 0

def parseAndSaveToDatabase(filesDirectory, file, _7zipLocation, cnx, listOfEntries, xml): #cnx is database connection
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
    t1 = time.clock()
    parser = PDBParser()
    structure = parser.get_structure('PHA-L', 'C:/data/1/' + file[:-2])
    fileSize = convert_size(os.path.getsize('C:/data/1/' + file[:-2]))

    XMLParser.SubElement(structureHandler, "file_size").text = str(fileSize)

    print('pathsize in KB', convert_size(os.path.getsize('C:/data/1/' + file[:-2])))
    listOfEntries[filename]['filesize'] = convert_size(os.path.getsize('C:/data/1/' + file[:-2]))
    #print(insertEntryName(structure, cnx))

    print(int(round((time.clock() - t1) * 1000)), 'ms') # time in ticks
    parsingTime = int(round((time.clock() - t1) * 1000))
    listOfEntries[filename]['time'] = int(round((time.clock() - t1) * 1000))
    XMLParser.SubElement(structureHandler, "parsing_time").text = str(parsingTime)

    if len(WarningHackClass.listOfWarnings) != 0:
        listOfEntries[filename]['warnings'] = []
        for item in WarningHackClass.listOfWarnings:
            listOfEntries[filename]['warnings'].append(item)

    print ('warning: ', WarningHackClass.listOfWarnings)
    if os.path.exists('C:/data/1/' + file[:-2]):
        os.remove('C:/data/1/' + file[:-2])


def insertIntoDB(cnx):
    import mysql.connector

    cursor = cnx.cursor()

    cursor.execute("INSERT INTO entries "
               "(Name) "
               "VALUES ('asdasd')")
    cnx.commit()

    cursor.close()
    cnx.close()

def insertEntryName(pdbParser, cnx):

    cursor = cnx.cursor()
    cursor.execute("INSERT INTO entries "
               "(Name) "
               "VALUES ('" + pdbParser.id + "')")
    cnx.commit()

    cursor.close()
    cnx.close()
    return cursor.lastrowid



cnx = mysql.connector.connect(user='root', password='admin',
                                  host='localhost',
                                  database='bioparser')


listOfEntries = {}

xmlTree = XMLParser.Element("data")

iterator = 0
for file in files:
    iterator += 1
    parseAndSaveToDatabase(mypath, file, _7zipLocation, cnx, listOfEntries, xmlTree)
    if iterator == 10:
        break

XMLParser.ElementTree(xmlTree).write("filename.xml")