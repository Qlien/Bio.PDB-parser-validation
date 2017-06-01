import time

from Bio.PDB import PDBParser

parser = PDBParser()
t1 = time.clock()
structure = parser.get_structure('PHA-L', 'fa/pdb1fat.ent')

print(time.clock() - t1)
print(parser.header["author"])