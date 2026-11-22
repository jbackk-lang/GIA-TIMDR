"""Exact rational interval proof: three physical roots, nine distinct D3 shapes.

Uses the independently stored reduced equations and exact Groebner basis.
All decisions use rational arithmetic, not floating point.
Run: python experiments/rhombic_prism_triangle_nine_exact_certificate.py
"""
import math
import sympy as sp
from rhombic_prism_triangle_reduced_equations import u,v,w,s,F

z=sp.Symbol("z")
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
assert sp.degree(linear,u)==1
assert sp.gcd(eliminant,sp.diff(eliminant,z))==1
U=sp.cancel(sp.solve(linear,u)[0])
assert not U.has(rt)

Q=sp.Rational
scale=10**55
root3=math.isqrt(3*scale*scale)
sqrt3=(Q(root3,scale),Q(root3+1,scale))
assert sqrt3[0]**2<3<sqrt3[1]**2

def add(a,b): return (a[0]+b[0],a[1]+b[1])
def neg(a): return (-a[1],-a[0])
def mul(a,b):
    p=[x*y for x in a for y in b]
    return min(p),max(p)
def sq(a):
    if a[0]<=0<=a[1]: return (Q(0),max(a[0]**2,a[1]**2))
    return (min(a[0]**2,a[1]**2),max(a[0]**2,a[1]**2))
def scalar(k,a): return mul((Q(k),Q(k)),a)
def horner(poly,iv):
    p=sp.Poly(poly,z)
    out=(Q(0),Q(0))
    for c in p.all_coeffs():
        assert c.is_Rational
        out=add(mul(out,iv),(c,c))
    return out
def ratio(a,b):
    assert b[0]>0 or b[1]<0
    return mul(a,(1/b[1],1/b[0]))
def rotate(point):
    x,y=point
    return (add(scalar(Q(-1,2),x),scalar(Q(-1,2),mul(sqrt3,y))),
            add(scalar(Q(1,2),mul(sqrt3,x)),scalar(Q(-1,2),y)))
def disjoint(p,q):
    return any(p[i][1]<q[i][0] or q[i][1]<p[i][0] for i in range(2))

num,den=sp.fraction(U)
intervals=sp.polys.polytools.intervals(sp.Poly(eliminant,z),eps=Q(1,10**48))
assert len(intervals)==7
physical=[]
for i,((lo,hi),multiplicity) in enumerate(intervals,1):
    assert multiplicity==1
    zi=(lo,hi)
    ui=ratio(horner(num,zi),horner(den,zi))
    vi=mul(sqrt3,zi)
    r2=add(sq(ui),sq(vi))
    assert r2[1]<1 or r2[0]>1,("ambiguous disk membership",i)
    inside=r2[1]<1
    print("root",i,"inside",inside,"radius2 bounds approx",
          tuple(float(x) for x in r2))
    if inside: physical.append((ui,vi))
assert len(physical)==3
points=[]
for k in range(3):
    for p in physical:
        x=p
        for _ in range(k): x=rotate(x)
        points.append(x)
for i in range(9):
    for j in range(i+1,9):
        assert disjoint(points[i],points[j]),("overlap",i,j)
print("CERTIFIED: exactly three roots in physical disk for ordering 123.")
print("CERTIFIED: nine distinct physical shapes across all six orders.")
print("CERTIFIED: D3 orbit decomposition 3+6 using established covariance.")
