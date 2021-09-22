#python Variables 
import ast 

context = {ast.Store : "#store", ast.Load : "#load", ast.Del : "#del"}

class Var(ast.AST):
    #ctx: Load/Store/Del/Starred
    def __init__(self, id, dtype=None, ctx=None):
        self._id = id 
        self._ctx = ctx
        self._dtype = dtype
        self._fields = ["id", "ctx", "dtype"]
    
    @property
    def id(self):
        return self._id 
    
    @id.setter
    def id(self,n_id):
        self._id = n_id 

    @property
    def dtype(self):
        return self._dtype 
    
    @dtype.setter
    def dtype(self,n_dtype):
        self._dtype = n_dtype 

    @property
    def ctx(self):
        return self._ctx 
    
    @ctx.setter
    def ctx(self,n_ctx):
        self._ctx = n_ctx
    
    @property
    def fields(self):
        return self._fields