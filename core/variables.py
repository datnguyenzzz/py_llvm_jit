#python Variables 
import ast 

class Var(ast.AST):
    #ctx: Load/Store/Del/Starred
    def __init__(self, id, ctx=None):
        self._id = id 
        self._ctx = ctx
        self._fields = ["id", "ctx"]
    
    @property
    def id(self):
        return self._id 
    
    @id.setter
    def id(self,n_id):
        self._id = n_id 

    @property
    def ctx(self):
        return self._ctx 
    
    @ctx.setter
    def ctx(self,n_ctx):
        self._ctx = n_ctx
    
    @property
    def fields(self):
        return self._fields