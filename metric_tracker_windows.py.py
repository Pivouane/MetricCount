import yaml
import json
import git
from git import Repo
import os.path
import os
import sys

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

def metric_count(input):
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

    f.close()
    l_result = []
    l_result.append(LOC)
    l_result.append(eLOC)
    l_result.append(Comment)
    l_result.append(Blank)
    l_result.append(function)
    return l_result

def metric_tracker(input , output) : 
    commits = []
    commit = ""
    repo_path = ""
    target_path = "" 
    f = open(input , 'r')
    i = 0 
    for line in f : 
        if i ==  0 :
            index = line.find("repository: ") + 12 
            while index < len(line) and line[index] != "\n" : 
                repo_path += line[index]
                index += 1 
        elif i == 1 : 
            index = line.find("target_path: ") + 13
            while index < len(line) and line[index] != "\n" : 
                target_path += line[index]
                index += 1 
        elif i > 2 : 
            commit = ""
            index = line.find("- ") + 2 
            while index < len(line) and line[index] != "\n" : 
                commit += line[index]
                index += 1 
            commits.append(commit)
        i += 1 
    repo = Repo(repo_path)
    input_file = os.path.join(repo_path, target_path)
    f2 = open(output , "w")
    f2.write("{"+ "\n")
    f2.write("  \"repositery\": "+ "\""+ repo_path + "\",\n")
    f2.write("  \"target_path\": "+ "\""+ target_path + "\",\n")
    f2.write("  \"metric_values\":\n")
    f2.write("          {"+ "\n")
    i = 0 
    for c in commits : 

        f2.write("            " + "\"" + c + "\""+ ":\n")
        f2.write("                  {" + "\n")
        repo.git.checkout(c)
        l = metric_count(input_file)
        f2.write("                    \"LOC\": " + "\"" + str(l[0]) + "\""+ ",\n" )
        f2.write("                    \"eLOC\": " + "\"" + str(l[1]) + "\""+ ",\n" )
        f2.write("                    \"Comment\": " + "\"" +str(l[2]) + "\""+ ",\n" )
        f2.write("                    \"Blank\": " + "\"" + str(l[3]) + "\""+ ",\n" )
        f2.write("                    \"Nfunc\": " + "\"" + str(l[4]) + "\""+ "\n" )
        if i == len(commits) -1 : 
            f2.write("                  }"+ "\n")
        else : 
            f2.write("                  },"+ "\n")
        i += 1 
    f2.write("          }"+ "\n")
    f2.write("}" + "\n")
import sys

if(len(sys.argv) != 3):
    print("usage: ./metric_tracker.py (inputfile) (outputfile)")
metric_tracker(sys.argv[1],sys.argv[2])
