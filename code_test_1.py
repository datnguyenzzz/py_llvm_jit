from llvm_jit import py_llvm_jit

@py_llvm_jit(PARSE=True, LLFUNC=True)
def test_11(flag):
    c = 123
    if flag:
       c = 432
    else:
       c = 123 
    
    return c
 
print(test_11(True)) 
print(test_11(False))