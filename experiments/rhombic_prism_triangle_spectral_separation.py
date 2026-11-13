"""Exact rational spectral separation of the 3- and 6-shape classes.

Sturm root counts certify that the two algebraic cosine classes lie in
disjoint rational intervals; no floating point is used in these checks.
"""
import sympy as sp

c=sp.symbols("c")
P3=(3439853568*c**5-174103840768*c**4+
    3145786042786*c**3-590528708979*c**2+
    2034692645632*c-1345672319791)
P6=(411102815929*c**4-22711964978020*c**3+
    103536116470230*c**2-164124750044260*c+
    38719737491257)

def main():
    a=sp.Poly(P3,c,domain=sp.QQ)
    b=sp.Poly(P6,c,domain=sp.QQ)
    assert a.is_irreducible and b.is_irreducible
    assert sp.gcd(a,b).degree()==0
    lo3,hi3=sp.Rational(1,2),sp.Rational(3,5)
    lo6,hi6=sp.Rational(1,4),sp.Rational(1,3)
    assert a.count_roots(lo3,hi3)==1
    assert b.count_roots(lo6,hi6)==1
    assert a.eval(lo3)*a.eval(hi3)!=0
    assert b.eval(lo6)*b.eval(hi6)!=0
    assert hi6<lo3
    # For R in SO(3), tr(R)=1+2*cos(theta).
    assert 1+2*hi6<1+2*lo3
    print("3-shape spectral cosine: 1/2 < c3 < 3/5")
    print("6-shape spectral cosine: 1/4 < c6 < 1/3")
    print("Disjoint trace ranges: tr(R6)<5/3<2<tr(R3)")
    print("PASS: exact rational spectral separation via Sturm root counts")

if __name__=="__main__":
    main()
