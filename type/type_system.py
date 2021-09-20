#####################################################
#it takes a tuple of arguments to a single output.  #
#t : a            (Type Variable)                   #
#  | C {t}        (Named Constructor)               #
#  | t            (Type Application)                #
#  | [t] -> t     (Function type)                   #
#####################################################

class Constructor(object):
    def __init__(self, s):
        self._s = s 

    def __eq__(self, other):
        if isinstance(other, Constructor):
            return self._s == other._s 
        else:
            return False
    
    def __repr__(self):
        return self._s 

class Application(object):
    def __init__(self, a, b):
        self._a = a 
        self._b = b 
    
    def __eq__(self, other):
        if isinstance(other, Application):
            return self._a == other._a and self._b == other._b
        else:
            return False
    
    def __repr__(self):
        return str(self._a) + " " + str(self._b)
    
int32 = Constructor("Int32") 
int64 = Constructor("Int64") 
float32 = Constructor("Float")
double64 = Constructor("Double")
void = Constructor("Void")

array = lambda x: Application(Constructor("Array"), x) 
array_int32 = array(int32) 
array_int64 = array(int64) 
array_double64 = array(double64)

if __name__=="__main__":
    print(array_int64)

