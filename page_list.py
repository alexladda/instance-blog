import pathlib

# define the path
currentDirectory = pathlib.Path('pages')

# define the pattern
currentPattern = "*.md"

list=[]

for currentFile in currentDirectory.glob(currentPattern):
    list.append(currentFile.stem)
    print(list)
