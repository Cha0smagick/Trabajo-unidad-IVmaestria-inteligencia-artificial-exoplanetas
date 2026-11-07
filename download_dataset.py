"""
Script para descargar el dataset Kepler Exoplanet Search Results de Kaggle.
Requiere: pip install kaggle
Y configurar credenciales: https://www.kaggle.com/settings/account -> Create New Token -> kaggle.json en ~/.kaggle/
"""
import os
from pathlib import Path

def download_dataset():
    try:
        import kaggle
        print("Descargando dataset NASA Kepler Exoplanet Search Results...")
        kaggle.api.dataset_download_files(
            'nasa/kepler-exoplanet-search-results',
            path='.',
            unzip=True
        )
        print("✓ Dataset descargado y descomprimido en el directorio actual")
        
        # Verificar archivo principal
        csv_path = Path('cumulative.csv')
        if csv_path.exists():
            size_mb = csv_path.stat().st_size / (1024*1024)
            print(f"✓ cumulative.csv encontrado ({size_mb:.1f} MB)")
        else:
            print("⚠ cumulative.csv no encontrado tras descarga")
            
    except ImportError:
        print("✗ Módulo 'kaggle' no instalado. Ejecuta: pip install kaggle")
        print("\nAlternativa manual:")
        print("1. Ve a https://www.kaggle.com/datasets/nasa/kepler-exoplanet-search-results")
        print("2. Click 'Download' -> 'cumulative.csv'")
        print("3. Coloca el archivo en esta carpeta")
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nVerifica que tienes kaggle.json en ~/.kaggle/ (Linux/Mac) o %USERPROFILE%\\.kaggle\\ (Windows)")

if __name__ == '__main__':
    download_dataset()