#Python literals. Missing List, Tuple, Dict 
import ast 

class Int(ast.AST):
    def __init__(self, n, typ=None):
        self._n = n 
        self._type = typ
        self._fields = ["n"]

    @property 
    def n(self):
        return self._n

    @n.setter 
    def n(self,new_n):
        self_n = new_n
    
    @property
    def fields(self):
        return self._fields

class Float(ast.AST):
    def __init__(self, n, typ=None):
        self._n = n 
        self._type = typ 
        self._fields = ["n"]
    
    @property 
    def n(self):
        return self._n

    @n.setter 
    def n(self,new_n):
        self_n = new_n
    
    @property
    def fields(self):
        return self._fields

class Bool(ast.AST):
    def __init__(self, n):
        self._n = n 
        self._fields = ["n"]
    
    @property 
    def n(self):
        return self._n

    @n.setter 
    def n(self,new_n):
        self_n = new_n
    
    @property
    def fields(self):
        return self._fields