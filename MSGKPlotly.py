import numpy as np
import plotly.graph_objects as go

# ==============================================================================
# 1. NOŚNIK / CHRONOPROCES Ξ = (T, x, Γ, φ)
# Axis T: Osia parametru ewolucji (czas / nośnik)
# ==============================================================================
t = np.linspace(0, 4 * np.pi, 500)

# ==============================================================================
# 2. GAŁĄŹ G (GEOMETRIA)
# Powierzchnia obwiedni Γ(T, u) - skręcona wstęga/rura ugięta operatorem Weingartena
# ==============================================================================
u = np.linspace(-1, 1, 30)
T_mesh, U_mesh = np.meshgrid(t, u)

# Zmienna krzywizna obwiedni (Parametr P/Q - G10)
R_envelope = 1.5 + 0.5 * np.cos(T_mesh)
X_surf = T_mesh
Y_surf = R_envelope * np.cos(T_mesh + U_mesh * 0.5)
Z_surf = R_envelope * np.sin(T_mesh + U_mesh * 0.5)

# ==============================================================================
# 3. GAŁĄŹ M/S (SYGNAŁY CZASOWE x: T -> R^d)
# Trajektoria 1D ze skrętem sygnałowym, anomalią i defektem
# ==============================================================================
# Baza trajektorii
x_ms = t
y_ms = 1.5 * np.cos(t)
z_ms = 1.5 * np.sin(t)

# Punkt 1: Anomalia (> mean + 2σ) na t ~ 3.0
anom_idx = 120
y_ms[anom_idx] += 1.8
z_ms[anom_idx] += 1.2

# Punkt 2: Defekt (skok dyskretny) na t ~ 7.0
defect_idx = 280
y_ms[defect_idx:] += 0.8

# ==============================================================================
# 4. GAŁĄŹ G (G-REZONANS G5: HELIKALNY TRÓJWĘZEŁ 3D)
# Pierścień sprzężonych oscylatorów ułożonych w potrójną helisę wokół osi T
# ==============================================================================
t_res = np.linspace(8.0, 11.0, 200)
r_res = 0.6
nodes_x, nodes_y, nodes_z = [], [], []

for phase_shift in [0, 2 * np.pi / 3, 4 * np.pi / 3]:
    nodes_x.extend(t_res)
    nodes_y.extend(1.8 * np.cos(t_res) + r_res * np.cos(4 * t_res + phase_shift))
    nodes_z.extend(1.8 * np.sin(t_res) + r_res * np.sin(4 * t_res + phase_shift))

# ==============================================================================
# 5. GAŁĄŹ K (MODALNOŚĆ I FAZA φ: T -> (f, φ, A))
# Torus / Wiązka włóknista synchronizacji fazowej między modami
# ==============================================================================
t_k = np.linspace(1.0, 4.0, 100)
phi_k = 5 * t_k
y_k = 0.5 * np.cos(phi_k)
z_k = 0.5 * np.sin(phi_k)

# ==============================================================================
# BUDOWANIE WIZUALIZACJI PLOTLY
# ==============================================================================
fig = go.Figure()

# A. Chronoproces / Osia T
fig.add_trace(
    go.Scatter3d(
        x=t,
        y=np.zeros_like(t),
        z=np.zeros_like(t),
        mode="lines",
        line=dict(color="gray", width=4, dash="dash"),
        name="Chronoproces Ξ (Nośnik T)",
    )
)

# B. Gałąź G: Powierzchnia Obwiedni (Operator Weingartena)
fig.add_trace(
    go.Surface(
        x=X_surf,
        y=Y_surf,
        z=Z_surf,
        opacity=0.25,
        colorscale="Viridis",
        showscale=False,
        name="Gałąź G: Obwiednia Γ(T,u)",
    )
)

# C. Gałąź M/S: Trajektoria sygnałowa
fig.add_trace(
    go.Scatter3d(
        x=x_ms,
        y=y_ms,
        z=z_ms,
        mode="lines",
        line=dict(color="cyan", width=6),
        name="Gałąź M/S: Trajektoria x(T)",
    )
)

# D. Zdarzenia M/S (Anomalia, Defekt)
fig.add_trace(
    go.Scatter3d(
        x=[x_ms[anom_idx]],
        y=[y_ms[anom_idx]],
        z=[z_ms[anom_idx]],
        mode="markers",
        marker=dict(size=10, color="red", symbol="diamond"),
        name="M/S: Anomalia (>2σ)",
    )
)

fig.add_trace(
    go.Scatter3d(
        x=[x_ms[defect_idx]],
        y=[y_ms[defect_idx]],
        z=[z_ms[defect_idx]],
        mode="markers",
        marker=dict(size=10, color="orange", symbol="square"),
        name="M/S: Defekt (Skok ΔS)",
    )
)

# E. Gałąź G: G-Rezonans (Trójwęzeł Helikalny G5)
fig.add_trace(
    go.Scatter3d(
        x=nodes_x,
        y=nodes_y,
        z=nodes_z,
        mode="markers",
        marker=dict(size=3, color="magenta"),
        name="Gałąź G: G-Rezonans G5 (Trójwęzeł)",
    )
)

# F. Gałąź K: Węzeł Synchronizacji Fazowej
fig.add_trace(
    go.Scatter3d(
        x=t_k,
        y=y_k,
        z=z_k,
        mode="lines",
        line=dict(color="yellow", width=5),
        name="Gałąź K: Wiązka Fazowa φ(T)",
    )
)

# ==============================================================================
# OPIS I GEOMETRIA UKŁADU
# ==============================================================================
fig.update_layout(
    title="Geometryczna Architektura Ekosystemu GIA-TIMDR",
    scene=dict(
        xaxis_title="Chronoproces T (Nośnik)",
        yaxis_title="Wymiar Stanu Y",
        zaxis_title="Wymiar Stanu Z",
        aspectratio=dict(x=2.5, y=1, z=1),
        camera=dict(eye=dict(x=1.8, y=1.2, z=0.8)),
    ),
    margin=dict(l=0, r=0, b=0, t=40),
)

fig.show()