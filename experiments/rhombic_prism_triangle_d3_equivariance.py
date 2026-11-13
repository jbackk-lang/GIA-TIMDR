"""Equivariance of three-reflection rotation words under triangle rotation.

For the base equilateral triangle, the +120 degree spatial rotation
about its centroid cyclically permutes the three side faces.
The parameter vector (u,v) rotates by the same angle.
This script checks affine conjugacy for generators and order anomalies.
Run: python experiments/rhombic_prism_triangle_d3_equivariance.py
"""
import numpy as np
from rhombic_prism_mobility_screw_coupling import build_generators,compose

S=np.sqrt(3.)
C=np.array([[-.5,-S/2,0],[S/2,-.5,0],[0,0,1.]])
p=np.array([.5,S/6,0.])
K=(C,p-C@p)

def inv(g):
    R,b=g
    return R.T,-R.T@b

def conj(k,g):
    return compose(compose(k,g),inv(k))

def anomaly(g,indices):
    a,b,c=[g[i] for i in indices]
    P=compose(compose(a,b),c)
    Q=compose(compose(c,b),a)
    return compose(P,inv(Q))

def close(g,h,tol=2e-12):
    return np.allclose(g[0],h[0],rtol=0,atol=tol) and np.allclose(g[1],h[1],rtol=0,atol=tol)

def main():
    for u,v in ((.2,.1),(-.5,-.3),(0.,0.),(.31,-.52)):
        uv=C@np.array([u,v,0.])
        old,_,_=build_generators(u,v)
        new,_,_=build_generators(*uv[:2])
        g=[compose(old[0],old[i]) for i in (2,3,4)]
        h=[compose(new[0],new[i]) for i in (2,3,4)]
        for i in range(3):
            assert close(conj(K,g[i]),h[(i+1)%3])
        for word in ((0,1,2),(1,2,0),(2,0,1)):
            perm=tuple((i+1)%3 for i in word)
            assert close(conj(K,anomaly(g,word)),anomaly(h,perm))
        print(f"PASS u={u} v={v}: generators and all cyclic-order anomalies equivariant")
    print("These are numerical checks of an exact geometric conjugacy theorem.")

if __name__=="__main__":
    main()
