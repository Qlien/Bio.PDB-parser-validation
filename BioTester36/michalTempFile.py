
import sys, os, warnings
from Bio.PDB import *

pdbl = PDBList()
pdbl.retrieve_pdb_file('1FAT')

parser = PDBParser()
structure = parser.get_structure('PHA-L', 'fa/pdb1fat.ent')
parser = MMCIFParser()

