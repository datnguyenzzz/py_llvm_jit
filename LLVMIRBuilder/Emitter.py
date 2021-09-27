#IRBuilder is the workhorse of LLVM Intermediate representation 
#(IR) generation. It allows you to fill the basic blocks of your functions with LLVM instructions.

import sys 
sys.path.append("../")

from LLVMIRBuilder.LLVM_types import *

from collections import defaultdict
from llvmlite import ir

class LLVMEmitter(object):
    #Contains properties : 
    #self._function : LLVM Function 
    #self._builder: LLVM Builder 
    #self._locals: Local variables
    #self._meta_data: Array of metadatas 
    #self._exit_block: Exit block 
    #self._spec_types: type specialization 
    #self._ret_type: return type 
    #self._arg_types: Argument types 

    def __init__(self, spec_types, ret_type, arg_types):
        self._function = None 
        self._builder = None 
        self._locals = {} 
        self._meta_data = defaultdict(dict)
        self._exit_block = None 
        self._spec_types = spec_types 
        self._ret_type = ret_type 
        self._arg_types = arg_types
    
    @property 
    def function(self):
        return self._function
    
    @property 
    def builder(self):
        return self._builder

    @property 
    def locals(self):
        return self._locals
    
    @property 
    def meta_data(self):
        return self._meta_data

    @property 
    def exit_block(self):
        return self._exit_block

    @property 
    def spec_types(self):
        return self._spec_types
    
    @property 
    def ret_type(self):
        return self._ret_type
    
    @property 
    def arg_types(self):
        return self._arg_types
    
    @function.setter
    def function(self, n_function):
        self._function = n_function
    
    @builder.setter
    def builder(self, n_builder):
        self._builder = n_builder
    
    @exit_block.setter
    def exit_block(self, n_exit_block):
        self._exit_block = n_exit_block
    
    def start_function(self, name, module, ret_type, arg_types):
        #typedef int32_t (*fnty)(double, int32_t *);
        func_type = ir.FunctionType(ret_type, arg_types, False)
        function = ir.Function(module, func_type, name)

        entry_block = function.append_basic_block("entry") 
        builder = ir.IRBuilder(entry_block)
        self.function = function
        self.builder = builder
        self.exit_block = function.append_basic_block("exit")
    
    def end_function(self):
        self._builder.position_at_end(self._exit_block)

        if 'retval' in self._locals:
            #return a variable 
            retval = self._builder.load(self._locals['retval']) 
            self._builder.ret(retval) 
        else:
            self._builder.ret_void()

    def add_block(self, name):
        return self._function.append_basic_block(name)

    #traverse thought AST tree 
    def visit(self, node):
        name = f"visit_{type(node).__name__}"
        if hasattr(self, name):
            return getattr(self,name)(node) 
        else:
            return self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        print(vars(node))
    
    def generic_visit(self,node):
        return NotImplementedError

if __name__ == "__main__":
    pass 
    
        