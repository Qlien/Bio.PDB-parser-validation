import xml.etree.ElementTree as ET
import csv


tree = ET.parse('C:/data/parserPermissiveFalsepython27.xml')
root = tree.getroot()

filesWithWarnings = []
warningTypes = []
allFiles = 0
warningFiles = 0
namesToSizesToWarningsList = []
print (root.tag)
iterator = 0
for structure in root:
    tempNamesToSizesToWarningsList = [structure.attrib['name'], 0, 0, 0] # name of the structure, sizeOfTheStructure, numberOfWarnings, warningTypes
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

with open("C:/data/parserPermissiveFalsepython27.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(namesToSizesToWarningsList)
print()