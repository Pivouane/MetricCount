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

types = ["string" , "int", "short", "bool", "long", "signed", "double" , "float" ,"unsigned", "char", "byte", "void"]
op = ["/=" , "+=" , "-=" , "*=" , "="] 

def func_name(str):
    res = ""
    for type in types :
        if  str.find(type) != -1 :
            if str.find("(") != -1:
                ind = str.find("(")-1
                while str[ind] == ' ' :
                    ind -= 1
                while ind > 0 and str[ind] != ' ':
                    res += str[ind]
                    ind -=1
                break
    return res[::-1]

def func_used(str):
    res = ""
    if  str.find(".") != -1 :
        if str.find("(") != -1:
            ind = str.find("(")-1
            while str[ind] == ' ' :
                ind -= 1
            while ind > 0 and str[ind] != '.':
                res += str[ind]
                ind -=1
    return res[::-1]    

def class_name(str):
    res = ""
    if  str.find("class") != -1 :
        ind = str.find("class") + 5
        while str[ind] == ' ' :
            ind += 1
        while ind < len(str) and str[ind] != ' ' and str[ind]!= "\n" :
            res += str[ind]
            ind +=1
    return res

def var_used(str):
    res = ""
    for type in op :
        if str.find(type) != -1 :
            if str.find(";") != -1:
                ind = str.find(type)-2
                while str[ind] == ' ' :
                    ind -= 1
                while ind > 0 and str[ind] != ' ':
                    res += str[ind]
                    ind -=1
                break
    
    if res != "" : 
        return res[::-1]
    else:
        if str.find("return") != -1 :
            ind = str.find("return")+ 6 
            while str[ind] == ' ' :
                ind += 1
            while ind < len(str) and str[ind] != ';' and str[ind]!= "\n" :
                res += str[ind]
                ind +=1
    return res

def local_method(str , global_method) : 
    res = "" 
    for meth in global_method : 
        for m in meth : 
            if str.find(m) != -1 : 
                res = m
                break 
    return res 

def oom_counter(input , output):
    f = open(input , 'r')
    label = []
    global_method = []
    method_used = []
    variable_used = []
    method_index = -1
    index = -1
    in_comment = False
    opened = 0
    closed = 0
    in_method = False 
    tmp = ""
    for line in f :
        if len(line.strip()) > 0:
            if not in_comment :
                if is_effective_line(line) :
                    tmp = class_name(line)
                    if tmp != "":
                        index += 1 
                        label.append(tmp)
                        global_method.append([])
                        method_used.append([])
                    if True : 
                        tmp = func_name(line)
                        if tmp != "" :
                            global_method[index].append(tmp)
                            method_used[index].append(tmp)
                            variable_used.append([])
                            method_index += 1
                            in_method = True
                    if line.find(";") != -1 and in_method == True: 
                        tmp = var_used(line) 
                        if tmp != "" : 
                            if tmp not in method_used :  
                                variable_used[method_index].append(tmp)
                        tmp = local_method(line , global_method)
                        if tmp != "" : 
                            method_used[index].append(tmp)
                        tmp = func_used(line)
                        if tmp != "" : 
                            if tmp not in method_used :  
                                method_used[index].append(tmp)
                if line.find("/*") != -1:
                    if line.rfind("*/") != -1 and line.rfind("*/") > line.rfind("/*") :
                        in_comment = False
                    else :
                        in_comment = True
                    if line.find("{") != -1 and line.find("{") < line.find("/*") and in_method == True:
                        opened += 1
                    if line.find("}") != -1 and line.find("}") < line.find("/*") and in_method == True:
                        closed += 1
                    if line.find("{") != -1 and not in_comment and in_method == True:
                        opened += 1
                    if line.find("}") != -1 and not in_comment and in_method == True:
                        closed += 1
            else :
                if line.find("*/")!= -1:
                    in_comment = False
                    if line.rfind("{") != -1 and line.rfind("{") > line.rfind("*/") and in_method == True: 
                        opened += 1
                    if line.rfind("}") != -1 and line.rfind("}") > line.rfind("*/") and in_method == True: 
                        closed += 1
                    
                    if is_effective_line(line) :
                        tmp = class_name(line)
                        if tmp != "":
                            index += 1
                            label.append(tmp)
                            global_method.append([])
                            method_used.append([])
                        if True :
                            tmp = func_name(line)
                            if tmp != "" :
                                global_method[index].append(tmp)
                                method_used[index].append(tmp)
                                variable_used.append([])
                                method_index += 1
                                in_method = True
                        if line.find(";") != -1 and in_method == True:
                            tmp = var_used(line) 
                            if tmp != "" :
                                variable_used[method_index].append(tmp)
                            tmp = local_method(line , global_method)
                            if tmp != "" :
                                if tmp not in method_used :  
                                    method_used[index].append(tmp)
                            tmp = func_used(line)
                            if tmp != "" :
                                if tmp not in method_used :  
                                    method_used[index].append(tmp)
                if line.find("/*") != -1:
                    in_comment = True
            if opened == closed and opened > 0:
                opened = 0
                closed = 0
                in_method = False
    
    f.close()
    f2 = open(output, 'w')
    for i in range(len(label)) : 
        f2.write(label[i]+ "\n")
        f2.write("   - wmc = " + str(len(global_method[i]))+ "\n")
        cbo = 0
        for j in range(len(global_method)) : 
            if j != i : 
                for met in method_used[i] : 
                    if met in global_method[j] : 
                        for met2 in method_used[j] : 
                            if met2 in  global_method[i] : 
                                cbo += 1             
        f2.write("   - cbo = " + str(cbo)+ "\n")
        rfc = len(method_used[i])
        f2.write("   - rfc = " + str(rfc)+ "\n")
        lcom = 0 
        f2.write("   - lcom = " + str(0)+ "\n")


import sys

if(len(sys.argv) != 3):
    print("usage: ./oom_counter.py (inputfile) (outputfile)")
else:
    oom_counter(sys.argv[1],sys.argv[2])
