import sys 
sys.path.append("../")

from custom_types.basics import *

from llvmlite import ir

pointer = ir.PointerType

int_type = ir.IntType(32) 
float_type = ir.FloatType()
double_type = ir.DoubleType() 
bool_type = ir.IntType(1) 

void_type = ir.VoidType()
void_ptr = pointer(ir.IntType(8))

# LLVM types mapping

llvm_types_map = {
    int32 : int_type, 
    int64 : int_type,
    float32 : float_type,
    double64 : double_type,
} 

def to_llvm_type(dtype):
    return llvm_types_map[dtype]