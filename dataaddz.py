print("\033c\033[43;30m\ngive me a file to input? ")
filevarin=""
filevarout=""
var1=[]
var2=[]
start1=0
start2=0
i=0
counter=0
filesin=input()
print("\033[43;30m\ngive me a file to output? ")
filesout=input()
print("\033[43;30m\ngive me a a number to addicinate? ")
t=int(input())
f1=open(filesin,"r")
filevarin=f1.read()
f1.close()
var1=filevarin.split("\n")
for n in var1:
    if start1!=0:
        filevarout=filevarout+"\n"
    start1=start1+1
    start2=0
    var2=n.split(",")
    counter=0
    for m in var2:
        m=m.strip()
        i=int(m)
        if start2!=0:
            filevarout=filevarout+","
        start2=start2+1
        if counter==2:
            filevarout=filevarout+" "+str(i+t)
        else:
            filevarout=filevarout+str(i)
        counter=counter+1
        if counter==3:
            counter=0
f2=open(filesout,"w")
f2.write(filevarout)
f2.close()
        