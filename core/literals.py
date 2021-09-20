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
        self._n = new_n
    
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
        self._n = new_n
    
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
        self._n = new_n
    
    @property
    def fields(self):
        return self._fields

class List(ast.AST):
    def __init__(self, elts, ctx):
        self._elts = elts 
        self._ctx = ctx 
        self._fields = ["elts", "ctx"] 
    
    @property 
    def elts(self):
        return self._elts

    @elts.setter 
    def elts(self,new_elts):
        self._elts = new_elts 
    
    @property 
    def ctx(self):
        return self._ctx

    @ctx.setter 
    def ctx(self,new_ctx):
        self._ctx = new_ctx
    
    @property
    def fields(self):
        return self._fields

class Tuple(ast.AST):
    def __init__(self, elts, ctx):
        self._elts = elts 
        self._ctx = ctx 
        self._fields = ["elts", "ctx"] 
    
    @property 
    def elts(self):
        return self._elts

    @elts.setter 
    def elts(self,new_elts):
        self._elts = new_elts 
    
    @property 
    def ctx(self):
        return self._ctx

    @ctx.setter 
    def ctx(self,new_ctx):
        self._ctx = new_ctx
    
    @property
    def fields(self):
        return self._fields

class Set(ast.AST):
    def __init__(self, elts):
        self._elts = elts 
        self._fields = ["elts"] 
    
    @property 
    def elts(self):
        return self._elts

    @elts.setter 
    def elts(self,new_elts):
        self._elts = new_elts 
    
    @property
    def fields(self):
        return self._fields

class Dict(ast.AST):
    def __init__(self, keys, values):
        self._keys = keys 
        self._values = values
        self._fields = ["keys", "values"] 
    
    @property 
    def keys(self):
        return self._keys

    @keys.setter 
    def keys(self,new_keys):
        self._keys = new_keys 
    
    @property 
    def values(self):
        return self._values

    @values.setter 
    def values(self,new_values):
        self._values = new_values
    
    @property
    def fields(self):
        return self._fields