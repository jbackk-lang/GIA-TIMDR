"""Two exact angle cases for a triangular prism with three rhombic sides.

The closed prism topology imposes a geometric constraint: if all three
lateral parallelograms are exact rhombi, both triangular ends must be
equilateral and congruent. We therefore vary two rhombus angles; the third
is constrained by the three edge directions of the equilateral triangle.

Base edge vectors:
 e1=(1,0,0), e2=(-1/2,sqrt(3)/2,0), e3=(-1/2,-sqrt(3)/2,0).
The translation t has unit length, so each side parallelogram is a rhombus.
Cases are specified by c1=t.e1 and c2=t.e2; c3=-c1-c2.
"""
import sympy as s
from itertools import combinations
from collections import Counter

r3=s.sqrt(3)
I=s.eye(3); O=s.zeros(3,1)
e=(s.Matrix([1,0,0]),s.Matrix([-s.Rational(1,2),r3/2,0]),s.Matrix([-s.Rational(1,2),-r3/2,0]))

def simp_mat(M):
    return M.applyfunc(s.simplify)

def reflection(n,c):
    n=s.Matrix(n)
    M=simp_mat(I-2*(n*n.T)/n.dot(n))
    b=simp_mat(2*c*n/n.dot(n))
    return M,b

def compose(A,B):
    M,b=A; N,d=B
    return simp_mat(M*N),simp_mat(M*d+b)

def eq(A,B):
    return all(s.simplify(x-y)==0 for x,y in zip(tuple(A[0])+tuple(A[1]),tuple(B[0])+tuple(B[1])))

def axis(M):
    ns=(M-I).nullspace()
    return ns[0] if ns else None

def classify(T):
    M,b=T
    if eq(T,(I,O)): return "identity",None
    if M==I: return "translation",None
    u=axis(M)
    if u is None: return "other",None
    pitch=s.simplify(u.dot(b))
    cosine=s.simplify((s.trace(M)-1)/2)
    return ("screw" if pitch!=0 else "rotation"),cosine

def make_case(c1,c2):
    # t=(c1,(2*c2+c1)/sqrt(3),w), with |t|=1.
    tx=c1
    ty=(2*c2+c1)/r3
    w2=s.simplify(1-tx**2-ty**2)
    if not (w2.is_positive or w2.is_zero):
        raise ValueError(f"no real prism for c1={c1}, c2={c2}: w^2={w2}")
    w=s.sqrt(w2)
    t=s.Matrix([tx,ty,w])
    assert s.simplify(t.dot(t)-1)==0
    assert [s.simplify(t.dot(v)) for v in e]==[c1,c2,-c1-c2]
    # bottom and top triangular planes
    G=[reflection((0,0,1),0),reflection((0,0,1),w)]
    # three rhombus planes through each base edge and the translation t
    for v in e:
        n=v.cross(t)
        G.append(reflection(n,0))
    return t,w,G

def main():
    cases=[
      ("A: 60deg and 90deg",s.Rational(1,2),s.Rational(0)),
      ("B: 60deg and arccos(1/4)",s.Rational(1,2),s.Rational(1,4)),
    ]
    for label,c1,c2 in cases:
        t,w,G=make_case(c1,c2)
        c3=-c1-c2
        # The acute rhombus angle has cosine |t.e_i|.
        acute_cos=sorted([abs(c1),abs(c2),abs(c3)],reverse=True)
        pair_kinds=Counter(); pair_cos=Counter(); pair_details=[]
        for i,j in combinations(range(5),2):
            T=compose(G[i],G[j])
            kind,cosine=classify(T)
            pair_kinds[kind]+=1
            if cosine is not None: pair_cos[str(cosine)]+=1
            pair_details.append((i,j,kind,cosine))
        assert pair_kinds["translation"]==1
        assert pair_kinds["rotation"]==9
        # Each pair of distinct intersecting planes produces a pure rotation;
        # parallel end planes produce a translation by 2w.
        assert s.simplify(pair_details[0][2] == "translation")
        print(f"CASE {label}")
        print(f"t=({s.simplify(t[0])},{s.simplify(t[1])},{s.simplify(t[2])})")
        print(f"height={w}; translation_length={s.simplify(2*w)}")
        print(f"rhombus_edge_dot_products=({c1},{c2},{c3})")
        print(f"acute_rhombus_angles_cosines={acute_cos}")
        print(f"pair_types={dict(pair_kinds)}")
        print(f"pair_rotation_cosines={dict(pair_cos)}")
        print(f"pair_details={pair_details}")
        print("")

    print("GEOMETRIC CONSTRAINT: three exact rhombi force both triangular ends to be equilateral and congruent.")
    print("The two angle inputs are not independent of the third: c1+c2+c3=0.")
    print("LIMIT: these are exact face-reflection pair tests; no physical interaction or knot claim.")

if __name__=="__main__":
    main()
