"""Audit the spectral multiset of nine physical centroid-return configurations.

The 9 shapes come from rotating the 3 physical roots by 0,120,240 degrees.
For each shape, search all six orders, retaining those for which the
centroid-return displacement vanishes. Check the two trace classes (3+6).
"""
import itertools
import numpy as np
from scipy.optimize import root
from rhombic_prism_triangle_six_orders import generators,delta,center

ROT=np.array([[-.5,-np.sqrt(3)/2],[np.sqrt(3)/2,-.5]])
SEEDS=[(-.49519165,-.50610070),(-.58610596,-.33838843),(-.68589188,-.17579820)]
ORDERS=list(itertools.permutations(range(3)))

def residual(x):
    g=generators(*x)
    R,b=delta(g,(0,1,2))
    return R@center(*x)+b-center(*x)

def main():
    roots=[]
    for seed in SEEDS:
        sol=root(lambda x:residual(x)[:2],seed,tol=1e-12)
        assert np.linalg.norm(residual(sol.x))<1e-8
        roots.append(sol.x)
    shapes=[]
    for x in roots:
        for k in range(3):
            y=np.linalg.matrix_power(ROT,k)@x
            assert all(np.linalg.norm(y-z)>1e-5 for z in shapes)
            shapes.append(y)
    assert len(shapes)==9
    values=[]
    for i,x in enumerate(shapes):
        g=generators(*x);O=center(*x)
        cs=[]
        for order in ORDERS:
            R,b=delta(g,order)
            if np.linalg.norm(R@O+b-O)<1e-8:
                cs.append((np.trace(R)-1)/2)
        assert cs,("missing return order",i)
        assert max(cs)-min(cs)<1e-8,("order-dependent cosine at fixed shape",i,cs)
        values.append(float(np.mean(cs)))
    c3=values[3]
    c6=values[0]
    assert abs(c3-c6)>0.1
    assert sum(abs(x-c3)<1e-8 for x in values)==3
    assert sum(abs(x-c6)<1e-8 for x in values)==6
    print("3-point orbit cosine",c3)
    print("6-point orbit cosine",c6)
    print("PASS: nine distinct configurations, two spectral classes with multiplicities 3+6")

if __name__=="__main__":
    main()
