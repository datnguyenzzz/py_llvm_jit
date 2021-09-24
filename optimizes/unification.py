#Solving equal realtion got by type inference 
#the optimal result called "most general unifier" 

#ONLY SUPPORT BINARY RELATIONS 
#IN LARGE SCALE, ALL RELATIONS WILL BE INVOLVED

#Step. 1: If Ψ1 or Ψ2 is a variable or constant, then:
#	a) If Ψ1 or Ψ2 are identical, then return NIL. 
#	b) Else if Ψ1is a variable, 
#		a. then if Ψ1 occurs in Ψ2, then return FAILURE
#		b. Else return { (Ψ2/ Ψ1)}.
#	c) Else if Ψ2 is a variable, 
#		a. If Ψ2 occurs in Ψ1 then return FAILURE,
#		b. Else return {( Ψ1/ Ψ2)}. 
#	d) Else return FAILURE. 
#Step.2: If the initial Predicate symbol in Ψ1 and Ψ2 are not same, then return FAILURE.
#Step. 3: IF Ψ1 and Ψ2 have a different number of arguments, then return FAILURE.
#Step. 4: Set Substitution set(SUBST) to NIL. 
#Step. 5: For i=1 to the number of elements in Ψ1. 
#	a) Call Unify function with the ith element of Ψ1 and ith element of Ψ2, and put the result into S.
#	b) If S = failure then returns Failure
#	c) If S ≠ NIL then do,
#		a. Apply S to the remainder of both L1 and L2.
#		b. SUBST= APPEND(S, SUBST). 
#Step.6: Return SUBST. 


from custom_types.basics import * 
from functools import reduce

#TCon = type 
#TVar = variable 
#TFunc = f(g1(),g2(),...) => gk()
#TApp = f(..)

def empty():
    return {}

def occurs_check(var, f):
    def lookup(f):
        if isinstance(f, TCon):
            return set() 
        elif isinstance(f, TApp):
            #fn(...)(args)
            return lookup(f.fn) | lookup(f.args) 
        elif isinstance(f, TFunc):
            #f(g1(),g2(),...) => ret()
            return reduce(set.union, map(lookup, f.args)) | lookup(f.ret)
        elif isinstance(f, TVar):
            return set([f])

    return var in lookup(f)

def bind(var, f):
    if var == f:
        return empty() 
    elif occurs_check(var, f):
        raise InfiniteType(var, f) 
    else:
        return dict([(var,f)])

def unify(f_1,f_2):
    if isinstance(f_1,TApp) and isinstance(f_2,TApp):
        pass 
    elif isinstance(f_1,TCon) and isinstance(f_2,TCon) and (f_1==f_2):
        return empty() 
    elif isinstance(f_1,TFunc) and isinstance(f_2,TFunc):
        pass
    elif isinstance(f_1, TVar):
        return bind(f_1.value, f_2) 
    elif isinstance(f_2, TVar): 
        return bind(f_2.value, f_1) 
    else:
        raise InferenceError(f_1,f_2)

def apply(cp, x):
    if isinstance(x, TCon):
        return x 
    elif isinstance(x, TApp):
        #cp ( fn(...)(args) )
        # = cp(fn(...)) (cp(args))
        return TApp(apply(cp, x.fn), apply(cp, x.args))
    elif isinstance(x, TFunc):
        # cp ( f(g1(),g2(),...) => ret() )
        # f(cp(g1()), cp(g2()), ...) => cp(ret())
        args = [apply(cp,a) for a in x.args]
        ret = apply(cp, x.ret)
        return TFunc(args, ret)
    elif isinstance(x, TVar):
        #cp(x) => y <-> CP[x/y]
        return cp.get(x.value, x)

def applyList(s, xs):
    return [(apply(s,x) , apply(s,y)) for x,y in xs]

def merge(cp, substitution):
    # S1[x1/y1] + S2[x2/y2] => [x/y : x2/cp(S1(y2))]  
    tmp = dict((x, apply(cp,y)) for x,y in substitution.items()) 
    _tmp = cp.copy() 
    _tmp.update(tmp) 
    return _tmp

def solve(relations):
    mgu = {} 
    tmp = relations 
    while len(tmp) > 0:
        (x,y) = tmp.pop() 
        cp = unify(x,y)
        tmp = applyList(cp, tmp)
        mgu = merge(cp, mgu)

    print(mgu)

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
