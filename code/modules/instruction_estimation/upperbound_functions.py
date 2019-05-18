#!/usr/bin/env python3

import glob
import subprocess

def functions():

    subprocess.check_call("./maqao.intel64 analyze --uarch=HWL -lf ../../nas_bt/bin/bt.B.x > ../results/instructions_estimation/functions_list", shell=True)

    for file in glob.glob('../results/instructions_estimation/functions_list'):
        with open(file,encoding="utf-8") as f:
            functions_list = f.readlines()
        y=[x.partition("| ")[2].partition(" ")[0].strip('\n') for x in functions_list]
        functions = list(filter(None, y))
        del functions[0]
        functions.insert(0,"MAIN_")
        
    new_content = []
    for file in glob.glob('../results/upper_bound/upperbound_sc'):
        with open(file,encoding="utf-8") as f:
            content = f.readlines()
        content.insert(0,"Begin - MAIN_  0\n")
        content.insert(len(content),"End - MAIN_\n")
        content = [x.strip('\n') for x in content]

        flag=0
        flag1=0
        #function=functions
        for j in functions:
            for i in content:
                a=i.strip(' ')
                if a.partition("Begin - ")[2].partition(" ")[0]==j:
                    flag1=1
                    new_content.append(i)
                if a.partition("End - ")[2].partition(" ")[0]==j:
                    flag1=0
                    new_content.append(i)
                    break
                if a.partition("Begin")[1]=="Begin" and a.partition("Begin - ")[2].partition(" ")[0]!=j and flag1==1:
                    flag=flag+1
                if a.partition("End")[1]=="End" and a.partition("End - ")[2].partition(" ")[0]!=j and flag1==1:
                    flag=flag-1
                
                if a.partition("Loop")[1]=="Loop" and flag1==1 and flag==0:
                    new_content.append(i)

            
       

        thefile = open('../results/upper_bound/upperbounds_functions', 'w')
        for item in new_content:
            thefile.write("%s\n" % item)
        new_content=[]
if __name__ == '__main__':
    functions()
