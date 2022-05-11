#!/usr/bin/env python3

def is_effective_line(str) :
    string = str.replace(" ", "")
    if string.find("}//") == 0 or string.find("{//") == 0 :
        return False
    if string.find("//") == 0 or string.find("/*") == 0 or string.find("*/") == len(str)-2 :
        return False
    if (string.find("}") == 0 or string.find("{") == 0) and len(string) == 1 :
        return False
    if string.find("}//") == 0 or string.find("{//") == 0:
        return False
    if string.find("{/*") == 0 and (string.find("*/") == len(str)-2 or string.find("*/") == -1):
        return False
    if string.find("*/}") == len(str)-3 :
        return False
    return True

def metric_count(input , output):
    f = open(input , 'r')
    LOC = 0
    eLOC = 0
    Comment = 0
    Blank = 0
    function = 0
    in_comment = False
    opened = 0
    closed = 0
    for line in f :
        if len(line.strip()) > 0:  # Detect line without blank line
            LOC += 1
            if not in_comment :
                if line.find("/*") != -1:
                    Comment += 1
                    if line.rfind("*/") != -1 and line.rfind("*/") > line.rfind("/*") :
                        in_comment = False
                    else :
                        in_comment = True
                    if line.find("{") != -1 and line.find("{") < line.find("/*"):
                        opened += 1
                    if line.find("}") != -1 and line.find("}") < line.find("/*"):
                        closed += 1
                if is_effective_line(line.strip()):
                    eLOC += 1
                if line.find("//") != -1 and not in_comment:
                    Comment += 1
                if line.find("{") != -1 and not in_comment:
                    opened += 1
                if line.find("}") != -1 and not in_comment:
                    closed += 1
            else :
                Comment += 1
                if line.find("*/")!= -1 :
                    in_comment = False
                    if line.rfind("{") != -1 and line.rfind("{") > line.rfind("*/"):
                        opened += 1
                    if line.rfind("}") != -1 and line.rfind("}") > line.rfind("*/"):
                        closed += 1
                    if is_effective_line(line.strip()):
                        eLOC += 1
                        if line.find("/*") != -1:
                            in_comment = True
            if opened == closed and opened > 0:
                function += 1
                opened = 0
                closed = 0
        else :
            Blank += 1

    f.close();

    f2 = open(output, 'w')
    f2.write("LOC = " +  str(LOC) + "\n")
    f2.write("eLOC = " + str(eLOC)+ "\n")
    f2.write("Comment : " + str(Comment)+ "\n")
    f2.write("Blank : " + str(Blank)+ "\n")
    f2.write("No. of functions : " + str(function)+ "\n")
    f2.close()

import sys

if(len(sys.argv) != 3):
    print("usage: ./metric_counter.py (inputfile) (outputfile)")
metric_count(sys.argv[1],sys.argv[2])
