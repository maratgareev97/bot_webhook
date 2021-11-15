a=5*216**1256 - 5*36**1146 + 4*6**1053 - 1087
s=0
while a>0:
    otvet=a%6
    a=a//6
    s+=otvet
print(s)

