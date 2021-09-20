import ast 

class Return(ast.AST):
    def __init__(self,value):
        self._value = value 
        self._fields = ["value"]
    
    @property
    def value(self):
        return self._value 
    
    @value.setter 
    def value(self,n_value):
        self._value = n_value
    
    @property 
    def fields(self):
        return self._fields