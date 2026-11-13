"""Exact Gröbner elimination for three-rotation centroid-return conditions.

Requires sympy. The two-variable equations are imported from the
symbolic reduction script. Real-root isolation is exact; floating
approximations are for display and physical-domain filtering.
"""
import sympy as sp
from rhombic_prism_triangle_reduced_equations import u,v,w,s,F

z=sp.symbols("z")
constraint=sp.Poly(w*w+u*u+v*v-1,w)
E=[]
for i in range(3):
    rem=sp.rem(sp.Poly(sp.expand(F[i]),w),constraint).as_expr()
    q=sp.cancel(rem/((u*u+v*v-1)*(w if i==2 else 1)))
    q=sp.rem(sp.Poly(sp.expand(q),s),sp.Poly(s*s-3,s)).as_expr()
    E.append(sp.expand(q.subs(s,sp.sqrt(3)).subs(v,sp.sqrt(3)*z)))

G=sp.groebner(E,u,z,order="lex",extension=sp.sqrt(3))
assert len(G.polys)==2
linear,elim=(p.as_expr() for p in G.polys)
assert sp.degree(linear,u)==1
P5=1152*z**5+264*z**4-132*z**3-33*z**2+4*z+1
P8=(12544*z**8-448*z**7-18432*z**6-248*z**5+
    6968*z**4+1668*z**3-945*z**2-372*z-27)
assert sp.rem(sp.Poly(elim,z),sp.Poly((z*z-1)*P5*P8,z)).is_zero
U=sp.solve(linear,u)[0]
intervals=sp.polys.polytools.intervals(sp.Poly(elim,z),eps=sp.Rational(1,10**14))
assert len(intervals)==7
inside=[]
for (lo,hi),mult in intervals:
    zz=(lo+hi)/2
    uu=float(U.subs(z,zz));vv=float(sp.sqrt(3)*zz)
    radius2=uu*uu+vv*vv
    print(f"z={float(zz):+.12f} u={uu:+.12f} v={vv:+.12f} radius2={radius2:.9f}")
    if radius2<1: inside.append((uu,vv))
assert len(inside)==3
print("Exactly seven real algebraic solutions; three lie in the physical disk.")
print("NOTE: domain classification uses high-precision isolated-root approximations.")
