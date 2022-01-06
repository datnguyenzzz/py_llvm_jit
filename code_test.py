from llvm_jit import py_llvm_jit
import time

print("=============== test 1 =====================")
@py_llvm_jit(PARSE=False, LLFUNC=False)
def test_1(a):
    return a

print(test_1(5),"\n")

print("=============== test 2 =====================")
@py_llvm_jit(PARSE=False, LLFUNC=False)
def test_2(a):
    return a

print(test_2(5.32),"\n")

print("=============== test 3 =====================")
@py_llvm_jit(PARSE=False, LLFUNC=False)
def test_3(a,b):
    c = a + b 
    return c

print(test_3(3,5),"\n")

print("=============== test 4 =====================")
@py_llvm_jit(PARSE=False, LLFUNC=False)
def test_4(a):
    c = 1 
    if a%2==0:
        c = 2 
    else:
        c = 3
    return c

print(test_4(3),"\n")

print("=============== test 5 =====================")
@py_llvm_jit(PARSE=False, LLFUNC=False)
def test_5(a):
    c = 0
    for i in range(0,a,1):
        c = c + i
    return c

print(test_5(10),"\n")

print("=============== test 6 =====================")
@py_llvm_jit(PARSE=False, LLFUNC=False)
def test_6(a):
    return a

print(test_6(1123.3),"\n")

print("=============== test 7 =====================")
@py_llvm_jit(PARSE=False, LLFUNC=False)
def test_7(a,b):
    c = a / b
    return c

print(test_7(1123.3, 123.3),"\n")

print("=============== test 8 =====================")
@py_llvm_jit(PARSE=False, LLFUNC=False)
def test_8(a,b):
    c = 0
    if ((a+b)/2) % 3 == 0:
        c = 1 
    else:
        c = 2 
    return c

print(test_8(12,1245),"\n")

print("=============== test 10 =====================")
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