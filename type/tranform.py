#tranform ast tree to defined core language
#parsing a function/module to class

import sys 
import inspect
import types
from textwrap import * 
sys.path.append("../")

import ast
#--Core language
from core.node_visitor import * 
from core.control_fow import *
from core.expressions import *
from core.functions_classes import * 
from core.literals import * 
from core.statements import * 
from core.subscripting import * 
from core.variables import *

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
        return self.visit(self._ast)
    
    def visit_Module(self,node):
        body = list(map(self.visit, list(node.body)))
        return body[0]
    
    def visit_arg(self, node):
        #print("* arg *",node.arg)
        return Var(node.arg)
    
    def visit_arguments(self, node):
        #print("* args *",node.args)
        args = list(map(self.visit, list(node.args)))
        return args

    def visit_FunctionDef(self, node):
        #name, args, body, decorators_list, returns
        print("* funcdef *", ast.dump(node.args))
        name = node.name
        args = self.visit(node.args)
        
        #body = list(map(self.visit, list(node.body))) 
        
    
if __name__ == "__main__":
    def test_func(x,y):
        return x * y

    tranform = Tranformer()
    print(tranform(test_func))