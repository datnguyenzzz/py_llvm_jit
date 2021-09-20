import ast 

class For(ast.AST):
    def __init__(self, target, iter, body, orelse, type_comment=None):
        self._target = target
        self._iter = iter 
        self._body = body  
        self._orelse = orelse 
        self._type_comment = type_comment
        self._fields = ["target","iter","body","orelse","type_comment"]
    
    @property
    def target(self):
        return self._target 
    
    @target.setter 
    def target(self,n_target):
        self._target = n_target
    
    @property
    def iter(self):
        return self._iter 
    
    @iter.setter 
    def iter(self,n_iter):
        self._iter = n_iter
    
    @property
    def body(self):
        return self._body
    
    @body.setter 
    def body(self,n_body):
        self._body = n_body
    
    @property
    def orelse(self):
        return self._orelse 
    
    @orelse.setter 
    def orelse(self,n_orelse):
        self._orelse = n_orelse
    
    @property
    def type_comment(self):
        return self._type_comment 
    
    @type_comment.setter 
    def type_comment(self,n_type_comment):
        self._type_comment = n_type_comment
    
    @property
    def fields(self):
        return self._fields

class While(ast.AST):
    def __init__(self, test, body, orelse):
        self._test = test 
        self._body = body 
        self._orelse = orelse 
        self._fields = ["test", "body", "orelse"]

    @property
    def test(self):
        return self._test
    
    @test.setter 
    def test(self,n_test):
        self._test = n_test
    
    @property
    def body(self):
        return self._body 
    
    @body.setter 
    def body(self,n_body):
        self._body = n_body
    
    @property
    def orelse(self):
        return self._orelse
    
    @orelse.setter 
    def orelse(self,n_orelse):
        self._orelse = n_orelse
    
    @property
    def fields(self):
        return self._fields

class If(ast.AST):
    def __init__(self, test, body, orelse):
        self._test = test 
        self._body = body 
        self._orelse = orelse 
        self._fields = ["test", "body", "orelse"]

    @property
    def test(self):
        return self._test
    
    @test.setter 
    def test(self,n_test):
        self._test = n_test
    
    @property
    def body(self):
        return self._body 
    
    @body.setter 
    def body(self,n_body):
        self._body = n_body
    
    @property
    def orelse(self):
        return self._orelse
    
    @orelse.setter 
    def orelse(self,n_orelse):
        self._orelse = n_orelse
    
    @property
    def fields(self):
        return self._fields
    
        