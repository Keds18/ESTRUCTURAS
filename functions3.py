import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import streamlit as st

# Calculo de reacciones por carga puntual
def ReaccionPuntual(Long, CP):
    R1 = CP[0] * (Long - CP[1]) / Long
    R2 = CP[0] * CP[1] / Long
    return R1, R2

# Diagrama de momento flector por carga puntual
def DMFPuntual(Long, CP, Paso=0.1):
    R1, _ = ReaccionPuntual(Long, CP)
    x = np.linspace(0, Long, int(Long / Paso) + 1)
    DMF = []
    for xi in x:
        if xi < CP[1]:
            M = -R1 * xi
        else:
            M = -(R1 * xi - CP[0] * (xi - CP[1]))
        DMF.append(M)
    return np.array(DMF)

# Diagrama de fuerza cortante por carga puntual
def DFCPuntual(Long, CP, Paso=0.1):
    R1, _ = ReaccionPuntual(Long, CP)
    x = np.linspace(0, Long, int(Long / Paso) + 1)
    DFC = []
    for xi in x:
        if xi < CP[1]:
            F = R1
        else:
            F = R1 - CP[0]
        DFC.append(F)
    return np.array(DFC)

# Calculo de reacciones por carga distribuida
def ReaccionDistribuida(Long, CD):
    L = CD[2] - CD[1]  # Longitud de la carga
    C = CD[0] * L      # Carga total
    X = CD[1] + L / 2  # Centroide
    R1 = C * (Long - X) / Long
    R2 = C * X / Long
    return R1, R2

# Diagrama de momento flector por carga distribuida
def DMFDistribuida(Long, CD, Paso=0.1):
    R1, _ = ReaccionDistribuida(Long, CD)
    L = CD[2] - CD[1]
    x = np.linspace(0, Long, int(Long / Paso) + 1)
    DMF = []
    for xi in x:
        if xi < CD[1]:
            M = R1 * xi
        elif xi <= CD[2]:
            a = xi - CD[1]
            M = R1 * xi - CD[0] * a**2 / 2
        else:
            M = R1 * xi - CD[0] * L * (xi - CD[1] - L / 2)
        DMF.append(-M)  # Invertido para convención negativa
    return np.array(DMF)

# Diagrama de fuerza cortante por carga distribuida
def DFCDistribuida(Long, CD, Paso=0.1):
    R1, _ = ReaccionDistribuida(Long, CD)
    L = CD[2] - CD[1]
    x = np.linspace(0, Long, int(Long / Paso) + 1)
    DFC = []
    for xi in x:
        if xi < CD[1]:
            F = R1
        elif xi <= CD[2]:
            F = R1 - CD[0] * (xi - CD[1])
        else:
            F = R1 - CD[0] * L
        DFC.append(F)
    return np.array(DFC)

# Función para graficar los diagramas
def Grafica(long, posicion, momento, cortante):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.2, 
                        subplot_titles=('Diagrama de Momento Flector (DMF)', 'Diagrama de Fuerza Cortante (DFC)'))

    # Modo oscuro
    bg_color = "#1e1e1e"
    grid_color = "#444"
    text_color = "#ffffff"

    # Momento flector
    fig.add_trace(go.Scatter(x=posicion, y=momento, mode='lines', fill='tozeroy',
                             line=dict(color='#ff4500'), name='Momento Flector'), row=1, col=1)
    fig.add_trace(go.Scatter(x=[0, long], y=[0, 0], mode='lines',
                             line=dict(color='#800080', width=8), name='Viga'), row=1, col=1)

    # Fuerza cortante
    fig.add_trace(go.Scatter(x=posicion, y=cortante, mode='lines', fill='tozeroy',
                             line=dict(color='#00bfff'), name='Fuerza Cortante'), row=2, col=1)
    fig.add_trace(go.Scatter(x=[0, long], y=[0, 0], mode='lines',
                             line=dict(color='#800080', width=8), name='Viga'), row=2, col=1)

    fig.update_layout(height=600, width=800, showlegend=False,
                      paper_bgcolor=bg_color, plot_bgcolor=bg_color,
                      font=dict(color=text_color),
                      xaxis_title='Longitud de la viga (m)',
                      xaxis2_title='Longitud de la viga (m)',
                      yaxis_title='Momento flector (Ton·m)',
                      yaxis2_title='Fuerza cortante (Ton)',
                      xaxis=dict(gridcolor=grid_color),
                      xaxis2=dict(gridcolor=grid_color),
                      yaxis=dict(gridcolor=grid_color),
                      yaxis2=dict(gridcolor=grid_color))

    st.plotly_chart(fig)

# Función para obtener diagramas globales sumados
def Global(long, paso, esfuerzos):
    DMF = np.zeros(int(long / paso) + 1)
    DFC = np.zeros(int(long / paso) + 1)
    for mf in esfuerzos:
        DMF += mf[0]
        DFC += mf[1]
    return DMF, DFC
