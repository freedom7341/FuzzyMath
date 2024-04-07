import random
import math

# 
fuzzy_get_sigfigs = lambda x : len(str(x).rstrip("0")) if len(str(x).split(".", 1)) == 1 else len(str(x).replace(".", "").lstrip("0"))
fuzzy_get_bigfig = lambda x, y : x if (fuzzy_get_sigfigs(x) > fuzzy_get_sigfigs(y)) else y
fuzzy_fuzz_num = lambda precision, sigfig : precision * (math.sqrt(sigfig) / 10)
sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

def fuzzy_mult_loop(x, y, endType, precision=1):
    a = int(x * (10 ** (fuzzy_get_sigfigs(x))))
    b = int(y * (10 ** (fuzzy_get_sigfigs(y))))
    c = 0
    i = 0
    
    
    while b != 0:
        a = a << 1
        if (b % 2):
            c += a
            c = c * (1 + (sign(endType * ((-1) ** endType)) * fuzzy_fuzz_num(precision, fuzzy_get_sigfigs(a))))
        b = b >> 1
        i += 1
    
    return c / (2 * 10 ** (fuzzy_get_sigfigs(x)) * 10 ** (fuzzy_get_sigfigs(y)))

def fuzzyarithmetic(operation, precision=1):
    match operation:
        case 0: # Multiplication
            return lambda x, y : list(random.triangular(fuzzy_mult_loop(float(i[1]), float(y if len(str(y).strip('[]').split(',')) == 1 else str(y).strip('[]').split(',')[i[0]]), 1, precision), fuzzy_mult_loop(float(i[1]), float(y if len(str(y).strip('[]').split(',')) == 1 else str(y).strip('[]').split(',')[i[0]]), 2, precision), fuzzy_mult_loop(float(i[1]), float(y if len(str(y).strip('[]').split(',')) == 1 else str(y).strip('[]').split(',')[i[0]]), 0, precision)) for i in list(enumerate(str(x).strip('[]').split(','))))
        case 1: # Division
            return lambda x, y : random.triangular(fuzzy_mult_loop(x, round(1 / y, fuzzy_get_sigfigs(y)), 1, precision), fuzzy_mult_loop(x, round(1 / y, fuzzy_get_sigfigs(y)), 2, precision), fuzzy_mult_loop(x, round(1 / y, fuzzy_get_sigfigs(y)), 0, precision))
        case 2: # Addition
            return lambda x, y : random.triangular((x + y) * (1 - fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y))), (x + y) * (1 + fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y))), x + y)
        case 3: # Subtraction
            return lambda x, y : random.triangular((x - y) * (1 - fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y))), (x - y) * (1 + fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y))), x - y)


def fuzzyrange(x, y, operation ,precision=1):
    match operation:
        case 0: # Multiplication
            return list([fuzzy_mult_loop(float(i[1]), float(y if len(str(y).strip('[]').split(',')) == 1 else str(y).strip('[]').split(',')[i[0]]), 1, precision),fuzzy_mult_loop(float(i[1]), float(y if len(str(y).strip('[]').split(',')) == 1 else str(y).strip('[]').split(',')[i[0]]), 0, precision), fuzzy_mult_loop(float(i[1]), float(y if len(str(y).strip('[]').split(',')) == 1 else str(y).strip('[]').split(',')[i[0]]), 2, precision)] for i in list(enumerate(str(x).strip('[]').split(','))))
        case 1: # Division
            return list([fuzzy_mult_loop(x, round(1 / float(y if len(str(y).strip('[]').split(',')) == 1 else str(y).strip('[]').split(',')[i[0]]), fuzzy_get_sigfigs(float(y if len(str(y).strip('[]').split(',')) == 1 else str(y).strip('[]').split(',')[i[0]]))), 1, precision), fuzzy_mult_loop(x, round(1 / float(y if len(str(y).strip('[]').split(',')) == 1 else str(y).strip('[]').split(',')[i[0]]), fuzzy_get_sigfigs(float(y if len(str(y).strip('[]').split(',')) == 1 else str(y).strip('[]').split(',')[i[0]]))), 0, precision),fuzzy_mult_loop(x, round(1 / float(y if len(str(y).strip('[]').split(',')) == 1 else str(y).strip('[]').split(',')[i[0]]), fuzzy_get_sigfigs(float(y if len(str(y).strip('[]').split(',')) == 1 else str(y).strip('[]').split(',')[i[0]]))), 2, precision)] for i in list(enumerate(str(x).strip('[]').split(','))))
        case 2: # Addition
            return ((x + y) * (1 - fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y))), x + y, (x + y) * (1 + fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y))))
        case 3: # Subtraction
            return (((x - y) * (1 - fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y))), x - y,(x - y) * (1 + fuzzy_fuzz_num(precision, fuzzy_get_bigfig(x, y)))))

#print(fuzzyrange(fuzzyrange(5,5,1),5,1))