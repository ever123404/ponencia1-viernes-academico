
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# [Aquí iría la clase SistemaADRCompleto completa]

# 🎨 CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Sistema ADR - Demo Interactivo",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎯 TÍTULO PRINCIPAL
st.title("🌊 Sistema de Transporte ADR")
st.subheader("Simulación Interactiva de Contaminantes en Canal Abierto")

# 🎛️ SIDEBAR CON CONTROLES
st.sidebar.header("🎛️ Parámetros de Simulación")

# Parámetros del dominio
st.sidebar.subheader("📐 Geometría")
Lx = st.sidebar.slider("Longitud X [m]", 50, 200, 100)
Ly = st.sidebar.slider("Ancho Y [m]", 20, 80, 50)
resolucion = st.sidebar.selectbox("Resolución", ["Baja (20×10)", "Media (40×20)", "Alta (60×30)"])

# Parámetros físicos
st.sidebar.subheader("🌊 Flujo")
vx = st.sidebar.slider("Velocidad X [m/s]", 0.1, 2.0, 0.8, 0.1)
vy = st.sidebar.slider("Velocidad Y [m/s]", -0.5, 0.5, 0.1, 0.1)

# Tensor de difusividad
st.sidebar.subheader("🧮 Difusividad")
Dxx = st.sidebar.slider("D₁₁ [m²/s]", 1.0, 30.0, 15.0, 1.0)
Dyy = st.sidebar.slider("D₂₂ [m²/s]", 1.0, 10.0, 3.0, 1.0)
Dxy = st.sidebar.slider("D₁₂ = D₂₁ [m²/s]", 0.0, 5.0, 2.0, 0.5)

# Condición inicial
st.sidebar.subheader("🎯 Derrame Inicial")
x0 = st.sidebar.slider("Posición X [m]", 0.0, float(Lx), Lx*0.2)
y0 = st.sidebar.slider("Posición Y [m]", 0.0, float(Ly), Ly*0.5)
sigma = st.sidebar.slider("Dispersión σ [m]", 1.0, 10.0, 4.0, 0.5)
C0 = st.sidebar.slider("Concentración inicial [kg/m³]", 100, 5000, 2000, 100)

# Parámetros temporales
st.sidebar.subheader("⏱️ Tiempo")
t_final = st.sidebar.slider("Tiempo final [s]", 10, 120, 50, 5)
dt = st.sidebar.slider("Paso temporal [s]", 0.1, 2.0, 0.8, 0.1)

# 🚀 BOTÓN DE SIMULACIÓN
if st.sidebar.button("🚀 Ejecutar Simulación", type="primary"):
    # Configurar resolución
    if "Baja" in resolucion:
        nx, ny = 20, 10
    elif "Media" in resolucion:
        nx, ny = 40, 20
    else:
        nx, ny = 60, 30
    
    # Crear sistema
    with st.spinner("🔧 Configurando sistema..."):
        sistema = SistemaADRCompleto(Lx=Lx, Ly=Ly, nx=nx, ny=ny)
        sistema.vx = vx
        sistema.vy = vy
        sistema.D_tensor = np.array([[Dxx, Dxy], [Dxy, Dyy]])
        sistema.dt = dt
        sistema.t_final = t_final
    
    # Condición inicial
    C_inicial = sistema.condicion_inicial_derrame(x0=x0, y0=y0, sigma=sigma, C0=C0)
    
    # Ejecutar simulación
    with st.spinner("⚡ Ejecutando simulación..."):
        start_time = time.time()
        sistema.resolver_sistema_temporal(C_inicial, mostrar_progreso=False)
        sim_time = time.time() - start_time
    
    # Guardar en session state
    st.session_state.sistema = sistema
    st.session_state.sim_time = sim_time
    
    st.success(f"✅ Simulación completada en {sim_time:.2f} segundos")

# 📊 MOSTRAR RESULTADOS
if 'sistema' in st.session_state:
    sistema = st.session_state.sistema
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        masa_conservada = 100 * sistema.metricas['masa_total'][-1] / sistema.metricas['masa_total'][0]
        st.metric("🧮 Conservación Masa", f"{masa_conservada:.1f}%")
    
    with col2:
        dilucion = sistema.metricas['concentracion_max'][0] / sistema.metricas['concentracion_max'][-1]
        st.metric("💧 Factor Dilución", f"{dilucion:.1f}x")
    
    with col3:
        distancia = sistema.metricas['centroide_x'][-1] - sistema.metricas['centroide_x'][0]
        st.metric("🏃 Distancia Recorrida", f"{distancia:.1f} m")
    
    with col4:
        velocidad_obs = distancia / sistema.t_final
        st.metric("⚡ Velocidad Observada", f"{velocidad_obs:.3f} m/s")
    
    # Visualización principal
    fig = sistema.visualizar_evolucion_completa()
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de datos para descarga
    if st.checkbox("📊 Mostrar datos tabulares"):
        df_resultados = pd.DataFrame({
            'Tiempo [s]': sistema.tiempos,
            'Masa Total [kg]': sistema.metricas['masa_total'],
            'Conc. Máxima [kg/m³]': sistema.metricas['concentracion_max'],
            'Centroide X [m]': sistema.metricas['centroide_x'],
            'Centroide Y [m]': sistema.metricas['centroide_y']
        })
        st.dataframe(df_resultados)
        
        # Descarga CSV
        csv = df_resultados.to_csv(index=False)
        st.download_button(
            label="💾 Descargar datos CSV",
            data=csv,
            file_name=f"simulacion_adr_{int(time.time())}.csv",
            mime="text/csv"
        )

else:
    st.info("👈 Configure los parámetros y presione 'Ejecutar Simulación' para comenzar")
    
    # Mostrar información del método
    with st.expander("📚 Información del Método"):
        st.markdown("""
        ### 🧮 Ecuación ADR (Advección-Difusión-Reacción)
        
        $$\frac{\partial C}{\partial t} + \vec{v} \cdot \nabla C = \nabla \cdot (\mathbf{D} \nabla C) + S$$
        
        Donde:
        - $C$: concentración del contaminante
        - $\vec{v}$: campo de velocidades del flujo
        - $\mathbf{D}$: tensor de difusividad anisótropo
        - $S$: término fuente/sumidero
        
        ### 📐 Método de Elementos Finitos
        - Discretización espacial con elementos triangulares
        - Esquema temporal implícito para estabilidad
        - Matrices dispersas para eficiencia computacional
        """)
