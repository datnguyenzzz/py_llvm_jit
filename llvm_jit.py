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

AST = True
DEBUG = False
PARSE = True
INFER = False

def type_infer(ast):
    Tinfer = inference.TypeInference()
    ftype = Tinfer.visit(ast)
    mgu = unification.solve_system(Tinfer.relation)
    equal = "#="
    
    if INFER:
        print("relations = ",Tinfer.relation)
        print("cache = ", Tinfer.cache)
        print("num load = ", Tinfer.num_load)
        print("Func equation before inference: ", ftype)

    infer_ftype = unification.apply(mgu[equal], ftype) 
    
    if DEBUG:
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
    return (infer_ftype, mgu[equal])

def llvm_jit(source):
    def wrapper(*args): #args of source
        parsed = parser.Parser(source) 
        #print("---------------DEBUG------------")
        #print(ast_parsing.dump(parsed._ast))
        #print("---------------DEBUG------------")
        core = parsed.syntax_tree

        if AST:
            print("=============== AST =====================")
            print(ast_parsing.dump(core))

        #inference node to type
        iftype, mgu = type_infer(core)

        if PARSE:
            print("=============== PARSE =====================")
            print(ast_parsing.dump(core))
        
        if INFER:
            print("After unified: ", mgu) 
            print("Func equation after inference: ", iftype)

        return codegen.recompile(args,core, iftype, mgu)
    
    return wrapper

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

