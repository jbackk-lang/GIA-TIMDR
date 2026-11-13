"""Eliminate w from the exact centroid-return polynomial system.

Requires sympy. Uses the physical constraint w²=1-u²-v².
The three equations reduce to two polynomials in (u,v,s) and one
w times a polynomial in (u,v,s). In the physical domain w>0,
the common w² factor can be cancelled, giving three polynomial
conditions in u,v with s=+sqrt(3). No root completeness claimed.

Run: python experiments/rhombic_prism_triangle_reduced_equations.py
"""
import sympy as sp

u,v,w,s=sp.symbols("u v w s",real=True)
t=sp.Matrix([u,v,w])
edges=[sp.Matrix([1,0,0]),
       sp.Matrix([-sp.Rational(1,2),s/2,0]),
       sp.Matrix([-sp.Rational(1,2),-s/2,0])]
verts=[sp.Matrix([0,0,0]),sp.Matrix([1,0,0]),
       sp.Matrix([sp.Rational(1,2),s/2,0])]
O=sp.Matrix([(1+u)/2,s/6+v/2,w/2,1])
B=sp.diag(1,1,-1,1)
S=[]
for e,p in zip(edges,verts):
    n=e.cross(t)
    d=(n.T*n)[0]
    M=d*sp.eye(3)-2*n*n.T
    b=2*n*(n.T*p)[0]
    S.append(M.row_join(b).col_join(sp.Matrix([[0,0,0,d]])))

# r_i=B*(S_i/d_i). Thus P^-1 O and Q^-1 O are proportional
# to the two products below with the same positive denominator.
F=S[2]*B*S[1]*B*S[0]*B*O-S[0]*B*S[1]*B*S[2]*B*O
constraint=sp.Poly(w*w+u*u+v*v-1,w)
factor=u*u+v*v-1

def main():
    reduced=[]
    for i in range(3):
        rem=sp.rem(sp.Poly(sp.expand(F[i]),w),constraint).as_expr()
        if i<2:
            assert not rem.has(w)
            numerator=rem
        else:
            assert sp.expand(rem).subs(w,0)==0
            numerator=sp.cancel(rem/w)
            assert not numerator.has(w)
        quotient=sp.cancel(numerator/factor)
        assert not quotient.has(w)
        assert sp.expand(numerator-factor*quotient)==0
        # Replace s powers using the minimal polynomial s²=3.
        q=sp.rem(sp.Poly(sp.expand(quotient),s),
                 sp.Poly(s*s-3,s)).as_expr()
        reduced.append(sp.factor(q))
        print(f"E{i+1}(u,v,s) =",sp.factor(q))
        print("  degree_uv=",sp.Poly(q,u,v).total_degree(),
              " terms=",len(sp.Poly(q,u,v,s).terms()))
    print("Physical domain: u²+v²<1; s=+sqrt(3).")
    print("Exactly equivalent conditions: E1=E2=E3=0.")
    print("No exact root isolation or completeness result yet.")

if __name__=="__main__":
    main()
