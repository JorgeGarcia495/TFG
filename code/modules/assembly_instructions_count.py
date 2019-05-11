#!/usr/bin/env python3

import os
import glob
import subprocess

def create_asm():
    
    directory = '../results/instructions_estimation/'
    if not os.path.exists(directory):
        os.mkdir('../results/instructions_estimation/')
    
    #Binary disassembly:
    subprocess.check_call("./maqao.intel64 disass --uarch=HWL -dbg ../../nas_bt/bin/bt.B.x > ../results/instructions_estimation/app_asm", shell=True)
    #Loop list extraction:
    subprocess.check_call("./maqao.intel64 analyze --uarch=HWL -ll ../../nas_bt/bin/bt.B.x > ../results/instructions_estimation/loops_1", shell=True)

    #Loop list:
    for file in glob.glob('../results/instructions_estimation/loops_1'):
        with open(file,encoding="utf-8") as f:
            loops_1 = f.readlines()
    x1=[x.partition("| ")[2].partition(" ")[0] for x in loops_1]
    x2 = list(filter(None, x1))
    del x2[0]
    loop_list=",".join(x2)

    #Loops information (loop location in source code):
    subprocess.check_call("./maqao.intel64 cqa --uarch=HWL -dbg -ani ../../nas_bt/bin/bt.B.x loop="+loop_list+"> ../results/instructions_estimation/loops_2", shell=True)
    for file in glob.glob('../results/instructions_estimation/loops_2'):
        with open(file,encoding="utf-8") as f:
            loops_2 = f.readlines()
    x1=[x.strip('\n') for x in loops_2]
    loop_dict={}
    flag=0
    for i in x1:
        if i.partition("loop #")[1]=="loop #":
            flag=1
            loop_number=str(i.partition("loop #")[2])
        if flag==1:
            if i.partition("The loop is defined in")[1]=="The loop is defined in":
                loop_dict[loop_number]=i.partition(":")[2]
                flag=0
            else:
                loop_dict[loop_number]=0
            
        
    #Total assembly instructions per each function:
    new_content = []
    for file in glob.glob('../results/instructions_estimation/app_asm'):
        with open(file,encoding="utf-8") as f:
            content=f.readlines()
    content = [x.strip('\n') for x in content]
    content2= [x.split(" ") for x in content]        
    inst=0
    for i in range(len(content)):
        a=content[i].strip(' ')
        a1=a.partition("/")
        a2=a.partition(":")
        a3=a.partition(" ")[2]
        a4=(a3.partition("(")[2]).partition(" ")[0]           
        if a1[1]=="/":
            source_line=a2[2]
        else:
            if len(content2[i])>1:
                if a4 == "function":
                    new_content.append(str(inst-2))
                    funct=(a3.partition("(")[2]).partition(" ")[2]
                    new_content.append(funct)
                    inst=0
                elif a.rpartition(" ")[2]=="entry":
                    new_content.append(str(inst-2))
                    new_content.append("Loop entry"+a.rpartition(" ")[0]+" "+str(loop_dict[a.rpartition(" ")[0].rpartition(" ")[2]]))
                    inst=0
                elif a.rpartition(" ")[2]=="exit":
                    new_content.append(str(inst-2))
                    new_content.append("Loop exit"+a.rpartition(" ")[0])
                    inst=0
                inst=inst+1

       

    thefile = open('../results/instructions_estimation/asm_instructions', 'w')
    for item in new_content:
        thefile.write("%s\n" % item)

if __name__ == '__main__':
    create_asm()
