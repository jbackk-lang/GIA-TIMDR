"""Check reflection pairing of physical triangle-order centroid-return roots.

The reflection H fixes the line u=sqrt(3)*v. It maps the two
off-axis roots to one another, while fixing the on-axis root.
Also verifies invariance of centroid and rotation measures on
generic interior points, rather than only at solutions.

Run: python experiments/rhombic_prism_triangle_reflection_symmetry.py
"""
import numpy as np
from rhombic_prism_triangle_order_anomaly import measures

SQ3=np.sqrt(3.)
H=np.array([[.5,SQ3/2],[SQ3/2,-.5]])

def mirror(u,v):
    return H@np.array([u,v],dtype=float)

def main():
    assert np.allclose(H@H,np.eye(2),atol=1e-14)
    assert np.isclose(np.linalg.det(H),-1.,atol=1e-14)
    p1=np.array([-.49519165,-.50610070])
    p2=np.array([-.58610596,-.33838843])
    p3=np.array([-.68589188,-.17579820])
    print("mirror P1 =",mirror(*p1),"target P3 =",p3)
    print("mirror P2 =",mirror(*p2),"target P2 =",p2)
    assert np.linalg.norm(mirror(*p1)-p3)<5e-8
    assert np.linalg.norm(mirror(*p2)-p2)<5e-8
    for p in ((.2,.1),(.4,-.2),(-.1,.5),tuple(p1),tuple(p2),tuple(p3)):
        q=mirror(*p)
        ao,ar,_=measures(*p)
        bo,br,_=measures(*q)
        print("point",p,"mirror",q.tolist(),"A_O",ao,bo,"A_R",ar,br)
        assert np.isclose(ao,bo,rtol=1e-10,atol=1e-10)
        assert np.isclose(ar,br,rtol=1e-10,atol=1e-10)
    print("Reflection-invariance numerical tests passed.")
    print("These tests do not constitute a symbolic identity proof.")

if __name__=="__main__":
    main()
