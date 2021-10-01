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

# Array type 
def array_type(elt):
    #struct_type(data_type, dimensions, shape)
    #the type names are unique within a context, 
    # the name collisions are resolved by LLVM automatically.
    struct_type = ir.global_context.get_identified_type('ndarray_' + str(elt)) 

    if struct_type.elements:
        return struct_type
    
    struct_type.set_body(
        pointer(elt), 
        ir.IntType(32),
        pointer(ir.IntType(32)) 
    )

    return struct_type

int32_array = pointer(array_type(int_type))
int64_array = pointer(array_type(ir.IntType(64)))
double_array = pointer(array_type(double_type))

# LLVM types mapping

#custom type  =>  LLVM type
llvm_types_map = {
    int32 : int_type, 
    int64 : int_type,
    float32 : float_type,
    double64 : double_type,
    array_int32 : int32_array, 
    array_int64 : int64_array, 
    array_double64 : double_array
} 

def to_llvm_type(dtype):
    return llvm_types_map[dtype]