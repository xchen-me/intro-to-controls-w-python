# Author: Xu Chen, University of Washington
# Lecture 5: transfer functions, poles and zeros, responses in python-control
import control as co
import matplotlib.pyplot as plt
import numpy as np

num = [1, 2]                     # numerator coefficients:   s + 2
den = [1, 2, 3]                  # denominator coefficients: s^2 + 2s + 3
sys_tf = co.tf(num, den)
print(sys_tf)
print('poles =', co.poles(sys_tf), ' zeros =', co.zeros(sys_tf))

T, yout = co.step_response(sys_tf)
plt.plot(T, yout); plt.grid(True); plt.xlabel('Time (sec)'); plt.ylabel('y'); plt.show()

# responses to other inputs
u1 = 2 * np.ones_like(T)         # a constant input of 2
u2 = np.sin(T)                   # a sinusoidal input
T, yout_u1 = co.forced_response(sys_tf, T, u1)
T, yout_u2 = co.forced_response(sys_tf, T, u2)
