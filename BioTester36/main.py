import time

from Bio.PDB import PDBParser

parser = PDBParser()
t1 = time.clock()
structure = parser.get_structure('PHA-L', 'C:/data/1/pdb5lg3.ent')

print(time.clock() - t1)
print(parser.header["author"])