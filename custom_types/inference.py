#inference type to Variable
#%ptr = alloca i32
#store i32 3, i32* %ptr
#%val = load i32* %ptr
#%join = phi i32 [ %plusOne, %left], [ -1, %right]
 
# So need to inference to own-defined type in LLVM [%..]

#ONLY SUPPORT EQUALITY RELATIONS 
#IN LARGE SCALE, ALL RELATIONS WILL BE INVOLVED
import sys
import string
sys.path.append("../")

from custom_types.basics import *
from Parser.parser import *

def set_name():
    k = 0 
    while True:
        for a in string.ascii_lowercase:
            yield "".join([a,str(k)]) if k > 0 else a 
        
        k += 1

class TypeInference(object):
    def __init__(self):
        self._type_ret = None
        self._names = set_name() 
        self._relation = []
        self._num_load = []
        self._cache = {}
    
    @property 
    def type_ret(self):
        return self._type_ret
    
    @property 
    def relation(self):
        return self._relation

    @property
    def cache(self):
        return self._cache
    
    @property
    def num_load(self):
        return self._num_load
    
    def __call__(self, node):
        self.visit(node)
   
    def get_name(self):
        return TVar('$' + next(self._names)) 
    
    def get_name_TCon(self):
        return TCon('$' + next(self._names)) 
    
    def visit(self, node, attrs = None):
        visit_name = f"visit_{type(node).__name__}" 
        if hasattr(self, visit_name):
            return getattr(self, visit_name)(node, attrs) 
        else:
            return self.visit_generic(node)

    def visit_Var(self, node, dtype = None):
        if (dtype is not None) and (node.id not in self._cache):
            self._cache[node.id] = dtype
        
        node.dtype = self._cache[node.id] 
        #print("** var **", node , "\n" , vars(node))
        return node.dtype
    
    def visit_Int(self, node, attrs = None):
        node.dtype = self.get_name() 
        self._num_load.append((node.dtype,int(node.n)))
        self._relation.append(("#=", node.dtype, int64))
        return node.dtype
    
    def visit_Float(self, node, attrs = None):
        node.dtype = self.get_name() 
        self._num_load.append((node.dtype,float(node.n)))
        self._relation.append(("#=", node.dtype, float32))
        return node.dtype
    
    def visit_List(self, node, attrs = None):
        return array(int32) 
    
    def visit_Tuple(self, node, attrs = None):
        return array(int32)
    
    def visit_Subscript(self, node, attrs = None):
        #print("** Subscript **", vars(node))
        new_mem = self.get_name()
        type_arr = self.visit(node.value) 
        type_attr = self.visit(node.nslice) 
        self._relation.append(("#=", type_arr, array(new_mem)))
        if isinstance(type_attr, list):
            self._relation.extend([("#=", t, int32) for t in type_attr])
        else:
            self._relation.append(("#=", type_attr, int32))
        return new_mem

    def visit_Index(self, node, attrs = None):
        #print("** index **",vars(node))
        return self.visit(node.index)
    
    def visit_Slice(self, node, attrs = None):
        type_attr = [] 
        type_attr.append(self.visit(node.lower))
        type_attr.append(self.visit(node.upper))
        type_attr.append(self.visit(node.step))

        return type_attr
    
    def visit_BinOp(self, node, attrs = None):
        #print("** BinOp **",node.right)
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        self._relation.append(("#=", type_left, type_right)) 

        return type_right
 
    def visit_Assign(self, node, attrs = None):
        #print("------ infer assign -------")
        #doesn't support subsequent assignment
        #Int/Float --> $ptr
        #node.value = Int/Float/Op
        dtype_value = self.visit(node.value)
        #print(dtype_value)
        targets = node.targets
        if targets.id in self._cache:
            # y = x , x = $ptr => y = $ptr
            self._relation.append(("#=", dtype_value, self._cache[targets.id])) 

        _ = self.visit(node.targets, dtype_value)
        #print("------ infer assign -------")
        return None

    def visit_args(self, args):
        type_args = [self.get_name() for _ in args] 

        i = 0
        for arg, type_arg in zip(args, type_args):
            type_args[i] = self.visit(arg, type_arg)
            i += 1
        
        return type_args

    def visit_Call(self, node, attrs = None):
        #node.func = name of func called 
        #will be touch later 
        type_args = self.visit_args(node.args) 
        return type_args

    def visit_For(self, node, attrs = None):
        for_id = self.visit(node.target, int64)
        range_bounded = self.visit(node.iter)
        
        self._relation.append(("#=",for_id,int64)) 
        self._relation.extend([("#=",b,int64) for b in range_bounded])
        
        _ = list(map(self.visit, node.body))
        return None
    
    #def visit_If(self, node, attrs = None):
        #print("-----if infer--------")
        #_ = self.visit(node.body) 
        #_ = self.visit(node.orelse)
        #print("-----if infer--------")
    
    #def visit_Compare(self, node, attrs = None):
        #left ops comparetors 
        # 0 <= i < n <=> 0 [<=, <] [i,n]
    #    left = [self.visit(node.left)]
    #    comparators = list(map(self.visit, node.comparators)) 
    #    left.extend(comparators)
    #    ops = node.ops 
    #    rel = [(ops[i],left[i],left[i+1]) for i in range(len(ops))] 
    #    for r in rel:
    #        self._relation.append(r)

    #    return None
    
    def visit_While(self, node, attrs = None):
        _ = self.visit(node.test)
        _ = list(map(self.visit, node.body))
        return None
    
    def visit_FunctionDef(self, node, attrs = None):
        type_args = self.visit_args(node.args)
        self._type_ret = TVar("$ret")
        _ = list(map(self.visit, node.body)) 

        #print("** cache **",self._cache)
        #print("** relation **", self._equal_relation)
        return TFunc(type_args, self._type_ret)
    
    def visit_Return(self, node, attrs = None):
        type_ret = self.visit(node.value)
        self._relation.append(("#=",type_ret, self._type_ret))
        return type_ret

    def visit_generic(self,node):
        return NotImplementedError
    
if __name__ == "__main__":
    pass