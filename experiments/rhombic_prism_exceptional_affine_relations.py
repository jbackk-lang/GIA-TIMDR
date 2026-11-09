"""Exact exceptional affine-reflection relations for the rhombic triangular prism.

The five generators are reflections in the two triangular end planes and
the three actual lateral-face planes. Each lateral plane passes through its
own base edge, so its affine offset is included.
"""
import sympy as s

u, v, w = s.symbols("u v w", real=True)
I3 = s.eye(3)
R0 = s.diag(1, 1, -1)
A = s.Matrix([0, 0, 0])
B = s.Matrix([1, 0, 0])
C = s.Matrix([s.Rational(1, 2), s.sqrt(3)/2, 0])
vertices = (A, B, C)
edges = (
    s.Matrix([1, 0, 0]),
    s.Matrix([-s.Rational(1, 2), s.sqrt(3)/2, 0]),
    s.Matrix([-s.Rational(1, 2), -s.sqrt(3)/2, 0]),
)

def homogeneous(R, b):
    H = s.eye(4)
    H[:3, :3] = R
    H[:3, 3] = b
    return H

def reflection_in_plane(normal, point):
    nn = s.simplify(normal.dot(normal))
    R = s.simplify(I3 - 2*normal*normal.T/nn)
    b = s.simplify(2*normal*(normal.dot(point))/nn)
    return homogeneous(R, b)

def generators(U, V, W):
    T = s.Matrix([U, V, W])
    S0 = homogeneous(R0, s.zeros(3, 1))
    S1 = homogeneous(R0, s.Matrix([0, 0, 2*W]))
    sides = []
    normals = []
    for edge, point in zip(edges, vertices):
        normal = edge.cross(T)
        normals.append(normal)
        sides.append(reflection_in_plane(normal, point))
    return (S0, S1, *sides)

def inverse_isometry(H):
    R = H[:3, :3]
    b = H[:3, 3]
    return homogeneous(R.T, -R.T*b)

def main():
    # 1. A whole line of two commuting pairs: horizontal end planes and
    #    the first lateral plane are mutually perpendicular when v=0.
    S0, S1, S2, S3, S4 = generators(u, 0, w)
    assert s.simplify(S0*S2 - S2*S0) == s.zeros(4)
    assert s.simplify(S1*S2 - S2*S1) == s.zeros(4)
    print("PASS: v=0 gives two exact commuting reflection pairs.")
    print("relations: s0*s2=s2*s0; s1*s2=s2*s1")

    # 2. At (u,v,w)=(1/2,0,sqrt(3)/2), a glide-reflection conjugacy
    #    maps the third lateral plane to the second.
    W = s.sqrt(3)/2
    S0p, S1p, S2p, S3p, S4p = generators(s.Rational(1, 2), 0, W)
    G = s.simplify(S2p*S1p*S0p)
    assert s.simplify(G*S3p*inverse_isometry(G) - S4p) == s.zeros(4)
    print("PASS: at (1/2,0,sqrt(3)/2), G=s2*s1*s0 conjugates s3 to s4.")
    print("This is an additional glide-reflection relation on the v=0 branch.")

    # 3. On E1, test the exact condition for s2*s0*s2 and s3 to commute.
    #    Their normals are R2*k and e2 x t. Their dot product is:
    T = s.Matrix([u, v, w])
    n2 = edges[0].cross(T)
    n3 = edges[1].cross(T)
    R2 = s.simplify(I3 - 2*n2*n2.T/n2.dot(n2))
    k = s.Matrix([0, 0, 1])
    dot = s.factor((R2*k).dot(n3))
    numerator = s.factor((2*(v**2+w**2)*dot).subs(w**2, 1-u**2-v**2))
    expected = s.sqrt(3)*u**3 - u**2*v + 2*s.sqrt(3)*u*v**2 - s.sqrt(3)*u + v
    assert s.simplify(numerator-expected) == 0
    on_ellipse = s.factor(numerator.subs(u**2, 1-4*v**2))
    assert s.simplify(on_ellipse - 2*v**2*(2*v-s.sqrt(3)*u)) == 0
    print("PASS: exact orthogonality condition derived on E1.")
    print("E1: u^2+4*v^2=1")
    print("additional commuting-pair condition on E1: 2*v^2*(2*v-sqrt(3)*u)=0")
    print("non-degenerate isolated solutions: (u,v)=(1/2,sqrt(3)/4),(-1/2,-sqrt(3)/4)")

    # 4. Verify the extra affine reflections really commute at the positive
    #    isolated point; this is stronger than checking only normal vectors.
    U0, V0, W0 = s.Rational(1, 2), s.sqrt(3)/4, s.Rational(3, 4)
    S0q, S1q, S2q, S3q, S4q = generators(U0, V0, W0)
    conjugated_bottom = s.simplify(S2q*S0q*S2q)
    assert s.simplify(conjugated_bottom*S3q - S3q*conjugated_bottom) == s.zeros(4)
    print("PASS: at (1/2,sqrt(3)/4,3/4), s2*s0*s2 commutes with s3 exactly.")
    print("All checks include the correct affine offsets of the lateral planes.")

if __name__ == "__main__":
    main()
