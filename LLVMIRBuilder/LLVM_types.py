from llvmlite import ir

pointer = ir.PointerType

int_type = ir.IntType(32) 
float_type = ir.FloatType()
double_type = ir.DoubleType() 
bool_type = ir.IntType(1) 

void_type = ir.VoidType()
void_ptr = pointer(ir.IntType(8))