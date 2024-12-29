import tcg
import sys
import os
import itertools as it
from subprocess import Popen,PIPE,STDOUT
import math
import random
random.seed(313)

# misc utilities
def toarr(s):return[int(x) for x in s.split(' ')]

# random utilities
rand=random.randint # random integer
def randf(a,b):return random.random()*(b-a)+a # random float
def randa(n,a,b):return[rand(a,b) for _ in range(n)] # random array

# math utilities
gcd=math.gcd
def lcm(a,b):return a*b/gcd(a,b)
def isprime(x):
    i=2
    while i*i<x:
        if x%i==0:return False
        i+=1
    return True

# writing utilities
buf=""
def write(x,newl='\n'):
    global buf
    buf+=str(x)+newl # write x to the buffer
def writea(*arrs): # write arrays to the buffer
    for arr in arrs:
        write(' '.join(str(x) for x in arr))
    
# reading utilities
lines=[]
cur_line=0
def read():
    global cur_line
    cur_line+=1
    return lines[cur_line-1].strip()
def reada():
    return toarr(read())

def to_lines(data):
    global lines,cur_line
    lines=data.strip().splitlines()
    cur_line=0

def read_file(fname):
    to_lines(open(fname).read())

# output utils
def run(prog,inp):
    file=f'./build/{prog}'
    p=Popen([file],stdout=PIPE,stdin=PIPE,stderr=STDOUT)
    stdout=p.communicate(input=inp.encode())[0]
    return stdout.decode()

def process_tc(tcs,tcout):
    global buf
    buf=""
    write(len(tcs))
    for tc in tcs:
        tcout(*tc)
    tc_data,buf=buf,""
    return tc_data

def process_ans(failing_ans,ansout):
    global buf
    buf=""
    for ans in failing_ans:
        ansout(*ans)
    ans_data,buf=buf,""
    return ans_data

# PARAMS
# TODO: make this customizable in the command line options
TC=100

def cli():
    # TODO: make this like actual proper command line interface stuff idk
    pname=sys.argv[1]
    verify=False
    if len(sys.argv)>=3:
        verify=sys.argv[2]=='v'

    print(f"Testing {pname}")
    test_file=f'{pname}-test.py'
    lcls=locals()
    exec(open(test_file).read(),globals(),lcls)

    # mandatory fcns
    gen=lcls['gen']
    solve=lcls['solve']
    tcout=lcls['tcout']
    ansin=lcls['ansin']
    ansout=lcls['ansout']
    if verify:tcin=lcls['tcin']

    # process
    # STEP 0 (optional)
    if verify:
        # use pname.in and pname.out files to see if our brute force solution is correct
        # read the data
        read_file(f'{pname}.in')
        t=int(read())
        tcs=[tcin() for _ in range(t)]
        sol=[solve(*tc) for tc in tcs]
        # read answers
        read_file(f'{pname}.out')
        ans=[ansin() for _ in range(t)]

        # compare
        fails=[]
        for i in range(t):
            if sol[i]!=ans[i]:fails.append(i)
        if len(fails)==0:
            print('Verification passed!')
        else:
            f=','.join(str(x+1) for x in fails)
            print(f"Verification failed testcases: {f}")
            return

    # 1. generate a bunch of test cases
    tcs=[gen() for _ in range(TC)]

    # 2. process those test cases
    tc_data=process_tc(tcs,tcout)

    # 3. solve those test cases by brute force
    sol=[solve(*tc) for tc in tcs]

    # 4. run the script on those test cases
    # TODO: add recompilation step
    out=run(pname,tc_data)
    to_lines(out)

    # 6. compare the answers
    # TODO: add support for custom answer verification (e.g. for constructive problems)
    failing_tcs=[]
    failing_ans=[]
    for tc in range(TC):
        ans=sol[tc]
        guess=ansin()
        if ans==guess:continue
        failing_tcs.append(tcs[tc])
        failing_ans.append(sol[tc])
    
    if len(failing_tcs)==0:
        print("All tests passed!")
    else:
        print(f"Tests failed: {len(failing_tcs)}")

        # 7. output the failing testcases
        tc_file=f'{pname}.Fin'
        ans_file=f'{pname}.Fout'

        with open(tc_file,'w') as file:
            file.write(process_tc(failing_tcs,tcout))
        
        with open(ans_file,'w') as file:
            file.write(process_ans(failing_ans,ansout))