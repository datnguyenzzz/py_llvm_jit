def f(x):
    if x == 1:
        return x
    tmp = f(x-1) * x
    return tmp