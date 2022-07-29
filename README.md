## **An implementation of Python similar to PyPy, CPython,.... A library helps translate Python code to low-level language and compile it with LLVM JIT Compiler.**

## **Stack:**

- llvmlite is a lightweight binding package to the LLVM APIs, it depends on LLVM.

- LLVM is the JIT compiler framework for producing executable code from various inputs.

- Numpy 

## **Usage:**

```
from llvm_jit import py_llvm_jit

@py_llvm_jit(PARSE=True, LLFUNC=True)
def addup(a,b):
    step = 1
    c = 0
    for i in range(a,b,step):
        if i%2==1:
            c = c + 1
        else:
            c = c - 1 
    return c
    
print(addup(1,1000000000))
```

## **Arguments:**

```
- PARSE = True/False : Print parse tree into console

- LLFUNC = True/False : Print LLVM intermediate representation into console

```

## **Results:**

```
Time consumption without py_llvm_jit: 1.323523412332s
Result: 1

Time comsumption with py_llvm_jit: 0.000000012s
Result: 1
```
