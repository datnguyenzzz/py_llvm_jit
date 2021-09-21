import ast 

class Subscript(ast.AST):
    def __init__(self, ctx, value, nslice=None):
        self._ctx = ctx 
        self._value = value 
        self._nslice = nslice
        self._fields = ["ctx", "value", "slice"]
    
    @property
    def ctx(self):
        return self._ctx
    
    @ctx.setter 
    def ctx(self,n_ctx):
        self._ctx = n_ctx
    
    @property
    def value(self):
        return self._value
    
    @value.setter 
    def value(self,n_value):
        self._value = n_value
    
    @property
    def nslice(self):
        return self._nslice
    
    @nslice.setter 
    def nslice(self,n_nslice):
        self._nslice = n_nslice
    
    @property
    def fields(self):
        return self._fields

class Slice(ast.AST):
    def __init__(self, lower, upper, step):
        self._lower = lower 
        self._upper = upper 
        self._step = step
        self._fields = ["lower", "upper", "step"]
    
    @property
    def lower(self):
        return self._lower
    
    @lower.setter 
    def lower(self,n_lower):
        self._lower = n_lower
    
    @property
    def upper(self):
        return self._upper
    
    @upper.setter 
    def upper(self,n_upper):
        self._upper = n_upper
    
    @property
    def step(self):
        return self._step
    
    @step.setter 
    def step(self,n_step):
        self._step = n_step
    
    @property
    def fields(self):
        return self._fields