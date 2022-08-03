
import string
import random
def id_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

idlist=[]
for a in range(100):
    idlist.append(id_generator())