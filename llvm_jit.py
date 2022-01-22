import sys 
import os
import argparse 
import pprint

CURR = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(CURR+"/custom_types")

from Parser import parser
from custom_types import inference
from custom_types.basics import *
from AST import ast_parsing
from utils import file_op
from optimizes import unification
from LLVMIRBuilder import Emitter
from compiler import codegen

AST = False
DEBUG = False
PARSE = False
INFER = False
LLFUNC = True

def type_infer(ast):
    Tinfer = inference.TypeInference()
    ftype = Tinfer.visit(ast)
    mgu = unification.solve_system(Tinfer.relation)
    equal = "#="
    
    if DEBUG:
        print("relations = ",Tinfer.relation)
        print("cache = ", Tinfer.cache)
        print("num load = ", Tinfer.num_load)
        print("Func equation before inference: ", ftype)

    infer_ftype = None
    if len(mgu) != 0:
        infer_ftype = unification.apply(mgu[equal], ftype) 
    
    if DEBUG and len(mgu)>0:
        print("mgu test")
        for x in mgu[equal].keys():
            print(type(x),type(mgu[equal][x]))
        print("after infer")
        for a in ftype.args:
            print(type(a))
        print(type(ftype.ret))

        print("before infer")
        for a in infer_ftype.args:
            print(type(a))
        print(type(infer_ftype.ret))
    
    equal_equations = mgu[equal] if len(mgu)>0 else {}
    
    return (infer_ftype, equal_equations, Tinfer.relation)

def py_llvm_jit(PARSE, LLFUNC):
    def llvm_jit(source):
        def wrapper(*args): #args of source
            parsed = parser.Parser(source) 
            core = parsed.syntax_tree

            if AST:
                print("=============== AST =====================")
                print(ast_parsing.dump(parsed._ast))
                
            if PARSE:
                print("=============== PARSE =====================")
                print(ast_parsing.dump(core))
                print("===========================================")

            #inference node to type
            iftype, mgu, bef_uni = type_infer(core)      
            
            if INFER:
                print("Func equation after inference: ", iftype)

            return codegen.recompile(args,core, iftype, mgu, LLFUNC)
        
        return wrapper
    return llvm_jit

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser() 
    arg_parser.add_argument("--AST",required=False) 
    arg_parser.add_argument("--parse", required=False)
    arg_parser.add_argument("--inference", required=False)
    arg_parser.add_argument("--debug",required=False)
    args = arg_parser.parse_args()

    AST = True
    DEBUG = args.debug
    PARSE = args.parse 
    INFER = args.inference

