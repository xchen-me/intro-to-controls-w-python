# Author: Xu Chen, University of Washington
# Lecture 19: PID design with the root locus and Python
import numpy as np
import control as ct
import matplotlib.pyplot as plt

G = ct.tf([1, 8], np.convolve(np.convolve([1, 3], [1, 6]), [1, 10]))

# P only: click the zeta = 0.456 point on the root locus to read K (about 121.5)
ct.root_locus(G); plt.show()

C_pd = ct.tf([1, 55.97], [1])          # PD zero, gain read from root locus
ct.root_locus(C_pd * G); plt.show()

C_pi = ct.tf([1, 0.1], [1, 0])         # PI: pole at 0, zero at -0.1
ct.root_locus(C_pd * C_pi * G); plt.show()

T1 = ct.feedback(121.5 * G, 1)
T2 = ct.feedback(5.33 * C_pd * G, 1)
T3 = ct.feedback(5.17 * C_pd * C_pi * G, 1)
for T in (T1, T2, T3):
    t, y = ct.step_response(T, np.linspace(0, 3, 3000))
    plt.plot(t, y)
plt.show()
