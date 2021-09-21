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

class Parser(Visitor):

    #ast.NodeVisitor.visit(node) --> self.visit_classname() 

    def __init__(self, source):
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
        self._syntax_tree = self.visit(self._ast)
    
    @property 
    def syntax_tree(self):
        return self._syntax_tree 
    
    @syntax_tree.setter 
    def syntax_tree(self, n_tree):
        self._syntax_tree = n_tree
    
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
        ctx = context[node.ctx.__class__]
        return Var(node.id, ctx)
    
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
    
    def visit_AugAssign(self, node):      
        op = ops[node.op.__class__]
        target = self.visit(node.target) 
        value = self.visit(node.value)

        if isinstance(node.op,ast.Add) or isinstance(node.op,ast.Sub) or \
           isinstance(node.op,ast.Mult) or isinstance(node.op,ast.Div) or \
           isinstance(node.op,ast.LShift) or isinstance(node.op,ast.RShift) or \
           isinstance(node.op,ast.BitOr) or isinstance(node.op,ast.BitAnd) or \
           isinstance(node.op,ast.BitXor) or isinstance(node.op,ast.Pow) :
            return Assign(target, BinOp(target, op, value))
        else:
            raise TypeError("Doesn't support and=")

    def visit_For(self, node):
        #target, iter, body, orelse
        print(ast.dump(node)) 
        target = self.visit(node.target) 
        iters = self.visit(node.iter)
        body = list(map(self.visit, node.body)) 
        orelse = node.orelse
        return For(target,iters,body,orelse)

    def visit_While(self, node):
        #test, body, orelse
        test = self.visit(node.test)
        body = list(map(self.visit, node.body)) 
        orelse = node.orelse 
        return While(test, body, orelse)

    def visit_Call(self, node):
        func = self.visit(node.func)
        args = list(map(self.visit, node.args)) 
        keywords = node.keywords
        return Call(func,args,keywords)
    
    def visit_Compare(self, node):
        left = self.visit(node.left)
        op = [ops[o.__class__] for o in node.ops]
        comparators = list(map(self.visit, node.comparators)) 
        return Compare(left, op, comparators)
    
if __name__ == "__main__":
    def test_func(x,y):
        i,t = 0,0 
        while i < 10:
            t += i 
            i += 1 
        
        return t

    parser = Parser(test_func)
    print(parser.syntax_tree)