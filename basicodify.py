# Hacky script to take a bunch of "high-level" basic files and convert it to a minimal BASICODE listing.
# Note: this does not tokenize the input: It just uses a bunch of regular expressions.

import re
from sys import stdout
from argparse import ArgumentParser, FileType

parser = ArgumentParser()
parser.add_argument("files", nargs="+", type=FileType("r"))
parser.add_argument("-o", "--output", action="store")
parsedArgs = parser.parse_args()

srcLines = []
for f in parsedArgs.files:
    srcLines += f.readlines()

# Labels are GOTO/GOSUB targets or constant definitions.
labelTable = {}

whitespaceMatcher = re.compile(r"\s*$")
lineNumberMatcher = re.compile(r"\d+:\s*$")
labelMatcher = re.compile(r"_\w+_:\s*$")
lineMatcher = re.compile(r"\s.*")
commentMatcher = re.compile(r"\s*#.*$")
assignmentMatcher = re.compile(r"_\w+_\s*=.*$")
ifThenMatcher = re.compile(r".*IF.*THEN.*$")

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
        codeLines[currentLine] = codeLines[currentLine] + [l.rstrip("\r\n").strip()]

def findRemStatement(line):
    inString = False
    atStatementStart = True
    for index, char in enumerate(line):
        if char == '"':
            inString = not inString
            atStatementStart = False
        elif not inString:
            if atStatementStart and line[index:index+3].upper() == "REM" and (
                    index + 3 == len(line) or not (line[index+3].isalnum() or line[index+3] in "_$")):
                return index
            if not char.isspace():
                atStatementStart = char == ":"
    return -1

def replaceLabels(l):
    r = []
    for i in l:
        remIndex = findRemStatement(i)
        remStatement = ""
        if remIndex >= 0:
            remStatement = i[remIndex:]
            i = i[:remIndex]
        for (k,v) in labelTable.items():
            i = i.replace(k, v)
        r.append(i + remStatement)
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
        remIndex = findRemStatement(i)
        remStatement = ""
        if remIndex >= 0:
            remStatement = i[remIndex:]
            i = i[:remIndex]
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
        s = s + remStatement.rstrip()
        if len(s) > 56:
            raise Exception("Line " + str(len(s)-56) + " characters too long: " + s)
        r.append(s)
    return r

codeLines = { n:collapse(l) for (n, l) in codeLines.items() }    

# THEN GOTO = THEN
def removeGotos(l):
    r = []
    for i in l:
        remIndex = findRemStatement(i)
        if remIndex >= 0:
            r.append(i[:remIndex].replace("THENGOTO", "THEN") + i[remIndex:])
        else:
            r.append(i.replace("THENGOTO", "THEN"))
    return r

codeLines = { n:removeGotos(l) for (n, l) in codeLines.items() }    

result = []

def appendLine(l):
    if l.strip().isdigit():
        return
    if l.strip() != "":
        result.append(l)

# Pack code into lines of at most 60 characters
for (num,line) in codeLines.items():
    currentLine = num
    outline = str(currentLine)
    separator= ""
    for l in line:
        if len(outline) + 1 + len(l) > 60:
            appendLine(outline)
            currentLine += 10
            outline = str(currentLine)
            separator = ""
        if ifThenMatcher.match(l) and findRemStatement(l) < 0:
            outline += separator + l
            appendLine(outline)
            currentLine += 10
            outline = str(currentLine)
            separator = ""
        else:
            outline += separator + l
            separator = ":"
            if findRemStatement(l) >= 0:
                appendLine(outline)
                currentLine += 10
                outline = str(currentLine)
                separator = ""
    appendLine(outline)

result.sort(key=lambda l: int(re.match(r"\d+", l).group()))

output = stdout
if parsedArgs.output:
    output = open(parsedArgs.output, "w")

for l in result:
    output.write(l)
    output.write("\n")
