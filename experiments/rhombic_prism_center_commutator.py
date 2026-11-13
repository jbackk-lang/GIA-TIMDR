"""Exact affine commutator tests for the rhombic triangular prism.

For g,h in SE(3), K=g h g^-1 h^-1. A nonidentity K fixes the
centroid O exactly iff (R_K-I)O+b_K=0. Numerical scans are evidence
about selected parameters, not a proof that no other solutions exist.

Run: python experiments/rhombic_prism_center_commutator.py
"""
import numpy as np
from rhombic_prism_mobility_screw_coupling import build_generators, compose, IDENTITY

def inv(g):
    R,b=g
    return R.T,-R.T@b

def act(g,x):
    return g[0]@x+g[1]

def center(u,v):
    w=np.sqrt(1-u*u-v*v)
    return np.array([(1+u)/2,np.sqrt(3)/6+v/2,w/2])

def commutator(g,h):
    return compose(compose(compose(g,h),inv(g)),inv(h))

def rotations(gens):
    # bottom reflection combined with each of the three side reflections
    return [compose(gens[0],gens[i]) for i in (2,3,4)]

def diagnostics(u,v):
    gens,_,_=build_generators(u,v)
    O=center(u,v)
    out=[]
    r=rotations(gens)
    for i,j in ((0,1),(0,2),(1,2)):
        g,h=r[i],r[j]
        K=commutator(g,h)
        fixed_residual=np.linalg.norm(act(K,O)-O)
        nonidentity=np.linalg.norm(K[0]-IDENTITY,ord='fro')
        order_gap=np.linalg.norm(act(compose(g,h),O)-act(compose(h,g),O))
        # K fixes O iff g h(O)=h g(O) is NOT generally true; these
        # are independent tests and must not be conflated.
        assert np.allclose(K[0].T@K[0],IDENTITY,atol=2e-10)
        assert abs(np.linalg.det(K[0])-1)<2e-10
        out.append((i,j,fixed_residual,nonidentity,order_gap))
    return out

def main():
    for u,v in ((0.,0.),(.01,0.),(.2,.1),
                (.4/np.sqrt(2),.4/np.sqrt(2))):
        for i,j,res,rot,gap in diagnostics(u,v):
            print(f"u={u:.8g},v={v:.8g},pair={i}{j},"
                  f"centroid_return_residual={res:.12g},"
                  f"rotation_nonidentity={rot:.12g},"
                  f"composition_order_gap={gap:.12g}")
    # A fixed-center nontrivial rotation is possible in SE(3), even
    # though it is not guaranteed for the chosen prism generators.
    O=np.array([.3,.2,.7])
    angle=np.pi/3
    R=np.array([[np.cos(angle),-np.sin(angle),0],
                [np.sin(angle),np.cos(angle),0],[0,0,1]])
    b=O-R@O
    assert np.allclose(R@O+b,O)
    assert np.linalg.norm(R-IDENTITY)>1
    print("CONTROL: nontrivial fixed-center rotation identity verified")

if __name__=="__main__":
    main()
