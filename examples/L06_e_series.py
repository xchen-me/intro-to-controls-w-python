# Author: Xu Chen, University of Washington
# Lecture 6: e = sum of 1/n!
import math
print(math.e)
for ii in range(10):
    print(sum(1 / math.factorial(k) for k in range(ii)))
