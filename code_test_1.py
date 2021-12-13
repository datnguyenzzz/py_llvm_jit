from llvm_jit import llvm_jit

@llvm_jit
def func(a,b):
    c = a + b 
    
    for i in range(a,b,2):
        c = c + i 
    
    return c

print(func(1,8))