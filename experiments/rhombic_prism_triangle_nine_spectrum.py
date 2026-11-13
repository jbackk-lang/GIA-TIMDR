"""Audit the 3x3 -> 9x9 rotation-conjugation spectrum.

Requires numpy and scipy. Run from repository root:
python experiments/rhombic_prism_triangle_nine_spectrum.py
"""
import numpy as np
from scipy.optimize import root
from rhombic_prism_mobility_screw_coupling import build_generators,compose

I=np.eye(3)
def inv(g):
    R,b=g
    return R.T,-R.T@b

def delta(u,v):
    gs,w,_=build_generators(u,v)
    g=[compose(gs[0],gs[i]) for i in (2,3,4)]
    p=compose(compose(g[0],g[1]),g[2])
    q=compose(compose(g[2],g[1]),g[0])
    return compose(p,inv(q)),np.array([.5+u/2,np.sqrt(3)/6+v/2,w/2])

def displacement(x):
    (R,b),O=delta(*x)
    return R@O+b-O

def audit(x):
    (R,b),O=delta(*x)
    assert np.linalg.norm(R@O+b-O)<1e-8
    assert np.linalg.norm(R.T@R-I)<1e-10
    theta=np.arccos(np.clip((np.trace(R)-1)/2,-1,1))
    T=np.kron(R,R)
    assert np.linalg.norm(T.T@T-np.eye(9))<1e-10
    actual=np.linalg.eigvals(T)
    expected=[1]*3+[np.exp(1j*theta)]*2+[np.exp(-1j*theta)]*2+[np.exp(2j*theta),np.exp(-2j*theta)]
    for a in expected:
        assert min(abs(a-b) for b in actual)<1e-9
    scalar=[I/np.sqrt(3)]
    skew=[]
    sym=[np.diag([1,-1,0])/np.sqrt(2),np.diag([1,1,-2])/np.sqrt(6)]
    for a,b in ((0,1),(0,2),(1,2)):
        A=np.zeros((3,3));A[a,b]=1/np.sqrt(2);A[b,a]=-1/np.sqrt(2)
        skew.append(A)
        B=np.zeros((3,3));B[a,b]=B[b,a]=1/np.sqrt(2)
        sym.append(B)
    basis=np.stack([x.ravel() for x in scalar+skew+sym],axis=1)
    assert np.linalg.norm(basis.T@basis-np.eye(9))<1e-12
    blocks=basis.T@T@basis
    for a,b in ((0,1),(1,4),(4,9)):
        for c,d in ((0,1),(1,4),(4,9)):
            if (a,b)!=(c,d):
                assert np.linalg.norm(blocks[a:b,c:d])<1e-10
    print("root",x,"theta_deg",np.degrees(theta),"A_R",np.sum((R-I)**2),
          "block_traces",[np.trace(blocks[a:b,a:b]) for a,b in ((0,1),(1,4),(4,9))])
    return theta

def main():
    seeds=[(-.49519165,-.50610070),(-.58610596,-.33838843),(-.68589188,-.17579820)]
    angles=[]
    for seed in seeds:
        solution=root(lambda x:displacement(x)[:2],seed,tol=1e-12)
        assert np.linalg.norm(displacement(solution.x))<1e-8
        angles.append(audit(solution.x))
    assert abs(angles[0]-angles[2])<1e-8
    assert abs(angles[0]-angles[1])>.1
    print("PASS: 9x9 spectrum and 1+3+5 invariant block decomposition")

if __name__=="__main__":
    main()
