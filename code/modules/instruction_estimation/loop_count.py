#!/usr/bin/env python3

import glob

def count(directory):

    new_content = []
    for file in glob.glob(directory+'asm_instructions'):
        with open(file,encoding="utf-8") as f:
            content = f.readlines()
        content = [x.strip('\n') for x in content]
	
        flag = 0
        lines= 0
        loop_discard=[]
        for i in content:
            #Begin:
            i2 = i.strip(' ')
            i3=(i2.partition(" ")[2]).partition(";")[0]
            i4=i2.rpartition(" ")[2]
            i5=i2.rpartition(" ")[0].rpartition(" ")[2]
            i6=i2.rpartition(" ")[2]

            if i3=="entry" and i4=="0":
                loop_discard.append(i5)           
            if i3 == "entry" and i5 not in loop_discard:
                flag=flag+1
                new_content.append("Loop entry; "+str(flag)+" "+i4)
            elif i3=="exit" and i6 not in loop_discard:
                new_content.append("Loop exit; "+str(flag))
                flag=flag-1
            else:
                if i5 not in loop_discard and i6 not in loop_discard:
                    new_content.append(i)
            
            #End
            lines += 1
       

        thefile = open(directory+'asm_instructions_loop_sync', 'w')
        for item in new_content:
            thefile.write("%s\n" % item)
        new_content=[]
if __name__ == '__main__':
    count()
