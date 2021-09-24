import sys 
import os
import argparse 
import pprint

CURR = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(CURR+"/custom_types")

import llvmlite.binding as llvm
from llvmlite import ir

from Parser import parser
from custom_types import inference
from AST import ast_parsing
from utils import file_op
from optimizes import unification

def build_AST_tree(IN, OUT):
    source = file_op.read_from_file(IN)
    ast_tree = ast_parsing.dump(source)

    if OUT == None:
        print(ast_tree)
    else:
        file_op.write_to_file(OUT, ast_tree)

def parsing(IN):
    source = file_op.read_from_file(IN) 
    parsed = parser.Parser(source) 
    core = parsed.syntax_tree

    #inference node to type
    Tinfer = inference.TypeInference()
    Tinfer(core)

    #Testing Tinfer attributes
    print(ast_parsing.dump(core))
    print("******************************************")
    print("relations = ",Tinfer.relation)
    print("cache = ", Tinfer.cache)
    print("num load = ", Tinfer.num_load)
    print("******************************************")
    #Unify relation
    print(unification.solve_system(Tinfer.relation))

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser() 
    arg_parser.add_argument("--AST",required=False) 
    arg_parser.add_argument("--parse", required=False)
    arg_parser.add_argument("--input", required=True)
    arg_parser.add_argument("--output",required=False)
    args = arg_parser.parse_args()

    if args.AST == "True":
        FILENAME_IN = args.input
        FILENAME_OUT = args.output
        build_AST_tree(FILENAME_IN, FILENAME_OUT)
    
    if args.parse == "True":
        FILENAME_IN = args.input 
        parsing(args.input)

