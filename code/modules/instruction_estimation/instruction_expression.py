#!/usr/bin/env python3

import glob
import subprocess

def total_instructions():
    result = {}
    subprocess.check_call("./maqao.intel64 analyze --uarch=HWL -lf ../../nas_bt/bin/bt.B.x > ../results/instructions_estimation/functions_list", shell=True)

    for file in glob.glob('../results/instructions_estimation/functions_list'):
        with open(file,encoding="utf-8") as f:
            functions_list = f.readlines()
        y=[x.partition("| ")[2].partition(" ")[0].strip('\n') for x in functions_list]
        functions = list(filter(None, y))
        del functions[0]
        functions.insert(0,"MAIN_")

    new_content = []
    for file in glob.glob('../results/instructions_estimation/instructions_upperbounds'):
        with open(file) as f:
            content = f.readlines()
        #print((file.partition("/")[2]).partition("/")[2])
        content = [x.strip('\n') for x in content]
        
    functions_dict=dict.fromkeys(functions,[])
    for k,_ in functions_dict.items():
        functions_dict[k]=[]
    
    for f in functions:
        flag=0
        for i in content:
            i1=i.strip(' ')
            i2=i1.partition("_):")[0]
            i3=i1.partition(")")[2]
            if i2==f:
                flag=1
            if flag==1 and i3!="" and i2!=f:
                flag=0
            if flag==1:
                functions_dict[f].append(i1)
	
    for f in functions:
        flag = 0
        upperbound="*1"
        upperbound_expression=""
        if functions_dict[f]==[]:
            continue
        for i in functions_dict[f]:
            #Begin:
            i2 = i.strip(' ')
            i3=(i2.partition(" ")[2]).partition(";")[0]
            i4=list(filter(None,i2.partition(":")[2].split(' ')))
            if i3 == "entry":
                if len(i4)==2:
                    uppbound=int(i4[1])-int(i4[0])+1
                    upperbound=upperbound+"*"+str(uppbound)
                if len(i4)>2:
                    uppbound=int(i4[0])-int(i4[1])+1
                    upperbound=upperbound+"*"+str(uppbound)
                if i4=="":
                    uppbound=1
                    upperbound=upperbound+"*"+str(uppbound)
                flag=flag+1
            elif i3== "exit":
                flag=flag-1
                upperbound=upperbound.rpartition("*")[0]
            else:
                upperbound_expression=upperbound_expression+"+"+i+upperbound                
            #End

        new_content.append("Function: "+f)
        new_content.append("Total Instructions: "+str(eval(upperbound_expression.partition("*")[2])))
        new_content.append("Total instructions expression: "+upperbound_expression.partition("*")[2])
        new_content.append("------------------------------------------------------------------------")
        result[new_content[len(new_content)-4]] = [new_content[len(new_content)-3], new_content[len(new_content)-2]]


    thefile = open('../results/instructions_estimation/total_instructions_per_function', 'w')
    for item in new_content:
        thefile.write("%s\n" % item)
    new_content=[]
    return result
    
if __name__ == '__main__':
    total_instructions()
