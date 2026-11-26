import numpy as np
import plotly.graph_objects as go
from scipy.integrate import quad
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Ejercicio 11 - Difusión de Calor", layout="wide"
)

st.title("🔥 Difusión de Calor y Temperatura Promedio en Barras Metálicas")
st.markdown(
    "Aplicación interactiva basada en el **Ejercicio 11** del Proyecto Aula de Cálculo Integral."
)

# --- Panel Lateral: Controles Dinámicos ---
st.sidebar.header("Parámetros de la Barra")
a = st.sidebar.number_input(
    "Extremo izquierdo $a$ (m)", value=0.0, step=0.5, format="%.2f"
)
b = st.sidebar.number_input(
    "Extremo derecho $b$ (m)", value=5.0, step=0.5, format="%.2f"
)

if a >= b:
    st.sidebar.error("Error: El extremo 'a' debe ser menor que el extremo 'b'.")
    st.stop()

k = st.sidebar.slider(
    "Coeficiente de intensidad térmica ($k$)", 0.1, 5.0, 1.0, 0.1
)

# --- Modelo Matemático de Temperatura T(x) ---
# Usamos una distribución parabólica centrada en la mitad de la barra: T(x) = -k*(x - x_centro)^2 + 100
centro = (a + b) / 2


def T(x):
    return -k * (x - centro) ** 2 + 100


# --- Cálculo de la Integral y Temperatura Promedio ---
# Usamos scipy.integrate.quad para calcular la integral definida con alta precisión
integral_valor, _ = quad(T, a, b)
T_prom = integral_valor / (b - a)

# --- Resultados Numéricos en Pantalla ---
col1, col2, col3 = st.columns(3)
col1.metric("Longitud de la Barra ($b - a$)", f"{b - a:.2f} m")
col2.metric(
    "Integral Definida $\\int_a^b T(x)dx$", f"{integral_valor:.2f} °C·m"
)
col3.metric("Temperatura Promedio ($T_{prom}$)", f"{T_prom:.2f} °C")

st.markdown("---")

# --- Gráfica 1: Distribución de Temperatura T(x) ---
st.subheader("Gráfica de la Distribución de Calor y Área Bajo la Curva")
x_vals = np.linspace(a, b, 500)
y_vals = T(x_vals)

fig_curva = go.Figure()
# Curva de temperatura
fig_curva.add_trace(
    go.Scatter(
        x=x_vals,
        y=y_vals,
        mode="lines",
        name="T(x)",
        line=dict(color="firebrick", width=3),
    )
)
# Área sombreada bajo la curva
fig_curva.add_trace(
    go.Scatter(
        x=np.concatenate([[a], x_vals, [b]]),
        y=np.concatenate([[0], y_vals, [0]]),
        fill="tozeroy",
        fillcolor="rgba(255, 69, 0, 0.2)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Área de Calor",
    )
)
# Línea horizontal del valor promedio
fig_curva.add_hline(
    y=T_prom,
    line_dash="dash",
    line_color="blue",
    annotation_text=f"T_prom = {T_prom:.2f}°C",
    annotation_position="bottom right",
)

fig_curva.update_layout(
    xaxis_title="Posición en la Barra x (m)",
    yaxis_title="Temperatura (°C)",
    template="plotly_white",
    hovermode="x unified",
)
st.plotly_chart(fig_curva, use_container_width=True)

# --- Visualización 2: Barra Metálica con Gradiente Térmico ---
st.subheader("Representación Física de la Barra Metálica (Gradiente Térmico)")

# Generamos puntos espaciales para el gradiente de la barra
x_barra = np.linspace(a, b, 100)
t_barra = T(x_barra)

fig_barra = go.Figure(
    data=go.Heatmap(
        z=[t_barra],
        x=x_barra,
        y=["Barra"],
        colorscale="Jet",  # Azul (frío) a Rojo (caliente)
        colorbar=dict(title="Temp (°C)"),
        zmin=0,
        zmax=120,
    )
)

fig_barra.update_layout(
    yaxis=dict(showticklabels=False),
    xaxis_title="Longitud de la barra (m)",
    height=180,
    margin=dict(l=20, r=20, t=10, b=30),
    template="plotly_white",
)
st.plotly_chart(fig_barra, use_container_width=True)