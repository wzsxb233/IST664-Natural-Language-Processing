import random
import string

listCode=[]

for i in range(1,100):
    listCode.append(''.join(random.sample(string.ascii_uppercase+string.digits,8)))