import streamlit as st   # Para crear aplicaciones web
import numpy as np       # Manejo de arreglos y funciones matemáticas
import functions3 as f    # Funcion personalizadaa creada para cálculos y gráficos 
import matplotlib.pyplot as plt  # Para crear gráficos
import pandas as pd      # Para manejar datos en forma de tablas (DataFrames)

# Configuración de Streamlit
#st.title("ANÁLISIS ESTRUCTUAL")  # Título de la aplicación (Aparece en la izqueirda)
st.markdown("<h1 style='text-align: center;'>ANÁLISIS ESTRUCTURAL</h1>", unsafe_allow_html=True)
st.markdown("## DIAGRAMAS DE MOMENTOS Y FUERZAS CORTANTES")  # Subtítulo de la aplicación
st.header("1.Datos")  # Encabezado para la sección de datos
                    # Si tenemos otro subtitulo colocamos: st.subheader("Viga")
# Entrada de datos
Long = st.slider("Longitud de la viga (m)", 1, 30, 1, 1) # slider se usa generar una barra de desplazamiento.NOmbre, parametro minimo, maximo, valor minimo por defecto q aparece, step(saltos de avance)
Paso = st.slider("Paso para los cálculos (m)", 0.1, 1.0, 0.1, 0.1) # Le damos un rango de valores para el paso, el valor por defecto es 0.1 y el paso es 0.1

# LOGICA INTERNA DE LA APLICACION
# Inicializar la lista de cargas puntuales si no existe en el estado de sesión
if 'cargas_puntuales' not in st.session_state: # Verifica si la lista de cargas puntuales ya existe en el estado de sesión, para q se guarde la info luego de recargar la pagina
    st.session_state.cargas_puntuales = []  # Si no existe, la inicializa como una lista vacía

# Función para agregar una nueva carga puntual
def agregar_carga_puntual():       # Se define una función para agregar una carga puntual
    st.session_state.cargas_puntuales.append({'peso_cp': 0.1, 'posicion_cp': 0}) # Se agrega un diccionario con valores por defecto a la lista de cargas puntuales
                                                                               # append, p agregar 2 atributos:peso_cp=1 q sera el minimo valor y posicion_cp=0
# Función para eliminar una carga puntual
def eliminar_carga_puntual(idx):   # Se define una función para eliminar una carga puntual
    del st.session_state.cargas_puntuales[idx] # Se elimina el elemento en la posición idx de la lista de cargas puntuales









# Título
st.header("2.Cargas puntuales")  # H2_Encabezado para la sección de cargas puntuales

# Botón para agregar una nueva carga puntual
if st.button("Agregar carga puntual"): # Si se presiona el botón "Agregar carga puntual", se llama a la función para agregar una carga puntual
    agregar_carga_puntual()            # Se agrega una nueva carga puntual a la lista de cargas puntuales

# Mostrar las cargas puntuales existentes en filas 
for idx, carga in enumerate(st.session_state.cargas_puntuales): # Se itera sobre la lista de cargas puntuales y se enumeran para mostrar cada carga en una fila
    # Se definen las columnas para cada fila usando st.columns, donde cada número representa el ancho relativo de la columna
    cols = st.columns([1, 4, 4, 2])  # Definir las columnas para cada fila, tengo 4 columnas, la primera es para el nombre de la carga, la segunda para el peso, la tercera para la posición y la cuarta para eliminar
    with cols[0]:                # Se utiliza el contexto de la columna para mostrar el nombre de la carga
        st.write(f"P{idx + 1}:") # Se muestra el número de la carga (P1, P2, etc.)
    with cols[1]:                # Se utiliza el contexto de la columna para mostrar el peso de la carga
        carga['peso_cp'] = st.number_input(f'Peso {idx + 1} (Ton)', min_value=0.1, step=0.1, key=f'peso_cp_{idx + 1}') # Se utiliza number_input para permitir la entrada de un número, con un valor mínimo de 1 y un paso de 1
    with cols[2]:  # Columna para la posición de la carga
        carga['posicion_cp'] = st.number_input(
        f'Posición {idx + 1} (m)',
        min_value=0.0,
        max_value=50.0,
        step=0.5,
        key=f'posicion_cp_{idx + 1}'
    )
    with cols[3]:                # Se utiliza el contexto de la columna para mostrar el botón de eliminar
        if st.button(f"Eliminar", key=f"eliminar_cp_{idx + 1}"): # Si se presiona el botón "Eliminar", se llama a la función para eliminar la carga puntual
            eliminar_carga_puntual(idx)  # Se elimina la carga puntual en la posición idx de la lista de cargas puntuales









# Inicializar la lista de cargas distribuidas si no existe en el estado de sesión
if 'cargas_distribuidas' not in st.session_state: # Verifica si la lista de cargas distribuidas ya existe en el estado de sesión, para q se guarde la info luego de recargar la pagina
    st.session_state.cargas_distribuidas = []     # Si no existe, la inicializa como una lista vacía

# Función para agregar una nueva carga distribuida
def agregar_carga_distribuida():
    st.session_state.cargas_distribuidas.append({'peso_cd': 0.1, 'posicion_inicial_cd': 0, 'posicion_final_cd': 0}) # Se agrega un diccionario con valores por defecto a la lista de cargas distribuidas

# Función para eliminar una carga distribuida
def eliminar_carga_distribuida(idx):
    del st.session_state.cargas_distribuidas[idx]

# Título
st.header("3.Cargas distribuidas")

# Botón para agregar una nueva carga distribuida
if st.button("Agregar carga distribuida"):
    agregar_carga_distribuida()

# Mostrar las cargas distribuidas existentes en filas
for idx, carga in enumerate(st.session_state.cargas_distribuidas):
    cols = st.columns([1, 4, 4, 4, 3])  # Definir las columnas para cada fila, donde la primera es para el nombre de la carga, la segunda para el peso, la tercera para la posición inicial, la cuarta para la posición final y la quinta para eliminar
    with cols[0]:                       # ya lo dimensiona en la pantalla
        st.write(f"P{idx + 1}:")
    with cols[1]:
        carga['peso_cd'] = st.number_input(f'Peso {idx + 1} (Ton/m)', min_value=0.1, step=0.1, key=f'peso_cd_{idx + 1}')
    with cols[2]:
        carga['posicion_inicial_cd'] = st.number_input(
        f'Posición inicial {idx + 1} (m)',
        min_value=0.0,
        max_value=50.0,
        step=0.5,
        key=f'posicion_inicial_cd_{idx + 1}'
    )
    with cols[3]:
        carga['posicion_final_cd'] = st.number_input(
        f'Posición final {idx + 1} (m)',
        min_value=0.0,
        max_value=50.0,
        step=0.5,
        key=f'posicion_final_cd_{idx + 1}'
    )
    with cols[4]:
        if st.button(f"Eliminar", key=f"eliminar_cd_{idx + 1}"):
            eliminar_carga_distribuida(idx)

# Sección de resultados
st.markdown("<hr>", unsafe_allow_html=True)










st.title("4.Resultados")

# Selección de carga para mostrar el gráfico
opciones_carga = ['Grafica global', 'Cargas puntuales', 'Cargas distribuidas']
carga_seleccionada = st.selectbox("Selecciona el tipo de carga para graficar", opciones_carga)

# Mostrar el gráfico de la carga seleccionada
if carga_seleccionada == 'Cargas puntuales':
    # Crear una lista de etiquetas como "Peso 1", "Peso 2", etc.
    opciones_puntuales = [f"Peso {idx + 1}" for idx in range(len(st.session_state.cargas_puntuales))]
    
    if opciones_puntuales: ## Verifica si hay cargas puntuales disponibles
        carga_puntual = st.selectbox("Selecciona una carga puntual", opciones_puntuales)
        
        if carga_puntual:
            idx_carga = opciones_puntuales.index(carga_puntual)  # Obtener el índice de la carga seleccionada
            carga = st.session_state.cargas_puntuales[idx_carga]
            # Calcular DMF y DFC para carga puntual
            CP = [carga['peso_cp'], carga['posicion_cp']]
            dmf1 = f.DMFPuntual(Long, CP, Paso)
            dfc1 = f.DFCPuntual(Long, CP, Paso)
            
            f.Grafica(Long, np.linspace(0, Long, int(Long / Paso) + 1), dmf1, dfc1)

elif carga_seleccionada == 'Cargas distribuidas':
    # Crear una lista de etiquetas como "Peso 1", "Peso 2", etc.
    opciones_distribuidas = [f"Peso {idx + 1}" for idx in range(len(st.session_state.cargas_distribuidas))]
    
    if opciones_distribuidas:
        carga_distribuida = st.selectbox("Selecciona una carga distribuida", opciones_distribuidas)
        
        if carga_distribuida:
            idx_carga = opciones_distribuidas.index(carga_distribuida)  # Obtener el índice de la carga seleccionada
            carga = st.session_state.cargas_distribuidas[idx_carga]
            # Calcular DMF y DFC para carga distribuida
            CD = [carga['peso_cd'], carga['posicion_inicial_cd'], carga['posicion_final_cd']]
            dmf3 = f.DMFDistribuida(Long, CD, Paso)
            dfc3 = f.DFCDistribuida(Long, CD, Paso)
            
            f.Grafica(Long, np.linspace(0, Long, int(Long / Paso) + 1), dmf3, dfc3)
            

# Botón para generar gráfico general y tabla
if st.button("Generar gráfico general y tabla"):
    # Listas para almacenar los resultados de los diagramas de cada carga
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
