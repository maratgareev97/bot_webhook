'''141)    Текстовый файл 24-s1.txt состоит не более чем из 106 заглавных латинских букв
(A..Z). Текст разбит на строки различной длины. Определите количество строк,
в которых встречается комбинация F*O, где звёздочка обозначает любой символ.'''
my_file=open('24-s1.txt','r')
t=my_file.readlines()
k=0
l=0
max=[]
for i in range(len(t)-2):
    if t[i]=='F' and t[i+2]=='O':
        k+=1
        l=mas.append(k)
    else:
        k=0
print(l)
    
        