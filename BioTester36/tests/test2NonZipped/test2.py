import glob
import os
import unittest
import xml.etree.ElementTree as ET
from Parser import testParsingTimeAndSaveToXml

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self._7zipLocation = "C:/Program Files/7-Zip/"
        os.chdir(os.getcwd())
        self.files = glob.glob('files/*pdb*')

        testParsingTimeAndSaveToXml(self.files, os.getcwd() + "\\", "results36", os.getcwd() + "\\", PERMISSIVE=1,
                                    filesZipped=False, _7zipLocation=self._7zipLocation, deleteFileAfterError=False)

    def testOne(self):
        treeExpected = ET.parse(os.getcwd() + "\\results36TestPermTrueExpected.xml").getroot()
        treeXML = ET.parse(os.getcwd() + "\\results36PermTrue.xml").getroot()

        for item1a, item2a in zip(treeExpected, treeXML):
            self.failUnless(item1a.attrib['name'] == item2a.attrib['name'])
            #print(item1a.attrib['name'], item2a.attrib['name'])
            for item1b, item2b in zip(item1a, item2a):
                if(item1b.tag == 'warnings' and item2b.tag == 'warnings'):
                    self.failUnless(len(item1b) == len(item2b))
                    #print(len(item1b))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
