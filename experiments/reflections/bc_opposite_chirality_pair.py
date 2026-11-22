"""Compare opposite traversal with opposite chirality for BC screw strands.

The second map is the mirror-conjugate of the BC screw by reflection in a
plane containing the screw axis. This reverses angular handedness while
preserving the axial advance. Exact Fraction arithmetic is used throughout.
"""
from __future__ import annotations
import sys
from pathlib import Path
from fractions import Fraction as Q
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.boerdijk_coxeter_tetrahelix import INITIAL_VERTICES, SCREW_ROTATION, SCREW_TRANSLATION, _dot, _sub, _cross

def tr(A): return tuple(tuple(A[j][i] for j in range(3)) for i in range(3))
def mv(A,p): return tuple(sum((A[i][j]*p[j] for j in range(3)),Q(0)) for i in range(3))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mm(A,B): return tuple(tuple(sum((A[i][k]*B[k][j] for k in range(3)),Q(0)) for j in range(3)) for i in range(3))
def orbit(p,A,b,n):
    out=[p]
    for _ in range(n): out.append(add(mv(A,out[-1]),b))
    return tuple(out)
def seg_intersection(p1,p2,q1,q2):
    u,v,w=sub(p2,p1),sub(q2,q1),sub(q1,p1)
    # Solve using any nonsingular 2x2 coordinate minor, then verify all 3D coords.
    for i,j in ((0,1),(0,2),(1,2)):
        det=u[i]*(-v[j])-(-v[i])*u[j]
        if det==0: continue
        # [u_i,-v_i;u_j,-v_j] [s,t] = [w_i,w_j]
        s=(w[i]*(-v[j])-(-v[i])*w[j])/det
        t=(u[i]*w[j]-u[j]*w[i])/det
        if 0<=s<=1 and 0<=t<=1 and all(p1[k]+s*u[k]==q1[k]+t*v[k] for k in range(3)):
            return True
        return False
    # Parallel case: reject unless collinear; if collinear, project and test intervals.
    if _dot(_cross(w,u),_cross(w,u)) != 0: return False
    axis=next(k for k in range(3) if u[k]!=0)
    lo=max(min(p1[axis],p2[axis]),min(q1[axis],q2[axis]))
    hi=min(max(p1[axis],p2[axis]),max(q1[axis],q2[axis]))
    return lo<=hi

def main():
    A=tr(SCREW_ROTATION); b=SCREW_TRANSLATION
    # Reflection M in plane spanned by screw axis (2,1,0) and z-axis.
    n=(Q(1),Q(-2),Q(0)); nn=_dot(n,n)
    M=tuple(tuple(Q(int(i==j))-2*n[i]*n[j]/nn for j in range(3)) for i in range(3))
    A_m=mm(mm(M,A),M); b_m=mv(M,b)
    # Same axial direction, opposite angular direction: mirror conjugation.
    axis=(Q(2),Q(1),Q(0)); axis_point=(Q(0),Q(0),Q(-2,5)); axis_sq=_dot(axis,axis)
    p=INITIAL_VERTICES[0]
    proj=tuple(axis_point[k]+axis[k]*_dot(sub(p,axis_point),axis)/axis_sq for k in range(3))
    q=tuple(2*proj[k]-p[k] for k in range(3))
    def z(x): return _dot(sub(x,axis_point),axis)
    def r2(x):
        v=sub(x,axis_point)
        return _dot(v,v)-z(x)**2/axis_sq
    one=orbit(p,A,b,64); two=orbit(q,A_m,b_m,64)
    assert all(r2(x)==Q(54,25) for x in one+two)
    da=z(one[1])-z(one[0]); db=z(two[1])-z(two[0])
    assert da==db and da!=0
    point_hits=[(i,j) for i,x in enumerate(one) for j,y in enumerate(two) if x==y]
    assert not point_hits
    crossings=[(i,j) for i in range(64) for j in range(64) if seg_intersection(one[i],one[i+1],two[j],two[j+1])]
    # Report intersections rather than assume a knot/link type.
    print("PASS: exact mirror-conjugate screw maps preserve common axis and radius.")
    print(f"radius_squared={r2(p)}; axial_steps=({da},{db})")
    print("angular_handedness=opposite by mirror conjugation")
    print(f"sampled_point_coincidences={len(point_hits)}")
    print(f"polyline_segment_intersections={len(crossings)}")
    if crossings: print(f"first_segment_intersection={crossings[0]}")
    print("LIMIT: finite polygonal samples are not a closed link and do not establish a linking number.")

if __name__=="__main__": main()
