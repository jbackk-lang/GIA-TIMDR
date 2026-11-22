"""Distinct centroid-return shapes across all six generator orderings.

Given three high-precision candidate roots for ordering 123, use exact
D3 covariance and reversal pairing to produce nine candidate shapes.
Tests separation numerically; exact completeness depends on the prior
Groebner/real-root certificate.
"""
import numpy as np

SQ3=np.sqrt(3.)
C=np.array([[-.5,-SQ3/2],[SQ3/2,-.5]])
H=np.array([[.5,SQ3/2],[SQ3/2,-.5]])
ROOTS=np.array([
    [-.49519165,-.50610070],
    [-.58610596,-.33838843],
    [-.68589188,-.17579820],
])

def main():
    assert np.allclose(C@C@C,np.eye(2),atol=1e-14)
    assert np.allclose(H@H,np.eye(2),atol=1e-14)
    assert np.allclose(H@C@H,C.T,atol=1e-14)
    assert np.linalg.norm(H@ROOTS[0]-ROOTS[2])<5e-8
    assert np.linalg.norm(H@ROOTS[1]-ROOTS[1])<5e-8
    orbit=np.array([np.linalg.matrix_power(C,k)@p for k in range(3) for p in ROOTS])
    distances=[np.linalg.norm(orbit[i]-orbit[j]) for i in range(9) for j in range(i+1,9)]
    minimum=min(distances)
    print("Nine candidate shapes, in order: (123),(231),(312) ordering families")
    for i,p in enumerate(orbit):
        print(f"{i+1:2d}: u={p[0]:+.12f} v={p[1]:+.12f}")
    print(f"Minimum pairwise distance = {minimum:.12f}")
    assert minimum>.19
    axial=np.array([np.linalg.matrix_power(C,k)@ROOTS[1] for k in range(3)])
    off=np.array([np.linalg.matrix_power(C,k)@ROOTS[j] for k in range(3) for j in (0,2)])
    assert len(axial)==3 and len(off)==6
    print("D3 orbit sizes: axial=3; off-axis=6")
    print("Numerical separation is not an interval-arithmetic certificate.")

if __name__=="__main__":
    main()
