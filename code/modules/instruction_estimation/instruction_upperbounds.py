#!/usr/bin/env python3

import glob
import subprocess

def upperbounds():

    subprocess.check_call("./maqao.intel64 analyze --uarch=HWL -lf ../../nas_bt/bin/bt.B.x > ../results/instructions_estimation/functions_list", shell=True)

    for file in glob.glob('../results/instructions_estimation/functions_list'):
        with open(file,encoding="utf-8") as f:
            functions_list = f.readlines()
        y=[x.partition("| ")[2].partition(" ")[0].strip('\n') for x in functions_list]
        functions = list(filter(None, y))
        del functions[0]
        functions.insert(0,"MAIN_")
    
    for file in glob.glob('../results/instructions_estimation/asm_instructions_loop_sync'):
        with open(file) as f:
            content = f.readlines()
        content = [x.strip('\n') for x in content]


    for file in glob.glob('../results/upper_bound/upperbounds_functions'):
        with open(file) as f:
            content2 = f.readlines()
        content2 = [x.strip('\n') for x in content2]

   
    kk=dict.fromkeys(functions,[])
    kk2=dict.fromkeys(functions,[])
    for k,_ in kk.items():
        kk[k]=[]
        kk2[k]=[]
    
    flag=0
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
                kk[f].append(i1)

    flag=0
    for f in functions:
        flag=0
        for i in content2:
            i1=i.strip(' ')
            i2=i1.partition("Begin - ")[2].partition(" ")[0]
            i3=i1.partition("End - ")[2].partition(" ")[0]
            if i2==f:
                flag=1
            if flag==1 and i3==f:
                flag=0
            if flag==1:
                kk2[f].append(i1)

        
    flag = 0
    new_content = []
    counter = 0
    for f in functions:
        for i in kk[f]:
            counter=0
            for j in kk2[f]:
                counter=counter+1
                i2=i.strip(' ')
                j2=j.strip(' ')
                i3=(i2.partition(" ")[2]).partition(" ")[0]
                j3=(j2.partition(" ")[2]).partition(" ")[0]
                i4=((i2.partition(" ")[2]).partition(" ")[2]).partition(" ")[0]
                j4=((j2.partition(" ")[2]).partition(" ")[2]).strip(' ')
                j5=j4.partition(" ")[0]
                if i3=="entry;" and j3=="entry" and i4==j5:
                    new_content.append(i+" "+j2.rpartition(" ")[0]+" "+j2.rpartition(" ")[2])
                    del kk2[f][0:counter]
                    flag=1
                    break
                else:
                    flag=0
            if flag==0:
                new_content.append(i)            
                
        
    thefile = open('../results/instructions_estimation/instructions_upperbounds', 'w')
    for item in new_content:
        thefile.write("%s\n" % item)
    new_content=[]
if __name__ == '__main__':
    upperbounds()
