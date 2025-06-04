import streamlit as st
import numpy as np
import functions3 as f
import matplotlib.pyplot as plt
import pandas as pd

# TÍTULO PRINCIPAL
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🔧 ANÁLISIS ESTRUCTURAL</h1>", unsafe_allow_html=True)
st.markdown("## 📈 Diagramas de momentos y fuerzas cortantes", unsafe_allow_html=True)

# SECCIÓN 1: DATOS
st.markdown("---")
st.markdown("### 📌 1. Datos de entrada", unsafe_allow_html=True)
# Entrada de datos
Long = st.slider("📏 Longitud de la viga (m)", 1, 30, 1, 1)
Paso = st.slider("🔢 Paso para los cálculos (m)", 0.1, 1.0, 0.1, 0.1)

# LOGICA INTERNA DE LA APLICACION
# Inicialización de cargas puntuales
if 'cargas_puntuales' not in st.session_state:
    st.session_state.cargas_puntuales = []
  
# Función para agregar una nueva carga puntual
def agregar_carga_puntual():
    st.session_state.cargas_puntuales.append({'peso_cp': 0.1, 'posicion_cp': 0})
  
# Función para eliminar una carga puntual
def eliminar_carga_puntual(idx):
    del st.session_state.cargas_puntuales[idx]

# SECCIÓN 2: CARGAS PUNTUALES
st.markdown("---")
st.markdown("### 🎯 2. Cargas puntuales", unsafe_allow_html=True)

# Botón para agregar una nueva carga puntual
if st.button("➕ Agregar carga puntual"):
    agregar_carga_puntual()

# Mostrar las cargas puntuales existentes en filas 
for idx, carga in enumerate(st.session_state.cargas_puntuales):
    cols = st.columns([1, 4, 4, 2])
    with cols[0]:
        st.markdown(f"<b style='color:#2980b9'>P{idx + 1}:</b>", unsafe_allow_html=True)
    with cols[1]:
        carga['peso_cp'] = st.number_input(f'⚖️ Peso {idx + 1} (Ton)', min_value=0.1, step=0.1, key=f'peso_cp_{idx + 1}')
    with cols[2]:
        carga['posicion_cp'] = st.number_input(
            f'📍 Posición {idx + 1} (m)',
            min_value=0.0,
            max_value=50.0,
            step=0.5,
            key=f'posicion_cp_{idx + 1}'
        )
    with cols[3]:
        if st.button("❌ Eliminar", key=f"eliminar_cp_{idx + 1}"):
            eliminar_carga_puntual(idx)

# Inicialización de cargas distribuidas
if 'cargas_distribuidas' not in st.session_state:
    st.session_state.cargas_distribuidas = []


# Función para agregar una nueva carga distribuida
def agregar_carga_distribuida():
    st.session_state.cargas_distribuidas.append({
        'peso_cd': 0.1,
        'posicion_inicial_cd': 0,
        'posicion_final_cd': 0
    })


# Función para eliminar una carga distribuida
def eliminar_carga_distribuida(idx):
    del st.session_state.cargas_distribuidas[idx]

# SECCIÓN 3: CARGAS DISTRIBUIDAS
st.markdown("---")
st.markdown("### 🌈 3. Cargas distribuidas", unsafe_allow_html=True)

# Botón para agregar una nueva carga distribuida
if st.button("➕ Agregar carga distribuida"):
    agregar_carga_distribuida()

# Mostrar las cargas distribuidas existentes en filas
for idx, carga in enumerate(st.session_state.cargas_distribuidas):
    cols = st.columns([1, 4, 4, 4, 3])
    with cols[0]:
        st.markdown(f"<b style='color:#16a085'>q{idx + 1}:</b>", unsafe_allow_html=True)
    with cols[1]:
        carga['peso_cd'] = st.number_input(f'⚖️ Peso {idx + 1} (Ton/m)', min_value=0.1, step=0.1, key=f'peso_cd_{idx + 1}')
    with cols[2]:
        carga['posicion_inicial_cd'] = st.number_input(
            f'🚩 Inicio {idx + 1} (m)',
            min_value=0.0,
            max_value=50.0,
            step=0.5,
            key=f'posicion_inicial_cd_{idx + 1}'
        )
    with cols[3]:
        carga['posicion_final_cd'] = st.number_input(
            f'🏁 Fin {idx + 1} (m)',
            min_value=0.0,
            max_value=50.0,
            step=0.5,
            key=f'posicion_final_cd_{idx + 1}'
        )
    with cols[4]:
        if st.button("❌ Eliminar", key=f"eliminar_cd_{idx + 1}"):
            eliminar_carga_distribuida(idx)

# SECCIÓN 4: RESULTADOS
st.markdown("---")
st.markdown("### 📊 4. Resultados", unsafe_allow_html=True)

# Selección de carga para mostrar el gráfico
opciones_carga = ['Grafica global', 'Cargas puntuales', 'Cargas distribuidas']
carga_seleccionada = st.selectbox("📌 Selecciona el tipo de carga para graficar", opciones_carga)
# Crear una lista de etiquetas como "Peso 1", "Peso 2", etc.
if carga_seleccionada == 'Cargas puntuales':
    opciones_puntuales = [f"Peso {idx + 1}" for idx in range(len(st.session_state.cargas_puntuales))]
    if opciones_puntuales:
        carga_puntual = st.selectbox("🎯 Selecciona una carga puntual", opciones_puntuales)
        if carga_puntual:
            idx_carga = opciones_puntuales.index(carga_puntual)
            carga = st.session_state.cargas_puntuales[idx_carga]
            CP = [carga['peso_cp'], carga['posicion_cp']]
            dmf1 = f.DMFPuntual(Long, CP, Paso)
            dfc1 = f.DFCPuntual(Long, CP, Paso)
            f.Grafica(Long, np.linspace(0, Long, int(Long / Paso) + 1), dmf1, dfc1)

elif carga_seleccionada == 'Cargas distribuidas':
    opciones_distribuidas = [f"Peso {idx + 1}" for idx in range(len(st.session_state.cargas_distribuidas))]
    if opciones_distribuidas:
        carga_distribuida = st.selectbox("🌈 Selecciona una carga distribuida", opciones_distribuidas)
        if carga_distribuida:
            idx_carga = opciones_distribuidas.index(carga_distribuida)
            carga = st.session_state.cargas_distribuidas[idx_carga]
            CD = [carga['peso_cd'], carga['posicion_inicial_cd'], carga['posicion_final_cd']]
            dmf3 = f.DMFDistribuida(Long, CD, Paso)
            dfc3 = f.DFCDistribuida(Long, CD, Paso)
            f.Grafica(Long, np.linspace(0, Long, int(Long / Paso) + 1), dmf3, dfc3)

# BOTÓN FINAL
if st.button("📊 Generar gráfico general y tabla"):
    esfuerzos = []
    # Cálculo de DMF y DFC para cada carga puntual
    for carga in st.session_state.cargas_puntuales:
        CP = [carga['peso_cp'], carga['posicion_cp']]
        dmf1 = f.DMFPuntual(Long, CP, Paso)
        dfc1 = f.DFCPuntual(Long, CP, Paso)
        esfuerzos.append([dmf1, dfc1])
    
    # Cálculo de DMF y DFC para cada carga distribuida
    for carga in st.session_state.cargas_distribuidas:
        CD = [carga['peso_cd'], carga['posicion_inicial_cd'], carga['posicion_final_cd']]
        dmf3 = f.DMFDistribuida(Long, CD, Paso)
        dfc3 = f.DFCDistribuida(Long, CD, Paso)
        esfuerzos.append([dmf3, dfc3])
    
    # Calcular los diagramas globales sumados
    DMF, DFC = f.Global(Long, Paso, esfuerzos)
    
    # Crear un array para las posiciones (x)
    x = np.linspace(0, Long, int(Long / Paso) + 1)
    
    # Crear el DataFrame para mostrar los resultados
    df = pd.DataFrame({
        'x': x,
        'DMF-Global': DMF,
        'DFC-Global': DFC
    })
    
    # Añadir las columnas para los diagramas individuales
    for i, carga in enumerate(st.session_state.cargas_puntuales):
        CP = [carga['peso_cp'], carga['posicion_cp']]
        dmf = f.DMFPuntual(Long, CP, Paso)
        dfc = f.DFCPuntual(Long, CP, Paso)
        df[f'DMF{i+1}'] = dmf
        df[f'DFC{i+1}'] = dfc
    
    for i, carga in enumerate(st.session_state.cargas_distribuidas):
        CD = [carga['peso_cd'], carga['posicion_inicial_cd'], carga['posicion_final_cd']]
        dmf = f.DMFDistribuida(Long, CD, Paso)
        dfc = f.DFCDistribuida(Long, CD, Paso)
        df[f'DMF{len(st.session_state.cargas_puntuales)+i+1}'] = dmf
        df[f'DFC{len(st.session_state.cargas_puntuales)+i+1}'] = dfc
    
    # Mostrar la tabla en Streamlit
    st.write(df)
    
    # Generar el gráfico general usando la función Grafica
    f.Grafica(Long, x, DMF, DFC)

st.markdown("""
<hr>
<div style='text-align: center; font-size: 0.9em; color: gray;'>
    <p>© 2025 <strong>Kevin_Galindo_Antezana</strong></p>
    <p>📧 Contacto: <a href="mailto:keds1810@gmail.com">keds1810@gmail.com</a></p>
    <p>Developed with Python + Streamlit</p>
    </div>
""", unsafe_allow_html=True)

