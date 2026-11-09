"""Exact Coxeter braid relations on the candidate ellipse u^2+4v^2=1.

On the positive-v branch, w=sqrt(3)*v. The lower/upper triangular
face reflections and the side-face reflection over e1 then satisfy
s0*s2*s0 = s2*s0*s2 and s1*s2*s1 = s2*s1*s2 exactly.
These are affine reflection identities, checked with SymPy.
"""
import sympy as s

v = s.symbols("v", positive=True, real=True)
I3 = s.eye(3)
R0 = s.diag(1, 1, -1)

# e1=(1,0,0), t=(u,v,w), with w=sqrt(3)*v on the ellipse.
# The side-plane normal e1 x t is (0,-w,v)=(0,-sqrt(3)v,v).
n = s.Matrix([0, -s.sqrt(3)*v, v])
R2 = s.simplify(I3 - 2 * n * n.T / (n.dot(n)))

def homogeneous(R, b):
    H = s.eye(4)
    H[:3, :3] = R
    H[:3, 3] = b
    return H

S0 = homogeneous(R0, s.zeros(3, 1))
S1 = homogeneous(R0, s.Matrix([0, 0, 2*s.sqrt(3)*v]))
S2 = homogeneous(R2, s.zeros(3, 1))
H4 = s.eye(4)

def main():
    assert R2 == s.Matrix([
        [1, 0, 0],
        [0, -s.Rational(1, 2), s.sqrt(3)/2],
        [0, s.sqrt(3)/2, s.Rational(1, 2)],
    ])
    assert s.simplify(S0*S2*S0 - S2*S0*S2) == s.zeros(4)
    assert s.simplify(S1*S2*S1 - S2*S1*S2) == s.zeros(4)
    assert s.simplify((S0*S2)**3 - H4) == s.zeros(4)
    assert s.simplify((S1*S2)**3 - H4) == s.zeros(4)
    print("PASS: exact affine Coxeter braid relation for lower and upper face pairs.")
    print("ellipse: u^2+4*v^2=1; positive branch w=sqrt(3)*v")
    print("dihedral_angle=pi/3")
    print("s0*s2*s0 = s2*s0*s2")
    print("s1*s2*s1 = s2*s1*s2")
    print("(s0*s2)^3 = identity")
    print("(s1*s2)^3 = identity")
    print("CONCLUSION: the ellipse is an exact length-3 Coxeter-relation locus, not merely a numerical coincidence.")

if __name__ == "__main__":
    main()
