#imports
import re
import time

#To later be taken from the command line
DATA_FILE_NAME = "all-OANC.txt"
OUTPUT_FILE_NAME = "dollar_output.txt"

#Creating the Regex Objects
wordBoundary = r"\b"
optionalWhiteSpace = r"\s?"
spaceHyphen = r"[\s-]+"
andChars = r"((and)|(&)|(AND))"
dollarTermination = r"(dollars?)"
centTermination = r"(cents?)"
currencyTermination = r"(" + dollarTermination + r")|(" + centTermination + r")"
numericNumbers = r"((\d{1,3}[,\s.]\d{3})|(\d+[,.]\d+)|(\d+))"
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
cases = [case0, case1, case2, case3]

print("The regex below handles the case, $<someDigits>, $<someDigits>.<someDigits>")
print(case0)
print("The regex below handles the case, <x> dollars | <y> cents | <x> dollars and <y> cents where x and y numeric")
print(case1)
print("The regex below handles the case, <x> dollars | <y> cents | <x> dollars and <y> cents where x and y textual")
print(case2)
print("The regex below handles the case, <x> <thousand|million|billion|trillion> dollar(s) | $<x> <thousand|million|billion|trillion> where x numeric")
print(case3)

currencyCompleteRegexes = [re.compile(case) for case in cases]

t_0 = time.time()
print(f"t_0 = {t_0}")
# Opening the File for Input
outputItems = []
with open(DATA_FILE_NAME, "r") as dataFile:
    # Openning the File for Output
    for dataLine in dataFile:
        dataLine = dataLine.strip()

        #used to store the iteratable result of mathces, one for each of the above cases
        currencyIters = []

        for currencyCompleteRegex in currencyCompleteRegexes:
            currencyIters.append(currencyCompleteRegex.finditer(dataLine))
        
        for currencyIter in currencyIters:
            for currency in currencyIter:
                outputItems.append(currency.group())
t_1 = time.time()
print(f"t_1 = {t_1} | t_1 - t_0 = {t_1 - t_0}")
with open(OUTPUT_FILE_NAME, "w") as outputFile:
    for outputItem in outputItems:
        outputFile.write(outputItem)
t_2 = time.time()
print(f"t_2 = {t_2} | t_2 - t_1 = {t_2 - t_1}")


        # currencyTerminationList = currencyTerminationRegex.findall(dataLine)
        # numericNumbersIters = numericNumbersRegex.finditer(dataLine)
        # for numericNumberIter in numericNumbersIters:
        #     startSpan, endSpan = numericNumberIter.span()
        #     print(numericNumberIter)
        #     print(dataLine[startSpan - 10: min(endSpan + 10, len(dataLine) - 1)])
        # currencyBeginIters = currencyBeginRegex.finditer(dataLine)
        # if currencyTerminationList:
        #     print(currencyTerminationList)
        #     print(dataLine)
        # if numericNumbersList:
        #     print(numericNumbersList)
        #     print(dataLine)
        #     count += 1
        #     if count > 10:
        #         break

        # for currencyBeginIter in currencyBeginIters:
        #     startSpan, endSpan = currencyBeginIter.span()
        #     print(currencyBeginIter)
        #     print(dataLine[startSpan - 10: min(endSpan + 10, len(dataLine) - 1)])
        
        # print(f"<{dataLine}>"
    