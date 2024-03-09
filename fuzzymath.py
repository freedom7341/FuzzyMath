import random
import re
import math

fuzzy_get_sigfigs = lambda x : len((re.match( r'[1-9](\d*[1-9])?', str(x).replace('.', ''))).group())
fuzzy_get_bigfig = lambda x, y : x if (fuzzy_get_sigfigs(x) > fuzzy_get_sigfigs(y)) else y
fuzzy_fuzz_num = lambda precision, sigfig : precision * (math.sqrt(sigfig) / 10)
sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

def fuzzy_mult_loop(x, y, endType, precision=1):
    a = int(x*(10**(fuzzy_get_sigfigs(x))))
    b = int(y*(10**(fuzzy_get_sigfigs(y))))
    c = 0
    i = 0
    
    
    while b != 0:
        a = a << 1
        if (b % 2):
            c += a
            c = c*(1+(sign(endType*((-1)**endType))*fuzzy_fuzz_num(precision, fuzzy_get_sigfigs(a))))
        b = b >> 1
        i += 1
    
    return c / (2*10**(fuzzy_get_sigfigs(x))*10**(fuzzy_get_sigfigs(y)))

def fuzzyarithmetic(operation, precision=1):
    match operation:
        case 0: # Multiplication
            return lambda x, y : random.triangular(fuzzy_mult_loop(x, y, 1, precision), fuzzy_mult_loop(x, y, 2, precision), fuzzy_mult_loop(x, y, 0, precision))
        case 1: # Division
            return lambda x, y : x / y
        case 2: # Addition
            return lambda x, y : random.triangular((x + y) * (1 - fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y))), (x + y) * (1 + fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y))), x + y)
        case 3: # Subtraction
            return lambda x, y : random.triangular((x - y) * (1 - fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y))), (x - y) * (1 + fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y))), x - y)
    
    # triangular distribution?
    
adding=fuzzyarithmetic(0, 0)
print(adding(24.5,6.3))