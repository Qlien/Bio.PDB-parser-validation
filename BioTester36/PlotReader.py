import os
import xml.etree.ElementTree as ET
import csv

# file that sums up whole xml file inoto summary of errors
tree = ET.parse('C:/data/ParseResultsPython36Perm1.xml')
root = tree.getroot()

filesWithWarnings = []
warningTypes = []
allFiles = 0
warningFiles = 0
namesToSizesToWarningsList = []
print (root.tag)
iterator = 0
for structure in root:
    tempNamesToSizesToWarningsList = [structure.attrib['name'], 0, 0, 0] # name of the structure, sizeOfTheStructure, numberOfWarnings, parsingTime
    for item in structure:
        if item.tag == 'file_size':
            tempNamesToSizesToWarningsList[1] = int(item.text)
        if item.tag == 'parsing_time':
            tempNamesToSizesToWarningsList[3] = int(item.text)
        if item.tag == "warnings":
            filesWithWarnings.append(structure.attrib['name'])
            for warning in item:
                tempNamesToSizesToWarningsList[2] = tempNamesToSizesToWarningsList[2] + 1
                if warning.attrib['name'] not in warningTypes:
                    warningTypes.append(warning.attrib['name'])
    if tempNamesToSizesToWarningsList[2] > 0:
        print(tempNamesToSizesToWarningsList)
        namesToSizesToWarningsList.append(tempNamesToSizesToWarningsList)
    iterator += 1

print(os.getcwd())
with open(os.getcwd() + "\\plotData.csv", "w") as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(namesToSizesToWarningsList)