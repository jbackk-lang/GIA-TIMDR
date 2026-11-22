"""Exact polynomial system for triangle-order centroid-return configurations.

Run: python experiments/rhombic_prism_triangle_polynomial_system.py
Requires SymPy. This constructs an exact algebraic system; it does not
claim to have isolated or counted all of its real physical solutions.
"""
import sympy as sp

u,v,w,s=sp.symbols("u v w s",real=True)
t=sp.Matrix([u,v,w])
edges=[sp.Matrix([1,0,0]),
       sp.Matrix([-sp.Rational(1,2),s/2,0]),
       sp.Matrix([-sp.Rational(1,2),-s/2,0])]
vertices=[sp.Matrix([0,0,0]),sp.Matrix([1,0,0]),
          sp.Matrix([sp.Rational(1,2),s/2,0])]
O=sp.Matrix([(1+u)/2,s/6+v/2,w/2,1])
B=sp.diag(1,1,-1,1)

def scaled_side(e,p):
    n=e.cross(t)
    D=(n.T*n)[0]
    M=D*sp.eye(3)-2*n*n.T
    b=2*n*(n.T*p)[0]
    return M.row_join(b).col_join(sp.Matrix([[0,0,0,D]])),D

pairs=[scaled_side(e,p) for e,p in zip(edges,vertices)]
S=[x[0] for x in pairs]
D=[x[1] for x in pairs]
# For r_i=bottom_reflection * side_reflection,
# r_i^-1=side_reflection * bottom_reflection.
# Delta=P*Q^-1 fixes O iff P^-1 O=Q^-1 O.
# Common denominator D1*D2*D3 is strictly positive in the domain.
lhs=S[2]*B*S[1]*B*S[0]*B*O
rhs=S[0]*B*S[1]*B*S[2]*B*O
F=lhs[:3,0]-rhs[:3,0]

def main():
    sub={u:0,v:0,w:1,s:sp.sqrt(3)}
    values=[sp.simplify(x.subs(sub)) for x in F]
    print("F(0,0,1,sqrt(3)) =",values)
    assert sp.simplify(sum(x*x for x in values)-9)==0
    print("Exact equations: F1=F2=F3=0")
    print("Constraints: u^2+v^2+w^2=1; s^2=3; w>0; D_i>0")
    print("Degrees:",[sp.Poly(x,u,v,w,s).total_degree() for x in F])
    print("Term counts:",[len(sp.Poly(x,u,v,w,s).terms()) for x in F])
    print("Side denominators:",D)

if __name__=="__main__":
    main()
