# Explicit reduced equations for centroid-return problem

The polynomial construction in `experiments/rhombic_prism_triangle_reduced_equations.py` eliminates the height using `w²=1-u²-v²`, cancels nonzero factors in the open disk, and reduces powers of `s` using `s²=3`, `s=+sqrt(3)`.

**Independent local SymPy verification (2026-11-13):** the resulting polynomial degrees in `u,v` are **5, 5, 4**. The three expressions below are the exact reduced equations, up to an irrelevant common nonzero scalar:

```text
4 E1 =
 15u^5 + 5sqrt(3)u^4v + 15u^4 + 21u^3v² + 3sqrt(3)u³v
 -21u³ + 7sqrt(3)u²v³ + 6u²v² - 7sqrt(3)u²v -21u²
 -6uv⁴ -sqrt(3)uv³ -3uv² +6u
 -2sqrt(3)v⁵ -v⁴ -sqrt(3)v³ -3v² +2sqrt(3)v +6

-4 E2 =
 6sqrt(3)u⁵ +33u⁴v +6sqrt(3)u⁴ +21sqrt(3)u³v² +18u³v
 -12sqrt(3)u³ +27u²v³ +15sqrt(3)u²v² -30u²v
 -12sqrt(3)u² +11sqrt(3)uv⁴ +18uv³ -18sqrt(3)uv²
 -18uv +6sqrt(3)u +6v⁵ +5sqrt(3)v⁴ -12v³
 -12sqrt(3)v² +6v +6sqrt(3)

-4 E3 =
 15u⁴ -sqrt(3)u³v -6u³ -27u²v² +3sqrt(3)u²v
 -6u² -13sqrt(3)uv³ +6uv² +4sqrt(3)uv +6u
 -6v⁴ +3sqrt(3)v³ +6v² -6sqrt(3)v
```

The physical zero set is exactly the common zero set of E1, E2, E3 within `u²+v²<1`, assuming the original three side-plane denominators are nonzero (they are positive in the nondegenerate domain).

**Scientific status:** reduction is exact. No claim is made here that the earlier three numerical candidates exhaust the roots or that a D3 symmetry orbit has been proved. A resultant/Groebner elimination and certified real-root isolation remain outstanding. The reduction concerns affine rigid motions and by itself does not imply a quantum triangle anomaly.
