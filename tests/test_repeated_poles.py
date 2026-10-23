"""Author: Xu Chen. Checks for the tunable repeated-pole demonstration."""
import unittest
import numpy as np
from demos.repeated_poles_app import calculate
class RepeatedPoles(unittest.TestCase):
    def test_quadratic_exact_roots(self):
        np.testing.assert_allclose(calculate(2)['roots'],[[-1,0],[-1,0]],atol=1e-12)
    def test_degree_and_real_polynomial_symmetry(self):
        for n in [12,20,40]:
            d=calculate(n);p=np.array([complex(*v) for v in d['roots']])
            self.assertEqual(len(p),n)
            self.assertTrue(np.isfinite(p).all())
            self.assertAlmostEqual(p.sum().real,-n,places=8)
            self.assertAlmostEqual(p.sum().imag,0,places=8)
            self.assertAlmostEqual(d['max_displacement'],max(abs(p+1)))
    def test_invalid_order(self):
        for n in [1,41,12.5,True]:
            with self.assertRaises(ValueError):calculate(n)
