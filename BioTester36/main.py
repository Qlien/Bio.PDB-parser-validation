import os
import time

from Bio.PDB import PDBParser

parser = PDBParser()
t1 = time.clock()
structure = parser.get_structure('PHA-L', 'C:/data/pdb9xim.ent')



print(time.clock() - t1)
print(parser.header["author"])

if os.path.exists('C:/data/1/pdb4no0.ent'):
    os.remove('C:/data/1/pdb4no0.ent')