import glob
import os
from Parser import testParsingTimeAndSaveToXml

mypath = os.getcwd() + "files/"
_7zipLocation = "C:/Program Files/7-Zip/"
os.chdir(os.getcwd())
files = glob.glob('files/*pdb*')

testParsingTimeAndSaveToXml(files, os.getcwd() + "\\", "results36Test", os.getcwd() + "\\",  PERMISSIVE=1, filesZipped=False, _7zipLocation=_7zipLocation, deleteFileAfterError=False)