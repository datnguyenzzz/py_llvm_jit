#Extract tree from AST module 

import ast 
import pprint

def _parse(node):
    if isinstance(node, ast.AST):
        field = ((name, _parse(value)) for name,value in ast.iter_fields(node))

        return (node.__class__.__name__, dict(field))
    elif isinstance(node, list):
        return [_parse(child) for child in node]
    elif isinstance(node, str):
        return repr(node) 
    return node

def ast_tree(node):
    if not isinstance(node, ast.AST):
        raise TypeError(f'Expected AST node = {node.__class__.__name__}')
    
    return _parse(node)

def format_ast(node, **kws):
    return pprint.pformat(ast_tree(node,), **kws)

def dump(node):
    return format_ast(node)

if __name__ == "__main__":
    source = """a = 2 + 4"""
    #source = """def f(x):
    #                return x"""

    node = ast.parse(source)
    print(ast.dump(node))
    print(dump(node))