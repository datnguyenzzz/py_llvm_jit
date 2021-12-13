import sys 

from functools import reduce 

import numpy as np 
from llvmlite import ir
import llvmlite.binding as llvm

from optimizes import unification,llvm_passes
from custom_types.basics import *
from LLVMIRBuilder import Emitter
from . import jit_wrapper

FUNC_CACHE = {}

# modules in the IR layer allow you to build and group functions together, 
# modules in the binding layer give access to compilation, 
# linking and execution of code. 
# To distinguish between them, 
# the module class in the binding layer is called ModuleRef 
# as opposed to llvmlite.ir.Module.

MODULE = ir.Module('pyjit')

def arg_py_type(arg):
    if isinstance(arg, int) and arg <= sys.maxsize:
        return int64 
    elif isinstance(arg, float):
        return double64
    elif isinstance(arg, np.ndarray):
        if arg.dtype == np.dtype('int32'):
            return array(int32)
        elif arg.dtype == np.dtype('int64'):
            return array(int64)
        elif arg.dtype == np.dtype('float'):
            return array(float32)
        elif arg.dtype == np.dtype('double'):
            return array(double64)
    else:
        raise Exception(f'Type not supported {type(arg)}')

def determined(arg):
    #define argument x is determined or not 

    def _get_variables(x):
        if isinstance(x, TCon):
            return set() 
        elif isinstance(x, TVar):
            return set([x])
        elif isinstance(x, TApp):
            return _get_variables(x.fn) | _get_variables(x.arg) 
        elif isinstance(x, TFunc):
            return reduce(set.union, map(_get_variables, x.args)) | _get_variables(x.ret)
    
    tmp = _get_variables(arg)
    return len(tmp) == 0

def create_execution_engine():
    # Create an ExecutionEngine suitable for JIT code generation on
    # the host CPU
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine() 
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    
    return engine

def code_gen(ast, specialization, spec_args, spec_ret):
    llvm_code = Emitter.LLVMEmitter(specialization, spec_args, spec_ret, MODULE)
    llvm_code.visit(ast)

    mod = llvm_passes.tuning(MODULE)

    engine = create_execution_engine() 
    engine.add_module(mod)

    return (llvm_code.function,engine)

def recompile(args, ast, infer_type, mgu):
    type_args = list(map(arg_py_type, list(args)))
    main_func = TFunc(args = type_args, ret = TVar("$ret"))
    unified = unification.unify(infer_type, main_func)
    
    specialization = unification.merge(unified, mgu)

    spec_ret = unification.apply(specialization, TVar("$ret")) 
    spec_args = [unification.apply(specialization, arg) for arg in type_args]
    
    if determined(spec_ret) and all(map(determined, spec_args)):
        func_name = "".join([ast.name,str(hash(tuple(spec_args)))])

        if func_name in FUNC_CACHE:
            return FUNC_CACHE[func_name](*args)
        else:
            llfunc,engine = code_gen(ast, specialization, spec_args, spec_ret)
            #already compile module 
            #need return compiled function from module 
            # translate to runnable function
            print("=============== LLVM FUNC =====================")
            print(llfunc)
            print("=============== RESULT =====================")
            wrap = jit_wrapper.JitWrapper(llfunc,engine)
            runnable_func = wrap.jit_module()
            FUNC_CACHE[func_name] = runnable_func
            return runnable_func(*args)
    else:
        raise Exception('Some argument has not been determined')