# Author: Xu Chen, University of Washington
"""Compute root loci numerically and emit pgfplots code (for book/fig/*.tex)."""
import numpy as np


def branches(num, den, kmin=1e-4, kmax=1e5, n=4000, extra_k=()):
    num = np.atleast_1d(np.array(num, float)); den = np.atleast_1d(np.array(den, float))
    ks = np.unique(np.concatenate([[0.0], np.logspace(np.log10(kmin), np.log10(kmax), n), extra_k]))
    nump = np.concatenate([np.zeros(len(den) - len(num)), num])
    prev = np.roots(den).astype(complex)
    out = [prev]
    for k in ks[1:]:
        r = np.roots(den + k * nump).astype(complex)
        # match to previous ordering (greedy nearest neighbour)
        used = set(); cur = np.empty_like(prev)
        for i, p in enumerate(prev):
            d = [abs(p - q) if j not in used else np.inf for j, q in enumerate(r)]
            j = int(np.argmin(d)); used.add(j); cur[i] = r[j]
        out.append(cur); prev = cur
    return ks, np.array(out)  # shape (nK, nbranches)


def clip_path(z, xlim, ylim):
    """split a complex path into segments inside the window"""
    segs, cur = [], []
    for p in z:
        if xlim[0] <= p.real <= xlim[1] and ylim[0] <= p.imag <= ylim[1]:
            cur.append(p)
        else:
            if len(cur) > 1: segs.append(cur)
            cur = []
    if len(cur) > 1: segs.append(cur)
    return segs


def thin(seg, tol):
    out = [seg[0]]
    for p in seg[1:]:
        if abs(p - out[-1]) > tol: out.append(p)
    if out[-1] is not seg[-1]: out.append(seg[-1])
    return out


def rl_tikz(num, den, xlim, ylim, width='9cm', height='6cm', zeta=None, points=(), labels=(),
            asymptotes=None, kmax=1e5, extra='', color='red', arrows=True, title=None, axis_extra=''):
    ks, B = branches(num, den, kmax=kmax)
    tol = 0.004 * max(xlim[1] - xlim[0], ylim[1] - ylim[0])
    L = []
    L.append(r'\begin{tikzpicture}')
    L.append(r'\begin{axis}[width=%s, height=%s, xmin=%g, xmax=%g, ymin=%g, ymax=%g, axis lines=middle, '
             r'xlabel={$\mathrm{Re}$}, ylabel={$\mathrm{Im}$}, xlabel style={at={(ticklabel* cs:1)}, anchor=west}, '
             r'ylabel style={at={(ticklabel* cs:1)}, anchor=south}, tick label style={font=\scriptsize}, '
             r'clip=true%s%s]' % (width, height, xlim[0], xlim[1], ylim[0], ylim[1],
                                  (', title={%s}' % title) if title else '', (', ' + axis_extra) if axis_extra else ''))
    if asymptotes:
        c, angs = asymptotes
        for a in angs:
            R = 3 * max(xlim[1] - xlim[0], ylim[1] - ylim[0])
            x2 = c + R * np.cos(np.radians(a)); y2 = R * np.sin(np.radians(a))
            L.append(r'\addplot[gray, dashed, forget plot] coordinates {(%.4f,0) (%.4f,%.4f)};' % (c, x2, y2))
    if zeta is not None:
        th = np.arccos(zeta); R = 3 * max(-xlim[0], ylim[1])
        L.append(r'\addplot[blue, thick, forget plot] coordinates {(0,0) (%.4f,%.4f)};' % (-R * np.cos(th), R * np.sin(th)))
        L.append(r'\addplot[blue, thick, forget plot] coordinates {(0,0) (%.4f,%.4f)};' % (-R * np.cos(th), -R * np.sin(th)))
    for b in range(B.shape[1]):
        for seg in clip_path(B[:, b], xlim, ylim):
            seg = thin(seg, tol)
            if len(seg) < 2: continue
            coords = ' '.join('(%.4f,%.4f)' % (p.real, p.imag) for p in seg)
            L.append(r'\addplot[very thick, %s, forget plot] coordinates {%s};' % (color, coords))
            if arrows and len(seg) > 6:
                i = len(seg) // 2; p, q = seg[i], seg[i + 1]
                L.append(r'\draw[->, very thick, %s] (axis cs:%.4f,%.4f) -- (axis cs:%.4f,%.4f);' % (color, p.real, p.imag, q.real, q.imag))
    for p in np.roots(den):
        L.append(r'\node[font=\large, inner sep=0] at (axis cs:%.4f,%.4f) {$\times$};' % (p.real, p.imag))
    if len(np.atleast_1d(num)) > 1:
        for z in np.roots(num):
            L.append(r'\draw[thick, fill=white] (axis cs:%.4f,%.4f) circle (3pt);' % (z.real, z.imag))
    for (x, y) in points:
        L.append(r'\fill[blue] (axis cs:%.4f,%.4f) circle (2.5pt);' % (x, y))
    for (x, y, txt, anchor) in labels:
        L.append(r'\node[font=\scriptsize, anchor=%s] at (axis cs:%.4f,%.4f) {%s};' % (anchor, x, y, txt))
    if extra: L.append(extra)
    L.append(r'\end{axis}')
    L.append(r'\end{tikzpicture}')
    return '\n'.join(L)


def step_coords(num, den, T, n=300, k=1.0):
    import control as ct
    t = np.linspace(0, T, n)
    _, y = ct.step_response(ct.tf(np.array(num) * k, den), t)
    y = np.asarray(y).ravel()
    return ' '.join('(%.4f,%.4f)' % (a, b) for a, b in zip(t, y))


def zeta_cross(num, den, zeta, rmax=100, n=200000):
    """points s on the zeta line (upper half) where angle(G)=180 deg; returns list of (s, K)"""
    num = np.atleast_1d(np.array(num, float)); den = np.array(den, float)
    d = np.exp(1j * (np.pi - np.arccos(zeta)))
    rs = np.linspace(1e-4, rmax, n); s = rs * d
    G = np.polyval(num, s) / np.polyval(den, s)
    ph = np.angle(-G)  # zero when G is negative real
    out = []
    for i in range(len(rs) - 1):
        if np.sign(ph[i]) != np.sign(ph[i + 1]) and abs(ph[i]) < 1:
            si = s[i]; K = abs(np.polyval(den, si) / np.polyval(num, si))
            out.append((si, K))
    return out
