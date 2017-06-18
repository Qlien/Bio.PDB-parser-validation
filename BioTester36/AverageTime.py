import os
import xml.etree.ElementTree as ET
import csv
import numpy

# file that sums up whole xml file inoto summary of errors
tree = ET.parse('C:/data/ParseResultsPermissiveFalse.xml')
root = tree.getroot()

int64 = 0
print (root.tag)
iterator = 0
for structure in root:
    for item in structure:
        if item.tag == 'parsing_time':
            int64 += int(item.text)
    iterator += 1

print(int64/ iterator)