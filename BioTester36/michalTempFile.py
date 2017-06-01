
import sys, os, warnings

import time
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

mypath = "C:/Users/Michal/AppData/Local/VirtualStore/Program Files (x86)/GnuWin32/bin"
_7zipLocation = "C:/Program Files/7-Zip/"
pathToStore = "C:/data/1"
os.chdir(mypath)
files = glob.glob('*.gz')

def parseAndSaveToDatabase(filesDirectory, file, _7zipLocation, cnx): #cnx is database connection
    path = "\""+ _7zipLocation+ '7z.exe' + "\" "+ 'e '+ "\""+ filesDirectory+ '/' + file + "\"" + ' -o'+ "\"" + pathToStore+ "\""
    print(path)
    subprocess.call(path)

    t1 = time.clock()
    parser = PDBParser()
    structure = parser.get_structure('PHA-L', 'C:/data/1/' + file[:-2])

    #print(insertEntryName(structure, cnx))
    if os.path.exists('C:/data/1/' + file[:-2]):
        os.remove('C:/data/1/' + file[:-2])

    print(time.clock() - t1)


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
for file in files:
    parseAndSaveToDatabase(mypath, file, _7zipLocation, cnx)