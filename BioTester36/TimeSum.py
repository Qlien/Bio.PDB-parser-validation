import os
import xml.etree.ElementTree as ET
import csv
import numpy

#tree = ET.parse('C:/data/ParseResultsPermissiveFalse.xml')
tree = ET.parse('C:/data/ParseResultsPython36Perm1.xml')
root = tree.getroot()

int64 = 0
for structure in root:
    for item in structure:
        if item.tag == 'parsing_time':
            int64 += int(item.text)

print(int64)