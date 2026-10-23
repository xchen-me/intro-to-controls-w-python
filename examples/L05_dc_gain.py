# Author: Xu Chen, University of Washington
# Lecture 5: the DC gain, and why stability must be checked first
import control as co
s = co.tf('s')
G = (2*s+3)/(4*s**2+3*s+1)
print(co.dcgain(G))              # 3.0

H = co.tf([0, 3], [1, -2])
print(co.dcgain(H))              # -1.5, but meaningless: H is unstable
T, yout = co.step_response(H)
print(yout)                      # grows without bound
