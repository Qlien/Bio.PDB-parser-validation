import time

from Bio.PDB import PDBParser

#parser = PDBParser(PERMISSIVE = 1) #the same as default permissive
# Strict parser
strict_parser = PDBParser(PERMISSIVE=0) #restrictive
t1 = time.clock()
#structure = parser.get_structure('PHA-L', 'fa/1fat.pdb')

strict_structure = strict_parser.get_structure('PHA-L', 'fa/1fat.pdb')


print(time.clock() - t1)
#print(parser.header["author"])

print(strict_parser.header["name"])