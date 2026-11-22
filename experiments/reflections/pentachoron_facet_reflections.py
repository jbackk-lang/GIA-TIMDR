"""Exact facet-reflection experiment for the regular 4-simplex (pentachoron).

The five vertices are v_i=e_i-(1/5)(1,1,1,1,1) in the sum-zero
subspace of Q^5. The five facet reflections are affine isometries of that
4D subspace, represented exactly in Q^5.
"""
from fractions import Fraction as Q
from itertools import product
from collections import Counter

N=5
ONE=tuple(Q(1,5) for _ in range(N))
V=tuple(tuple(Q(int(i==j))-Q(1,5) for j in range(N)) for i in range(N))
I=tuple(tuple(Q(int(i==j)) for j in range(N)) for i in range(N))
Z=tuple(Q(0) for _ in range(N))

def dot(a,b): return sum((x*y for x,y in zip(a,b)),Q(0))
def mv(A,x): return tuple(sum((A[i][j]*x[j] for j in range(N)),Q(0)) for i in range(N))
def mm(A,B): return tuple(tuple(sum((A[i][k]*B[k][j] for k in range(N)),Q(0)) for j in range(N)) for i in range(N))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def compose(after,before):
    A,b=after; C,d=before
    return mm(A,C), add(mv(A,d),b)

def reflection(i):
    v=V[i]
    A=tuple(tuple(I[r][c]-Q(5,2)*v[r]*v[c] for c in range(N)) for r in range(N))
    b=tuple(-Q(1,2)*x for x in v)
    return A,b

G=tuple(reflection(i) for i in range(N))
def trace(A): return sum((A[i][i] for i in range(N)),Q(0))

def main():
    # Geometry of regular 4-simplex facets.
    assert all(dot(v,v)==Q(4,5) for v in V)
    assert all(dot(V[i],V[j])==Q(-1,5) for i in range(N) for j in range(N) if i!=j)
    for i in range(N):
        for j in range(N):
            if i!=j:
                assert all(compose(G[i],G[i])[0][r][c]==I[r][c] for r in range(N) for c in range(N))
                # Each reflection fixes the four vertices of its facet.
                assert all(add(mv(G[i][0],V[k]),G[i][1])==V[k] for k in range(N) if k!=i)

    pair_cosines=[]
    pair_maps=[]
    for i in range(N):
        for j in range(i+1,N):
            T=compose(G[i],G[j])
            pair_maps.append(T)
            # Product is identity on 3D complement of span(v_i,v_j)
            # within sum-zero R4; its nontrivial plane rotation has cos=-7/8.
            # Ambient R5 trace = 1 (all-ones direction) + 2 fixed + 2cos(theta).
            cosine=(trace(T[0])-3)/2
            pair_cosines.append(cosine)
    assert set(pair_cosines)=={Q(-7,8)}
    assert len(set(pair_maps))==10

    # Enumerate reduced words: no adjacent repeated facet reflection.
    prev=[((),(I,Z))]
    counts={}
    for length in range(1,6):
        cur=[]
        for word,T in prev:
            for i in range(N):
                if word and word[-1]==i: continue
                cur.append((word+(i,),compose(G[i],T)))
        maps=[T for _,T in cur]
        counts[length]=(len(cur),len(set(maps)))
        assert len(cur)==N*(N-1)**(length-1)
        assert len(set(maps))==len(maps), (length,"duplicate affine maps")
        prev=cur

    # Niven theorem: -7/8 is not an allowed rational cosine for rational
    # multiples of pi, so each two-facet product has infinite order.
    assert Q(-7,8) not in {Q(0),Q(1,2),Q(-1,2),Q(1),Q(-1)}
    print("PASS: exact regular 4-simplex facet geometry in Q^5 sum-zero subspace.")
    print("vertices=5; tetrahedral facets=5; facet-pair products=10.")
    print("unit-normal inner product = -1/4")
    print("two-facet product rotation cosine = -7/8")
    print("all 10 pair products have infinite order (Niven theorem).")
    for n,(words,maps) in counts.items():
        print(f"word_length_{n}: reduced_words={words}; distinct_affine_maps={maps}")
    print("RESULT: pentachoron facet reflections generate non-periodic 4D rotations;")
    print("         reduced words through length 5 show no affine-map collisions.")
    print("LIMIT: finite enumeration is not a proof of freeness; no physical force or knot claim.")

if __name__=="__main__": main()
