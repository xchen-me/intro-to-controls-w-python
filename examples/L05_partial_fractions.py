# Author: Xu Chen, University of Washington
# Lecture 5, Inverse Laplace transform: partial fraction expansions
import sympy
s = sympy.symbols('s')
G = 32/s/(s+4)/(s+8)
print(sympy.apart(G))        # 1/(s + 8) - 2/(s + 4) + 1/s

G = 2/(s+1)/(s+2)**2
print(sympy.apart(G))        # -2/(s + 2) - 2/(s + 2)**2 + 2/(s + 1)
