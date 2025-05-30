"""
Dashboard Interactivo para Transporte de Contaminantes en Canal Abierto
Metodología Integrada de Enseñanza - Ecuación ADR con FEM

Autor: Sistema de Demostración Académica
Propósito: FASE 1 - Impacto visual para Congreso Internacional de Didáctica Matemática
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.interpolate import griddata
import time
import os

# Configuración de página
st.set_page_config(
    page_title="🌊 Dashboard ADR - Amazonas Canal",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2e8b57;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-left: 4px solid #2e8b57;
        padding-left: 1rem;
    }
    .metric-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class ADRSolver:
    """Solver para Ecuación Advección-Difusión-Reacción usando Elementos Finitos"""
    
    def __init__(self, nx, ny, Lx, Ly):
        self.nx = nx  # Nodos en x
        self.ny = ny  # Nodos en y
        self.Lx = Lx  # Longitud en x
        self.Ly = Ly  # Longitud en y
        self.dx = Lx / (nx - 1)
        self.dy = Ly / (ny - 1)
        self.n_nodes = nx * ny
        
        # Crear malla
        self.x = np.linspace(0, Lx, nx)
        self.y = np.linspace(0, Ly, ny)
        self.X, self.Y = np.meshgrid(self.x, self.y, indexing='ij')
        
    def node_index(self, i, j):
        """Convierte índices (i,j) a índice global"""
        return i * self.ny + j
    
    def create_mass_matrix(self):
        """Matriz de masa para elementos finitos bilineales"""
        M = sp.lil_matrix((self.n_nodes, self.n_nodes))
        
        # Elemento rectangular con funciones de forma bilineales
        Me = (self.dx * self.dy / 36) * np.array([
            [4, 2, 1, 2],
            [2, 4, 2, 1],
            [1, 2, 4, 2],
            [2, 1, 2, 4]
        ])
        
        for i in range(self.nx - 1):
            for j in range(self.ny - 1):
                # Nodos del elemento
                nodes = [
                    self.node_index(i, j),
                    self.node_index(i+1, j),
                    self.node_index(i+1, j+1),
                    self.node_index(i, j+1)
                ]
                
                # Ensamblar matriz local
                for p in range(4):
                    for q in range(4):
                        M[nodes[p], nodes[q]] += Me[p, q]
        
        return M.tocsr()
    
    def create_stiffness_matrix(self, Dxx, Dyy, Dxy, u, v, decay):
        """Matriz de rigidez para difusión anisotrópica y advección"""
        K = sp.lil_matrix((self.n_nodes, self.n_nodes))
        
        for i in range(self.nx - 1):
            for j in range(self.ny - 1):
                # Tensor de difusividad en el elemento
                D_tensor = np.array([
                    [Dxx, Dxy],
                    [Dxy, Dyy]
                ])
                
                # Velocidad en el elemento
                u_elem = u
                v_elem = v
                
                # Matriz local (simplificada para demostración)
                Ke = self.compute_element_stiffness(D_tensor, u_elem, v_elem, decay)
                
                nodes = [
                    self.node_index(i, j),
                    self.node_index(i+1, j),
                    self.node_index(i+1, j+1),
                    self.node_index(i, j+1)
                ]
                
                # Ensamblar
                for p in range(4):
                    for q in range(4):
                        K[nodes[p], nodes[q]] += Ke[p, q]
        
        return K.tocsr()
    
    def compute_element_stiffness(self, D_tensor, u, v, decay):
        """Calcula matriz de rigidez local"""
        # Simplificación para demostración - en implementación real usaría cuadratura
        dx, dy = self.dx, self.dy
        
        # Matriz de difusión
        Kd = (1/6) * np.array([
            [2*D_tensor[0,0]/dx + 2*D_tensor[1,1]/dy, -2*D_tensor[0,0]/dx + D_tensor[1,1]/dy, -D_tensor[0,0]/dx - D_tensor[1,1]/dy, D_tensor[0,0]/dx - 2*D_tensor[1,1]/dy],
            [-2*D_tensor[0,0]/dx + D_tensor[1,1]/dy, 2*D_tensor[0,0]/dx + 2*D_tensor[1,1]/dy, D_tensor[0,0]/dx - 2*D_tensor[1,1]/dy, -D_tensor[0,0]/dx - D_tensor[1,1]/dy],
            [-D_tensor[0,0]/dx - D_tensor[1,1]/dy, D_tensor[0,0]/dx - 2*D_tensor[1,1]/dy, 2*D_tensor[0,0]/dx + 2*D_tensor[1,1]/dy, -2*D_tensor[0,0]/dx + D_tensor[1,1]/dy],
            [D_tensor[0,0]/dx - 2*D_tensor[1,1]/dy, -D_tensor[0,0]/dx - D_tensor[1,1]/dy, -2*D_tensor[0,0]/dx + D_tensor[1,1]/dy, 2*D_tensor[0,0]/dx + 2*D_tensor[1,1]/dy]
        ])
        
        # Matriz de advección
        Ka = (1/6) * np.array([
            [-u - v, u - v, u + v, -u + v],
            [-u + v, -u - v, u + v, u - v],
            [u - v, -u - v, -u + v, u + v],
            [u + v, -u + v, -u - v, u - v]
        ])
        
        # Matriz de reacción (masa multiplicada por coeficiente)
        Kr = decay * (dx * dy / 36) * np.array([
            [4, 2, 1, 2],
            [2, 4, 2, 1],
            [1, 2, 4, 2],
            [2, 1, 2, 4]
        ])
        
        return Kd + Ka + Kr
    
    def solve_timestep(self, C_old, dt, source_term, Dxx, Dyy, Dxy, u, v, decay):
        """Resuelve un paso temporal usando Crank-Nicolson"""
        M = self.create_mass_matrix()
        K = self.create_stiffness_matrix(Dxx, Dyy, Dxy, u, v, decay)
        
        # Sistema: (M + dt/2 * K) * C_new = (M - dt/2 * K) * C_old + dt * F
        A = M + 0.5 * dt * K
        b = (M - 0.5 * dt * K) @ C_old + dt * source_term
        
        # Aplicar condiciones de frontera (Dirichlet homogéneas)
        self.apply_boundary_conditions(A, b)
        
        # Resolver sistema lineal
        C_new = spla.spsolve(A, b)
        return C_new
    
    def apply_boundary_conditions(self, A, b):
        """Aplica condiciones de frontera Dirichlet homogéneas"""
        # Bordes de la malla
        boundary_nodes = []
        
        # Borde inferior y superior
        for i in range(self.nx):
            boundary_nodes.append(self.node_index(i, 0))
            boundary_nodes.append(self.node_index(i, self.ny-1))
        
        # Borde izquierdo y derecho
        for j in range(1, self.ny-1):
            boundary_nodes.append(self.node_index(0, j))
            boundary_nodes.append(self.node_index(self.nx-1, j))
        
        # Modificar matriz y vector
        for node in boundary_nodes:
            A[node, :] = 0
            A[node, node] = 1
            b[node] = 0

def load_data_files():
    """Carga archivos CSV de datos"""
    data_files = {
        'parametros_rio': None,
        'mediciones_campo': None,
        'condiciones_iniciales': None
    }
    
    data_dir = 'data'
    if os.path.exists(data_dir):
        try:
            if os.path.exists(f'{data_dir}/parametros_rio.csv'):
                data_files['parametros_rio'] = pd.read_csv(f'{data_dir}/parametros_rio.csv')
            if os.path.exists(f'{data_dir}/mediciones_campo.csv'):
                data_files['mediciones_campo'] = pd.read_csv(f'{data_dir}/mediciones_campo.csv')
            if os.path.exists(f'{data_dir}/condiciones_iniciales.csv'):
                data_files['condiciones_iniciales'] = pd.read_csv(f'{data_dir}/condiciones_iniciales.csv')
        except Exception as e:
            st.warning(f"Error cargando archivos: {e}")
    
    return data_files

def create_sample_data():
    """Crea datos de muestra si no existen archivos"""
    # Parámetros del río
    parametros = {
        'parametro': ['longitud_canal', 'ancho_canal', 'profundidad_media', 'velocidad_media', 
                      'rugosidad_manning', 'temperatura_agua', 'pH', 'conductividad'],
        'valor': [5000, 200, 3.5, 1.2, 0.035, 26.5, 7.8, 150],
        'unidad': ['m', 'm', 'm', 'm/s', '-', '°C', '-', 'μS/cm']
    }
    
    # Puntos de medición georreferenciados
    np.random.seed(42)
    n_points = 15
    mediciones = {
        'punto_id': [f'P{i:02d}' for i in range(1, n_points+1)],
        'latitud': -3.4 + np.random.normal(0, 0.1, n_points),
        'longitud': -60.0 + np.random.normal(0, 0.1, n_points),
        'distancia_fuente': np.random.uniform(100, 4900, n_points),
        'profundidad': np.random.uniform(1.0, 5.0, n_points),
        'concentracion_inicial': np.random.exponential(2.0, n_points)
    }
    mediciones['latitud'] = np.sort(mediciones['latitud'])[::-1]
    
    # Condiciones iniciales
    condiciones = {
        'x_fuente': [1000],
        'y_fuente': [100],
        'masa_contaminante': [500],
        'tiempo_derrame': [0],
        'tipo_contaminante': ['Químico_Industrial']
    }
    
    return pd.DataFrame(parametros), pd.DataFrame(mediciones), pd.DataFrame(condiciones)

def main():
    # Título principal
    st.markdown('<h1 class="main-header">🌊 Sistema ADR - Transporte de Contaminantes Canal Amazonas</h1>', unsafe_allow_html=True)
    st.markdown('<div class="warning-box">💡 <strong>Demo Metodología Reverse Engineering:</strong> Observe primero el resultado completo, luego deconstruiremos la matemática paso a paso.</div>', unsafe_allow_html=True)
    
    # Cargar datos
    data_files = load_data_files()
    if all(df is None for df in data_files.values()):
        st.info("📁 Generando datos de muestra (en producción se cargarían desde CSV)")
        parametros_df, mediciones_df, condiciones_df = create_sample_data()
    else:
        parametros_df = data_files['parametros_rio']
        mediciones_df = data_files['mediciones_campo']
        condiciones_df = data_files['condiciones_iniciales']
    
    # Sidebar con controles
    st.sidebar.markdown('<div class="section-header">🎛️ Parámetros de Simulación</div>', unsafe_allow_html=True)
    
    # Parámetros físicos
    st.sidebar.subheader("💧 Propiedades del Canal")
    L_channel = st.sidebar.slider("Longitud del canal (m)", 1000, 10000, 5000)
    W_channel = st.sidebar.slider("Ancho del canal (m)", 50, 500, 200)
    U_velocity = st.sidebar.slider("Velocidad media (m/s)", 0.1, 3.0, 1.2)
    
    st.sidebar.subheader("🔬 Parámetros del Contaminante")
    mass_spill = st.sidebar.slider("Masa derramada (kg)", 10, 1000, 500)
    Dxx = st.sidebar.slider("Difusividad longitudinal (m²/s)", 1.0, 50.0, 20.0)
    Dyy = st.sidebar.slider("Difusividad transversal (m²/s)", 0.1, 5.0, 2.0)
    Dxy = st.sidebar.slider("Difusividad cruzada (m²/s)", -2.0, 2.0, 0.5)
    decay_rate = st.sidebar.slider("Tasa de decaimiento (1/día)", 0.0, 2.0, 0.1)
    
    st.sidebar.subheader("⚙️ Parámetros Numéricos")
    nx = st.sidebar.selectbox("Nodos en X", [21, 41, 61, 81], index=1)
    ny = st.sidebar.selectbox("Nodos en Y", [11, 21, 31, 41], index=1)
    dt_hours = st.sidebar.slider("Paso temporal (horas)", 0.1, 2.0, 0.5)
    total_time = st.sidebar.slider("Tiempo total (días)", 1, 10, 5)
    
    # Botón de simulación
    run_simulation = st.sidebar.button("🚀 Ejecutar Simulación ADR", type="primary")
    
    # Layout principal con columnas
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-header">📊 Datos de Campo</div>', unsafe_allow_html=True)
        
        # Mostrar parámetros del río
        if parametros_df is not None:
            st.subheader("🌊 Parámetros del Río")
            st.dataframe(parametros_df, use_container_width=True)
        
        # Visualización georreferenciada
        if mediciones_df is not None:
            st.subheader("📍 Puntos de Medición Georreferenciados")
            
            fig_map = px.scatter_mapbox(
                mediciones_df,
                lat="latitud",
                lon="longitud",
                hover_name="punto_id",
                hover_data=["distancia_fuente", "profundidad"],
                color="concentracion_inicial",
                size="profundidad",
                color_continuous_scale="Viridis",
                zoom=8,
                height=400
            )
            fig_map.update_layout(mapbox_style="open-street-map")
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">🎯 Tensor de Difusividad</div>', unsafe_allow_html=True)
        
        # Visualización del tensor de difusividad
        D_tensor = np.array([[Dxx, Dxy], [Dxy, Dyy]])
        eigenvals, eigenvecs = np.linalg.eig(D_tensor)
        
        # Gráfico del tensor
        theta = np.linspace(0, 2*np.pi, 100)
        ellipse_x = np.sqrt(eigenvals[0]) * np.cos(theta)
        ellipse_y = np.sqrt(eigenvals[1]) * np.sin(theta)
        
        fig_tensor = go.Figure()
        fig_tensor.add_trace(go.Scatter(
            x=ellipse_x, y=ellipse_y,
            mode='lines', name='Elipse de Difusividad',
            line=dict(color='blue', width=3)
        ))
        fig_tensor.add_trace(go.Scatter(
            x=[0, eigenvecs[0,0]*np.sqrt(eigenvals[0])],
            y=[0, eigenvecs[1,0]*np.sqrt(eigenvals[0])],
            mode='lines+markers', name=f'Eje 1 (λ={eigenvals[0]:.2f})',
            line=dict(color='red', width=2)
        ))
        fig_tensor.add_trace(go.Scatter(
            x=[0, eigenvecs[0,1]*np.sqrt(eigenvals[1])],
            y=[0, eigenvecs[1,1]*np.sqrt(eigenvals[1])],
            mode='lines+markers', name=f'Eje 2 (λ={eigenvals[1]:.2f})',
            line=dict(color='green', width=2)
        ))
        fig_tensor.update_layout(
            title="Anisotropía del Medio",
            xaxis_title="Dirección X", yaxis_title="Dirección Y",
            height=400, showlegend=True
        )
        fig_tensor.update_xaxes(scaleanchor="y", scaleratio=1)
        st.plotly_chart(fig_tensor, use_container_width=True)
        
        # Métricas del tensor
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("🔢 Determinante", f"{np.linalg.det(D_tensor):.3f}")
        st.metric("📐 Razón de Anisotropía", f"{max(eigenvals)/min(eigenvals):.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Simulación principal
    if run_simulation:
        st.markdown('<div class="section-header">🧮 Simulación ADR en Progreso</div>', unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Configurar solver
        solver = ADRSolver(nx, ny, L_channel, W_channel)
        dt = dt_hours * 3600  # Convertir a segundos
        n_steps = int(total_time * 24 * 3600 / dt)
        
        # Condición inicial (fuente puntual)
        C = np.zeros(solver.n_nodes)
        source_x, source_y = L_channel * 0.2, W_channel * 0.5  # 20% río abajo, centro
        
        # Encontrar nodo más cercano a la fuente
        distances = np.sqrt((solver.X.flatten() - source_x)**2 + (solver.Y.flatten() - source_y)**2)
        source_node = np.argmin(distances)
        
        # Término fuente (impulso inicial)
        source_term = np.zeros(solver.n_nodes)
        source_term[source_node] = mass_spill / (solver.dx * solver.dy)  # Concentración inicial
        
        # Arrays para almacenar resultados
        times = []
        concentrations = []
        max_concentrations = []
        
        # Simulación temporal
        for step in range(n_steps):
            if step == 0:
                # Aplicar fuente solo en el primer paso
                C = solver.solve_timestep(C, dt, source_term, Dxx, Dyy, Dxy, U_velocity, 0, decay_rate/86400)
                source_term *= 0  # Remover fuente después del primer paso
            else:
                C = solver.solve_timestep(C, dt, np.zeros_like(C), Dxx, Dyy, Dxy, U_velocity, 0, decay_rate/86400)
            
            # Guardar resultados cada cierto número de pasos
            if step % max(1, n_steps // 50) == 0:
                times.append(step * dt / 3600)  # Convertir a horas
                concentrations.append(C.reshape(solver.nx, solver.ny).copy())
                max_concentrations.append(np.max(C))
            
            # Actualizar barra de progreso
            progress_bar.progress((step + 1) / n_steps)
            status_text.text(f"Paso {step+1}/{n_steps} - Tiempo: {step*dt/3600:.1f} hrs - C_max: {np.max(C):.2e} kg/m³")
        
        progress_bar.progress(1.0)
        status_text.text("✅ Simulación completada!")
        
        # Visualización de resultados
        st.markdown('<div class="section-header">📈 Resultados de la Simulación</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Animación de la evolución de concentración
            fig_anim = make_subplots(
                rows=2, cols=2,
                subplot_titles=("Concentración Actual", "Evolución Temporal", "Perfil Longitudinal", "Perfil Transversal"),
                specs=[[{"type": "surface"}, {"type": "scatter"}],
                       [{"type": "scatter"}, {"type": "scatter"}]]
            )
            
            # Frame selector
            frame_idx = st.slider("Seleccionar tiempo de visualización", 0, len(times)-1, len(times)//2)
            current_time = times[frame_idx]
            current_C = concentrations[frame_idx]
            
            # Superficie 3D de concentración
            fig_3d = go.Figure(data=[go.Surface(
                z=current_C,
                x=solver.x,
                y=solver.y,
                colorscale='Viridis',
                colorbar=dict(title="Concentración<br>(kg/m³)")
            )])
            fig_3d.update_layout(
                title=f"Concentración en t = {current_time:.1f} hrs",
                scene=dict(
                    xaxis_title="Distancia (m)",
                    yaxis_title="Ancho (m)",
                    zaxis_title="Concentración (kg/m³)"
                ),
                height=500
            )
            st.plotly_chart(fig_3d, use_container_width=True)
            
            # Evolución temporal de concentración máxima
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(
                x=times, y=max_concentrations,
                mode='lines+markers',
                name='Concentración Máxima',
                line=dict(color='red', width=2)
            ))
            fig_time.update_layout(
                title="Evolución Temporal de Concentración Máxima",
                xaxis_title="Tiempo (hrs)",
                yaxis_title="Concentración Máxima (kg/m³)",
                height=400
            )
            st.plotly_chart(fig_time, use_container_width=True)
        
        with col2:
            # Métricas de ingeniería
            st.subheader("📊 Métricas de Impacto")
            
            peak_concentration = max(max_concentrations)
            peak_time = times[np.argmax(max_concentrations)]
            final_concentration = max_concentrations[-1]
            
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.metric("🎯 Concentración Pico", f"{peak_concentration:.2e} kg/m³")
            st.metric("⏰ Tiempo al Pico", f"{peak_time:.1f} hrs")
            st.metric("📉 Concentración Final", f"{final_concentration:.2e} kg/m³")
            st.metric("⚡ Tasa Reducción", f"{(1-final_concentration/peak_concentration)*100:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Análisis de dispersión
            st.subheader("📐 Análisis de Dispersión")
            
            # Calcular centroide de la pluma
            total_mass = np.sum(current_C)
            if total_mass > 0:
                x_centroid = np.sum(current_C * solver.X) / total_mass
                y_centroid = np.sum(current_C * solver.Y) / total_mass
                
                # Momentos de segundo orden
                sigma_xx = np.sum(current_C * (solver.X - x_centroid)**2) / total_mass
                sigma_yy = np.sum(current_C * (solver.Y - y_centroid)**2) / total_mass
                
                st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                st.metric("📍 Centroide X", f"{x_centroid:.0f} m")
                st.metric("📍 Centroide Y", f"{y_centroid:.0f} m")
                st.metric("📏 Dispersión X", f"{np.sqrt(sigma_xx):.0f} m")
                st.metric("📏 Dispersión Y", f"{np.sqrt(sigma_yy):.0f} m")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Comparación con datos experimentales (simulados)
        st.markdown('<div class="section-header">🔬 Validación con Datos de Campo</div>', unsafe_allow_html=True)
        
        if mediciones_df is not None:
            # Interpolación de resultados en puntos de medición
            points_sim = []
            for _, row in mediciones_df.iterrows():
                # Convertir lat/lon a coordenadas del modelo (simplificado)
                x_point = (row['latitud'] + 3.4) * 50000  # Conversión aproximada
                y_point = (row['longitud'] + 60.0) * 20000
                
                # Interpolar concentración
                if 0 <= x_point <= L_channel and 0 <= y_point <= W_channel:
                    conc_interp = griddata(
                        (solver.X.flatten(), solver.Y.flatten()),
                        current_C.flatten(),
                        (x_point, y_point),
                        method='linear',
                        fill_value=0
                    )
                    points_sim.append(conc_interp)
                else:
                    points_sim.append(0)
            
            # Comparación
            comparison_df = mediciones_df.copy()
            comparison_df['concentracion_simulada'] = points_sim
            comparison_df['error_relativo'] = np.abs(
                comparison_df['concentracion_simulada'] - comparison_df['concentracion_inicial']
            ) / (comparison_df['concentracion_inicial'] + 1e-10) * 100
            
            fig_validation = go.Figure()
            fig_validation.add_trace(go.Scatter(
                x=comparison_df['concentracion_inicial'],
                y=comparison_df['concentracion_simulada'],
                mode='markers',
                marker=dict(size=10, color='blue', opacity=0.7),
                name='Puntos de Validación'
            ))
            fig_validation.add_trace(go.Scatter(
                x=[0, comparison_df['concentracion_inicial'].max()],
                y=[0, comparison_df['concentracion_inicial'].max()],
                mode='lines',
                line=dict(color='red', dash='dash'),
                name='Línea Perfecta (1:1)'
            ))
            fig_validation.update_layout(
                title="Validación: Simulación vs Mediciones de Campo",
                xaxis_title="Concentración Medida (kg/m³)",
                yaxis_title="Concentración Simulada (kg/m³)",
                height=400
            )
            st.plotly_chart(fig_validation, use_container_width=True)
            
            # Estadísticas de validación
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Error Medio", f"{comparison_df['error_relativo'].mean():.1f}%")
            with col2:
                st.metric("📈 Error Máximo", f"{comparison_df['error_relativo'].max():.1f}%")
            with col3:
                r_squared = np.corrcoef(comparison_df['concentracion_inicial'], 
                                      comparison_df['concentracion_simulada'])[0,1]**2
                st.metric("🎯 R²", f"{r_squared:.3f}")
    
    # Footer informativo
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        🎓 <strong>Sistema Demostrativo - Metodología Reverse Engineering</strong><br>
        Ecuación ADR resuelta mediante Elementos Finitos | Tensores de Difusividad Anisótropa<br>
        <em>Próximo paso: Deconstrucción didáctica paso a paso en notebooks interactivos</em>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()