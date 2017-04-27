import time

from Bio.PDB import PDBParser

parser = PDBParser()
t1 = time.clock()
structure = parser.get_structure('PHA-L', 'fa/1fat.pdb')

print(time.clock() - t1)