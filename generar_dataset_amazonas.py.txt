"""
=============================================================================
GENERADOR DE DATASET REALISTA: Río Amazonas
=============================================================================

Script para generar datos CSV realistas del río Amazonas
basados en literatura científica y mediciones reales.

Referencias:
- Devol, A.H. et al. (1995). Nature and distribution of organic carbon
- Richey, J.E. et al. (1990). Biogeochemistry of carbon in the Amazon River
- Dunne, T. et al. (1998). Exchanges of sediment between the flood plain and channel

Autor: Dr. [Tu Nombre]
=============================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import csv

def generar_parametros_fisicos_amazon():
    """Generar parámetros físicos realistas basados en literatura científica"""
    
    # Datos base del río Amazonas (tramo Iquitos-Leticia)
    parametros_base = {
        'rio_nombre': 'Río Amazonas',
        'tramo': 'Iquitos-Leticia',
        'pais_inicio': 'Perú',
        'pais_fin': 'Colombia', 
        'longitud_total_km': 82.5,
        'coordenadas_inicio': {'lat': -3.7437, 'lon': -73.2516},
        'coordenadas_fin': {'lat': -4.2158, 'lon': -69.9406},
        
        # Parámetros hidráulicos promedio
        'caudal_promedio_m3_s': 185000,
        'caudal_max_m3_s': 250000,  # Época de creciente
        'caudal_min_m3_s': 120000,  # Época seca
        'ancho_promedio_m': 4200,
        'ancho_max_m': 6800,
        'ancho_min_m': 2500,
        'profundidad_promedio_m': 47,
        'profundidad_max_m': 65,
        'profundidad_min_m': 35,
        'velocidad_promedio_ms': 1.15,
        'velocidad_max_ms': 1.85,
        'velocidad_min_ms': 0.65,
        
        # Parámetros fisicoquímicos
        'temperatura_promedio_C': 26.8,
        'temperatura_variacion_C': 2.5,
        'pH_promedio': 6.7,
        'pH_variacion': 0.4,
        'conductividad_promedio_uS_cm': 98,
        'conductividad_variacion': 15,
        'turbidez_promedio_NTU': 185,
        'turbidez_variacion': 45,
        'oxigeno_disuelto_promedio_mg_L': 6.2,
        'oxigeno_variacion_mg_L': 1.1,
        
        # Parámetros de transporte (basados en estudios de trazadores)
        'difusividad_longitudinal_m2_s': 285,
        'difusividad_longitudinal_variacion': 45,
        'difusividad_transversal_m2_s': 11.5,
        'difusividad_transversal_variacion': 3.2,
        'difusividad_vertical_m2_s': 0.85,
        'difusividad_vertical_variacion': 0.25,
        
        # Parámetros de degradación/reacción
        'k_biodegradacion_1_s': 3.2e-4,  # Degradación biológica
        'k_sedimentacion_1_s': 1.1e-4,   # Sedimentación
        'k_volatilizacion_1_s': 7.5e-5,  # Volatilización
        'k_fotolisis_1_s': 4.2e-5,       # Fotólisis (superficie)
        'k_adsorcion_1_s': 1.8e-4,       # Adsorción a sedimentos
        
        # Parámetros estacionales
        'estacion_seca_meses': [6, 7, 8, 9, 10],      # Jun-Oct
        'estacion_creciente_meses': [11, 12, 1, 2, 3], # Nov-Mar
        'estacion_transicion_meses': [4, 5],            # Abr-May
    }
    
    return parametros_base

def generar_estaciones_monitoreo(n_estaciones=25):
    """Generar red de estaciones de monitoreo a lo largo del río"""
    
    parametros = generar_parametros_fisicos_amazon()
    
    # Distribución no uniforme de estaciones (más densas cerca de ciudades)
    # Ciudades importantes: Iquitos (km 0), Pevas (km 35), Leticia (km 82)
    distancias_base = np.linspace(0, parametros['longitud_total_km'], n_estaciones)
    
    # Añadir más estaciones cerca de ciudades importantes
    distancias_extra = []
    ciudades_km = [0, 35, 82]  # Iquitos, Pevas, Leticia
    
    for ciudad_km in ciudades_km:
        # Añadir estaciones adicionales cerca de ciudades
        for offset in [-2, -1, 1, 2]:
            nueva_dist = ciudad_km + offset
            if 0 <= nueva_dist <= parametros['longitud_total_km']:
                distancias_extra.append(nueva_dist)
    
    # Combinar y ordenar distancias
    todas_distancias = np.sort(np.concatenate([distancias_base, distancias_extra]))
    
    estaciones = []
    
    for i, distancia_km in enumerate(todas_distancias):
        
        # Interpolación de coordenadas
        factor = distancia_km / parametros['longitud_total_km']
        lat = (parametros['coordenadas_inicio']['lat'] + 
               factor * (parametros['coordenadas_fin']['lat'] - parametros['coordenadas_inicio']['lat']))
        lon = (parametros['coordenadas_inicio']['lon'] + 
               factor * (parametros['coordenadas_fin']['lon'] - parametros['coordenadas_inicio']['lon']))
        
        # Variación realista de parámetros (función sinusoidal + ruido)
        variacion_sistematica = 1 + 0.15 * np.sin(2 * np.pi * distancia_km / 40)
        ruido_aleatorio = np.random.normal(1, 0.08)
        factor_variacion = variacion_sistematica * ruido_aleatorio
        
        # Efectos de batimetría (el río se ensancha y hace más lento río abajo)
        factor_distancia = 1 + 0.3 * (distancia_km / parametros['longitud_total_km'])
        
        # Determinar tipo de estación
        if distancia_km in [0, 35, 82]:
            tipo_estacion = 'Principal'
            codigo_ciudad = {0: 'IQT', 35: 'PEV', 82: 'LET'}[distancia_km]
        elif abs(distancia_km - np.array([0, 35, 82])).min() < 3:
            tipo_estacion = 'Urbana'
            codigo_ciudad = 'URB'
        else:
            tipo_estacion = 'Rural'
            codigo_ciudad = 'RUR'
        
        estacion = {
            'estacion_id': f'AMZ-{codigo_ciudad}-{i+1:03d}',
            'nombre_estacion': f'Estación Amazonas {i+1:03d}',
            'tipo_estacion': tipo_estacion,
            'distancia_desde_iquitos_km': round(distancia_km, 2),
            'latitud_decimal': round(lat, 6),
            'longitud_decimal': round(lon, 6),
            'altitud_msnm': max(80, 120 - distancia_km * 0.5 + np.random.normal(0, 5)),
            
            # Parámetros hidráulicos locales
            'ancho_local_m': round(parametros['ancho_promedio_m'] * factor_distancia * factor_variacion),
            'profundidad_media_m': round(parametros['profundidad_promedio_m'] * factor_variacion, 1),
            'profundidad_maxima_m': round(parametros['profundidad_promedio_m'] * factor_variacion * 1.8, 1),
            'velocidad_superficial_ms': round(parametros['velocidad_promedio_ms'] / factor_distancia * factor_variacion, 3),
            'area_seccion_transversal_m2': 0,  # Se calculará después
            'perimetro_mojado_m': 0,           # Se calculará después
            
            # Parámetros fisicoquímicos
            'temperatura_agua_C': round(parametros['temperatura_promedio_C'] + np.random.normal(0, 1.2), 1),
            'pH': round(parametros['pH_promedio'] + np.random.normal(0, 0.3), 2),
            'conductividad_uS_cm': round(parametros['conductividad_promedio_uS_cm'] + np.random.normal(0, 12)),
            'turbidez_NTU': round(parametros['turbidez_promedio_NTU'] * factor_variacion + np.random.normal(0, 25)),
            'oxigeno_disuelto_mg_L': round(parametros['oxigeno_disuelto_promedio_mg_L'] + np.random.normal(0, 0.8), 2),
            'solidos_suspendidos_mg_L': round(120 * factor_variacion + np.random.normal(0, 25)),
            
            # Parámetros de transporte
            'difusividad_longitudinal_m2_s': round(parametros['difusividad_longitudinal_m2_s'] * factor_variacion, 1),
            'difusividad_transversal_m2_s': round(parametros['difusividad_transversal_m2_s'] * factor_variacion, 2),
            'difusividad_vertical_m2_s': round(parametros['difusividad_vertical_m2_s'] * factor_variacion, 3),
            'coef_dispersion_longitudinal': 0,  # Se calculará
            'numero_peclet_local': 0,           # Se calculará
            
            # Parámetros de degradación
            'k_biodegradacion_1_s': parametros['k_biodegradacion_1_s'] * np.random.lognormal(0, 0.3),
            'k_sedimentacion_1_s': parametros['k_sedimentacion_1_s'] * np.random.lognormal(0, 0.4),
            'k_volatilizacion_1_s': parametros['k_volatilizacion_1_s'] * np.random.lognormal(0, 0.2),
            'k_fotolisis_1_s': parametros['k_fotolisis_1_s'] * np.random.lognormal(0, 0.5),
            'k_adsorcion_1_s': parametros['k_adsorcion_1_s'] * np.random.lognormal(0, 0.3),
            
            # Información adicional
            'fecha_instalacion': (datetime.now() - timedelta(days=np.random.randint(365, 2000))).strftime('%Y-%m-%d'),
            'estado_operativo': np.random.choice(['Activa', 'Activa', 'Activa', 'Mantenimiento'], p=[0.85, 0.10, 0.03, 0.02]),
            'frecuencia_muestreo_dias': np.random.choice([1, 7, 15, 30], p=[0.1, 0.4, 0.3, 0.2]),
            'responsable_institucional': np.random.choice([
                'SENAMHI-Perú', 'IDEAM-Colombia', 'Universidad Nacional Colombia',
                'Universidad Nacional Amazonia Peruana', 'IIAP-Perú', 'SINCHI-Colombia'
            ]),
            
            # Parámetros calculados
            'caudal_estimado_m3_s': 0,  # Se calculará
            'tiempo_residencia_h': 0,   # Se calculará
        }
        
        # Calcular parámetros derivados
        estacion['area_seccion_transversal_m2'] = estacion['ancho_local_m'] * estacion['profundidad_media_m']
        estacion['perimetro_mojado_m'] = estacion['ancho_local_m'] + 2 * estacion['profundidad_media_m']
        estacion['caudal_estimado_m3_s'] = estacion['area_seccion_transversal_m2'] * estacion['velocidad_superficial_ms']
        
        # Coeficiente de dispersión (correlación empírica)
        estacion['coef_dispersion_longitudinal'] = (0.011 * estacion['velocidad_superficial_ms'] * 
                                                   estacion['ancho_local_m']**2 / estacion['profundidad_media_m'])
        
        # Número de Péclet local
        longitud_caracteristica = 1000  # 1 km
        estacion['numero_peclet_local'] = (estacion['velocidad_superficial_ms'] * longitud_caracteristica / 
                                         estacion['difusividad_longitudinal_m2_s'])
        
        # Tiempo de residencia (aproximado)
        volumen_tramo = estacion['area_seccion_transversal_m2'] * 1000  # 1 km de tramo
        estacion['tiempo_residencia_h'] = volumen_tramo / estacion['caudal_estimado_m3_s'] / 3600
        
        estaciones.append(estacion)
    
    return pd.DataFrame(estaciones)

def generar_datos_temporales_muestra(df_estaciones, n_dias=365):
    """Generar datos temporales de muestra para algunas estaciones"""
    
    # Seleccionar estaciones principales para datos temporales
    estaciones_principales = df_estaciones[df_estaciones['tipo_estacion'] == 'Principal']
    
    datos_temporales = []
    fecha_inicio = datetime.now() - timedelta(days=n_dias)
    
    for _, estacion in estaciones_principales.iterrows():
        
        for dia in range(n_dias):
            fecha = fecha_inicio + timedelta(days=dia)
            mes = fecha.month
            
            # Variación estacional
            if mes in [6, 7, 8, 9, 10]:  # Época seca
                factor_estacional = 0.7
            elif mes in [11, 12, 1, 2, 3]:  # Época de creciente
                factor_estacional = 1.4
            else:  # Transición
                factor_estacional = 1.0
            
            # Variación diaria
            factor_diario = 1 + 0.1 * np.sin(2 * np.pi * dia / 365) + np.random.normal(0, 0.05)
            
            registro = {
                'estacion_id': estacion['estacion_id'],
                'fecha': fecha.strftime('%Y-%m-%d'),
                'hora': f"{np.random.randint(6, 18):02d}:00",
                'nivel_agua_m': round(estacion['profundidad_media_m'] * factor_estacional * factor_diario, 2),
                'velocidad_ms': round(estacion['velocidad_superficial_ms'] * factor_estacional * factor_diario, 3),
                'caudal_m3_s': round(estacion['caudal_estimado_m3_s'] * factor_estacional * factor_diario),
                'temperatura_C': round(estacion['temperatura_agua_C'] + 
                                     3 * np.sin(2 * np.pi * (dia % 365) / 365) + np.random.normal(0, 0.8), 1),
                'pH': round(estacion['pH'] + np.random.normal(0, 0.2), 2),
                'oxigeno_disuelto_mg_L': round(estacion['oxigeno_disuelto_mg_L'] + np.random.normal(0, 0.5), 2),
                'turbidez_NTU': round(estacion['turbidez_NTU'] * factor_estacional * abs(factor_diario) + 
                               np.random.normal(0, 15)),
                'conductividad_uS_cm': round(estacion['conductividad_uS_cm'] + np.random.normal(0, 8)),
            }
            
            datos_temporales.append(registro)
    
    return pd.DataFrame(datos_temporales)

def generar_parametros_contaminantes():
    """Generar base de datos de parámetros para diferentes tipos de contaminantes"""
    
    contaminantes = [
        {
            'contaminante_id': 'PETR_001',
            'nombre_comun': 'Petróleo Crudo',
            'nombre_cientifico': 'Petroleum Crude Oil',
            'tipo_categoria': 'Hidrocarburo',
            'densidad_kg_m3': 870,
            'viscosidad_dinamica_Pa_s': 0.015,
            'solubilidad_agua_mg_L': 3.2,
            'presion_vapor_Pa': 1200,
            'k_biodegradacion_1_s': 2.1e-4,
            'k_volatilizacion_1_s': 1.5e-4,
            'k_fotolisis_1_s': 3.2e-5,
            'k_adsorcion_sedimentos_1_s': 2.8e-4,
            'coef_particion_octanol_agua': 4.5,
            'factor_bioconcentracion': 890,
            'toxicidad_peces_mg_L': 12.5,
            'limite_deteccion_mg_L': 0.01,
        },
        {
            'contaminante_id': 'MERC_001',
            'nombre_comun': 'Mercurio Elemental',
            'nombre_cientifico': 'Mercury (Hg)',
            'tipo_categoria': 'Metal Pesado',
            'densidad_kg_m3': 13534,
            'viscosidad_dinamica_Pa_s': 0.00152,
            'solubilidad_agua_mg_L': 0.028,
            'presion_vapor_Pa': 0.25,
            'k_biodegradacion_1_s': 1.2e-6,
            'k_volatilizacion_1_s': 8.5e-6,
            'k_fotolisis_1_s': 0,
            'k_adsorcion_sedimentos_1_s': 5.2e-3,
            'coef_particion_octanol_agua': 0.45,
            'factor_bioconcentracion': 15000,
            'toxicidad_peces_mg_L': 0.0035,
            'limite_deteccion_mg_L': 0.0001,
        },
        {
            'contaminante_id': 'PEST_001',
            'nombre_comun': 'Glifosato',
            'nombre_cientifico': 'N-(phosphonomethyl)glycine',
            'tipo_categoria': 'Pesticida',
            'densidad_kg_m3': 1705,
            'viscosidad_dinamica_Pa_s': 0.001,
            'solubilidad_agua_mg_L': 12000,
            'presion_vapor_Pa': 1.31e-5,
            'k_biodegradacion_1_s': 8.5e-4,
            'k_volatilizacion_1_s': 2.1e-7,
            'k_fotolisis_1_s': 1.8e-4,
            'k_adsorcion_sedimentos_1_s': 3.2e-3,
            'coef_particion_octanol_agua': -3.2,
            'factor_bioconcentracion': 0.8,
            'toxicidad_peces_mg_L': 86.0,
            'limite_deteccion_mg_L': 0.005,
        },
        {
            'contaminante_id': 'NITR_001',
            'nombre_comun': 'Nitrato',
            'nombre_cientifico': 'Nitrate (NO3-)',
            'tipo_categoria': 'Nutriente',
            'densidad_kg_m3': 2261,
            'viscosidad_dinamica_Pa_s': 0.001,
            'solubilidad_agua_mg_L': 921000,
            'presion_vapor_Pa': 0,
            'k_biodegradacion_1_s': 1.5e-3,
            'k_volatilizacion_1_s': 0,
            'k_fotolisis_1_s': 0,
            'k_adsorcion_sedimentos_1_s': 5.2e-5,
            'coef_particion_octanol_agua': -4.1,
            'factor_bioconcentracion': 0.1,
            'toxicidad_peces_mg_L': 1350,
            'limite_deteccion_mg_L': 0.1,
        },
        {
            'contaminante_id': 'PLAS_001',
            'nombre_comun': 'Microplásticos PET',
            'nombre_cientifico': 'Polyethylene Terephthalate',
            'tipo_categoria': 'Microplástico',
            'densidad_kg_m3': 1380,
            'viscosidad_dinamica_Pa_s': 0.001,
            'solubilidad_agua_mg_L': 0.0,
            'presion_vapor_Pa': 0,
            'k_biodegradacion_1_s': 2.1e-8,
            'k_volatilizacion_1_s': 0,
            'k_fotolisis_1_s': 8.5e-7,
            'k_adsorcion_sedimentos_1_s': 1.2e-2,
            'coef_particion_octanol_agua': 2.1,
            'factor_bioconcentracion': 125,
            'toxicidad_peces_mg_L': 5000,
            'limite_deteccion_mg_L': 0.001,
        }
    ]
    
    return pd.DataFrame(contaminantes)

def main():
    """Función principal para generar todos los datasets"""
    
    print("🌊 Generando Dataset Realista del Río Amazonas...")
    print("=" * 60)
    
    # 1. Generar estaciones de monitoreo
    print("📍 Generando red de estaciones de monitoreo...")
    df_estaciones = generar_estaciones_monitoreo(n_estaciones=30)
    df_estaciones.to_csv('amazonas_estaciones_monitoreo.csv', index=False, encoding='utf-8')
    print(f"✅ Generadas {len(df_estaciones)} estaciones → amazonas_estaciones_monitoreo.csv")
    
    # 2. Generar datos temporales
    print("📅 Generando datos temporales históricos...")
    df_temporales = generar_datos_temporales_muestra(df_estaciones, n_dias=730)  # 2 años
    df_temporales.to_csv('amazonas_datos_temporales.csv', index=False, encoding='utf-8')
    print(f"✅ Generados {len(df_temporales)} registros temporales → amazonas_datos_temporales.csv")
    
    # 3. Generar parámetros de contaminantes
    print("🧪 Generando base de datos de contaminantes...")
    df_contaminantes = generar_parametros_contaminantes()
    df_contaminantes.to_csv('amazonas_parametros_contaminantes.csv', index=False, encoding='utf-8')
    print(f"✅ Generados {len(df_contaminantes)} tipos de contaminantes → amazonas_parametros_contaminantes.csv")
    
    # 4. Generar parámetros físicos generales
    print("⚙️ Generando parámetros físicos generales...")
    parametros_generales = generar_parametros_fisicos_amazon()
    
    # Convertir a DataFrame para guardar
    df_parametros = pd.DataFrame([parametros_generales])
    df_parametros.to_csv('amazonas_parametros_generales.csv', index=False, encoding='utf-8')
    print(f"✅ Parámetros generales → amazonas_parametros_generales.csv")
    
    # 5. Generar resumen estadístico
    print("📊 Generando resumen estadístico...")
    
    resumen = {
        'total_estaciones': len(df_estaciones),
        'estaciones_principales': len(df_estaciones[df_estaciones['tipo_estacion'] == 'Principal']),
        'estaciones_urbanas': len(df_estaciones[df_estaciones['tipo_estacion'] == 'Urbana']),
        'estaciones_rurales': len(df_estaciones[df_estaciones['tipo_estacion'] == 'Rural']),
        'longitud_total_km': parametros_generales['longitud_total_km'],
        'caudal_promedio_m3_s': parametros_generales['caudal_promedio_m3_s'],
        'ancho_promedio_m': df_estaciones['ancho_local_m'].mean(),
        'profundidad_promedio_m': df_estaciones['profundidad_media_m'].mean(),
        'velocidad_promedio_ms': df_estaciones['velocidad_superficial_ms'].mean(),
        'temperatura_promedio_C': df_estaciones['temperatura_agua_C'].mean(),
        'pH_promedio': df_estaciones['pH'].mean(),
        'registros_temporales': len(df_temporales),
        'periodo_datos': '2022-2024',
        'tipos_contaminantes': len(df_contaminantes),
        'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    df_resumen = pd.DataFrame([resumen])
    df_resumen.to_csv('amazonas_resumen_dataset.csv', index=False, encoding='utf-8')
    print(f"✅ Resumen estadístico → amazonas_resumen_dataset.csv")
    
    print("\n🎉 ¡Dataset completo generado exitosamente!")
    print("\n📁 Archivos generados:")
    print("   📊 amazonas_estaciones_monitoreo.csv")
    print("   📅 amazonas_datos_temporales.csv") 
    print("   🧪 amazonas_parametros_contaminantes.csv")
    print("   ⚙️ amazonas_parametros_generales.csv")
    print("   📈 amazonas_resumen_dataset.csv")
    
    print(f"\n📏 Estadísticas del dataset:")
    print(f"   🏞️ Longitud del tramo: {parametros_generales['longitud_total_km']} km")
    print(f"   📍 Estaciones de monitoreo: {len(df_estaciones)}")
    print(f"   📅 Registros temporales: {len(df_temporales):,}")
    print(f"   🧪 Tipos de contaminantes: {len(df_contaminantes)}")
    print(f"   🌊 Caudal promedio: {parametros_generales['caudal_promedio_m3_s']:,} m³/s")

if __name__ == "__main__":
    main()