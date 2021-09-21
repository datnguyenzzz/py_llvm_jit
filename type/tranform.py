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
        return body
    
    def visit_arg(self, node):
        #print("* arg *",node.arg)
        return Var(node.arg)
    
    def visit_arguments(self, node):
        #print("* args *",node.args)
        args = list(map(self.visit, node.args))
        return args

    def visit_Name(self, node):
        return Var(node.id)
    
    def visit_Tuple(self, node):
        #print("* Tuple *",node.elts)
        elts = list(map(self.visit, node.elts))
        return elts
    
    def visit_List(self, node):
        #print("* List *",node.elts)
        elts = list(map(self.visit, node.elts))
        return elts
    
    def visit_Num(self, node):
        n = node.n 
        if isinstance(n,float):
            return Float(n) 
        else:
            return Int(n) 
    
    def visit_Bool(self, node):
        return Bool(node.n)

    def visit_BoolOp(self, node):
        op = ops[node.op.__class__]
        values = list(map(self.visit, node.values)) 
        return BoolOp(op,values)
    
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right) 
        op = ops[node.op.__class__] 

        return BinOp(left, op, right)

    def visit_Assign(self, node):
        #targets , value
        #targets = name, tuple, list
        #print("* Assign *",node.value)
        targets = self.visit(node.targets[0]) 
        value = self.visit(node.value)
        return Assign(targets,value)

    def visit_Return(self, node):
        #print("* Return *",node.value)
        value = self.visit(node.value)
        return value

    def visit_FunctionDef(self, node):
        #name, args, body, decorators_list, returns
        #print("* funcdef *", node.returns)
        name = node.name
        args = self.visit(node.args)

        body = list(map(self.visit, node.body))
        
        #still doesn't support decorator 
        decorator_list = node.decorator_list 
        returns = node.returns

        func = FunctionDef(name, args, body, decorator_list, returns)
        return func
    
if __name__ == "__main__":
    def test_func(x,y):
        #a,b,c,d = 2,3,4,5
        #a = 10 and 3
        #b = 4 
        tmp = x * y
        return 10

    tranform = Tranformer()
    print(tranform(test_func))