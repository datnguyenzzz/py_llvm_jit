#IRBuilder is the workhorse of LLVM Intermediate representation 
#(IR) generation. It allows you to fill the basic blocks of your functions with LLVM instructions.

import sys 
sys.path.append("../")

from LLVMIRBuilder.LLVM_types import *

from core.expressions import *
from collections import defaultdict
from llvmlite import ir

def set_const(val):
    if isinstance(val, int):
        return ir.Constant(int_type, val) 
    elif isinstance(val, float):
        return ir.Constant(double_type, val) 
    elif isinstance(val, bool):
        return ir.Constant(bool_type, int(val))
    else:
        raise NotImplementedError 

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
    #self._module: Module for wrap function together 

    def __init__(self, spec_types, arg_types, ret_type, chief_module):
        self._function = None 
        self._builder = None 
        self._locals = {} 
        self._meta_data = defaultdict(dict)
        self._exit_block = None 
        self._spec_types = spec_types 
        self._ret_type = ret_type 
        self._arg_types = arg_types
        self._module = chief_module

    @property
    def module(self):
        return self._module
    
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

        #print("-------------------")
        #print(function) 
        #print(entry_block)
        #print(builder) 
        #print(self.exit_block)
        #print("-------------------")
    
    def end_function(self):
        self._builder.position_at_end(self._exit_block)

        if 'retval' in self._locals:
            #return a variable 
            retval = self._builder.load(self._locals['retval']) 
            self._builder.ret(retval) 
        else:
            self._builder.ret_void()

    #add block to function
    def add_block(self, name):
        return self._function.append_basic_block(name)
    
    #Unconditional jump to the target
    def branch(self, next_block):
        self._builder.branch(next_block)
    
    def cbranch(self, cond, block_1, block_2):
        self._builder.cbranch(cond, block_1, block_2)
        
    #positioning at end of block 
    def set_block(self, block):
        self._block = block 
        self._builder.position_at_end(block)

    #traverse thought AST tree 
    def visit(self, node):
        name = f"visit_{type(node).__name__}"
        if hasattr(self, name):
            return getattr(self,name)(node) 
        else:
            return self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        #print(vars(node))
        rettype = to_llvm_type(self._ret_type)
        argtype = list(map(to_llvm_type, self._arg_types))
        fname = name_hashed(node.name, self._arg_types) 
        self.start_function(fname, self._module, rettype, argtype)
        
        for (node_arg, llvm_arg, func_arg) in zip(node.args, self._function.args, self._arg_types):
            arg_name = node_arg.id 
            llvm_arg.name = arg_name

            if is_array(func_arg):
                zero,one,two = set_const(0), set_const(1), set_const(2) 
                #getelementptr
                #get the address of a subelement of an aggregate data structure
                data = self._builder.gep(llvm_arg, [zero, zero], name=(arg_name + "_data")) 
                dims = self._builder.gep(llvm_arg, [zero, one], name=(arg_name + "_dims")) 
                shape = self._builder.get(llvm_arg, [zero, two], name=(arg_name + "_shape"))

                self._meta_data[arg_name]['data'] = self._builder.load(data) 
                self._meta_data[arg_name]['dims'] = self._builder.load(dims) 
                self._meta_data[arg_name]['shape'] = self._builder.load(shape) 
                self._locals[arg_name] = llvm_arg
            else:
                #alloca and store func arg to
                arg_ref = self._builder.alloca(to_llvm_type(func_arg)) 
                self._builder.store(llvm_arg, arg_ref) 
                self._locals[arg_name] = arg_ref
                #print(f"{arg_name} = {llvm_arg} -> {arg_ref}")
        
        if rettype is not void_type:
            self._locals['retval'] = self._builder.alloca(rettype, name="retval")
        
        #print(self._locals)
        _ = list(map(self.visit, node.body)) 
        self.end_function()
    
    def visit_Return(self, node):
        #print("-------------- <llvm return> -----------------------")
        #print(node)
        #print(vars(node.value))
        llvm_value = self.visit(node.value)
        if llvm_value.type != void_type:
            self._builder.store(llvm_value, self._locals['retval'])
        
        self.branch(self._exit_block)
        #print("-------------- </llvm return> -----------------------")
    
    def visit_Int(self,node):
        return ir.Constant(int_type, node.n)
    
    def visit_Float(self,node):
        return ir.Constant(double_type, node.n)
    
    def visit_Str(self, node):
        return ir.Constant(string_type(len(node.s)), node.s)
    
    def visit_Call(self,node):
        sz = len(node.args) 
        args = [] 
        for _arg in node.args:
            args.append(self.visit(_arg))
            
        return (args,None)
    
    def visit_For(self,node):
        #print("------for -- llvm ir-------")
        init_block = self.function.append_basic_block('for.init') 
        cond_block = self.function.append_basic_block('for.cond')
        body_block = self.function.append_basic_block('for.body') 
        end_block = self.function.append_basic_block('for.end')
        
        #increament init
        self.branch(init_block)
        self.set_block(init_block)
        
        args,_ = self.visit(node.iter)
        start,end = args[0], args[1]
        if len(args) == 2:
            inc_size = ir.Constant(int_type, 1) 
        else:
            inc_size = args[2]
            
        inc = self.visit(node.target)
        self._builder.store(start, inc)
        
        #loop condition
        self.branch(cond_block)
        self.set_block(cond_block)
        cond = self._builder.icmp_signed('<', self._builder.load(inc), end) 
        self.cbranch(cond, body_block, end_block)
        
        # loop body
        self.set_block(body_block)
        _ = list(map(self.visit, node.body))
        
        # increment counter 
        succ = self._builder.add(inc_size, self._builder.load(inc)) 
        self._builder.store(succ, inc) 
        
        #exit the loop 
        self.branch(cond_block)
        self.set_block(end_block)
        #print("------for -- llvm ir-------")
    
    def visit_Var(self, node):
        #print("------Var -- llvm ir-------")
        #must be declared 
        context = node.ctx
        if context == "#load":
            return self.builder.load(self._locals[node.id])
        elif context == "#store":
            id_name = node.id 
            local_v = self._builder.alloca(int_type, name=id_name)
            self._locals[id_name] = local_v
            return local_v
        else:
            raise Exception(f"Does not support {context} operation")
        #print("------Var -- llvm ir-------")

    def visit_BinOp(self,node):
        #print(vars(node))
        op = node.op 
        left = self.visit(node.left)
        right = self.visit(node.right)
        #print("left =",left,) 
        #print("right =",right)
        if op == "#add":
            if left.type == int_type:
                return self.builder.add(left, right)
            else:
                return self.builder.fadd(left,right)
        elif op == "#sub":
            if left.type == int_type:
                return self.builder.sub(left, right)
            else:
                return self.builder.fsub(left,right)
        elif op == "#mult":
            if left.type == int_type:
                return self.builder.mul(left, right)
            else:
                return self.builder.fmul(left,right)
        elif op == "#div":
            if left.type == int_type:
                return self.builder.sdiv(left, right)
            else:
                return self.builder.fdiv(left,right)
        elif op == "#mod":
            if left.type == int_type:
                return self.builder.srem(left, right)
            else:
                raise Exception(f"Haven't support remainder for float")
        else:
            raise Exception(f"Haven't support operation {op} yet")
    
    def visit_Assign(self, node):
        target_var = node.targets.id
        llvm_var = None 
        llvm_value = self.visit(node.value)
        if target_var in self._locals:
            #already allocated 
            llvm_var = self._locals[target_var]
        else:
            #first time 
            llvm_var = self.builder.alloca(llvm_value.type, name=target_var)
        
        self.builder.store(llvm_value, llvm_var) 
        self._locals[target_var] = llvm_var 
        return llvm_var
    
    def visit_If(self,node):
        #print(type(node.test), isinstance(node.test, Compare))
        if isinstance(node.test, Compare):
            cond = self.visit(node.test)
        else:
            left_value = self.visit(node.test)
            op = "=="
            right_value = ir.Constant(bool_type, 1)
            cond = self._builder.icmp_signed(op, left_value, right_value) 
        
        with self._builder.if_else(cond) as (then, orelse):
            with then:
                _ = self.visit(node.body) 
            with orelse:
                _ = self.visit(node.orelse) 
    
    def visit_Bool(self, node):
        print("--------- llvm bool-------------")
        n = 0 if node.n==False else 1 
        return ir.Constant(bool_type, n)
        print("--------- llvm bool-------------")
      
    def visit_Compare(self,node):
        #print("------------- llvm cond ----------------")
        #print(vars(node))
        left_value = self.visit(node.left) 
        right_value = self.visit(node.comparators[0])
        op = node.ops[0]
        #print(left_value) 
        #print(op) 
        #print(right_value)
        return self._builder.icmp_signed(op, left_value, right_value) 
        #print("------------- llvm cond ----------------")

    def generic_visit(self,node):
        return NotImplementedError

if __name__ == "__main__":
    pass 
    
        