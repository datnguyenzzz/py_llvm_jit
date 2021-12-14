from llvm_jit import llvm_jit
import time

@llvm_jit
def addup(a,b):
    step = 1
    c = a + b 
    
    for i in range(a,b,step):
        if (a+b+i)%2==0:
            c = c + i
        else:
            c = c - i 
    
    return c


s = time.time()
print(addup(1,20))
print(time.time() - s)