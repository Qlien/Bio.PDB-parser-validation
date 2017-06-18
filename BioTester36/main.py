import glob
import os
from Parser import testParsingTimeAndSaveToXml

mypath = "C:/Users/Michal/AppData/Local/VirtualStore/Program Files (x86)/GnuWin32/bin/"
_7zipLocation = "C:/Program Files/7-Zip/"
pathToStore = "C:/data/1/"
os.chdir(mypath)
files = glob.glob('pdb*.gz')

testParsingTimeAndSaveToXml(files, pathToStore, "results36", mypath,  PERMISSIVE=1, filesZipped=True, _7zipLocation=_7zipLocation, deleteFileAfterError=False)