"""Exact characteristic/minimal polynomials of the 9D conjugation action.

The 9D operator is R tensor R for R in SO(3).
This test is symbolic (SymPy), with no numerical eigenvalue approximations.
"""
import sympy as sp

def main():
    l,c,s=sp.symbols("lambda c s",real=True)
    R=sp.Matrix([[c,-s,0],[s,c,0],[0,0,1]])
    T=sp.kronecker_product(R,R)
    chi=sp.factor(T.charpoly(l).as_expr())
    target=(l-1)**3*(l*l-2*c*l+1)**2*(l*l-(4*c*c-2)*l+1)
    # Reduce modulo the defining unit-circle identity.
    assert sp.rem(sp.Poly(sp.expand(chi-target),s),sp.Poly(s*s+c*c-1,s)).is_zero
    # Independently calculate determinant and check the factorization.
    assert sp.rem(sp.Poly(sp.expand((l*sp.eye(9)-T).det()-target),s),
                  sp.Poly(s*s+c*c-1,s)).is_zero
    # Generic minimal polynomial is the square-free part of chi.
    generic=(l-1)*(l*l-2*c*l+1)*(l*l-(4*c*c-2)*l+1)
    # Verify annihilation of T using s^2=1-c^2.
    P=sp.eye(9)*0
    for coefficient in sp.Poly(generic,l).all_coeffs():
        P=P*T+coefficient*sp.eye(9)
    for entry in P:
        assert sp.rem(sp.Poly(sp.expand(entry),s),
                      sp.Poly(s*s+c*c-1,s)).is_zero
    # Invariant subspaces: scalar 1D, antisymmetric 3D, symmetric traceless 5D.
    basis=[sp.eye(3)]
    for i,j in ((0,1),(0,2),(1,2)):
        E=sp.zeros(3);E[i,j]=1;E[j,i]=-1;basis.append(E)
    D1=sp.diag(1,-1,0);D2=sp.diag(1,1,-2)
    basis.extend([D1,D2])
    for i,j in ((0,1),(0,2),(1,2)):
        E=sp.zeros(3);E[i,j]=E[j,i]=1;basis.append(E)
    assert len(basis)==9
    B=sp.Matrix.hstack(*[sp.Matrix(9,1,list(X)) for X in basis])
    assert B.det()!=0
    M=B.inv()*T*B
    for a,b in ((0,1),(1,4),(4,9)):
        for d,e in ((0,1),(1,4),(4,9)):
            if (a,b)!=(d,e):
                for x in M[a:b,d:e]:
                    assert sp.rem(sp.Poly(sp.expand(x),s),
                                  sp.Poly(s*s+c*c-1,s)).is_zero
    print("PASS: exact 9x9 characteristic polynomial")
    print("chi_9 =",sp.factor(target))
    print("PASS: degree-5 generic annihilating/minimal polynomial")
    print("PASS: invariant 1+3+5 blocks")

if __name__=="__main__":
    main()
