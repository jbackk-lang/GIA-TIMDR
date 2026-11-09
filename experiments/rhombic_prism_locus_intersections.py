"""Intersection map of the 12 pairwise Coxeter loci for the rhombic prism.

Coordinates: U=u, X=sqrt(3)*v. The exact defining polynomials have rational
coefficients in (U,X). Resultants isolate candidate intersections; numerical
back-substitution filters real points in the open configuration disk.
The high-multiplicity center and six triple points are verified exactly.
"""
from collections import Counter
from itertools import combinations
import sympy as s

from rhombic_prism_mobility_screw_coupling import length_four_spectrum

U, X = s.symbols("U X", real=True)

# Each polynomial is zero exactly when the indicated pair of face planes
# meets at the Coxeter angle pi/m, m=2 or m=3.
LOCI = {
    "T-S1:m2": X,
    "T-S2:m2": 3*U + X,
    "T-S3:m2": 3*U - X,
    "T-S1:m3": 3*U**2 + 4*X**2 - 3,
    "T-S2:m3": 39*U**2 + 18*U*X + 7*X**2 - 12,
    "T-S3:m3": 39*U**2 - 18*U*X + 7*X**2 - 12,
    "S1-S2:m2": U**2 - U*X - 1,
    "S1-S3:m2": U**2 + U*X - 1,
    "S2-S3:m2": U**2 - X**2 + 2,
    "S1-S2:m3": 3*U**4 - 6*U**3*X + 3*U**2*X**2 - 3*U**2 + 6*U*X + X**2,
    "S1-S3:m3": 3*U**4 + 6*U**3*X + 3*U**2*X**2 - 3*U**2 - 6*U*X + X**2,
    "S2-S3:m3": 3*U**4 - 6*U**2*X**2 + 24*U**2 + 3*X**4 - 8*X**2,
}
POLYS = {name: s.Poly(expr, U, X, domain="QQ") for name, expr in LOCI.items()}

def in_disk(U0, X0):
    # u^2+v^2<1 and v=X/sqrt(3)
    return U0*U0 + X0*X0/3 < 1 - 1e-9

def numeric_intersections():
    """Resultant-based scan; returns isolated real intersections in the open disk."""
    points = []
    for (name_a, poly_a), (name_b, poly_b) in combinations(POLYS.items(), 2):
        resultant = s.resultant(poly_a.as_expr(), poly_b.as_expr(), X)
        if resultant == 0:
            continue
        resultant_poly = s.Poly(resultant, U, domain="QQ")
        intervals = s.polys.polytools.intervals(
            resultant_poly, eps=s.Rational(1, 10**10)
        )
        for ((lo, hi), _multiplicity) in intervals:
            u0 = float((lo + hi)/2)
            try:
                x_roots = s.nroots(
                    s.Poly(poly_a.as_expr().subs(U, u0), X),
                    n=35, maxsteps=150
                )
            except (s.PolynomialError, ValueError):
                continue
            for root in x_roots:
                if abs(float(s.im(root))) > 1e-8:
                    continue
                x0 = float(s.re(root))
                if not in_disk(u0, x0):
                    continue
                try:
                    refined = s.nsolve(
                        [poly_a.as_expr(), poly_b.as_expr()], [U, X],
                        [u0, x0], tol=1e-24, maxsteps=80, prec=40
                    )
                    u1, x1 = float(refined[0]), float(refined[1])
                except (ValueError, ZeroDivisionError):
                    continue
                if not in_disk(u1, x1):
                    continue
                if max(abs(float(poly_a.as_expr().subs({U:u1, X:x1}))),
                       abs(float(poly_b.as_expr().subs({U:u1, X:x1})))) > 1e-6:
                    continue
                if not any((u1-a)**2 + (x1-b)**2 < 1e-10 for a,b in points):
                    points.append((u1, x1))
    return points

def active_loci(u0, x0, tol=1e-6):
    return [
        name for name, poly in POLYS.items()
        if abs(float(poly.as_expr().subs({U:u0, X:x0}))) < tol
    ]

def exact_high_order_checks():
    # Central configuration: all three end/side pairs are m=2 and all
    # three side/side pairs are m=3.
    center = active_loci(0, 0, tol=0)
    assert len(center) == 6

    # Six exact triple intersections, all at horizontal radius 2/sqrt(13).
    triple_points = [
        ( 2/s.sqrt(13), 0),
        (-2/s.sqrt(13), 0),
        ( 1/s.sqrt(13),  3/s.sqrt(13)),
        ( 1/s.sqrt(13), -3/s.sqrt(13)),
        (-1/s.sqrt(13),  3/s.sqrt(13)),
        (-1/s.sqrt(13), -3/s.sqrt(13)),
    ]
    for uu, xx in triple_points:
        active = [
            name for name, poly in POLYS.items()
            if s.simplify(poly.as_expr().subs({U:uu, X:xx})) == 0
        ]
        assert len(active) == 3, (uu, xx, active)

    # Validate the exact special configurations against the corrected
    # affine reflection generators, not planes forced through the origin.
    c0 = length_four_spectrum(0.0, 0.0)
    assert c0["distinct_maps"] == 65
    for uu, xx in triple_points:
        result = length_four_spectrum(float(s.N(uu)), float(s.N(xx/s.sqrt(3))))
        assert result["distinct_maps"] == 213
    generic = length_four_spectrum(0.31, 0.17)
    assert generic["distinct_maps"] == 320
    return len(center), len(triple_points), c0, generic

def main():
    center_count, triple_count, center_spectrum, generic_spectrum = exact_high_order_checks()
    points = numeric_intersections()
    multiplicities = Counter(len(active_loci(uu, xx)) for uu, xx in points)
    print("PASS: all 12 Coxeter-locus equations are exact rational polynomials in (u,sqrt(3)*v).")
    print(f"isolated_real_intersections_in_open_disk={len(points)}")
    print(f"intersection_multiplicity_counts={dict(sorted(multiplicities.items()))}")
    print(f"central_configuration_active_loci={center_count}")
    print(f"triple_intersection_points={triple_count}")
    print(f"center_length4_spectrum={center_spectrum['distinct_maps']}")
    print(f"generic_length4_spectrum={generic_spectrum['distinct_maps']}")
    print("triple_point_exact_coordinates: (u,X)=(±2/sqrt(13),0),(±1/sqrt(13),±3/sqrt(13))")
    print("NOTE: the total intersection count is a resultant/numerical-isolation scan; exact proof is asserted for the central and six triple points.")

if __name__ == "__main__":
    main()
