s = input(print("Enter"))
leftShifts = 1
for i in range(0,leftShifts):
    if (len(s)==1):
        pass
    else:
        for x in range(0,len(s)):
            if(x==0):
                temp[x]=s[len(s)-1]
            elif(x==(len(s)-1)):
                temp[x] = s[0]
            else:
                temp[x] = s[x+1]
        s=temp
print(s)