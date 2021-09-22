import ast 

class FunctionDef(ast.AST):
    def __init__(self,name, args, body, decorator_list, returns, type_comment = None):
        self._name = name
        self._args = args 
        self._body = body 
        self._decorator_list = decorator_list 
        self._returns = returns
        self._type_comment = type_comment
        self._fields = ["name","args", "body", "decorator_list", "returns", "type_comment"]
    @property
    def name(self):
        return self._name
    
    @name.setter 
    def name(self,n_name):
        self._name = n_name

    @property
    def args(self):
        return self._args 
    
    @args.setter 
    def args(self,n_args):
        self._args = n_args
    
    @property
    def body(self):
        return self._body
    
    @body.setter 
    def body(self,n_body):
        self._body = n_body 
    
    @property
    def decorator_list(self):
        return self._decorator_list 
    
    @decorator_list.setter 
    def decorator_list(self,n_decorator_list):
        self._decorator_list = n_decorator_list

    @property
    def returns(self):
        return self._returns
    
    @returns.setter 
    def returns(self,n_returns):
        self._returns = n_returns

    @property
    def type_comment(self):
        return self._type_comment
    
    @type_comment.setter 
    def decorator_list(self,n_type_comment):
        self._type_comment = n_type_comment
    
    @property
    def fields(self):
        return self._fields

class Lambda(ast.AST):
    def __init__(self, args, body):
        self._args = args 
        self._body = body 
        self._fields = ["args", "body"]
        
    @property
    def args(self):
        return self._args 
    
    @args.setter 
    def args(self,n_args):
        self._args = n_args
    
    @property
    def body(self):
        return self._body
    
    @body.setter 
    def body(self,n_body):
        self._body = n_body 
    
    @property
    def fields(self):
        return self._fields

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