
"""
output chemdraw figure numbers and names from latex document to output.txt

use main(doc name.tex) at bottom of document if there is a "master" latex
document with smaller files embedded 

use getnames(doc name.tex) if using a singular doc

"""

################################################################################

import re
import os

count = 0 
subdoc_count = 1
schemes = {}
subparts = {"one": "(a)", "two": "(b)", "three": "(c)", "four": "(d)"}

################################################################################

# enter your path to all the tex documents here if directory is not already set
# include double blackslashes instead of single
path="C:\\Users\\yesta\\Desktop\\Michael Thesis"
os.chdir(path)

################################################################################

# finds names of all subdocuments in master document, iterates through each to
# find figure number and names

def main(maindoc):
    global schemes
    chapters = []
    main = open(maindoc, "r")
    maincontent = main.readlines()

    for line in maincontent:
        if re.search(r"\B\\input", line):
            chapname = text_in_brackets(line)
            chapters += chapname

    for i in chapters:
        getnames(i)
        
        
################################################################################

# searches for replacecmpd, extracts name, updates count and checks for 
# duplicates. remove comments for printed results

def getnames(filepath):

    global count
    global schemes
    global subdoc_count

  #  print("\n", filepath)

    schemes["\nsubdoc" + str(subdoc_count)] = filepath 
    subdoc_count += 1

    file = open(filepath, "r")
    contents = file.readlines()

    for line in contents:
        if re.search(r"\B\\replacecmpd", line):
            text = text_in_brackets(line)[0]

            if text not in schemes.values():
                part = check_part(text)
                if part == "one":
                    count += 1
                    schemes[count] = get_part(text)
                  #  print(count, get_part(text))

                    new_key = str(count) + subparts[part]
                    schemes[new_key] = text
                   # print(count, subparts[part], text)

                elif part:
                    new_key = str(count) + subparts[part]
                    schemes[new_key] = text
                  #  print(count, subparts[part], text)

                else:
                    count += 1
                    schemes[count] = text
                  #  print(count, text)

    file.close()

################################################################################

# checks if text contains ".", returns part of text after the dot

def check_part(text):
    if "." in text:
        part = re.findall('\.(.+)', text)
        return part[0]

################################################################################

# finds only the first group of alphanumeric text

def get_part(text):
    chem = re.findall('([aA-zZ0-9]+)', text)
    return chem[0]

################################################################################

# finds the text in curly brackets

def text_in_brackets(line):
    text_in_brackets = re.findall('{((?:[a-zA-Z0-9.-])+?)}',line)
    return text_in_brackets

################################################################################

def writetofile():
    output = open("names.txt", "w")
    for num in schemes:
        a = str(num) + " " + schemes[num] + "\n"
        output.write(a)

    output.close()

################################################################################

### CHANGE FUNCTION CALLS HERE ###

main("Thesis.tex")
#getnames("MukaiyamaHydration.tex")


################################################################################
writetofile()
################################################################################