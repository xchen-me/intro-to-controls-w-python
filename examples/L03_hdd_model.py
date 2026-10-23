# Author: Xu Chen, University of Washington
# Lecture 3, Modeling: 16-mode hard-disk-drive actuator model
import numpy as np
import control as ct

Kp_vcm = 3.7976e7                                  # VCM gain
omega_vcm = np.array([0, 5300, 6100, 6500, 8050, 9600, 14800, 17400, 21000,
                      26000, 26600, 29000, 32200, 38300, 43300, 44800]) * 2 * np.pi
kappa_vcm = np.array([1, -1.0, 0.1, -0.1, 0.04, -0.7, -0.2, -1.0, 3.0,
                      -3.2, 2.1, -1.5, 2.0, -0.2, 0.3, -0.5])
zeta_vcm = np.array([0, 0.02, 0.04, 0.02, 0.01, 0.03, 0.01, 0.02, 0.02,
                     0.012, 0.007, 0.01, 0.03, 0.01, 0.01, 0.01])

P = ct.tf([0], [1])                                # start from an empty transfer function
for k, w, z in zip(kappa_vcm, omega_vcm, zeta_vcm):
    P = P + ct.tf([k * Kp_vcm], [1, 2 * z * w, w**2])

# Frequency response, as in the Lecture 3 figure (100 Hz to 60 kHz)
import matplotlib.pyplot as plt
f = np.logspace(2, np.log10(6e4), 2000)
mag, phase, _ = ct.frequency_response(P, 2 * np.pi * f)
fig, (a1, a2) = plt.subplots(2, 1, sharex=True)
a1.semilogx(f, 20 * np.log10(mag)); a1.set_ylabel('Gain [dB]'); a1.grid(True, which='both')
a2.semilogx(f, np.degrees(np.unwrap(phase)) % -360); a2.set_ylabel('Phase [deg]'); a2.grid(True, which='both')
a2.set_xlabel('Frequency [Hz]')
plt.show()
