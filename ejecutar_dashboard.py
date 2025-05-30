#!/usr/bin/env python3
"""
Script para ejecutar el Dashboard del Amazonas
"""
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
        print("\n🛑 Dashboard detenido por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    ejecutar_dashboard()
