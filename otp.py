import random
def genotp():
    u=[chr(i) for i in range(ord('A'),ord('Z')+1)]
    l=[chr(i) for i in range(ord('a'),ord('z')+1)]
    otp=''
    for i in range(2):
        otp+=random.choice(u)
        otp+=str(random.randint(0,9))
        otp+=random.choice(l)
    return otp
    