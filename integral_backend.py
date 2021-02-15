import functools
import numpy as np
from math import *

# Legendre Polinomial (less recursion)
# Syntax tree

@functools.lru_cache(10)
def legendre_polinomial(n, x):
    ''' Recurrent formula for Legendre Polinomials '''
    if n == 0: 
        return 1 # P0 = 1
    elif n == 1: 
        return x # P1 = x 
    else: 
        return ((2 * n-1)* x * legendre_polinomial(n-1, x)-(n-1) * legendre_polinomial(n-2, x))/float(n)

def legendre_polinomial_derivative(n, x):
    ''' Formula for Legendre Polinomials derivative'''
    return n / (1 - x * x) * (legendre_polinomial(n-1, x) - x * legendre_polinomial(n, x))

def legendre_polinomial_root(n, l, epsilon = 1e-12):
    ''' Find roots using Newton Method '''
    xn = l + epsilon
    xprev = 0
    
    while abs(xn - xprev) > epsilon:
        xprev = xn
        xn = xn - legendre_polinomial(n, xn) / legendre_polinomial_derivative(n, xn)

    return round(xn, 12)

def legendre_polinomial_all_roots(n):
    ''' Find all roots using Newton Method '''
    step = 1 / (2 * n)
    l, r = -1, 0
    tmp_r = l + step
    roots = []
    
    while l <= r:
        root = legendre_polinomial_root(n, l)
        if (root is not None) and (root not in roots):
            roots.append(root)
        l += step

    return roots

def quadrature_w_coeff(x, n):
    w = []
    
    for i in range(n // 2):
        wi = 2 / ( (1 - x[i] ** 2) * legendre_polinomial_derivative(n, x[i]) ** 2 )
        w.append(round(wi, 12))
    
    w_second_part = w[::-1]
    if n % 2:
        w.append(round(2 / ( legendre_polinomial_derivative(n, 0) ** 2 ), 12))
    w = w + w_second_part

    return np.array(w)

# Incomplete
def gaussian_quadrature(a, b, f, n = 25):
    ''' Numerical integration formula '''
    ## Temp Area ##
    def func(x):
        try:
            y = eval(f)
        except:
            y = 1e-12
        return y
    ## func in def params ##

    substitution_multiplier = (b - a) / 2
    func_subst = lambda x: func((b + a) / 2 + (b - a) / 2 * x)

    leg_roots = legendre_polinomial_all_roots(n)
    leg_roots_second_part = [-1 * elem for elem in leg_roots]
    leg_roots = sorted(list(set(leg_roots + leg_roots_second_part)))

    w = quadrature_w_coeff(leg_roots, n)
    f_data = func_subst(np.array(leg_roots))

    integral_q = np.dot(w, f_data)

    return round(integral_q * substitution_multiplier, 12)

def integrate_f(a, b, f_str):
    if 'x' not in f_str:
        return eval(f_str) * (b - a)
    return gaussian_quadrature(a, b, f_str)
