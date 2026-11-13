"""Exact elimination of cos(theta) for both D3 spectral orbits.

Compute the centroid-return Groebner basis, then eliminate the prism
parameters from the trace of the affine order commutator's rotation.
All polynomial identities are over QQ; no floating point is used for proofs.
"""
import sympy as sp
from rhombic_prism_triangle_reduced_equations import u,v,w,s,F

z,c=sp.symbols("z c")
rt=sp.sqrt(3)
constraint=sp.Poly(w*w+u*u+v*v-1,w)
E=[]
for i in range(3):
    rem=sp.rem(sp.Poly(sp.expand(F[i]),w),constraint).as_expr()
    q=sp.cancel(rem/((u*u+v*v-1)*(w if i==2 else 1)))
    q=sp.rem(sp.Poly(sp.expand(q),s),sp.Poly(s*s-3,s)).as_expr()
    E.append(sp.expand(q.subs(s,rt).subs(v,rt*z)))
G=sp.groebner(E,u,z,order="lex",extension=rt)
assert len(G.polys)==2
linear,eliminant=[p.as_expr() for p in G.polys]
U=sp.cancel(sp.solve(linear,u)[0])
assert not U.has(rt)
P5=1152*z**5+264*z**4-132*z**3-33*z**2+4*z+1
P8=(12544*z**8-448*z**7-18432*z**6-248*z**5+
    6968*z**4+1668*z**3-945*z**2-372*z-27)
assert sp.rem(sp.Poly(eliminant,z),sp.Poly((z*z-1)*P5*P8,z)).is_zero

B=sp.diag(1,1,-1)
t=sp.Matrix([u,v,w])
edges=[sp.Matrix([1,0,0]),sp.Matrix([-sp.Rational(1,2),rt/2,0]),
       sp.Matrix([-sp.Rational(1,2),-rt/2,0])]
M=[];ds=[]
for edge in edges:
    n=edge.cross(t)
    d=sp.expand(n.dot(n))
    M.append(B*(d*sp.eye(3)-2*n*n.T))
    ds.append(d)
# P=G1 G2 G3, Q=G3 G2 G1; rotation of Delta=P Q^{-1}.
numerator=sp.trace((M[0]*M[1]*M[2])*(M[0].T*M[1].T*M[2].T))
denominator=sp.prod(ds)**2
n=sp.rem(sp.Poly(sp.expand(numerator-denominator),w),constraint).as_expr()/2
d=sp.rem(sp.Poly(sp.expand(denominator),w),constraint).as_expr()
n=sp.expand(n.subs(v,rt*z))
d=sp.expand(d.subs(v,rt*z))
assert not n.has(rt) and not d.has(rt)

def reduce_mod(expr,poly):
    p=sp.Poly(poly,z,domain=sp.QQ)
    up=sp.Poly(U,z,domain=sp.QQ)%p
    out=sp.Poly(0,z,domain=sp.QQ)
    for coefficient in sp.Poly(expr,u).all_coeffs():
        out=(out*up+sp.Poly(coefficient,z,domain=sp.QQ))%p
    return out

expected5=(3439853568*c**5-174103840768*c**4+
           3145786042786*c**3-590528708979*c**2+
           2034692645632*c-1345672319791)
expected4=(411102815929*c**4-22711964978020*c**3+
           103536116470230*c**2-164124750044260*c+
           38719737491257)
for label,p,target,power in (("3-point orbit",P5,expected5,1),
                              ("6-point orbit",P8,expected4,2)):
    N=reduce_mod(n,p);D=reduce_mod(d,p)
    assert sp.gcd(D,sp.Poly(p,z,domain=sp.QQ)).degree()==0
    resultant=sp.resultant(p,N.as_expr()-c*D.as_expr(),z)
    primitive=sp.Poly(resultant,c).primitive()[1].as_expr()
    assert sp.expand(primitive-target**power)==0 or sp.expand(primitive+target**power)==0 or (
        sp.Poly(primitive,c).monic()==sp.Poly(target**power,c).monic())
    assert sp.Poly(target,c).is_irreducible
    print(label,": exact minimal polynomial =",sp.factor(target))
    print("resultant multiplicity:",power)
print("PASS: both exact algebraic spectral classes")
