def gen():
    # generate a testcase
    a=rand(1,10)
    b=rand(1,10)
    return a,b

def solve(a,b):
    return (a+b,)

def tcout(a,b):
    # output a testcase
    writea((a,b))

def ansin():
    # read an answer
    return (int(read()),)

def ansout(c):
    # output an answer
    write(c)

def tcin():
    # optional: read a testcase into the prior format
    return toarr(read())