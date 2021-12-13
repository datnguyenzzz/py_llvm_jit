from llvm_jit import llvm_jit

@llvm_jit
def func(a,b):
    c = a / b
    return c

print(func(6,8))