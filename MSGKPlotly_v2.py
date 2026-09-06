"""
Geometryczna architektura ekosystemu GIA-TIMDR -- szkic poglądowy.

UWAGA (poprawki względem pierwszej wersji, MSGKPlotly.py):
1. Gałęzie M/S, G, K rysowane są teraz w OSOBNYCH scenach 3D (osobne
   układy współrzędnych), nie we wspólnej przestrzeni Y/Z. Chronoproces
   Ξ=(T,x,Γ,φ) definiuje TRZY NIEZALEŻNE rzuty z jednego nośnika T, bez
   współdzielonej geometrii stanu -- jedyny dopuszczony wyjątek to most
   Fouriera M/S<->K, którego ten rysunek i tak nie przedstawia. Wspólna
   przestrzeń w oryginale sugerowała wizualnie identyfikację gałęzi,
   której formalizm wprost zabrania.
2. Powierzchnia obwiedni podpisana jest teraz jako "G8/G9 (operator
   Weingartena / skręt powierzchniowy)", nie "G10 (P/Q)". G10 to
   krzywizna KRZYWEJ obwiedni zaokrąglonego trójkąta (P=L0/L część
   prosta, Q=Lk/L część łukowa) -- zupełnie inny obiekt niż zmienny
   promień rurki 3D wzdłuż T narysowany tutaj.
3. Trójwęzeł G5 podpisany jest jako "metafora / szkic pojęciowy" --
   w aksjomacie G5 to abstrakcyjny warunek stabilności (dodatnia
   określoność macierzy M/K/Γ ⟹ brak bieguna na osi rzeczywistej), nie
   dosłowna krzywa przestrzenna do rysowania względem T.
4. Panel czwarty (złożony) jest jawnie podpisany jako "kompozyt
   ilustracyjny", żeby nie było wątpliwości, że to nie jest dosłowny
   wykres formalizmu, tylko wizualne zestawienie czterech niezależnych
   obiektów obok siebie.

Definicje M/S (anomalia >2σ, defekt jako skok ΔS) pozostają bez zmian --
zgodne z Axioms_S_TIMDR_Signal.md.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==============================================================================
# 1. NOŚNIK / CHRONOPROCES Ξ = (T, x, Γ, φ)
# ==============================================================================
t = np.linspace(0, 4 * np.pi, 500)

# ==============================================================================
# 2. GAŁĄŹ G (GEOMETRIA) -- powierzchnia obwiedni Γ(T,u), skręt/Weingarten (G8/G9)
# ==============================================================================
u = np.linspace(-1, 1, 30)
T_mesh, U_mesh = np.meshgrid(t, u)
R_envelope = 1.5 + 0.5 * np.cos(T_mesh)
X_surf = T_mesh
Y_surf = R_envelope * np.cos(T_mesh + U_mesh * 0.5)
Z_surf = R_envelope * np.sin(T_mesh + U_mesh * 0.5)

# ==============================================================================
# 3. GAŁĄŹ M/S (SYGNAŁY CZASOWE x: T -> R^d) -- trajektoria, anomalia, defekt
# ==============================================================================
x_ms = t.copy()
y_ms = 1.5 * np.cos(t)
z_ms = 1.5 * np.sin(t)

anom_idx = 120  # anomalia: > mean + 2*sigma
y_ms[anom_idx] += 1.8
z_ms[anom_idx] += 1.2

defect_idx = 280  # defekt: skok dyskretny > progu
y_ms[defect_idx:] += 0.8

# ==============================================================================
# 4. GAŁĄŹ G -- G-Rezonans G5: METAFORA trójwęzła helikalnego
#    (realny obiekt aksjomatu to predykat stabilności na macierzy M/K/Γ,
#    nie krzywa przestrzenna -- to jest wyłącznie szkic poglądowy)
# ==============================================================================
t_res = np.linspace(8.0, 11.0, 200)
r_res = 0.6
nodes_x, nodes_y, nodes_z = [], [], []
for phase_shift in [0, 2 * np.pi / 3, 4 * np.pi / 3]:
    nodes_x.extend(t_res)
    nodes_y.extend(1.8 * np.cos(t_res) + r_res * np.cos(4 * t_res + phase_shift))
    nodes_z.extend(1.8 * np.sin(t_res) + r_res * np.sin(4 * t_res + phase_shift))

# ==============================================================================
# 5. GAŁĄŹ K (MODALNOŚĆ I FAZA φ: T -> (f, φ, A)) -- wiązka fazowa
# ==============================================================================
t_k = np.linspace(1.0, 4.0, 100)
phi_k = 5 * t_k
y_k = 0.5 * np.cos(phi_k)
z_k = 0.5 * np.sin(phi_k)

# ==============================================================================
# BUDOWANIE WIZUALIZACJI -- 4 NIEZALEŻNE SCENY 3D (2x2), zamiast jednej
# wspólnej przestrzeni
# ==============================================================================
fig = make_subplots(
    rows=2,
    cols=2,
    specs=[[{"type": "scene"}, {"type": "scene"}], [{"type": "scene"}, {"type": "scene"}]],
    subplot_titles=(
        "Gałąź M/S: trajektoria x(T), anomalia, defekt",
        "Gałąź G: obwiednia Γ(T,u) -- skręt/Weingarten (G8/G9)",
        "Gałąź G: G-Rezonans G5 -- METAFORA (nie dosłowny obiekt)",
        "Gałąź K: wiązka fazowa φ(T)",
    ),
)

# Chronoproces (oś T) powtórzony w każdej scenie jako wspólny punkt odniesienia,
# NIE jako współdzielona geometria stanu
def chrono_axis(t_arr):
    return go.Scatter3d(
        x=t_arr,
        y=np.zeros_like(t_arr),
        z=np.zeros_like(t_arr),
        mode="lines",
        line=dict(color="gray", width=3, dash="dash"),
        name="Chronoproces Ξ (nośnik T)",
        showlegend=False,
    )


# Panel 1: M/S
fig.add_trace(chrono_axis(t), row=1, col=1)
fig.add_trace(
    go.Scatter3d(
        x=x_ms, y=y_ms, z=z_ms, mode="lines",
        line=dict(color="cyan", width=6), name="Trajektoria x(T)",
    ),
    row=1, col=1,
)
fig.add_trace(
    go.Scatter3d(
        x=[x_ms[anom_idx]], y=[y_ms[anom_idx]], z=[z_ms[anom_idx]],
        mode="markers", marker=dict(size=8, color="red", symbol="diamond"),
        name="Anomalia (>2σ)",
    ),
    row=1, col=1,
)
fig.add_trace(
    go.Scatter3d(
        x=[x_ms[defect_idx]], y=[y_ms[defect_idx]], z=[z_ms[defect_idx]],
        mode="markers", marker=dict(size=8, color="orange", symbol="square"),
        name="Defekt (skok ΔS)",
    ),
    row=1, col=1,
)

# Panel 2: G -- obwiednia Weingarten/skręt (G8/G9)
fig.add_trace(chrono_axis(t), row=1, col=2)
fig.add_trace(
    go.Surface(
        x=X_surf, y=Y_surf, z=Z_surf, opacity=0.6, colorscale="Viridis",
        showscale=False, name="Obwiednia Γ(T,u) [G8/G9]",
    ),
    row=1, col=2,
)

# Panel 3: G-Rezonans G5 (metafora)
fig.add_trace(chrono_axis(t_res), row=2, col=1)
fig.add_trace(
    go.Scatter3d(
        x=nodes_x, y=nodes_y, z=nodes_z, mode="markers",
        marker=dict(size=3, color="magenta"),
        name="G-Rezonans G5 -- metafora trójwęzła",
    ),
    row=2, col=1,
)

# Panel 4: K -- wiązka fazowa
fig.add_trace(chrono_axis(t_k), row=2, col=2)
fig.add_trace(
    go.Scatter3d(
        x=t_k, y=y_k, z=z_k, mode="lines",
        line=dict(color="gold", width=5), name="Wiązka fazowa φ(T)",
    ),
    row=2, col=2,
)

fig.update_layout(
    title=(
        "Geometryczna architektura ekosystemu GIA-TIMDR -- "
        "szkic poglądowy (4 niezależne gałęzie, bez wspólnej przestrzeni stanu)"
    ),
    height=900,
    width=1200,
    margin=dict(l=0, r=0, b=0, t=80),
    legend=dict(orientation="h", yanchor="bottom", y=-0.05),
)

for scene_key in ["scene", "scene2", "scene3", "scene4"]:
    fig.update_layout(
        **{
            scene_key: dict(
                xaxis_title="T",
                yaxis_title="stan (gałąź własna)",
                zaxis_title="stan (gałąź własna)",
                aspectratio=dict(x=2, y=1, z=1),
            )
        }
    )


# fig.show() bywa zawodne, gdy plotly nie ma poprawnie ustawionego
# domyślnego renderera ("browser") -- wtedy nic się nie otwiera i nie ma
# żadnego błędu. Zamiast tego: zapisz do pliku HTML obok skryptu i otwórz
# go jawnie przez system operacyjny.
import os
import webbrowser

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MSGKPlotly_v2.html")
fig.write_html(out_path)
print(f"Zapisano: {out_path}")

if os.name == "nt":
    os.startfile(out_path)
else:
    webbrowser.open("file://" + out_path)
