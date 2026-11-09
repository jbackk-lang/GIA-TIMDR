"""Diagnose the r=0.4 D3 endpoint: generator conjugacy and raw-word maps."""
import numpy as np
from rhombic_prism_mobility_screw_coupling import IDENTITY, build_generators, compose


def reflection_30():
    d = np.array([np.cos(np.pi/6), np.sin(np.pi/6), 0.0])
    n = np.array([-d[1], d[0], 0.0])
    return IDENTITY-2*np.outer(n, n)


def generator_permutation(u1, v1, u2, v2):
    g1, _, _ = build_generators(u1, v1)
    g2, _, _ = build_generators(u2, v2)
    S = reflection_30()
    permutation, residuals = [], []
    for M, b in g1:
        Mc, bc = S@M@S.T, S@b
        candidates = [max(np.linalg.norm(Mc-N), np.linalg.norm(bc-d))
                      for N, d in g2]
        j = int(np.argmin(candidates))
        permutation.append(j)
        residuals.append(candidates[j])
    return g1, g2, S, permutation, residuals


def all_word_conjugacy(g1, g2, S, permutation, max_length=8):
    states = [(IDENTITY, np.zeros(3), IDENTITY, np.zeros(3), -1)]
    max_matrix_error = max_offset_error = 0.0
    count = 0
    for depth in range(1, max_length+1):
        nxt = []
        for M1, b1, M2, b2, last in states:
            for i, gen1 in enumerate(g1):
                if i == last:
                    continue
                j = permutation[i]
                Q1, q1 = compose(gen1, (M1, b1))
                Q2, q2 = compose(g2[j], (M2, b2))
                nxt.append((Q1, q1, Q2, q2, i))
        states = nxt
    for M1, b1, M2, b2, _ in states:
        max_matrix_error = max(max_matrix_error, float(np.linalg.norm(S@M1@S.T-M2)))
        max_offset_error = max(max_offset_error, float(np.linalg.norm(S@b1-b2)))
        count += 1
    return count, max_matrix_error, max_offset_error


def enum_words(u, v, max_length=8):
    gens, _, _ = build_generators(u, v)
    states = [(IDENTITY, np.zeros(3), -1)]
    for depth in range(1, max_length+1):
        nxt = []
        for M, b, last in states:
            for i, gen in enumerate(gens):
                if i == last:
                    continue
                Q, q = compose(gen, (M, b))
                nxt.append((Q, q, i))
        states = nxt
    return [(M,b) for M,b,_ in states]


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
    g1,g2,S,perm,residuals=generator_permutation(*p0,*p1)
    print("GENERATOR_PERMUTATION",perm)
    print("GENERATOR_CONJUGACY_RESIDUALS",residuals)
    count, em, eb=all_word_conjugacy(g1,g2,S,perm)
    print(f"WORDWISE_CONJUGACY,length=8,words={count},max_matrix_error={em:.12g},max_offset_error={eb:.12g}")
    a=enum_words(*p0)
    b=enum_words(*p1)
    print(f"RAW_WORD_MAPS,{len(a)},{len(b)}")
    for d in (12,10,9,8,7,6):
        print(f"QUANTIZED_UNIQUE,{d},{len(quantized_unique(a,d))},{len(quantized_unique(b,d))}")
    aa,bb=angle_support(a),angle_support(b)
    print(f"ANGLE_SUPPORT,{len(aa)},{len(bb)},equal={np.array_equal(aa,bb)}")
    if len(aa)==len(bb):
        print(f"ANGLE_SUPPORT_MAX_DELTA,{np.max(np.abs(aa-bb)):.12g}")
    if max(residuals)>1e-10 or em>1e-10 or eb>1e-10:
        raise SystemExit(1)


if __name__=="__main__":
    main()
