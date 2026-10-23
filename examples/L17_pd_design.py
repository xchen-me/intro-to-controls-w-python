# Author: Xu Chen, University of Washington
# Lecture 17: PD design for K/(s(s+4)(s+6)), 16% overshoot, 3x faster settling
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
import numpy as np
import control as ct
import matplotlib.pyplot as plt
from rlfig import zeta_cross

den = np.poly([0, -4, -6])
zeta = -np.log(0.16) / np.sqrt(np.pi**2 + np.log(0.16)**2)       # 0.504
s0, K0 = zeta_cross([1], den, zeta)[0]                            # -1.204 + 2.065j, K = 43.4
print('zeta = %.3f, uncompensated pole %s, K = %.1f' % (zeta, np.round(s0, 3), K0))

for speedup in (3, 4):
    sd = speedup * s0                                             # target pole on the same ray
    alpha = sum(np.degrees(np.angle(sd - p)) for p in (0, -4, -6)) - 180   # zero angle
    zc = -(sd.real - sd.imag / np.tan(np.radians(alpha)))         # zero at -zc
    K = abs(np.polyval(den, sd)) / abs(sd + zc)                   # magnitude condition
    T = ct.feedback(ct.tf([K, K * zc], den), 1)
    info = ct.step_info(T)
    print('%dx: s_d = %s, zero = %.2f, K = %.1f, OS = %.1f%%, Ts = %.2f s'
          % (speedup, np.round(sd, 2), -zc, K, info['Overshoot'], info['SettlingTime']))
    t, y = ct.step_response(T, np.linspace(0, 5, 1000))
    plt.plot(t, y, label='PD %dx' % speedup)
t, y = ct.step_response(ct.feedback(ct.tf([K0], den), 1), np.linspace(0, 5, 1000))
plt.plot(t, y, label='uncompensated'); plt.legend(); plt.grid(True); plt.show()
