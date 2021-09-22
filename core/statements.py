import ast 

class Assign(ast.AST):
    def __init__(self, targets, value, type_comment=None):
        self._targets = targets 
        self._value = value 
        self._type_comment = type_comment 
        self._fields = ["targets","value","dtype","type_comment"]
    
    @property 
    def targets(self):
        return self._targets
    
    @targets.setter
    def targets(self,n_targets):
        self._targets = n_targets
    
    @property 
    def value(self):
        return self._value 
    
    @value.setter 
    def value(self,n_value):
        self._value = n_value
    
    @property 
    def type_comment(self):
        return self._type_comment
    
    @type_comment.setter 
    def type_comment(self,n_type_comment):
        self._type_comment = n_type_comment
    
    @property 
    def fields(self):
        return self._fields