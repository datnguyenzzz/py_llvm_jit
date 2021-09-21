#tranform ast tree to defined core language
#parsing a function/module to class

import sys 
import inspect
import types
from textwrap import * 
sys.path.append("../")

import ast
from core.node_visitor import Visitor 

class Tranformer(Visitor):
    
    #ast.NodeVisitor.visit(node) --> self.visit_classname() 

    def __call__(self, source):
        if isinstance(source, types.ModuleType) or \
           isinstance(source, types.FunctionType) or \
           isinstance(source, types.LambdaType):
            source = dedent(inspect.getsource(source))
        elif isinstance(source, str):
            source = dedent(source) 
        else:
            raise NotImplementedError 

        self._source = source 
        self._ast = ast.parse(source)
        print(ast.dump(self._ast))
        return self.visit(self._ast)

if __name__ == "__main__":
    def test_func(x):
        return x * 2

    tranform = Tranformer()
    print(tranform(test_func))