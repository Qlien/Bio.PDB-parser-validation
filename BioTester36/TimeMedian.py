import os
import xml.etree.ElementTree as ET
import csv
import numpy

tree = ET.parse('C:/data/ParseResultsPermissiveFalse.xml')
#tree = ET.parse('C:/data/ParseResultsPython36Perm1.xml')
root = tree.getroot()

times = []
iterator = 0
for structure in root:
    for item in structure:
        if item.tag == 'parsing_time':
            times.append(int(item.text))

times.sort()
print(times[int(len(times) / 2)])