"""
Test Exhaustivo de URLs de MercadoLibre
Para encontrar el formato correcto
"""

import requests
import time

def test_url(url, description):
    """Probar una URL y mostrar el resultado"""
    print(f"\n{'='*60}")
    print(f"PROBANDO: {description}")
    print(f"URL: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            if "notebook" in content.lower() or "laptop" in content.lower():
                print("✅ EXITO: Contenido encontrado")
                print(f"Tamaño: {len(content)} caracteres")
                # Buscar indicadores de productos
                if "ui-search-results" in content:
                    print("✅ Encontrado: ui-search-results")
                if "productos" in content.lower():
                    print("✅ Encontrado: productos")
                if "precio" in content.lower():
                    print("✅ Encontrado: precio")
            else:
                print("❌ No se encontró contenido relevante")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)  # Pausa entre requests

def main():
    """Probar todas las variaciones de URL"""
    print("🚀 INICIANDO PRUEBAS EXHAUSTIVAS DE URLS")
    print("="*60)
    
    base_urls = [
        # Formato 1: /listado/
        "https://www.mercadolibre.com.ar/listado/notebook",
        "https://www.mercadolibre.com.ar/listado/notebooks",
        "https://www.mercadolibre.com.ar/listado/laptop",
        
        # Formato 2: /search/
        "https://www.mercadolibre.com.ar/search?q=notebook",
        "https://www.mercadolibre.com.ar/search?query=notebook",
        "https://www.mercadolibre.com.ar/search?keywords=notebook",
        
        # Formato 3: /buscar/
        "https://www.mercadolibre.com.ar/buscar?q=notebook",
        "https://www.mercadolibre.com.ar/buscar?query=notebook",
        
        # Formato 4: Sin prefijo
        "https://www.mercadolibre.com.ar/notebook",
        "https://www.mercadolibre.com.ar/notebooks",
        
        # Formato 5: Con categoría
        "https://www.mercadolibre.com.ar/computacion/notebook",
        "https://www.mercadolibre.com.ar/tecnologia/notebook",
        
        # Formato 6: Con parámetros básicos
        "https://www.mercadolibre.com.ar/listado/notebook?_from=0",
        "https://www.mercadolibre.com.ar/search?q=notebook&_from=0",
        
        # Formato 7: Con filtros de precio
        "https://www.mercadolibre.com.ar/listado/notebook?price=100000-500000",
        "https://www.mercadolibre.com.ar/search?q=notebook&price=100000-500000",
        
        # Formato 8: Con ordenamiento
        "https://www.mercadolibre.com.ar/listado/notebook?sort=price_asc",
        "https://www.mercadolibre.com.ar/search?q=notebook&sort=price_asc",
    ]
    
    for i, url in enumerate(base_urls, 1):
        test_url(url, f"Formato {i}")
        
        if i % 5 == 0:  # Pausa cada 5 requests
            print("\n⏸️ Pausa de 3 segundos...")
            time.sleep(3)
    
    print(f"\n{'='*60}")
    print("🏁 PRUEBAS COMPLETADAS")
    print("="*60)

if __name__ == "__main__":
    main()
