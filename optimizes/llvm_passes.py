# documentation 
# https://llvm.org/devmtg/2014-04/PDFs/Talks/Passes.pdf

from llvmlite import ir 
import llvmlite.binding as llvm
#Initialize the LLVM core.
llvm.initialize()
#Initialize all targets
llvm.initialize_native_target()
#Initialize all code generators.
llvm.initialize_native_asmprinter()

def tuning(module):
    #create module 

    mod = llvm.parse_assembly(str(module)) 
    mod.verify() 
    
    pass_manager = llvm.PassManagerBuilder() 

    # optimization level 
    # 0 - no optimization 
    # 2 - enalbe most of optimization 
    # 3 - enables optimizations that take longer to perform
    # attempt to make programm run faster 
    pass_manager.opt_level = 3 

    # vectorizing loop 
    pass_manager.loop_vectorize = True 

    pass_module = llvm.ModulePassManager() 

    #optional optimization
    pass_module.add_constant_merge_pass()
    pass_module.add_dead_code_elimination_pass()
    pass_module.add_global_dce_pass()
    pass_module.add_global_optimizer_pass()
    pass_module.add_cfg_simplification_pass()
    pass_module.add_licm_pass()
    pass_manager.populate(pass_module)

    pass_module.run(mod)
    
    return mod
