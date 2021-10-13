import sys 
sys.path.append("../")

import numpy as np 

from optimizes import unification
from custom_types.basics import *

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

def recompile(args, ast, infer_type, mgu):
    type_arg = list(map(arg_py_type, args))
    print(type_arg)
    return None