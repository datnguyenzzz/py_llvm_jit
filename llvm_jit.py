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

def type_infer(ast):
    Tinfer = inference.TypeInference()
    ftype = Tinfer.visit(ast)
    mgu = unification.solve_system(Tinfer.relation)
    equal = "#="
    infer_ftype = unification.apply(mgu[equal], ftype) 
    if INFER:
        print("relations = ",Tinfer.relation)
        print("cache = ", Tinfer.cache)
        print("num load = ", Tinfer.num_load)
        print("Func equation before inference: ", ftype)
    
    return (infer_ftype, mgu[equal])

def llvm_jit(source):
    parsed = parser.Parser(source) 
    core = parsed.syntax_tree

    if AST:
        print(ast_parsing.dump(core))

    #inference node to type
    iftype, mgu = type_infer(core)

    if PARSE:
        print(ast_parsing.dump(core))
    
    if INFER:
        print("After unified: ", mgu) 
        print("Func equation after inference: ", iftype)

    return codegen.recompile(core, iftype, mgu)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser() 
    arg_parser.add_argument("--AST",required=False) 
    arg_parser.add_argument("--parse", required=False)
    arg_parser.add_argument("--inference", required=False)
    arg_parser.add_argument("--debug",required=False)
    arg_parser.add_argument("--input", required=True)
    arg_parser.add_argument("--output",required=False)
    args = arg_parser.parse_args()

    AST = args.AST
    DEBUG = args.debug
    PARSE = args.parse 
    INFER = args.inference

    FILENAME_IN = args.input
    FILENAME_OUT = args.output
    if FILENAME_IN:
        source = file_op.read_from_file(FILENAME_IN) 
        llvm_jit(source)

