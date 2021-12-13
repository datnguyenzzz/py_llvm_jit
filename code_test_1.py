from llvm_jit import llvm_jit

@llvm_jit
def addup(a,b):
    c = a + b 
    return c

print(addup(5.2, 3.3))