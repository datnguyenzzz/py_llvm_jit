from llvm_jit import py_llvm_jit
import time

@py_llvm_jit(PARSE=False, LLFUNC=True)
def test_1(a,b):
    return a+b

print(test_1(5,6),"\n")

@py_llvm_jit(PARSE=False, LLFUNC=False)
def addup(a,b):
    step = 1
    c = 0
    for i in range(a,b,step):
        if i%2==1:
            c = c + 1
        else:
            c = c - 1 
    return c

def addup_1(a,b):
    step = 1
    c = 0
    for i in range(a,b,step):
        if i%2==1:
            c = c + 1
        else:
            c = c - 1 
    return c

print("Function with LLVM JIT compiler")
print(addup(1,10000000),"\n")

print("Function without LLVM JIT compiler")
s = time.time() 
res = addup_1(1,10000000)
print("=============== TIME EXEC =====================")
print(time.time() - s)
print("=============== RESULT ========================")
print(res)