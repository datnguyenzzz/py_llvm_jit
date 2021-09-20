import sys 
import os
import argparse 

import llvmlite.binding as llvm
from llvmlite import ir

from AST import ast_parsing
from utils import file_op

def build_AST_tree(IN, OUT):
    source = file_op.read_from_file(IN)
    ast_tree = ast_parsing.dump(source)

    if OUT == None:
        print(ast_tree)
    else:
        file_op.write_to_file(OUT, ast_tree)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser() 
    arg_parser.add_argument("--AST",required=False) 
    arg_parser.add_argument("--input", required=True)
    arg_parser.add_argument("--output",required=False)
    args = arg_parser.parse_args()

    if args.AST == "True":
        FILENAME_IN = args.input
        FILENAME_OUT = args.output
        build_AST_tree(FILENAME_IN, FILENAME_OUT)
      

