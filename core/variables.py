#python Variables 
import ast 

class Var(ast.AST):
    #ctx: Load/Store/Del
    def __init__(self, id, ctx=None):
        self._id = id 
        self._ctx = ctx
        self._fields = ["id", "ctx"]