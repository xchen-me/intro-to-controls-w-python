# Author: Xu Chen, University of Washington
import numpy as np, sympy as sp
def routh(c, eps=sp.Symbol('epsilon', positive=True)):
    c=[sp.nsimplify(x) for x in c]; n=len(c)
    rows=[c[0::2], c[1::2]]; w=(n+1)//2
    rows=[r+[0]*(w-len(r)) for r in rows]; notes=[]
    while len(rows)<n:
        a,b=rows[-2],rows[-1]
        if all(sp.simplify(x)==0 for x in b):
            deg=n-len(rows)  # degree of row above
            deg=n-1-(len(rows)-2)
            aux=[a[i]*sp.Symbol('s')**(deg-2*i) for i in range(w)]
            daux=sp.Poly(sp.diff(sum(aux),sp.Symbol('s')),sp.Symbol('s')).all_coeffs()
            b=[daux[i] for i in range(0,len(daux),2)]; b=b+[0]*(w-len(b)); rows[-1]=b; notes.append(('aux',sum(aux)))
        if sp.simplify(b[0])==0: b[0]=eps; rows[-1]=b; notes.append('eps')
        r=[sp.simplify((b[0]*a[i+1]-a[0]*b[i+1])/b[0]) for i in range(w-1)]+[0]
        rows.append(r)
    return rows, notes
if __name__=='__main__':
    for c in [[1,10,31,1030],[1,2,3,6,5,3],[1,7,6,42,8,56],[1,3,1,2,3,1],[1,18,77,sp.Symbol('K')]]:
        R,nt=routh(c); print(c, 'roots', np.round(np.roots([float(x) if not isinstance(x,sp.Symbol) else 1000 for x in c]),3))
        for r in R: print('   ',r)
        print('   notes',nt)
