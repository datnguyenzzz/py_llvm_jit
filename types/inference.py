#inference type to Variable
#%ptr = alloca i32
#store i32 3, i32* %ptr
#%val = load i32* %ptr
#%join = phi i32 [ %plusOne, %left], [ -1, %right]
 
# So need to inference to own-defined type in LLVM [%..]
import sys
import string
sys.path.append("../")

from basics import *
from Parser.parser import *

def set_name():
    k = 0 
    while True:
        for a in string.ascii_lowercase:
            yield "".join([a,str(k)]) if k > 0 else a 
        
        k += 1

class TypeInference(object):
    def __init__(self,node):
        self._names = set_name() 
        self._equal_relation = []
        self._cache = {}
        self._syntax_tree = self.visit(node)
    
    @property 
    def syntax_tree(self):
        return self._syntax_tree 
    
    @syntax_tree.setter 
    def syntax_tree(self, n_tree):
        self._syntax_tree = n_tree
    
    def get_name(self):
        return TVar('$' + next(self._names)) 
    
    def visit(self, node, attrs = None):
        visit_name = f"visit_{type(node).__name__}" 
        if hasattr(self, visit_name):
            return getattr(self, visit_name)(node, attrs) 
        else:
            return self.visit_generic(node)

    def visit_Var(self, node, dtype = None):
        if dtype is not None:
            node.dtype = dtype 
            self._cache[node.id] = dtype
        else:
            if node.id in self._cache:
                node.dtype = self._cache[node.id] 
        print("* var *", vars(node))
        return node
    
    def visit_Int(self, node, attrs = None):
        node.dtype = self.get_name() 
        return node.dtype
    
    def visit_Float(self, node, attrs = None):
        node.dtype = self.get_name() 
        return node.dtype
 
    def visit_Assign(self, node, attrs = None):
        #Int/Float --> $ptr
        dtype_value = self.visit(node.value)
        
        targets = self.visit(node.targets) 
        if targets.id in self._cache:
            # y = x , x = $ptr => y = $ptr
            self._equal_relation.append((dtype_value, self._cache[targets.id])) 
        
        self._cache[targets.id] = dtype_value

        _ = self.visit(node.targets, dtype_value)
        return None
    
    def visit_FunctionDef(self, node, attrs = None):
        type_args = [self.get_name() for _ in node.args] 
        type_ret = TVar("$ret")

        for (arg, type_arg) in zip(node.args, type_args):
            _ = self.visit(arg, type_arg)
        
        _ = list(map(self.visit, node.body)) 

        return TFunc(type_args, type_ret)

    def visit_generic(self,node):
        return NotImplementedError
    
if __name__ == "__main__":
    def addup(n,a,b):
        x = 1
        for i in range(n):
            n += 1 + x
        return n

    parser_tree = Parser(addup) 
    node = parser_tree.syntax_tree 
    #inference node to type
    type_node = TypeInference(node)
    node = type_node.syntax_tree
    print(node)