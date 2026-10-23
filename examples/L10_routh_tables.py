# Author: Xu Chen, University of Washington
# Lecture 10: Routh tables for the lecture examples (uses tools/routh.py)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
import sympy as sp
from routh import routh

K = sp.Symbol('K')
for c in ([1, 10, 31, 1030],          # 1000/((s+2)(s+3)(s+5)), unity feedback
          [1, 2, 3, 6, 5, 3],         # special case 1 (zero in the first column)
          [1, 7, 6, 42, 8, 56],       # special case 2 (row of zeros)
          [1, 1, 4, 30],         # quick-check example: 2 RHP roots
          [1, 18, 77, K]):            # K/(s(s+7)(s+11)): stable for 0 < K < 1386
    rows, notes = routh(c)
    print(c)
    for r in rows:
        print('   ', r)
    if notes:
        print('    notes:', notes)
