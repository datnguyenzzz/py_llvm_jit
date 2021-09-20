import ast 

class UnaryOp(ast.AST):
    def __init__(self, op, operand):
        self._op = op 
        self._operand = operand
        self._fields = ["op", "operand"]
    
    @property
    def op(self):
        return self._op 
    
    @op.setter 
    def op(self,n_op):
        self._op = n_op
    
    @property
    def operand(self):
        return self._operand
    
    @operand.setter 
    def operand(self,n_operand):
        self._operand = n_operand
    
    @property
    def fields(self):
        return self._fields

class UnaryOp(ast.AST):
    def __init__(self, op, values):
        self._op = op 
        self._values = values
        self._fields = ["op", "values"]
    
    @property
    def op(self):
        return self._op 
    
    @op.setter 
    def op(self,n_op):
        self._op = n_op
    
    @property
    def values(self):
        return self._values
    
    @values.setter 
    def values(self,n_values):
        self._values = n_values
    
    @property
    def fields(self):
        return self._fields

class BinOp(ast.AST):
    def __init__(self, left, op, right):
        self._left = left 
        self._op = op 
        self._right = right 
        self._fields = ["left", "op", "right"]
    
    @property
    def left(self):
        return self._left
    
    @left.setter 
    def left(self,n_left):
        self._left = n_left
    
    @property
    def op(self):
        return self._op 
    
    @op.setter 
    def op(self,n_op):
        self._op = n_op
    
    @property
    def right(self):
        return self._right
    
    @op.setter 
    def right(self,n_right):
        self._right = n_right
    
    @property
    def fields(self):
        return self._fields
