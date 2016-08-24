a="11,2,3"
b=a.split(',')
c=[]
for x in b:
	x="\""+x+"\""
	c.append(x)
print(",".join(c))

def ch2utf(name):
    a=name.encode('utf-8',"s")
    return "".join(str(a).split("\\x"))[2:-1]


print(ch2utf("的.jpg"))
