"""Exact rational-interval certificate for physical triangle-order roots.

No float is used to classify the disk condition u²+v²<1.
The root intervals come from SymPy's exact real-root isolation.
All subsequent bounds are rational, including sqrt(3) enclosures.
Run: python experiments/rhombic_prism_triangle_certified_disk.py
"""
import math
import sympy as sp
from rhombic_prism_triangle_groebner_roots import z,elim,U

Q=sp.Rational
S=sp.sqrt(3)
SCALE=10**35
LOW=Q(math.isqrt(3*SCALE*SCALE),SCALE)
HIGH=LOW+Q(1,SCALE)
assert LOW*LOW<3<HIGH*HIGH

def add(a,b):
    return a[0]+b[0],a[1]+b[1]

def mul(a,b):
    p=[x*y for x in a for y in b]
    return min(p),max(p)

def div(a,b):
    assert b[0]>0 or b[1]<0,("denominator interval contains zero",b)
    inv=(1/b[1],1/b[0])
    return mul(a,inv)

def sq(a):
    if a[0]<=0<=a[1]:
        return Q(0),max(a[0]**2,a[1]**2)
    return min(a[0]**2,a[1]**2),max(a[0]**2,a[1]**2)

def algebraic_coeff(x):
    # All coefficients lie in Q(sqrt(3)); extract exactly.
    x=sp.expand(sp.radsimp(x))
    b=sp.expand(x).coeff(S)
    a=sp.simplify(x-b*S)
    assert a.is_Rational and b.is_Rational,(x,a,b)
    return add((a,a),mul((b,b),(LOW,HIGH)))

def poly_interval(expr,interval):
    poly=sp.Poly(sp.expand(expr),z,extension=S)
    acc=(Q(0),Q(0))
    for coeff in poly.all_coeffs():
        acc=add(mul(acc,interval),algebraic_coeff(coeff))
    return acc

def main():
    num,den=sp.fraction(sp.cancel(U))
    roots=sp.polys.polytools.intervals(sp.Poly(elim,z),eps=Q(1,10**24))
    assert len(roots)==7,("unexpected root count",len(roots))
    physical=[]
    for i,((lo,hi),multiplicity) in enumerate(roots,1):
        assert multiplicity==1
        zi=(lo,hi)
        ui=div(poly_interval(num,zi),poly_interval(den,zi))
        vi=mul((LOW,HIGH),zi)
        radius2=add(sq(ui),sq(vi))
        assert radius2[1]<1 or radius2[0]>1,("undecided disk membership",i,radius2)
        inside=radius2[1]<1
        if inside: physical.append(i)
        print("root",i,"z_bounds",zi,"u_bounds",ui,"radius2_bounds",radius2,
              "physical",inside)
    assert len(physical)==3,("physical root count",physical)
    print("CERTIFIED: exactly 3 physical roots for ordering 123.")
    print("CERTIFIED: all other isolated real roots are outside the open disk.")
    print("Combined with proven cyclic equivariance and reversal pairing,")
    print("each of the six orderings has exactly three physical roots.")
    print("To certify nine distinct shapes, additionally certify pairwise")
    print("separation of all rotated rational-interval boxes.")

if __name__=="__main__":
    main()
