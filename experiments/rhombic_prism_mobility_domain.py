"""Exact mobility and admissible-angle domain for a triangular prism with 3 rhombi.

All edge lengths are fixed to 1. The two triangular ends are congruent
equilateral triangles. Each lateral face is a rhombus, hence a parallelogram.
The upper triangle is a translate t of the lower one, with |t|=1.

The model has two internal shape degrees of freedom: t lies on the unit
sphere, with t_z>0 for a non-degenerate prism. This script verifies the
exact constraints and the area/volume formulas symbolically.
"""
import sympy as s

u, v = s.symbols("u v", real=True)
w = s.symbols("w", positive=True, real=True)
r3 = s.sqrt(3)

e1 = s.Matrix([1, 0, 0])
e2 = s.Matrix([-s.Rational(1, 2), r3/2, 0])
e3 = s.Matrix([-s.Rational(1, 2), -r3/2, 0])
edges = (e1, e2, e3)

t = s.Matrix([u, v, w])
unit_constraint = s.Eq(u**2 + v**2 + w**2, 1)
c = [s.simplify(t.dot(e)) for e in edges]

def main():
    assert s.simplify(e1+e2+e3) == s.zeros(3, 1)
    assert all(s.simplify(e.dot(e)-1) == 0 for e in edges)
    assert s.simplify(sum(c)) == 0
    assert s.simplify(sum(x**2 for x in c) - s.Rational(3,2)*(u**2+v**2)) == 0

    # Each lateral face has side vectors e_i and t, both unit length.
    # Its area is |e_i x t| = sqrt(1 - (e_i.t)^2).
    face_area_sq = [s.simplify(1-x**2) for x in c]
    assert face_area_sq == [
        1-u**2,
        1-(u**2-2*r3*u*v+4*v**2)/4,
        1-(u**2+2*r3*u*v+4*v**2)/4,
    ]

    # End-triangle area and prism volume.
    base_area = r3/4
    volume = base_area*w
    assert s.simplify(volume**2 - s.Rational(3,16)*w**2) == 0

    # For each rhombus, the acute angle gamma_i obeys cos(gamma_i)=|c_i|.
    # Since w>0, |c_i|<1, hence 0<gamma_i<=90 degrees.
    print("PASS: exact rhombic triangular-prism mobility constraints.")
    print("shape_parameters=(u,v), with u^2+v^2<1 and w=sqrt(1-u^2-v^2)>0")
    print("internal_shape_degrees_of_freedom=2")
    print(f"rhombus_angle_cosines={c}")
    print("constraint_c1+c2+c3=0")
    print("constraint_c1^2+c2^2+c3^2=3/2*(u^2+v^2)<3/2")
    print(f"lateral_face_area_squared={face_area_sq}")
    print("each_rhombus_angle_range=(0,90] degrees")
    print(f"end_triangle_area={base_area}")
    print(f"volume={volume}")
    print("maximum_volume=sqrt(3)/4 at u=v=0 (three squares)")
    print("degenerate_boundary=u^2+v^2=1, w=0 (zero volume)")
    print("IMPORTANT: preserving triangle area alone does not imply rigidity; preserving triangle side lengths does.")
    print("MODEL_SCOPE: parallelogram/rhombus side faces; all nine prism edge lengths equal 1.")

if __name__ == "__main__":
    main()
