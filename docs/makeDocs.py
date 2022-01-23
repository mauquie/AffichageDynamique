import os

f = open("excludeFiles.txt")

lines = f.readlines()
toExclude = []

for line in lines:
	if line[0] != "#" or len(line) < 2:
		toExclude.append(line.strip('\n').strip('\t'))
	
command = "sphinx-apidoc -f -P -e --templatedir=./source/_templates/apidocs/ -o ./source/generated/AffichageDynamiqueServer ../AffichageDynamiqueServer/ " + ' '.join(toExclude)
os.system(command)

command = "sphinx-apidoc -f -P -e --templatedir=./source/_templates/apidocs/ -o ./source/generated/SondageServer ../SondageServer/ " + ' '.join(toExclude)
os.system(command)

os.system("make html")
