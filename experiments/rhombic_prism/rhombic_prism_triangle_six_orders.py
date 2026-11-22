"""All six triangle-order anomalies and their D3 action.

Exact group identities:
 Delta_(k,j,i) = Delta_(i,j,k)^(-1).
 Spatial +120 degree rotation about base centroid conjugates each generator
 to its cyclic successor, provided the shape parameter rotates as well.
The numerical assertions below are regression tests of those identities.
"""
from itertools import permutations
import numpy as np
from rhombic_prism_mobility_screw_coupling import build_generators,compose

SQ3=np.sqrt(3.)
C=np.array([[-.5,-SQ3/2,0],[SQ3/2,-.5,0],[0,0,1.]])
base_centroid=np.array([.5,SQ3/6,0.])
K=(C,base_centroid-C@base_centroid)
PERMS=list(permutations(range(3)))

def inverse(g):
    R,b=g
    return R.T,-R.T@b

def delta(rotations,order):
    a,b,c=[rotations[i] for i in order]
    P=compose(compose(a,b),c)
    Q=compose(compose(c,b),a)
    return compose(P,inverse(Q))

def generators(u,v):
    original,w,_=build_generators(u,v)
    return [compose(original[0],original[i]) for i in (2,3,4)]

def center(u,v):
    return np.array([(.5+u/2),SQ3/6+v/2,np.sqrt(1-u*u-v*v)/2])

def measures(d,O):
    R,b=d
    q=R@O+b-O
    return float(q@q),float(np.sum((R-np.eye(3))**2))

def conjugate(k,g):
    return compose(compose(k,g),inverse(k))

def close(g,h):
    return np.allclose(g[0],h[0],atol=2e-11,rtol=0) and np.allclose(g[1],h[1],atol=2e-11,rtol=0)

def main():
    for u,v in ((0.,0.),(.2,.1),(-.4,-.3),(.31,-.52)):
        g=generators(u,v)
        O=center(u,v)
        uv=C@np.array([u,v,0.])
        u2,v2=uv[:2]
        h=generators(u2,v2)
        O2=center(u2,v2)
        assert np.allclose(K[0]@O+K[1],O2,atol=2e-12)
        for order in PERMS:
            d=delta(g,order)
            reverse=delta(g,order[::-1])
            assert close(reverse,inverse(d))
            ao,ar=measures(d,O)
            bo,br=measures(reverse,O)
            assert np.isclose(ao,bo,atol=1e-10)
            assert np.isclose(ar,br,atol=1e-10)
            rotated_order=tuple((i+1)%3 for i in order)
            d2=delta(h,rotated_order)
            assert close(conjugate(K,d),d2)
            co,cr=measures(d2,O2)
            assert np.isclose(ao,co,atol=1e-10)
            assert np.isclose(ar,cr,atol=1e-10)
        print(f"PASS shape=({u},{v}) all six orders: reverse and cyclic equivariance")
    print("Distinct reversal pairs:",[(tuple(i+1 for i in p),tuple(i+1 for i in p[::-1])) for p in PERMS if p<p[::-1]])
    print("The three cyclic families have congruent zero sets after parameter rotation.")
    print("This does not imply all three sets coincide at fixed (u,v).")

if __name__=="__main__":
    main()
