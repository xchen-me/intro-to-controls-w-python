"""Repeated poles and coefficient sensitivity. Author: Xu Chen, University of Washington.

Run: python examples/L10_repeated_poles.py --save out/repeated_poles.png
The exact integer coefficients are representable in float64 for these orders.
The root splitting is a conditioning/roundoff effect, not physical instability.
"""
import argparse
from math import comb
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def repeated_roots(n):
    coefficients = np.array([comb(n, k) for k in range(n + 1)], dtype=float)
    return np.roots(coefficients)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--save', type=Path)
    args = parser.parse_args()
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), constrained_layout=True)
    for ax, n in zip(axes, (12, 20)):
        poles = repeated_roots(n)
        ax.scatter(poles.real, poles.imag, marker='x', color='#4B2E83', label='Computed roots')
        ax.scatter([-1], [0], facecolor='none', edgecolor='#B7A57A', s=100, label='Exact root')
        ax.axhline(0, color='gray', lw=.5)
        ax.axvline(-1, color='gray', lw=.5)
        ax.set(title=rf'$(s+1)^{{{n}}}$', xlabel='Real part', ylabel='Imaginary part')
        ax.set_xlim(-1.55, -.45)
        ax.set_ylim(-.5, .5)
        ax.legend(fontsize=8)
        print(f'n={n}: max root displacement = {np.max(abs(poles + 1)):.6f}')
    print('Perturbation check: (s+1)^12 + 1e-12 has |s+1| = 0.1.')
    if args.save:
        args.save.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.save, dpi=180)
    else:
        plt.show()


if __name__ == '__main__':
    main()
