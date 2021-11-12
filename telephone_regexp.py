#imports
from os import sep
import re, time, sys

#To be taken from the command line
DATA_FILE_NAME = sys.argv[1]
OUTPUT_FILE_NAME = "telephone_output.txt"
print(f"INPUT FILE PROVIDED IS {DATA_FILE_NAME}")

#This is the complete numeric case for recognition of the numbers
caseComplete = r"(?<!\d)(\(?[0-9]{3}\)?(\s|-|\.|/)*)?([0-9]{3}(\s|-|\.|/)*[0-9]{4})\b"
print(f"REGEX USED TO RECOGNIZE NUMBERS IS {caseComplete}")

numberCompleteRegex = re.compile(caseComplete, re.IGNORECASE)

#Start of time to begin Regex Evaluation
# t_0 = time.time()
# print(f"t_0 = {t_0}")

print("Matched Items")

# Opening the File for Input
outputItems = []
with open(DATA_FILE_NAME, "r") as dataFile:
    # Openning the File for Output
    for dataLine in dataFile:
        dataLine = dataLine.strip()

        #used to store the iteratable result of mathces, one for each of the above cases
        numberIter = numberCompleteRegex.finditer(dataLine)

        for number in numberIter:
            newItem = number.group()
            outputItems.append(newItem)
            # print(newItem, dataLine, sep=" : ")
            print(newItem)

#End of the time for Regex, Start of the time to write to File
# t_1 = time.time()
# print(f"t_1 = {t_1} | t_1 - t_0 = {t_1 - t_0}")

with open(OUTPUT_FILE_NAME, "w") as outputFile:
    for outputItem in outputItems:
        outputFile.write(outputItem + "\n")

#End of the time to write to File
# t_2 = time.time()
# print(f"t_2 = {t_2} | t_2 - t_1 = {t_2 - t_1}")
