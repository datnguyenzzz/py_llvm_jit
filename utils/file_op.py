import os 

def read_from_file(filename):
    if os.path.isfile(filename):
        f = open(filename,"r")
        content = f.readlines() 
        tmp = ''.join(content)
        f.close() 
        return tmp
    else:
        raise FileNotFoundError(f"wrong file {filename}")

def write_to_file(filename, content):
    f = open(filename,"w")  
    f.write(content) 
    f.close()