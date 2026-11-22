"""Exact trace-power invariants for the 3D -> 9D rotation lift.

For T=R tensor R and c=cos(theta), tr(T^k)=(1+2*T_k(c))^2,
where T_k is the Chebyshev polynomial of the first kind.
"""
import sympy as sp

def main():
    c,s=sp.symbols("c s",real=True)
    R=sp.Matrix([[c,-s,0],[s,c,0],[0,0,1]])
    T=sp.kronecker_product(R,R)
    for k in range(0,9):
        observed=sp.trace(T**k)
        expected=(1+2*sp.chebyshevt(k,c))**2
        residual=sp.rem(sp.Poly(sp.expand(observed-expected),s),
                        sp.Poly(s*s+c*c-1,s))
        assert residual.is_zero,("trace identity",k)
        print("k =",k,"trace polynomial =",sp.expand(expected))
    print("PASS: exact trace-power invariants k=0..8")

if __name__=="__main__":
    main()
