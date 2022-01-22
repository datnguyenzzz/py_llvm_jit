from llvm_jit import py_llvm_jit

@py_llvm_jit(PARSE=True, LLFUNC=True)
def test_11(flag):
    if flag:
       return 123
    else:
       return 321
    
print(test_11(True)) 
print(test_11(False))