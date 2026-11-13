"""Falsifiable tests of helical center motion and rotation noncommutativity.

Geometry only: no clock, force, magnetic field, or astrophysical model is inferred.
Run: python experiments/rhombic_prism_helix_commutator_audit.py
"""
import numpy as np
from rhombic_prism_mobility_screw_coupling import build_generators, compose, IDENTITY
from rhombic_prism_axis_limit_study import extract_axis

def center(u,v):
    w=np.sqrt(1-u*u-v*v)
    return np.array([(1+u)/2, np.sqrt(3)/6+v/2, w/2])

def apply(g,x):
    return g[0]@x+g[1]

def power(g,n):
    result=(IDENTITY,np.zeros(3))
    for _ in range(n):
        result=compose(g,result)
    return result

def rotation_pair(gens,i,j):
    return compose(gens[i],gens[j])

def audit(u,v):
    gens,w,_=build_generators(u,v)
    O=center(u,v)
    # Base+side reflection is a proper rotation about a horizontal base edge.
    # Pair two different side rotations to expose noncommutativity.
    g=rotation_pair(gens,0,2)
    h=rotation_pair(gens,0,3)
    gh=compose(g,h)
    hg=compose(h,g)
    commutator_center=float(np.linalg.norm(apply(gh,O)-apply(hg,O)))
    commutator_linear=float(np.linalg.norm(gh[0]-hg[0],ord='fro'))
    # g is a pure rotation: its center orbit must be circular, not a helix.
    kind,params=extract_axis(*g,min_angle_deg=0.1)
    assert kind=="rotation_axis",(u,v,kind)
    a,p,pitch,theta,_,_=params
    rho=np.linalg.norm(np.cross(O-p,a))
    radius_errors=[]
    axial_errors=[]
    step_errors=[]
    x=O.copy()
    for n in range(1,25):
        x=apply(g,x)
        radial=np.linalg.norm(np.cross(x-p,a))
        radius_errors.append(abs(radial-rho))
        axial_errors.append(abs(np.dot(x-O,a)))
        prediction=2*rho*abs(np.sin(np.deg2rad(n*theta)/2))
        step_errors.append(abs(np.linalg.norm(x-O)-prediction))
    assert max(radius_errors)<1e-8
    assert max(axial_errors)<1e-8
    assert max(step_errors)<1e-8
    # Translation followed by g gives a screw only if the translation vector
    # is parallel to g's rotation axis. For a horizontal axis and vertical
    # translation, this composition is generally another offset rotation.
    T=compose(gens[1],gens[0])
    assert np.allclose(T[1],[0,0,2*w],atol=1e-12)
    print(f"u={u:.8g} v={v:.8g} center_commutator={commutator_center:.9g} "
          f"linear_commutator={commutator_linear:.9g} radius={rho:.9g} "
          f"theta_deg={theta:.9g} circle_max_error={max(radius_errors):.3g} "
          f"axial_max_error={max(axial_errors):.3g} displacement_max_error={max(step_errors):.3g}")

if __name__=="__main__":
    for params in ((0.,0.),(.01,0.),(.2,.1),(.4/np.sqrt(2),.4/np.sqrt(2))):
        audit(*params)
