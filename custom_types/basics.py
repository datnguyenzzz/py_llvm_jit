#####################################################
#it takes a tuple of arguments to a single output.  #
#t : a            (Type Variable)                   #
#  | C(t)        (Named Constructor)               #
#  | t            (Type Application)                #
#  | [t] -> t     (Function type)                   #
#####################################################

class TVar(object):
    def __init__(self, value):
        self._value = value 
    
    @property
    def value(self):
        return self._value

    @value.setter 
    def value(self,n_value): 
        self._value = n_value
        
    def __eq__(self, other):
        if isinstance(other, TVar):
            return self._value == other._value 
        else:
            return False
    
    def __hash__(self):
        return hash(self._value)
    
    def __repr__(self):
        return self._value

#Constructor: int32, int64, ...
class TCon(object):
    def __init__(self, value):
        self._value = value 

    @property
    def value(self):
        return self._value

    @value.setter 
    def value(self,n_value): 
        self._value = n_value
    
    def __hash__(self):
        return hash(self._value)

    def __eq__(self, other):
        if isinstance(other, TCon):
            return self._value == other._value 
        else:
            return False
    
    def __repr__(self):
        return self._value

class TApp(object):
    def __init__(self, fn, arg):
        self._fn = fn 
        self._arg = arg
    
    @property
    def fn(self):
        return self._fn

    @fn.setter 
    def fn(self,n_fn): 
        self._fn = n_fn

    @property
    def arg(self):
        return self._arg

    @arg.setter 
    def arg(self,n_arg): 
        self._arg = n_arg
    
    def __hash__(self):
        return hash((self._fn,self._arg))
    
    def __eq__(self, other):
        if isinstance(other, TApp):
            return self._fn == other._fn and self._arg == other._arg
        else:
            return False
    
    def __repr__(self):
        return str(self._fn) + " ( " + str(self._arg) + " ) "

class TFunc(object):
    def __init__(self, args, ret):
        self._args = args 
        self._ret = ret
    
    @property
    def args(self):
        return self._args

    @args.setter 
    def args(self,n_args): 
        self._args = n_args

    @property
    def ret(self):
        return self._ret

    @ret.setter 
    def ret(self,n_ret): 
        self._ret = n_ret
    
    def __eq__(self, other):
        if isinstance(other, TApp):
            return self._args == other._args and self._ret == other._ret
        else:
            return False
    
    def __repr__(self):
        return str(self._args) + " -> " + str(self._ret)

class InferenceError(Exception):
    def __init__(self, dtype_1, dtype_2):
        self._dtype_1 = dtype_1 
        self._dtype_2 = dtype_2 
    
    def __repr__(self):
        return '\n'.join(["Type mismatch: ",
                          f"Given: \t {str(self._dtype_1)}",
                          f"Expected: \t {str(self._dtype_2)}"])

class InfiniteType(Exception):
    def __init__(self, dtype_1, dtype_2):
        self._dtype_1 = dtype_1 
        self._dtype_2 = dtype_2 
    
    def __repr__(self):
        return '\n'.join(["Infinite occurs x = f(x): ",
                          f"Given: \t {str(self._dtype_1)}",
                          f"Expected: \t {str(self._dtype_2)}"])
  
 
int32 = TCon("Int32") 
int64 = TCon("Int64") 
float32 = TCon("Float")
double64 = TCon("Double")
void = TCon("Void")

array = lambda x: TApp(TCon("Array"), x) 
array_int32 = array(int32) 
array_int64 = array(int64) 
array_double64 = array(double64)

if __name__=="__main__":
    print(array_int64)

