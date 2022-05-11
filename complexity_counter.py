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

types = ["void" , "int", "char", "short", "long", "signed", "double" , "float" ,"unsigned"]
regions = ["if", "else if","case", "for", "while", "do while"]

def func_name(str):
    res = ""
    FAN_IN = 0
    for type in types :
        if  str.find(type) != -1 :
            if str.find("(") != -1:
                ind = str.find("(")-1
                while str[ind] == ' ' :
                    ind -= 1
                while ind > 0 and str[ind] != ' ':
                    res += str[ind]
                    ind -=1
                string = str.replace(" ", "")
                ind_u = string.find("(")
                ind_d = string.find(")")
                if ind_u + 1 != ind_d :
                    FAN_IN += 1
                while ind_u < ind_d :
                    if string[ind_u] == ',' :
                        FAN_IN += 1
                    ind_u += 1
                break;
    return res[::-1],FAN_IN

def cyclo_num(str):
    cyclo = 0
    FAN_OUT = 0
    for region in regions :
        if str.find(region) != -1:
            cyclo += 1
    if str.find("return") != -1 :
        FAN_OUT += 1
    return cyclo,FAN_OUT


def complexity_count(input , output):
    f = open(input , 'r')
    label = []
    cyclomatic_number = []
    FAN_IN = []
    FAN_OUT = []
    index = 0
    in_comment = False
    opened = 0
    closed = 0
    tmp3 = 0
    tmp4 = 0
    for line in f :
        if len(line.strip()) > 0:
            if not in_comment :
                tmp,tmp2 = func_name(line)
                if opened == 0 :
                    if tmp != "":
                        label.append(tmp)
                        FAN_IN.append(tmp2)
                if line.find("/*") != -1:
                    if line.rfind("*/") != -1 and line.rfind("*/") > line.rfind("/*") :
                        in_comment = False
                    else :
                        in_comment = True
                    if line.find("{") != -1 and line.find("{") < line.find("/*"):
                        opened += 1
                    if line.find("}") != -1 and line.find("}") < line.find("/*"):
                        closed += 1
                if line.find("{") != -1 and not in_comment:
                    opened += 1
                if opened != 0 :
                    a,b  = cyclo_num(line)
                    tmp3 += a
                    tmp4 += b
                if line.find("}") != -1 and not in_comment:
                    closed += 1
            else :
                if line.find("*/")!= -1 :
                    in_comment = False
                    if line.rfind("{") != -1 and line.rfind("{") > line.rfind("*/"):
                        opened += 1
                    if opened != 0:
                        a, b = cyclo_num(line)
                        tmp3 += a
                        tmp4 += b
                    if line.rfind("}") != -1 and line.rfind("}") > line.rfind("*/"):
                        closed += 1

                    if is_effective_line(line.strip()):
                        (tmp, tmp2)= func_name(line)
                        if opened == 0:
                            if tmp != "":
                                label.append(tmp)
                                FAN_IN.append(tmp2)
                        if line.find("/*") != -1:
                            in_comment = True
            if opened == closed and opened > 0:
                index += 1
                cyclomatic_number.append(tmp3 + 1 )
                FAN_OUT.append(tmp4)
                tmp3 = 0
                tmp4 = 0
                opened = 0
                closed = 0
    f.close();
    f2 = open(output, 'w')
    for i in range(len(label)) :
        f2.write(str(label[i])+":\n")
        f2.write("   - cyclomatic: "+ str(cyclomatic_number[i])+ "\n")
        aux = FAN_IN[i] + FAN_OUT[i]
        f2.write("   - ifc: "+str(aux)+"\n")
    f2.close()

import sys

if(len(sys.argv) != 3):
    print("usage: ./complexity_counter.py (inputfile) (outputfile)")
else:
    complexity_count(sys.argv[1],sys.argv[2])
