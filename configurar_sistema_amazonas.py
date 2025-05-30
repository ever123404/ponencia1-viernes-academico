"""
=============================================================================
CONFIGURACIÓN COMPLETA DEL SISTEMA AMAZONAS
=============================================================================

Script maestro para configurar el sistema completo de simulación de 
transporte de contaminantes en el río Amazonas.

Incluye:
- Verificación de dependencias
- Generación de datasets
- Configuración del dashboard Streamlit
- Validación del sistema

Autor: Dr. [Tu Nombre]
Para: Congreso Internacional sobre Didáctica de la Matemática
=============================================================================
"""

import sys
import subprocess
import pkg_resources
import os
from pathlib import Path
import json
import platform

def verificar_python_version():
    """Verificar que la versión de Python sea compatible"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro} detectado")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Se requiere Python 3.8 o superior")
        print("   Por favor actualiza Python antes de continuar")
        return False
    
    print("✅ Versión de Python compatible")
    return True

def obtener_dependencias_requeridas():
    """Lista de todas las dependencias necesarias"""
    dependencias = {
        'core': [
            'numpy>=1.21.0',
            'scipy>=1.7.0', 
            'pandas>=1.3.0',
            'matplotlib>=3.5.0',
            'seaborn>=0.11.0'
        ],
        'web': [
            'streamlit>=1.20.0',
            'plotly>=5.10.0'
        ],
        'scientific': [
            'sympy>=1.9.0',
            'scikit-learn>=1.0.0'
        ],
        'optional': [
            'jupyter>=1.0.0',
            'notebook>=6.4.0',
            'ipywidgets>=7.6.0'
        ]
    }
    return dependencias

def verificar_dependencias():
    """Verificar qué dependencias están instaladas"""
    dependencias = obtener_dependencias_requeridas()
    instaladas = []
    faltantes = []
    
    print("🔍 Verificando dependencias...")
    
    for categoria, paquetes in dependencias.items():
        print(f"\n📦 Categoría: {categoria}")
        
        for paquete in paquetes:
            nombre_paquete = paquete.split('>=')[0].split('==')[0]
            
            try:
                pkg_resources.get_distribution(nombre_paquete)
                print(f"   ✅ {nombre_paquete}")
                instaladas.append(paquete)
            except pkg_resources.DistributionNotFound:
                print(f"   ❌ {nombre_paquete} (faltante)")
                faltantes.append(paquete)
    
    return instaladas, faltantes

def instalar_dependencias(faltantes):
    """Instalar dependencias faltantes"""
    if not faltantes:
        print("✅ Todas las dependencias están instaladas")
        return True
    
    print(f"\n📥 Instalando {len(faltantes)} dependencias faltantes...")
    
    # Crear comando de instalación
    comando = [sys.executable, '-m', 'pip', 'install'] + faltantes
    
    try:
        # Mostrar comando que se ejecutará
        print(f"🔧 Ejecutando: {' '.join(comando)}")
        
        # Ejecutar instalación
        resultado = subprocess.run(
            comando, 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        print("✅ Dependencias instaladas exitosamente")
        print(resultado.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la instalación:")
        print(e.stderr)
        return False

def crear_estructura_directorios():
    """Crear estructura de directorios del proyecto"""
    directorios = [
        'data',
        'src', 
        'notebooks',
        'docs',
        'outputs',
        'temp'
    ]
    
    print("📁 Creando estructura de directorios...")
    
    for directorio in directorios:
        path = Path(directorio)
        path.mkdir(exist_ok=True)
        print(f"   📂 {directorio}/")
    
    # Crear archivos README en cada directorio
    readme_content = {
        'data': "# Datos del Río Amazonas\n\nContiene datasets CSV con parámetros reales del río.",
        'src': "# Código Fuente\n\nContiene módulos Python del sistema de simulación.",
        'notebooks': "# Notebooks Jupyter\n\nNotebooks didácticos para la metodología.",
        'docs': "# Documentación\n\nDocumentación técnica y metodológica.",
        'outputs': "# Resultados\n\nResultados de simulaciones y análisis.",
        'temp': "# Archivos Temporales\n\nArchivos temporales y de trabajo."
    }
    
    for directorio, contenido in readme_content.items():
        readme_path = Path(directorio) / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
    
    print("✅ Estructura de directorios creada")

def generar_configuracion_sistema():
    """Generar archivo de configuración del sistema"""
    config = {
        "sistema": {
            "nombre": "Amazonas Contaminant Transport System",
            "version": "1.0.0",
            "autor": "Dr. [Tu Nombre]",
            "fecha_creacion": "2024",
            "descripcion": "Sistema de simulación para transporte de contaminantes en el río Amazonas"
        },
        "parametros_default": {
            "rio": {
                "longitud_km": 82.5,
                "ancho_promedio_m": 4200,
                "velocidad_ms": 1.15,
                "profundidad_m": 47
            },
            "simulacion": {
                "n_elementos_fem": 100,
                "tiempo_simulacion_h": 48,
                "dt_output_h": 2.0
            },
            "contaminante_default": {
                "masa_kg": 1000,
                "posicion_derrame_km": 15,
                "tipo": "petroleo_crudo"
            }
        },
        "paths": {
            "data_dir": "./data/",
            "output_dir": "./outputs/",
            "temp_dir": "./temp/"
        },
        "streamlit": {
            "host": "localhost",
            "port": 8501,
            "theme": "light"
        }
    }
    
    config_file = "config_amazonas.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"⚙️ Configuración guardada en: {config_file}")
    return config

def crear_script_ejecutor():
    """Crear script para ejecutar el dashboard fácilmente"""
    
    script_content = """#!/usr/bin/env python3
\"\"\"
Script para ejecutar el Dashboard del Amazonas
\"\"\"
import subprocess
import sys
import os

def ejecutar_dashboard():
    print("🌊 Iniciando Dashboard del Amazonas...")
    print("📡 El dashboard se abrirá en: http://localhost:8501")
    print("🔄 Para detener: Ctrl+C")
    print("-" * 50)
    
    try:
        # Cambiar al directorio del script
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Ejecutar Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'streamlit_amazonas_dashboard.py',
            '--server.headless', 'false',
            '--server.address', 'localhost',
            '--server.port', '8501'
        ])
        
    except KeyboardInterrupt:
        print("\\n🛑 Dashboard detenido por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    ejecutar_dashboard()
"""
    
    with open("ejecutar_dashboard.py", 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Hacer ejecutable en sistemas Unix
    if platform.system() != 'Windows':
        os.chmod("ejecutar_dashboard.py", 0o755)
    
    print("🚀 Script ejecutor creado: ejecutar_dashboard.py")

def crear_requirements_txt():
    """Crear archivo requirements.txt completo"""
    dependencias = obtener_dependencias_requeridas()
    
    requirements_content = """# Dependencias para Sistema Amazonas
# Instalación: pip install -r requirements.txt

# === CORE CIENTÍFICO ===
numpy>=1.21.0
scipy>=1.7.0
pandas>=1.3.0
matplotlib>=3.5.0
seaborn>=0.11.0

# === WEB Y VISUALIZACIÓN ===
streamlit>=1.20.0
plotly>=5.10.0

# === MATEMÁTICA SIMBÓLICA ===
sympy>=1.9.0

# === MACHINE LEARNING (OPCIONAL) ===
scikit-learn>=1.0.0

# === JUPYTER (OPCIONAL) ===
jupyter>=1.0.0
notebook>=6.4.0
ipywidgets>=7.6.0

# === UTILIDADES ===
pathlib2>=2.3.6;python_version<"3.4"
"""
    
    with open("requirements.txt", 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    
    print("📄 Archivo requirements.txt creado")

def ejecutar_generador_datos():
    """Ejecutar el generador de datos del Amazonas"""
    print("🌊 Generando datasets del río Amazonas...")
    
    try:
        # Importar y ejecutar el generador
        from generar_dataset_amazonas import main as generar_datos
        generar_datos()
        print("✅ Datasets generados exitosamente")
        return True
    except ImportError:
        print("⚠️ Script generador no encontrado, creando datos básicos...")
        return crear_datos_basicos()
    except Exception as e:
        print(f"❌ Error generando datos: {e}")
        return False

def crear_datos_basicos():
    """Crear datos básicos si el generador completo no está disponible"""
    import pandas as pd
    import numpy as np
    
    # Datos mínimos para el funcionamiento
    estaciones_basicas = []
    
    for i in range(20):
        estacion = {
            'estacion_id': f'AMZ-{i+1:03d}',
            'nombre_estacion': f'Estación {i+1}',
            'distancia_km': i * 4,
            'latitud': -3.75 - i * 0.025,
            'longitud': -73.25 + i * 0.175,
            'ancho_local_m': 4200 + np.random.normal(0, 500),
            'velocidad_local_ms': 1.15 + np.random.normal(0, 0.2),
            'profundidad_local_m': 47 + np.random.normal(0, 8),
            'temperatura_agua_C': 26.5 + np.random.normal(0, 1.5),
            'pH': 6.7 + np.random.normal(0, 0.3)
        }
        estaciones_basicas.append(estacion)
    
    df = pd.DataFrame(estaciones_basicas)
    df.to_csv('data/amazonas_estaciones_basicas.csv', index=False)
    
    print("✅ Datos básicos creados en data/amazonas_estaciones_basicas.csv")
    return True

def validar_instalacion():
    """Validar que todo el sistema esté correctamente instalado"""
    print("\n🔍 Validando instalación completa...")
    
    validaciones = []
    
    # 1. Verificar Python
    validaciones.append(("Python >= 3.8", verificar_python_version()))
    
    # 2. Verificar dependencias críticas
    try:
        import numpy, pandas, matplotlib, streamlit
        validaciones.append(("Dependencias críticas", True))
    except ImportError as e:
        validaciones.append(("Dependencias críticas", False))
        print(f"   ❌ Falta: {e}")
    
    # 3. Verificar estructura de directorios
    directorios_requeridos = ['data', 'src', 'outputs']
    dirs_ok = all(Path(d).exists() for d in directorios_requeridos)
    validaciones.append(("Estructura de directorios", dirs_ok))
    
    # 4. Verificar archivos de configuración
    archivos_config = ['config_amazonas.json', 'requirements.txt', 'ejecutar_dashboard.py']
    config_ok = all(Path(f).exists() for f in archivos_config)
    validaciones.append(("Archivos de configuración", config_ok))
    
    # 5. Verificar datos
    datos_ok = Path('data').exists() and any(Path('data').glob('*.csv'))
    validaciones.append(("Datos del Amazonas", datos_ok))
    
    # Mostrar resultados
    print("\n📊 REPORTE DE VALIDACIÓN:")
    print("-" * 40)
    
    todo_ok = True
    for descripcion, estado in validaciones:
        icono = "✅" if estado else "❌"
        print(f"{icono} {descripcion}")
        if not estado:
            todo_ok = False
    
    print("-" * 40)
    
    if todo_ok:
        print("🎉 ¡SISTEMA COMPLETAMENTE INSTALADO Y VALIDADO!")
        print("\n🚀 Para iniciar el dashboard ejecuta:")
        print("   python ejecutar_dashboard.py")
        print("\n📊 O directamente:")
        print("   streamlit run streamlit_amazonas_dashboard.py")
    else:
        print("⚠️ Hay problemas en la instalación. Revisa los errores arriba.")
    
    return todo_ok

def mostrar_ayuda_post_instalacion():
    """Mostrar información útil después de la instalación"""
    help_text = """
╔══════════════════════════════════════════════════════════════════════════╗
║                       🌊 SISTEMA AMAZONAS INSTALADO 🌊                    ║
╚══════════════════════════════════════════════════════════════════════════╝

🚀 PARA INICIAR EL DASHBOARD:
   → python ejecutar_dashboard.py
   → O: streamlit run streamlit_amazonas_dashboard.py

📊 ARCHIVOS PRINCIPALES:
   📈 streamlit_amazonas_dashboard.py  - Dashboard principal
   🗃️ data/                           - Datos del río Amazonas  
   ⚙️ config_amazonas.json           - Configuración del sistema
   📋 requirements.txt                - Dependencias

🔧 COMANDOS ÚTILES:
   🔄 Actualizar dependencias:  pip install -r requirements.txt --upgrade
   🧹 Limpiar temporales:       rm -rf temp/* (Linux/Mac) o del temp\\* (Windows)
   📝 Ver configuración:        cat config_amazonas.json

🎓 PARA LA PONENCIA:
   1. Ejecuta el dashboard con datos del Amazonas
   2. Demuestra la simulación interactiva
   3. Explica la metodología paso a paso
   4. Muestra el código fuente como herramienta didáctica

📧 SOPORTE:
   Si hay problemas, verifica:
   - Versión de Python (>= 3.8)
   - Instalación de dependencias
   - Archivos en directorio data/

🎉 ¡LISTO PARA REVOLUCIONAR LA DIDÁCTICA MATEMÁTICA!
"""
    print(help_text)

def main():
    """Función principal de configuración"""
    print("🌊 CONFIGURACIÓN DEL SISTEMA AMAZONAS")
    print("=" * 60)
    print("Metodología Integrada para Enseñanza de Matemática Avanzada")
    print("Caso: Transporte de Contaminantes en Canal Abierto")
    print("=" * 60)
    
    # Paso 1: Verificar Python
    if not verificar_python_version():
        return False
    
    # Paso 2: Verificar e instalar dependencias
    instaladas, faltantes = verificar_dependencias()
    
    if faltantes:
        respuesta = input(f"\n❓ Se encontraron {len(faltantes)} dependencias faltantes. ¿Instalar automáticamente? (s/n): ")
        if respuesta.lower() in ['s', 'si', 'y', 'yes']:
            if not instalar_dependencias(faltantes):
                print("❌ Error en la instalación de dependencias")
                return False
        else:
            print("⚠️ Algunas funcionalidades pueden no funcionar sin todas las dependencias")
    
    # Paso 3: Crear estructura
    crear_estructura_directorios()
    
    # Paso 4: Generar configuración
    config = generar_configuracion_sistema()
    
    # Paso 5: Crear archivos auxiliares
    crear_requirements_txt()
    crear_script_ejecutor()
    
    # Paso 6: Generar datos
    ejecutar_generador_datos()
    
    # Paso 7: Validar instalación completa
    sistema_ok = validar_instalacion()
    
    # Paso 8: Mostrar ayuda
    if sistema_ok:
        mostrar_ayuda_post_instalacion()
    
    return sistema_ok

if __name__ == "__main__":
    try:
        exito = main()
        sys.exit(0 if exito else 1)
    except KeyboardInterrupt:
        print("\n🛑 Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)