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

def map_key(T):
    M,b=T
    return tuple(s.srepr(s.simplify(x)) for x in list(M)+list(b))

def direction_key(u):
    """Scale- and sign-independent exact direction key."""
    vals=list(u)
    k=next(i for i,x in enumerate(vals) if s.simplify(x)!=0)
    base=vals[k]
    ratios=[s.simplify(x/base) for x in vals]
    # Canonicalize sign by making first nonzero component +1.
    return tuple(ratios)

def axis_line_key(T):
    """Exact unoriented screw-axis line: canonical direction + closest point to origin."""
    M,b=T
    u=axis(M)
    lam=s.simplify(u.dot(b)/u.dot(u))
    rhs=simp_mat(b-lam*u)
    # On the plane perpendicular to u:
    # (I-M).T*(I-M) = 2*(1-cos(theta))*I.
    # This gives the closest-to-origin point of the axis without a symbolic
    # matrix inversion.
    cosine=s.simplify((s.trace(M)-1)/2)
    closest=simp_mat((I-M).T*rhs/(2*(1-cosine)))
    return direction_key(u), tuple(s.simplify(x) for x in closest)

def line_relation(L1,L2):
    """Exact relation of two distinct 3D lines."""
    d1=s.Matrix(L1[0]); p1=s.Matrix(L1[1])
    d2=s.Matrix(L2[0]); p2=s.Matrix(L2[1])
    normal=d1.cross(d2)
    delta=p2-p1
    if all(s.simplify(x)==0 for x in normal):
        return "parallel" if any(s.simplify(x)!=0 for x in delta.cross(d1)) else "coincident"
    return "intersecting" if s.simplify(delta.dot(normal))==0 else "skew"

def enumerate_layer(G, max_length=4):
    layer=[((),(I,O))]
    results={}
    for length in range(1,max_length+1):
        nxt=[]
        unique={}
        for word,T in layer:
            for i,g in enumerate(G):
                if word and word[-1]==i:
                    continue
                new_word=word+(i,)
                new_T=compose(g,T)
                nxt.append((new_word,new_T))
                unique.setdefault(map_key(new_T),(new_word,new_T))
        results[length]=(len(nxt),unique)
        layer=nxt
    return results

def analyze_even_layer(unique):
    types=Counter()
    cosines=Counter()
    rotation_axes=Counter()
    screw_axes=Counter()
    screw_pitch_sq=Counter()
    screw_lines=Counter()
    examples={}
    for word,T in unique.values():
        kind,cosine=classify(T)
        types[kind]+=1
        if cosine is not None:
            cosines[str(cosine)]+=1
        if kind in ("rotation","screw"):
            u=axis(T[0])
            d=direction_key(u)
            if kind=="rotation":
                rotation_axes[d]+=1
            else:
                screw_axes[d]+=1
                pitch_sq=s.simplify((u.dot(T[1])**2)/u.dot(u))
                screw_pitch_sq[str(pitch_sq)]+=1
                screw_lines[axis_line_key(T)]+=1
                examples.setdefault(d,word)
    line_list=list(screw_lines)
    line_relations=Counter(
        line_relation(line_list[i],line_list[j])
        for i in range(len(line_list)) for j in range(i+1,len(line_list))
    )
    return types,cosines,rotation_axes,screw_axes,screw_pitch_sq,screw_lines,line_relations,examples

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
        layers=enumerate_layer(G,4)
        for length in (2,4):
            word_count,unique=layers[length]
            if length==2:
                expected=18 if c2==0 else 20
            else:
                expected=245 if c2==0 else 292
            assert len(unique)==expected, (label,length,len(unique),expected)
            print(f"length_{length}: reduced_words={word_count}; distinct_maps={len(unique)}; collisions={word_count-len(unique)}")
            if length==4:
                types,cosines,rot_axes,screw_axes,pitch_sq,screw_lines,line_relations,examples=analyze_even_layer(unique)
                print(f"length_4_isometry_types={dict(types)}")
                print(f"length_4_rotation_cosines={dict(cosines)}")
                print(f"length_4_distinct_rotation_axis_directions={len(rot_axes)}")
                print(f"length_4_distinct_screw_axis_directions={len(screw_axes)}")
                print(f"length_4_distinct_screw_axis_lines={len(screw_lines)}")
                print(f"length_4_screw_axis_line_relations={dict(line_relations)}")
                print(f"length_4_screw_axis_direction_counts={dict(screw_axes)}")
                print(f"length_4_normalized_screw_pitch_squared={dict(pitch_sq)}")
        print("")

    print("GEOMETRIC CONSTRAINT: three exact rhombi force both triangular ends to be equilateral and congruent.")
    print("The two angle inputs are not independent of the third: c1+c2+c3=0.")
    print("LIMIT: finite word enumeration does not prove global group structure, knotting, or physical interaction.")

if __name__=="__main__":
    main()
