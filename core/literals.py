#Python literals. Missing List, Tuple, Dict 
import ast 

class Int(ast.AST):
    def __init__(self, n, typ=None):
        self._n = n 
        self._type = typ
        self._fields = ["n"] 

class Float(ast.AST):
    def __init__(self, n, typ=None):
        self._n = n 
        self._type = typ 
        self._fields = ["n"]

class Bool(ast.AST):
    def __init__(self, n):
        self._n = n 
        self._fields = ["n"]