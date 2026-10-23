"""Author: Xu Chen. Independent mathematical checks for Lecture 10."""
import unittest
import numpy as np
import sympy as sp
from tools.routh import routh
from demos.routh_gain_app import simulate

class Lecture10(unittest.TestCase):
    def test_positive_coefficients_are_not_sufficient(self):
        s=sp.Symbol('s')
        self.assertEqual(sp.expand((s+3)*(s*s-2*s+10)),s**3+s*s+4*s+30)
        self.assertEqual(sum(np.roots([1,1,4,30]).real>0),2)
    def test_zero_pivot_limit(self):
        rows,notes=routh([1,2,3,6,5,3]);e=sp.Symbol('epsilon',positive=True)
        signs=[sp.limit(sp.sign(r[0]),e,0,dir='+') for r in rows]
        self.assertEqual(signs,[1,1,1,-1,1,1]);self.assertIn('eps',notes)
    def test_auxiliary_polynomial(self):
        rows,notes=routh([1,7,6,42,8,56]);s=sp.Symbol('s')
        self.assertEqual(notes[0][1],7*(s**4+6*s*s+8))
        self.assertEqual(rows[2],[28,84,0])
        self.assertEqual(sp.expand((s+7)*(s*s+2)*(s*s+4)),s**5+7*s**4+6*s**3+42*s*s+8*s+56)
    def test_gain_regimes(self):
        for gain,n in [(-20,1),(1000,0),(1800,2)]:
            self.assertEqual(sum(np.roots([1,18,77,gain]).real>1e-8),n)
        p=np.roots([1,18,77,1386]);self.assertTrue(np.allclose(np.sort(p.imag),[-np.sqrt(77),0,np.sqrt(77)]))
    def test_boundary_response(self):
        d=simulate(1386);t=np.linspace(0,10,len(d['y']));y=np.asarray(d['y']);w=np.sqrt(77)
        # Partial fractions of T(s)/s: constant + decaying exponential + sinusoid.
        expected=1-(77/401)*np.exp(-18*t)-(324/401)*np.cos(w*t)-(18*w/401)*np.sin(w*t)
        np.testing.assert_allclose(y,expected,atol=1e-6)
    def test_stable_response_settles(self):
        d=simulate(1000,duration=40)
        self.assertAlmostEqual(d['y'][-1],1,places=5)

if __name__=='__main__':unittest.main()
