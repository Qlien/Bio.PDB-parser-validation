import xml.etree.ElementTree as ET
import csv


tree = ET.parse('C:/Users/Michal/AppData/Local/VirtualStore/Program Files (x86)/GnuWin32/bin/parserData10-06-2017-14-00.xml')
root = tree.getroot()

filesWithWarnings = []
warningTypes = []
allFiles = 0
warningFiles = 0
namesToSizesToWarningsList = []
print (root.tag)
iterator = 0
for structure in root:
    tempNamesToSizesToWarningsList = [structure.attrib['name'], 0, 0] # name of the structure, sizeOfTheStructure, numberOfWarnings
    for item in structure:
        if item.tag == 'file_size':
            tempNamesToSizesToWarningsList[1] = int(item.text)
        if item.tag == "warnings":
            filesWithWarnings.append(structure.attrib['name'])
            for warning in item:
                tempNamesToSizesToWarningsList[2] = tempNamesToSizesToWarningsList[2] + 1
                if warning.attrib['name'] not in warningTypes:
                    warningTypes.append(warning.attrib['name'])
    if tempNamesToSizesToWarningsList[2] > 0:
        namesToSizesToWarningsList.append(tempNamesToSizesToWarningsList)
    iterator += 1
    print(iterator)

with open("namesToSizeToErrorsCount.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(namesToSizesToWarningsList)
print()