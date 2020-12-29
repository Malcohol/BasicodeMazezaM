# Hacky script to take a bunch of "high-level" basic files and convert it to a minimal BASICODE listing.
# Note: this does not tokenize the input: It just uses a bunch of regular expressions.

import re
import sys

# Labels are GOTO/GOSUB targets or constant definitions.
labelTable = {}

whitespaceMatcher = re.compile(r"\s*$")
lineNumberMatcher = re.compile(r"\d+:\s*$")
labelMatcher = re.compile(r"_\w+_:\s*$")
lineMatcher = re.compile(r"\s.*")
commentMatcher = re.compile(r"\s*#.*$")
assignmentMatcher = re.compile(r"_\w+_\s*=.*$")
ifThenMatcher = re.compile(r".*IF.*THEN.*$")

srcLines = []
for a in sys.argv[1:]:
    f = open(a)
    srcLines += f.readlines()

# Basicode programs start at 1000
currentLine = 1000

# A mapping from fixed line numbers to lines of code which will follow from there.
# Each label or explicit line number in the code will start a entry.
codeLines = { currentLine: [] }

# Parse the contents.
for l in srcLines:
    if whitespaceMatcher.match(l):
        continue
    elif lineNumberMatcher.match(l):
        colonIndex = l.find(":")
        currentLine = int(l[:colonIndex])
        codeLines[currentLine] = []
    elif labelMatcher.match(l):
        colonIndex = l.find(":")
        currentLine += 300
        labelTable[l[:colonIndex]] = str(currentLine)
        codeLines[currentLine] = []
    elif commentMatcher.match(l):
        continue
    elif assignmentMatcher.match(l):
        equalIndex = l.find("=")
        labelTable[l[:equalIndex].strip()] = l[equalIndex+1:].strip()
    elif lineMatcher.match(l):
        codeLines[currentLine] = codeLines[currentLine] + [l[:-1].strip()]

def replaceLabels(l):
    r = []
    for i in l:
        for (k,v) in labelTable.items():
            i = i.replace(k, v)
        r.append(i)
    return r

codeLines = { n:replaceLabels(l) for (n, l) in codeLines.items() }    

keywords = [ "PRINT", "INPUT", "GOTO", "GOSUB", "RETURN", "LET", "FOR", "TO",
    "STEP", "NEXT", "IF", "THEN", "ON", "RUN", "STOP", "END", "DIM", "READ", "DATA", "RESTORE", "REM",
    "TAB", "ABS", "SGN", "INT", "SQR", "SIN", "COS", "TAN", "ATN", "EXP", "LOG", "ASC", "VAL", "LEN", "CHR$", "LEFT$", "MID$", "RIGHT$",
    "AND", "OR", "NOT" ]

# Remove spaces where they won't confuse the parser
def collapse(l):
    r = []
    for i in l:
        s = ""
        tokens = []
        pretokens = i.split('\"')
        for j in range(0, len(pretokens)):
            if j%2 == 0:
                tokens += pretokens[j].split()
            else:
                tokens.append('\"' + pretokens[j] + '\"')
        for t in tokens:
            endsWithToken = False
            for k in keywords:
                if s.endswith(k):
                    endsWithToken = True
                    break
            if len(s) == 0 or endsWithToken or not s[-1].isalpha() or not t[0].isalpha():
                s = s + t
            else:
                s = s + " " + t
        if len(s) > 56:
            raise Exception("Line " + str(len(s)-56) + " characters too long: " + s)
        r.append(s)
    return r

codeLines = { n:collapse(l) for (n, l) in codeLines.items() }    

# THEN GOTO = THEN
def removeGotos(l):
    return [i.replace("THENGOTO", "THEN") for i in l ]

codeLines = { n:removeGotos(l) for (n, l) in codeLines.items() }    

result = []

# Pack code into lines of at most 60 characters
for (num,line) in codeLines.items():
    currentLine = num
    outline = str(currentLine)
    separator= ""
    for l in line:
        if len(outline) + 1 + len(l) > 60:
            result += [outline]
            currentLine += 10
            outline = str(currentLine)
            separator = ""
        if ifThenMatcher.match(l):
            outline += separator + l
            result += [outline]
            currentLine += 10
            outline = str(currentLine)
            separator = ""
        else:
            outline += separator + l
            separator = ":"
    if len(outline) > 4:
        result += [outline]


result.sort()

for l in result:
    print l
