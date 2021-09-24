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
    def __init__(self, con, dtype):
        self._con = con 
        self._dtype = dtype
    
    @property
    def con(self):
        return self._con

    @con.setter 
    def con(self,n_con): 
        self._con = n_con

    @property
    def dtype(self):
        return self._dtype

    @dtype.setter 
    def dtype(self,n_dtype): 
        self._dtype = n_dtype
    
    def __hash__(self):
        return hash((self._con,self._dtype))
    
    def __eq__(self, other):
        if isinstance(other, TApp):
            return self._con == other._con and self._dtype == other._dtype
        else:
            return False
    
    def __repr__(self):
        return str(self._con) + " " + str(self._dtype)

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

