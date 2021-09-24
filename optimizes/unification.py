#Solving equal realtion got by type inference 
#the optimal result called "most general unifier" 

#ONLY SUPPORT BINARY RELATIONS 
#IN LARGE SCALE, ALL RELATIONS WILL BE INVOLVED
# Unify( P(x1,y1) , P(x2,y2) ) => [x1/x2,y1/y2] 

from custom_types.basics import * 
from functools import reduce

def empty():
    return {}

def arguments(f):
    if isinstance(f, TCon):
        return set() 
    elif isinstance(f, TApp):
        return arguments(f.con) | arguments(f.dtype) 
    elif isinstance(f, TFunc):
        return reduce(set.union, map(arguments, f.args)) | arguments(f.ret)
    elif isinstance(f, TVar):
        return set([f])

def occurs_check(var, f):
    return var in arguments(f)

def bind(var, f):
    if var == f:
        #x = x ---> {}
        return empty() 
    elif occurs_check(var, f):
        #x = f(x) ---> infinite
        raise InfiniteType(var, f) 
    else:
        #a = x ---> a->b
        return dict([(var,f)])

def unify(f_1,f_2):
    if isinstance(f_1,TApp) and isinstance(f_2,TApp):
        pass 
    elif isinstance(f_1,TCon) and isinstance(f_2,TCon) and (f_1==f_2):
        return empty() 
    elif isinstance(f_1,TFunc) and isinstance(f_2,TFunc):
        pass
    elif isinstance(f_1, TVar): #occur check to avoid leading infinite term
        return bind(f_1.value, f_2) 
    elif isinstance(y, TVar): #occur check to avoid leading infinite term
        return bind(f_2.value, f_1) 
    else:
        raise InferenceError(f_1,f_2)

def solve(relations):
    mgu = {} 
    tmp = relations 

    while len(tmp) > 0:
        (x,y) = tmp.pop() 
        unification = unify(x,y)
        print(unification)

def solve_system(relations):
    equations = {} 
    for f,x,y in relations:
        # f - type expression 
        # x,y - TVar
        if f not in equations:
            equations[f] = [] 
        equations[f].append((x,y)) 
    
    for f in list(equations):
        _ = solve(equations[f])

if __name__ == "__main__":
    pass
