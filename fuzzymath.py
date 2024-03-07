import random
import re
import math

fuzzy_get_sigfigs = lambda x : len((re.match( r'[1-9](\d*[1-9])?', str(x).replace('.', ''))).group())
fuzzy_get_bigfig = lambda x, y : x if (fuzzy_get_sigfigs(x) > fuzzy_get_sigfigs(y)) else y
fuzzy_fuzz_num = lambda precision, sigfig : precision * (math.sqrt(sigfig) / 10)
def fuzzy_mult_loop(x, y):
    a = x
    b = y
    c = 0
    i = 0
    
    for i in range(math.ceil(math.log(b, 2))):
        a = a << 1
        if (b % 2):
            c += a
        b = b >> 1
        i += 1
    
    return c / 2

def fuzzyarithmetic(operation, precision):
    match operation:
        case 0: # Multiplication
            return lambda x, y : x * y
            
        case 1: # Division
            return lambda x, y : x / y
        case 2: # Addition
            return lambda x, y : random.triangular((x + y) * (1 - fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y))), random.triangular((x + y) * (1 + fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y)))), x + y)
        case 3: # Subtraction
            return lambda x, y : random.triangular((x - y) * (1 - fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y))), random.triangular((x - y) * (1 + fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y)))), x - y)
    
    # triangular distribution?

print(fuzzy_mult_loop(60, 25))