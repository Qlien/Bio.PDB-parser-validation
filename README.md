# Bio.PDB-parser-validation

Purpouse of this project is to process every structure present in PDB using PDBParser class available in Biopython library written in Python, and getting valuable information about structure size in relation to warnings appeared during parsing and parsing time.

Taking into account large size of structures combined and capricious connection to online database main assumption was to download compressed data, unpack it, process, save interesting data, and delete file. Collective information was then saved to xml file for further computations.

