"""Three-rotation order anomaly: centroid displacement vs orientation.

Compute Delta=(g1 g2 g3)(g3 g2 g1)^-1, with gi=bottom_reflection
composed with the i-th side reflection. A_O=||Delta(O)-O||^2;
A_R=||R_Delta-I||_F^2.

Optional SciPy search finds candidate zeros of A_O; always check
the full three-component centroid displacement residual. These are
classical SE(3) kinematics, NOT quantum triangle anomalies.

Run: python experiments/rhombic_prism_triangle_order_anomaly.py
"""
import numpy as np
from rhombic_prism_mobility_screw_coupling import build_generators, compose, IDENTITY

def inverse(g):
    R,b=g
    return R.T,-R.T@b

def center(u,v):
    w=np.sqrt(1-u*u-v*v)
    return np.array([(1+u)/2,np.sqrt(3)/6+v/2,w/2])

def delta(u,v):
    gens,_,_=build_generators(u,v)
    r=[compose(gens[0],gens[i]) for i in (2,3,4)]
    P=compose(compose(r[0],r[1]),r[2])
    Q=compose(compose(r[2],r[1]),r[0])
    return compose(P,inverse(Q))

def measures(u,v):
    R,b=delta(u,v)
    O=center(u,v)
    residual=R@O+b-O
    return float(residual@residual),float(np.sum((R-IDENTITY)**2)),residual

def main():
    for u,v in ((0.,0.),(.01,0.),(.2,.1),
                (.4/np.sqrt(2),.4/np.sqrt(2)),(.5,0.),(-.5,0.)):
        ao,ar,_=measures(u,v)
        print(f"PARAM u={u:.12g} v={v:.12g} A_O={ao:.12g} A_R={ar:.12g}")
    R,b=delta(0.,0.)
    assert np.allclose(R,IDENTITY,atol=1e-12)
    assert np.isclose(np.linalg.norm(b),3.,atol=1e-12)
    print(f"SYMMETRIC exact_numerical_check: translation={b.tolist()} length=3")
    try:
        from scipy.optimize import least_squares
    except ImportError:
        print("SciPy not installed; skipping candidate-zero search")
        return
    for guess in ((-.63,-.27),(-.684,-.18)):
        def f(x):
            u,v=x
            if u*u+v*v>=.98**2:
                return np.full(3,1e3)
            return measures(u,v)[2]
        sol=least_squares(f,guess,xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=5000)
        u,v=sol.x
        ao,ar,res=measures(u,v)
        print(f"CANDIDATE_ZERO u={u:.12g} v={v:.12g} "
              f"residual_norm={np.linalg.norm(res):.5g} A_R={ar:.12g} "
              f"solver_success={sol.success}")
        assert np.linalg.norm(res)<1e-7
        assert ar>1e-4

if __name__=="__main__":
    main()
