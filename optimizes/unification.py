#Solving equal realtion got by type inference 
#the optimal result called "most general unifier" 

#ONLY SUPPORT BINARY RELATIONS 
#IN LARGE SCALE, ALL RELATIONS WILL BE INVOLVED
# Unify( P(x1,y1) , P(x2,y2) ) => [...,...]

def solve(relations):
    print(relations)

def solve_system(relations):
    equations = {} 
    for f,x,y in relations:
        if f not in equations:
            equations[f] = [] 
        
        equations[f].append((x,y)) 
    
    for f in list(equations):
        _ = solve(equations[f])

if __name__ == "__main__":
    relations = [('#=', "$d", "$g"), ('#<=', "$f", "$c"), ('#<', "$c", "$g"), ('#=', "$e", "$c"), 
                 ('#=', "$c", '$e'), ('#=', '$c', '$h'), ('#=', '$h', '$c'), ('#=', '$e', '$ret')] 
    
    print(solve_system(relations))
