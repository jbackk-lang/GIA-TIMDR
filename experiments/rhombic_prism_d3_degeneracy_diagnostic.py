"""Diagnose the single D3 endpoint mismatch at r=0.4, phi=0 versus 60 degrees."""
import numpy as np
from rhombic_prism_mobility_screw_coupling import IDENTITY, build_generators, compose


def reflection_30():
    # Reflection in the vertical plane spanned by the 30-degree direction and z.
    d = np.array([np.cos(np.pi/6), np.sin(np.pi/6), 0.0])
    n = np.array([-d[1], d[0], 0.0])
    return IDENTITY-2*np.outer(n, n)


def match_generator_sets(u1, v1, u2, v2):
    g1, _, _ = build_generators(u1, v1)
    g2, _, _ = build_generators(u2, v2)
    S = reflection_30()
    residuals = []
    for M, b in g1:
        Mc, bc = S@M@S.T, S@b
        candidates = [max(np.linalg.norm(Mc-N), np.linalg.norm(bc-d))
                      for N, d in g2]
        residuals.append(min(candidates))
    return residuals


def enum_words(u, v, max_length=8):
    gens, _, _ = build_generators(u, v)
    states = [(IDENTITY, np.zeros(3), -1)]
    snapshots = {}
    for depth in range(1, max_length+1):
        nxt = []
        for M, b, last in states:
            for i, gen in enumerate(gens):
                if i == last:
                    continue
                Q, q = compose(gen, (M, b))
                nxt.append((Q, q, i))
        states = nxt
        if depth == max_length:
            snapshots = [(M,b) for M,b,_ in states]
    return snapshots


def quantized_unique(maps, decimals):
    return {tuple(np.round(np.r_[M.ravel(), b], decimals)) for M,b in maps}


def angle_support(maps):
    vals = []
    for M,b in maps:
        if np.linalg.det(M) <= 0 or np.linalg.norm(M-IDENTITY) <= 2e-7:
            continue
        c=np.clip((np.trace(M)-1)/2,-1,1)
        sk=np.array([M[2,1]-M[1,2],M[0,2]-M[2,0],M[1,0]-M[0,1]])
        s=.5*np.linalg.norm(sk)
        vals.append(np.degrees(np.arctan2(s,c)))
    return np.unique(np.round(vals,7))


def main():
    r=.4
    p0=np.array([r,0.0])
    p1=np.array([r*np.cos(np.pi/3),r*np.sin(np.pi/3)])
    print("GENERATOR_CONJUGACY_RESIDUALS",match_generator_sets(*p0,*p1))
    a=enum_words(*p0)
    b=enum_words(*p1)
    print(f"RAW_WORD_MAPS,{len(a)},{len(b)}")
    for d in (12,10,9,8,7,6):
        print(f"QUANTIZED_UNIQUE,{d},{len(quantized_unique(a,d))},{len(quantized_unique(b,d))}")
    aa,bb=angle_support(a),angle_support(b)
    print(f"ANGLE_SUPPORT,{len(aa)},{len(bb)},equal={np.array_equal(aa,bb)}")
    if len(aa)==len(bb):
        print(f"ANGLE_SUPPORT_MAX_DELTA,{np.max(np.abs(aa-bb)):.12g}")


if __name__=="__main__":
    main()
