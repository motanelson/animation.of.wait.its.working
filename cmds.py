import os
def loads(s):
    f1=open(s,"r")
    r=f1.read()
    f1.close()
    rr=r.split("\n")
    for n in range(len(rr)):
        rrr=rr[n].split("=")
        print(str(n)+":"+rrr[0])
    ss=input("give a option ? ")
    i=int(ss)
    rrr=rr[i].split("=")
    if len(rrr)<2:
        return ""
    else:
        return rrr[1]
print("\033c\033[43;30m\n")
t=True
s="main.pgm"
back=s
while t:
    if s.find(".pgm")>-1:
        back=s
        s=loads(s)
        
    else:
        s=loads(back)
        
    if s=="":
        t=False
    else:
        if s.find(".pgm")<0:
            os.system(s) 
    