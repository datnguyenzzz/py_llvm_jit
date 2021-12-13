from llvmlite import ir
import ctypes

class JitWrapper:
    def __init__(self, llfunc, engine):
        self._llfunc = llfunc 
        self._engine = engine 
        self.callable_func = None
    
    def jit_type(self, llvm_type):
        if isinstance(llvm_type, ir.IntType):
            runnable_type = getattr(ctypes, "c_int"+str(llvm_type.width))
        elif isinstance(llvm_type, ir.DoubleType):
            runnable_type = ctypes.c_double
        elif isinstance(llvm_type, ir.FloatType):
            runnable_type = ctypes.c_float
        elif isinstance(llvm_type, ir.VoidType):
            runnable_type = None 
        elif isinstance(llvm_type, ir.PointerType):
            #a[...]
            pointee = llvm_type.pointee
            if isinstance(pointee, ir.IntType):
                width = pointee.width
                if width == 8:
                    runnable_type = ctypes.c_char_p
                else:
                    runnable_type = ctypes.POINTER(wrap_type(pointee))
            elif isinstance(pointee, ir.VoidType):
                runnable_type = ctypes.c_void_p
            else:
                runnable_type = ctypes.POINTER(wrap_type(pointee))
        else:
            raise Exception(f"Unknow LLVM type {llvm_type}")
           
        return runnable_type
    
    def jit_module(self):
        self.callable_func = self.jit_func()
        runnable_func = self.dispatcher(self.callable_func)
        print(runnable_func)
        return runnable_func 
    
    def jit_func(self):
        llvm_args = self._llfunc.type.pointee.args
        llvm_ret = self._llfunc.type.pointee.return_type
        
        runnable_ret = self.jit_type(llvm_ret)
        runnable_args = list(map(self.jit_type, llvm_args))
        
        cfunctype = ctypes.CFUNCTYPE(runnable_ret, *runnable_args)
        func_address = self._engine.get_function_address(self._llfunc.name)
        
        runnable_func = cfunctype(func_address)
        runnable_func.__name__ = self._llfunc.name
        return runnable_func

    def dispatcher(self, fn):
        def call(*args):
            print("-----decor------")
            print(args)
            print(fn._argtypes_)
            print("-----decor------")
         
        call.__name__ = fn.__name__
        return call