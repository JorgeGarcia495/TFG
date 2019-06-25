#!/usr/bin/env python3

import glob

def parse(directory):

    new_content = []
    for file in glob.glob(directory+'BT/*.f'):
        with open(file) as f:
            content = f.readlines()
        content = [x.strip('\n') for x in content]	
        flag = 0
        flag1=0
        flag2=0
        counter = 0
        lines= 0
        lines1=1
        for i in content:
            #Begin:
            i2 = i.strip(' ')
            i3=i2.partition(" ")[0]
            if i3 == "do":
                flag=flag+1
                flag2=flag
                i4=i2.partition(" ")[2]
                if i4.partition(" ")[0]=="WHILE":
                    counter += 1
                    new_content.append(i)
                    new_content.append(' '*(i.count(' '))+"PRINT *,"+i4.partition(" ")[2]+","+str(lines1))
                    lines=lines-1
                else:
                    counter += 1
                    new_content.append(' '*(i.count(' '))+"PRINT *,"+'"Loop entry"'+","+str(flag)+","+str(lines1)+","+'":"'+","+(i2.partition(",")[0]).partition("=")[2]+","+i2.partition(",")[2])
                    new_content.append(i)
                    lines=lines-1
            elif i3=="enddo":
                counter += 1
                new_content.append(' '*(i.count(' ')+2)+"EXIT")
                new_content.append(i)
                new_content.append(' '*(i.count(' '))+"PRINT *,"+'"Loop exit"'+","+str(flag)+","+str(lines1))
                flag=flag-1
                flag2=flag2-1
                lines=lines-2
            elif i2.partition(" ")[0]+" "+i2.partition(" ")[2]=="end do":
                counter += 1
                new_content.append(' '*(i.count(' ')+2)+"EXIT")
                new_content.append(i)
                new_content.append(' '*(i.count(' '))+"PRINT *,"+'"Loop exit"'+","+str(flag)+","+str(lines1))
                flag=flag-1
                flag2=flag2-1
                lines=lines-2
            elif i3 == "call":
                if (i2.partition(" ")[2]).partition("(")[1]=="(":
                    if i2.partition(" ")[2][-1:]==")":
                        counter += 1
                        new_content.append(' '*(i.count(' '))+"PRINT *,"+'"Begin - '+i2.partition(" ")[2].partition("(")[0]+'"'+","+str(lines1))
                        new_content.append(i)
                        new_content.append(' '*(i.count(' '))+"PRINT *,"+'"End - '+i2.partition(" ")[2].partition("(")[0]+'"'+","+str(lines1))
                        lines=lines-2
                    else:
                        subroutine_name=i2.partition(" ")[2]
                        flag1=1
                        new_content.append(' '*(i.count(' '))+"PRINT *,"+'"Begin - '+subroutine_name.partition("(")[0]+'"'+","+str(lines1))
                        new_content.append(i)
                        lines=lines-1
                else:
                    counter += 1
                    new_content.append(' '*(i.count(' '))+"PRINT *,"+'"Begin - '+i2.partition(" ")[2]+'"'+","+str(lines1))
                    new_content.append(i)
                    new_content.append(' '*(i.count(' '))+"PRINT *,"+'"End - '+i2.partition(" ")[2]+'"'+","+str(lines1))
                    lines=lines-2

            elif flag1 == 1:
                 if i2.partition(" ")[2][-1:]==")":
                     flag1 = 0
                     counter += 1
                     new_content.append(i)
                     new_content.append(' '*(i.count(' '))+"PRINT *,"+'"End - '+subroutine_name.partition("(")[0]+'"'+","+str(lines1))
                     lines=lines-1
                 else:
                     new_content.append(i)
            else:
                new_content.append(i)
                
            #End
            lines += 1
            lines1 +=1


        thefile = open('../'+file.partition("/")[2], 'w')
        for item in new_content:
            thefile.write("%s\n" % item)
        new_content=[]
        
if __name__ == '__main__':
    parse()
