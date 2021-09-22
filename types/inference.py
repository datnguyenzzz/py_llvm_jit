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
        self._syntax_tree = self.visit(node)
    
    @property 
    def syntax_tree(self):
        return self._syntax_tree 
    
    @syntax_tree.setter 
    def syntax_tree(self, n_tree):
        self._syntax_tree = n_tree
    
    def get_name(self):
        return TVar('$' + next(self._names)) 
    
    def visit(self, node):
        visit_name = f"visit_{type(node).__name__}" 
        if hasattr(self, visit_name):
            return getattr(self, visit_name)(node) 
        else:
            return self.visit_generic(node)
    
    def visit_FunctionDef(self, node):
        print(node.args)

    def visit_generic(self,node):
        return NotImplementedError
    
if __name__ == "__main__":
    def addup(n):
        x = 1
        for i in range(n):
            n += 1 + x
        return n

    parser_tree = Parser(addup) 
    node = parser_tree.syntax_tree 
    print(vars(node))
    #inference node to type
    type_node = TypeInference(node)
    node = type_node.syntax_tree
    print(node)