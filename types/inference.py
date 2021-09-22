#inference type to Variable
#%ptr = alloca i32
#store i32 3, i32* %ptr
#%val = load i32* %ptr
#%join = phi i32 [ %plusOne, %left], [ -1, %right]
 
# So need to inference to own-defined type in LLVM [%..]

import string

def set_name():
    k = 0 
    while True:
        for a in string.ascii_lowercase:
            yield "".join([a,str(k)]) if k > 0 else a 
        
        k += 1

class TypeInference(object):
    def __init__(self):
        self.names = set_name() 

if __name__ == "__main__":
    pass