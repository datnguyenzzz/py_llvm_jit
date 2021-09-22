#####################################################
#it takes a tuple of arguments to a single output.  #
#t : a            (Type Variable)                   #
#  | C(t)        (Named Constructor)               #
#  | t            (Type Application)                #
#  | [t] -> t     (Function type)                   #
#####################################################

class TVar(object):
    def __init__(self, s):
        self._s = s 

    def __eq__(self, other):
        if isinstance(other, TVar):
            return self._s == other._s 
        else:
            return False
    
    def __repr__(self):
        return self._s 

class TCon(object):
    def __init__(self, s):
        self._s = s 

    def __eq__(self, other):
        if isinstance(other, TCon):
            return self._s == other._s 
        else:
            return False
    
    def __repr__(self):
        return self._s 

class TApp(object):
    def __init__(self, a, b):
        self._a = a 
        self._b = b 
    
    def __eq__(self, other):
        if isinstance(other, TApp):
            return self._a == other._a and self._b == other._b
        else:
            return False
    
    def __repr__(self):
        return str(self._a) + " " + str(self._b)
    
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

