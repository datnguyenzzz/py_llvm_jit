import sys 
import os

import llvmlite.binding as llvm
from llvmlite import ir

from AST import ast_parsing
from utils import file_op

if __name__ == "__main__":
    if len(sys.argv) < 1:
        raise TypeError("Missing file !!") 
    
    FILENAME_IN = sys.argv[1] 


    FILENAME_OUT = ""
    if len(sys.argv) > 2:
        FILENAME_OUT = sys.argv[2]

    source = file_op.read_from_file(FILENAME_IN)
    
    ast_tree = ast_parsing.dump(source)

    if FILENAME_OUT == "":
        print(ast_tree)
    else:
        file_op.write_to_file(FILENAME_OUT, ast_tree)
    

