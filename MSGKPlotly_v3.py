"""
Geometryczna architektura ekosystemu GIA-TIMDR -- szkic poglądowy, v3.

Poprawki względem v2 (na podstawie dalszej weryfikacji):
1. Zero-identyfikacja gałęzi: M/S, G (G8/G9), G5 i K mają teraz OSOBNE
   sceny/panele -- nie dzielą osi stanu. Wspólny jest tylko nośnik T.
2. G10 jest teraz pokazane OSOBNO i POPRAWNIE jako to, czym faktycznie
   jest w aksjomacie: krzywizna KRZYWEJ obwiedni zaokrąglonego trójkąta
   (P=L0/L część prosta, Q=Lk/L część łukowa), NIE deformacja
   powierzchni 3D. Panel obwiedni Weingartena (G8/G9) jest osobno i
   poprawnie podpisany, bez odniesienia do G10.
3. G5 (trójwęzeł) jest jawnie podpisane jako "szkic pojęciowy" -- w
   aksjomacie to warunek stabilności macierzy oscylatorów (dodatnia
   określoność M/K/Γ), nie krzywa do rysowania względem T.
4. Geometria G10 zweryfikowana numerycznie: fillet trójkąta 3-4-5
   (r_in=1 dokładnie) obliczony analitycznie (L0(R)=perim-2R*Σcot(θ/2),
   Lk(R)=2πR) ORAZ niezależnie przez shapely.buffer -- zgodność do 4
   miejsc po przecinku dla R∈{0, 0.3, 0.6, 0.9, 0.999}. Przy R→r_in,
   L0→0 i Q→1, dokładnie jak w aksjomacie ("R_max=r_in dla każdego
   trójkąta, Q→1 zawsze osiągalne").

Definicje M/S (anomalia >2σ, defekt jako skok ΔS) bez zmian -- zgodne
z Axioms_S_TIMDR_Signal.md.
"""

import os
import webbrowser

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==============================================================================
# 1. NOŚNIK / CHRONOPROCES Ξ = (T, x, Γ, φ)
# ==============================================================================
t = np.linspace(0, 4 * np.pi, 500)


def chrono_axis(t_arr):
    return go.Scatter3d(
        x=t_arr, y=np.zeros_like(t_arr), z=np.zeros_like(t_arr),
        mode="lines", line=dict(color="gray", width=3, dash="dash"),
        name="Chronoproces Ξ (nośnik T)", showlegend=False,
    )


# ==============================================================================
# 2. GAŁĄŹ G -- obwiednia Γ(T,u): skręt powierzchniowy / Weingarten (G8/G9)
#    (NIE G10 -- to inny obiekt, patrz sekcja 5 niżej)
# ==============================================================================
u = np.linspace(-1, 1, 30)
T_mesh, U_mesh = np.meshgrid(t, u)
R_envelope = 1.5 + 0.5 * np.cos(T_mesh)
X_surf = T_mesh
Y_surf = R_envelope * np.cos(T_mesh + U_mesh * 0.5)
Z_surf = R_envelope * np.sin(T_mesh + U_mesh * 0.5)

# ==============================================================================
# 3. GAŁĄŹ M/S (x: T -> R^d) -- trajektoria, anomalia (>2σ), defekt (skok ΔS)
# ==============================================================================
x_ms = t.copy()
y_ms = 1.5 * np.cos(t)
z_ms = 1.5 * np.sin(t)
anom_idx = 120
y_ms[anom_idx] += 1.8
z_ms[anom_idx] += 1.2
defect_idx = 280
y_ms[defect_idx:] += 0.8

# ==============================================================================
# 4. GAŁĄŹ G -- G-Rezonans G5: SZKIC POJĘCIOWY (nie obiekt formalny)
#    Realny obiekt aksjomatu: predykat stabilności na macierzy M/K/Γ.
# ==============================================================================
t_res = np.linspace(8.0, 11.0, 200)
r_res = 0.6
nodes_x, nodes_y, nodes_z = [], [], []
for phase_shift in [0, 2 * np.pi / 3, 4 * np.pi / 3]:
    nodes_x.extend(t_res)
    nodes_y.extend(1.8 * np.cos(t_res) + r_res * np.cos(4 * t_res + phase_shift))
    nodes_z.extend(1.8 * np.sin(t_res) + r_res * np.sin(4 * t_res + phase_shift))

# ==============================================================================
# 5. GAŁĄŹ K -- wiązka fazowa φ(T)
# ==============================================================================
t_k = np.linspace(1.0, 4.0, 100)
phi_k = 5 * t_k
y_k = 0.5 * np.cos(phi_k)
z_k = 0.5 * np.sin(phi_k)

# ==============================================================================
# 6. G10 -- krzywizna obwiedni zaokrąglonego trójkąta (P=L0/L, Q=Lk/L)
#    Zweryfikowane numerycznie (patrz docstring) niezależnie przez shapely.
# ==============================================================================
TRI = [(0.0, 0.0), (4.0, 0.0), (0.0, 3.0)]  # trojkat 3-4-5, r_in = 1 dokladnie


def triangle_r_in(V):
    a = np.hypot(*(np.array(V[1]) - np.array(V[2])))
    b = np.hypot(*(np.array(V[0]) - np.array(V[2])))
    c = np.hypot(*(np.array(V[0]) - np.array(V[1])))
    s = (a + b + c) / 2
    area = 0.5 * abs(
        (V[1][0] - V[0][0]) * (V[2][1] - V[0][1]) - (V[2][0] - V[0][0]) * (V[1][1] - V[0][1])
    )
    return area / s, a + b + c


def interior_angles(V):
    angs = []
    n = len(V)
    for i in range(n):
        p, c_, nx = np.array(V[(i - 1) % n]), np.array(V[i]), np.array(V[(i + 1) % n])
        u1, u2 = p - c_, nx - c_
        u1, u2 = u1 / np.linalg.norm(u1), u2 / np.linalg.norm(u2)
        angs.append(np.arccos(np.clip(np.dot(u1, u2), -1, 1)))
    return angs


def rounded_triangle_path(V, R, n_arc=60):
    """Dokladna sciezka obwiedni zaokraglonej (fillet) -- czysty numpy,
    zweryfikowane przeciwko shapely.buffer(-R).buffer(R) (zgodnosc do 4
    miejsc po przecinku dlugosci obwodu)."""
    pts = []
    n = len(V)
    for i in range(n):
        prev_v, cur_v, next_v = np.array(V[(i - 1) % n]), np.array(V[i]), np.array(V[(i + 1) % n])
        u1 = (prev_v - cur_v); u1 /= np.linalg.norm(u1)
        u2 = (next_v - cur_v); u2 /= np.linalg.norm(u2)
        theta = np.arccos(np.clip(np.dot(u1, u2), -1, 1))
        d = R / np.tan(theta / 2)
        T1, T2 = cur_v + d * u1, cur_v + d * u2
        bis = (u1 + u2); bis /= np.linalg.norm(bis)
        Oc = cur_v + (R / np.sin(theta / 2)) * bis
        a1 = np.arctan2(T1[1] - Oc[1], T1[0] - Oc[0])
        a2 = np.arctan2(T2[1] - Oc[1], T2[0] - Oc[0])
        diff = (a2 - a1 + np.pi) % (2 * np.pi) - np.pi
        angs = np.linspace(a1, a1 + diff, n_arc)
        pts.append(np.stack([Oc[0] + R * np.cos(angs), Oc[1] + R * np.sin(angs)], axis=1))
    path = np.concatenate(pts, axis=0)
    return np.vstack([path, path[0]])


r_in, perim = triangle_r_in(TRI)
angles = interior_angles(TRI)


def L0_of_R(R):
    return perim - 2 * R * sum(1 / np.tan(a / 2) for a in angles)


def Lk_of_R(R):
    return 2 * np.pi * R


R_curve = np.linspace(0.0, r_in * 0.999, 200)
L0_curve = np.array([L0_of_R(R) for R in R_curve])
Lk_curve = Lk_of_R(R_curve)
L_curve = L0_curve + Lk_curve
P_curve = L0_curve / L_curve
Q_curve = Lk_curve / L_curve

R_shapes = [0.0001, 0.5 * r_in, 0.9 * r_in]
shape_colors = ["#888888", "#1f77b4", "#d62728"]

# ==============================================================================
# BUDOWANIE WIZUALIZACJI -- 2x3: 4 sceny 3D (M/S, G8/G9, G5-metafora, K)
# + 2 panele xy dla G10 (osobno, poprawnie)
# ==============================================================================
fig = make_subplots(
    rows=2,
    cols=3,
    specs=[
        [{"type": "scene"}, {"type": "scene"}, {"type": "scene"}],
        [{"type": "scene"}, {"type": "xy"}, {"type": "xy"}],
    ],
    subplot_titles=(
        "M/S: trajektoria x(T), anomalia, defekt",
        "G: obwiednia Γ(T,u) -- skręt/Weingarten (G8/G9)",
        "G5: G-Rezonans -- SZKIC POJĘCIOWY (nie obiekt formalny)",
        "K: wiązka fazowa φ(T)",
        "G10: trójkąt i jego zaokrąglona obwiednia",
        "G10: P(R) i Q(R) -- monotoniczne, Q→1 przy R→r_in",
    ),
    horizontal_spacing=0.06,
    vertical_spacing=0.1,
)

# Panel 1: M/S
fig.add_trace(chrono_axis(t), row=1, col=1)
fig.add_trace(go.Scatter3d(x=x_ms, y=y_ms, z=z_ms, mode="lines",
                            line=dict(color="cyan", width=6), name="Trajektoria x(T)"), row=1, col=1)
fig.add_trace(go.Scatter3d(x=[x_ms[anom_idx]], y=[y_ms[anom_idx]], z=[z_ms[anom_idx]],
                            mode="markers", marker=dict(size=8, color="red", symbol="diamond"),
                            name="Anomalia (>2σ)"), row=1, col=1)
fig.add_trace(go.Scatter3d(x=[x_ms[defect_idx]], y=[y_ms[defect_idx]], z=[z_ms[defect_idx]],
                            mode="markers", marker=dict(size=8, color="orange", symbol="square"),
                            name="Defekt (skok ΔS)"), row=1, col=1)

# Panel 2: G -- G8/G9
fig.add_trace(chrono_axis(t), row=1, col=2)
fig.add_trace(go.Surface(x=X_surf, y=Y_surf, z=Z_surf, opacity=0.6, colorscale="Viridis",
                          showscale=False, name="Obwiednia Γ(T,u) [G8/G9]"), row=1, col=2)

# Panel 3: G5 -- metafora
fig.add_trace(chrono_axis(t_res), row=1, col=3)
fig.add_trace(go.Scatter3d(x=nodes_x, y=nodes_y, z=nodes_z, mode="markers",
                            marker=dict(size=3, color="magenta"),
                            name="G5 -- szkic (trójwęzeł, metafora)"), row=1, col=3)

# Panel 4: K
fig.add_trace(chrono_axis(t_k), row=2, col=1)
fig.add_trace(go.Scatter3d(x=t_k, y=y_k, z=z_k, mode="lines",
                            line=dict(color="gold", width=5), name="Wiązka fazowa φ(T)"), row=2, col=1)

# Panel 5: G10 -- ksztalt (trojkat + obwiednie przy kilku R)
tri_closed = TRI + [TRI[0]]
fig.add_trace(go.Scatter(x=[p[0] for p in tri_closed], y=[p[1] for p in tri_closed],
                          mode="lines", line=dict(color="black", width=1, dash="dot"),
                          name="trójkąt bazowy (R=0)"), row=2, col=2)
for R, col in zip(R_shapes, shape_colors):
    path = rounded_triangle_path(TRI, R)
    fig.add_trace(go.Scatter(x=path[:, 0], y=path[:, 1], mode="lines",
                              line=dict(color=col, width=3),
                              name=f"R={R/r_in:.2f}·r_in"), row=2, col=2)
fig.update_xaxes(scaleanchor="y5", scaleratio=1, row=2, col=2)

# Panel 6: G10 -- P(R)/Q(R)
fig.add_trace(go.Scatter(x=R_curve / r_in, y=P_curve, mode="lines",
                          line=dict(color="#1f77b4", width=3), name="P(R)=L0/L"), row=2, col=3)
fig.add_trace(go.Scatter(x=R_curve / r_in, y=Q_curve, mode="lines",
                          line=dict(color="#d62728", width=3), name="Q(R)=Lk/L"), row=2, col=3)
for R, col in zip(R_shapes, shape_colors):
    Pv = L0_of_R(R) / (L0_of_R(R) + Lk_of_R(R))
    fig.add_trace(go.Scatter(x=[R / r_in], y=[Pv], mode="markers",
                              marker=dict(size=9, color=col), showlegend=False), row=2, col=3)
fig.update_xaxes(title_text="R / r_in", row=2, col=3)
fig.update_yaxes(title_text="P, Q", row=2, col=3)

fig.update_layout(
    title=(
        "Geometryczna architektura ekosystemu GIA-TIMDR -- szkic poglądowy "
        "(gałęzie rozdzielone, G10 pokazane osobno i poprawnie)"
    ),
    height=1000,
    width=1500,
    margin=dict(l=0, r=0, b=0, t=90),
    legend=dict(orientation="h", yanchor="bottom", y=-0.05),
)

for scene_key in ["scene", "scene2", "scene3", "scene4"]:
    fig.update_layout(**{scene_key: dict(
        xaxis_title="T", yaxis_title="stan (gałąź własna)", zaxis_title="stan (gałąź własna)",
        aspectratio=dict(x=2, y=1, z=1),
    )})

# fig.show() bywa zawodne bez poprawnie ustawionego domyślnego renderera
# ("browser") -- zapisz do HTML i otwórz jawnie przez system operacyjny.
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MSGKPlotly_v3.html")
fig.write_html(out_path)
print(f"Zapisano: {out_path}")
if os.name == "nt":
    os.startfile(out_path)
else:
    webbrowser.open("file://" + out_path)
