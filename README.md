# Bio.PDB-parser-validation

Purpose of this project is to process every structure present in PDB using PDBParser class available in Biopython library written in Python, and getting valuable information about structure size in relation to warnings appeared during parsing and parsing time.

Taking into account large size of structures combined and capricious nature of connection to online database main assumption was to download compressed data, unpack it, process, save interesting data, and delete file. Collective information was then saved to xml file for further computations.

From given xml file second file was made with information about names of structures in relation to number of warnings, size of structure and parsing time.

## Main parsing function

Main parsing function takes both mandatory and optional arguments:

```
testParsingTimeAndSaveToXml(files, saveDirectory, outputName, filesDirectory = "", PERMISSIVE=1, filesZipped=True, _7zipLocation="", deleteFileAfterError=False)
```

filesDirectory - is a location of main folder where files are stored, can be left blank if every file in list given in second argument has whole location. Purpouse of this argument is to shorten files path, so the size of each one of them takes less memory.

files - as mentioned above can be list of full paths to processed files or what is preferable, only name of structure file (compressed or not compressed) or eventually name with short subpath.

saveDirectory - is a directory where result xml files will be stored

outputName - is a prefix name to result xml files. After outputName, function adds to the name by itself string "PermFalse" or "PermTrue" depending on choosen PERMISSIVE parameter, and "Errors" to xml file containing only files that couldn't be parsed.

PERMISSIVE=1 - by default 1 which is default as well in PDBParser. This parameter decides whether parse file in restrict way "0" or permissive way "0" (more forgiving to the structure inconsistency)

filesZipped=True - by default True. Function can parse compressed or non compressed files.

_7zipLocation="" - IMPORTANT. Function uses 7zip to decompress compressed files (program was choosen because of the license). If left blank function takes PATH location to the program, but it is highly suggested to provide path to where 7z.exe file is located on hard drive.

## Testing

function is tested using sample compressed and uncompressed data attached to project, then parsing and saving it to xml, and comparing to expected output results.
