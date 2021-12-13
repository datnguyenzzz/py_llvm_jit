from llvm_jit import llvm_jit

@llvm_jit
def addup(a,b):
    step = 2
    c = a + b 
    
    for i in range(a,b,step):
        c = c + i 
    
    return c

@llvm_jit
def test(a,b):
    c = 0
    if a==b:
        c = 1
    else:
        c = 2
    return c

#print(addup(1,8))
print(test(2,5))