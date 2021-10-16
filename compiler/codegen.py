import sys 
sys.path.append("../")

from functools import reduce 

import numpy as np 

from optimizes import unification
from custom_types.basics import *

FUNC_CACHE = {}

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

def recompile(args, ast, infer_type, mgu):
    type_args = list(map(arg_py_type, args))
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
            pass
    else:
        raise Exception('Some argument has not been determined')

    return None