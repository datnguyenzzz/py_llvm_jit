#Solving equal realtion got by type inference 
#the optimal result called "most general unifier" 

#ONLY SUPPORT BINARY RELATIONS 
#IN LARGE SCALE, ALL RELATIONS WILL BE INVOLVED
# Unify( P(x1,y1) , P(x2,y2) ) => [x1/x2,y1/y2] 

def solve(relations):
    pass

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
