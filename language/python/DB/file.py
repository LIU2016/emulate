'''

write read

readline readlines

writeline writelines

'''

import os

f = open("./files/text1.txt","w")
f.write("helloworld")
f.close

f=open("./files/text2.txt","a")
f.write("牛逼啊")
f.close()

f=open("./files/text3.txt","w")
strings=['asbdddd'+os.linesep , "xxxxxx"+os.linesep , "yyyyyyyy"+os.linesep]
f.writelines(strings)
f.close()

f=open("./files/text3.txt","r")

while True:
    contents=f.readline()
    if contents=='':
        break;
    else:
        print(contents)
f.seek(0)
contentlist=f.readlines()
print(contentlist)
i=0
while i<len(contentlist):
    print(contentlist[i])
    i=i+1







