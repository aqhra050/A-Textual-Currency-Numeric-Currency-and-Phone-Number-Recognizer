#imports
import re, time, sys

#To be taken from the command line
DATA_FILE_NAME = sys.argv[1]
OUTPUT_FILE_NAME = "dollar_output.txt"
print(f"INPUT FILE PROVIDED IS {DATA_FILE_NAME}")

#Creating the Regex Objects
wordBoundary = r"\b"
optionalWhiteSpace = r"\s?"
spaceHyphen = r"[\s-]*"
andChars = r"((and)|(&)|(AND))"
dollarTermination = r"(dollars?)"
centTermination = r"(cents?)"
currencyTermination = r"(" + dollarTermination + r")|(" + centTermination + r")"
numericNumbers = r"((\d{1,3}([,\s]\d{3})+(\.\d+)?)|(\d+[,.]\d+)|(\d+))"
currencyBegin = r"\$"
weights = r"(thousand)|(million)|(billion)|(trillion)"

#handling the textual numbers
nums1to9 = r"(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)"
nums10to19 = r"(ten)|(eleven)|(twelve)|(thirteen)|(fourteen)|(fifteen)|(sixteen)|(seventeen)|(eighteen)|(nineteen)"
textualTens = r"(twenty)|(thirty)|(forty)|(fifty)|(sixty)|(seventy)|(eighty)|(ninety)"
nums20to99 = r"(" + textualTens + r")(" + spaceHyphen + "(" + nums1to9 + r"))?"
nums1to99 = r"(" + nums20to99 + r")|(" + nums10to19 + r")|" + r"(" + nums1to9 + ")"
nums100to999 = r"(" + nums1to9 + r")" + spaceHyphen + r"hundred" + r"((" + spaceHyphen + andChars + r")?" + spaceHyphen + nums1to99 + r")?"
nums1to999 = r"(" + nums100to999 + ")|(" + nums1to99 + r")"
nums1toMIL = r"((" + nums1to999 + r")" + spaceHyphen + r"thousand" + r"((" + spaceHyphen + andChars + r")?" + spaceHyphen + nums1to999 + r")?)|(" + nums1to999 + r")"
nums1toBIL = r"((" + nums1to999 + r")" + spaceHyphen + r"million" + r"((" + spaceHyphen + andChars + r")?" + spaceHyphen + nums1to999 + r")?)|(" + nums1toMIL + r")"
nums1toTRIL = r"((" + nums1to999 + r")" + spaceHyphen + r"billion" + r"((" + spaceHyphen + andChars + r")?" + spaceHyphen + nums1to999 + r")?)|(" + nums1toBIL + r")"

textualNumbers = nums1toTRIL

#fractions!?

#handle the case $<someDigits>, $<someDigits>.<someDigits> | case0
case0 = currencyBegin + spaceHyphen + numericNumbers
#handle the case with <x> dollars | <y> cents | <x> dollars and <y> cents where x and y numeric | case1
case1 = r"(" + numericNumbers + spaceHyphen + dollarTermination + spaceHyphen + andChars + spaceHyphen + numericNumbers + spaceHyphen + centTermination + wordBoundary + r")|(" + numericNumbers + spaceHyphen + dollarTermination + wordBoundary + r")|(" + numericNumbers + spaceHyphen + centTermination + wordBoundary + r")"
#handle the case with <x> dollars | <x> cents | <x> dollars and <y> cents where x and y textual
case2 = r"(" + textualNumbers + spaceHyphen + dollarTermination + spaceHyphen + andChars + spaceHyphen + textualNumbers + spaceHyphen + centTermination + wordBoundary + r")|(" + textualNumbers + spaceHyphen + dollarTermination + wordBoundary + r")|(" + textualNumbers + spaceHyphen + centTermination + wordBoundary + r")"
#handle the case with <x> <thousand|million|billion|trillion> dollar(s) | $<y> <thousand|million|billion|trillion>
case3 = r"(" + numericNumbers + spaceHyphen + r"(" + weights + r")" + spaceHyphen + dollarTermination + wordBoundary + r")|(" +  currencyBegin + numericNumbers + spaceHyphen + r"(" + weights + wordBoundary + r"))"
case4 = r"(a dollars?)"

print("Note that the below regex are compiled to be case-insensitive")
print("The regex below handles the case, $<someDigits>, $<someDigits>.<someDigits>")
print(case0)
print("The regex below handles the case, <x> dollars | <y> cents | <x> dollars and <y> cents where x and y numeric")
print(case1)
print("The regex below handles the case, <x> dollars | <y> cents | <x> dollars and <y> cents where x and y textual")
print(case2)
print("The regex below handles the case, <x> <thousand|million|billion|trillion> dollar(s) | $<x> <thousand|million|billion|trillion> where x numeric")
print(case3)
print("The regex below handles the case, a dollar")
print(case4)

#this case is a combination of all the other cases
caseComplete = r"(" + case0 + r")|(" + case1 + r")|(" + case2 +  r")|(" + case3 + r")|(" + case4 + r")" 

currencyCompleteRegex = re.compile(caseComplete, re.IGNORECASE)

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
        currencyIter = currencyCompleteRegex.finditer(dataLine)

        for currency in currencyIter:
            newItem = currency.group()
            outputItems.append(newItem)
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
