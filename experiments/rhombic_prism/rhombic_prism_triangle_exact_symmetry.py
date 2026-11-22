"""Exact ideal symmetry test for the triangle-order centroid-return locus.

A zero remainder for all transformed generators proves preservation of
the algebraic zero set. For non-preservation, the Groebner basis has
a square-free univariate eliminant and a linear equation for u, hence
the ideal is radical; a nonzero normal form then witnesses failure
to preserve the zero set over the algebraic closure.

Run: python experiments/rhombic_prism_triangle_exact_symmetry.py
"""
import sympy as sp
from rhombic_prism_triangle_reduced_equations import u,v,w,s,F

def equations():
    c=sp.Poly(w*w+u*u+v*v-1,w)
    out=[]
    for i in range(3):
        rem=sp.rem(sp.Poly(sp.expand(F[i]),w),c).as_expr()
        q=sp.cancel(rem/((u*u+v*v-1)*(w if i==2 else 1)))
        q=sp.rem(sp.Poly(sp.expand(q),s),sp.Poly(s*s-3,s)).as_expr()
        out.append(sp.expand(q.subs(s,sp.sqrt(3))))
    return out

def main():
    eq=equations()
    G=sp.groebner(eq,u,v,order="lex",extension=sp.sqrt(3))
    assert len(G.polys)==2
    linear,univariate=[p.as_expr() for p in G.polys]
    assert sp.degree(linear,u)==1 and not univariate.has(u)
    assert sp.gcd(univariate,sp.diff(univariate,v))==1
    # Since the linear leading coefficient is constant and the
    # univariate eliminant is square-free, the ideal is radical.
    rt=sp.sqrt(3)
    mirror={u:(u+rt*v)/2,v:(rt*u-v)/2}
    rotate={u:(-u-rt*v)/2,v:(rt*u-v)/2}
    assert sp.expand(mirror[u].subs(mirror,simultaneous=True)-u)==0
    assert sp.expand(mirror[v].subs(mirror,simultaneous=True)-v)==0
    for name,T in (("mirror",mirror),("rotate120",rotate)):
        results=[]
        for e in eq:
            image=sp.expand(e.subs(T,simultaneous=True))
            rem=G.reduce(image)[1]
            results.append(rem==0)
        print(name,"zero_remainders=",results)
        if name=="mirror":
            assert all(results)
        else:
            assert not all(results)
    print("CERTIFIED: reflection preserves the exact algebraic locus.")
    print("CERTIFIED: 120-degree parameter rotation does not preserve it.")
    print("NOTE: rotation with simultaneous permutation of generator labels")
    print("is a different equivariance question and is not disproved here.")

if __name__=="__main__":
    main()
