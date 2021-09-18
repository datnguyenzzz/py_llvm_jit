import llvmlite.binding as llvm
from llvmlite import ir

mod = ir.Module(name = "Testing")
print(mod)
