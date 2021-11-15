my_file=open('отот.txt','r')
t=my_file.readlines()
print(t)
c=0
minim=9999999
for i in range(len(t)):
    c=t[i].count('A')
    if c<minim:
        minim=c
        print(i)
        b=i
k=0
stry=sorted(t[b])
print(stry)
y=0
for i in range(len(stry)-1):
    if stry[i]==stry[i+1]:
        k+=1
        if k>=y:
            y=k
            #print(stry[i])
    else:
        k=0
print(y+1,stry[i])
# print(t.count(stry[i]))
ss=0
for i in range(len(t)):
    ss+=t[i].count(stry[i])
print(ss)
    
    