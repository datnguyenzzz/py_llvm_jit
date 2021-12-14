from llvm_jit import py_llvm_jit
import time

@py_llvm_jit(AST=False, PARSE=False, INFER=True, LLFUNC=False)
def addup(a,b):
    step = 1
    
    f = 3 
    e = f 
    a = e 
    
    c = 100
    b = c
    c = a + b 
    
    
    for i in range(a,b,step):
        if (a+b+i)%2==(a+i)%2:
            c = c + i
        else:
            c = c - i 
    
    return c


print(addup(1,100))