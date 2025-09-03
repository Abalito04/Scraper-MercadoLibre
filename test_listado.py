"""
Test de la Estructura Correcta: listado.mercadolibre.com.ar
"""

import requests
import time

def test_listado_urls():
    """Probar URLs de listado.mercadolibre.com.ar"""
    
    print("🎯 PROBANDO ESTRUCTURA CORRECTA: listado.mercadolibre.com.ar")
    print("="*60)
    
    base_urls = [
        # Estructura básica
        "https://listado.mercadolibre.com.ar/notebook",
        "https://listado.mercadolibre.com.ar/laptop",
        "https://listado.mercadolibre.com.ar/computacion",
        
        # Con categorías
        "https://listado.mercadolibre.com.ar/computacion/notebook",
        "https://listado.mercadolibre.com.ar/tecnologia/notebook",
        
        # Con parámetros
        "https://listado.mercadolibre.com.ar/notebook?price=100000-500000",
        "https://listado.mercadolibre.com.ar/notebook?sort=price_asc",
        "https://listado.mercadolibre.com.ar/notebook?_from=0",
        
        # Combinaciones
        "https://listado.mercadolibre.com.ar/notebook?price=100000-500000&sort=price_asc",
        "https://listado.mercadolibre.com.ar/notebook?condition=new&sort=price_desc",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for i, url in enumerate(base_urls, 1):
        print(f"\n{i:2d}. PROBANDO: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"    Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"    Tamaño: {len(content)} caracteres")
                
                # Verificar contenido
                if "ui-search-results" in content:
                    print("    ✅ ui-search-results encontrado")
                if "notebook" in content.lower() or "laptop" in content.lower():
                    print("    ✅ Contenido de notebook encontrado")
                if "precio" in content.lower() or "price" in content.lower():
                    print("    ✅ Información de precio encontrada")
                
                # Contar productos aproximados
                product_count = content.count("ui-search-results__item")
                if product_count > 0:
                    print(f"    ✅ Productos encontrados: ~{product_count}")
                
                print("    🎉 ¡URL FUNCIONA!")
                return url  # Retornar la primera URL que funcione
                
            else:
                print(f"    ❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        time.sleep(1)  # Pausa entre requests
    
    print("\n❌ Ninguna URL funcionó")
    return None

if __name__ == "__main__":
    working_url = test_listado_urls()
    
    if working_url:
        print(f"\n🎯 URL FUNCIONANDO: {working_url}")
        print("¡Esta es la estructura correcta para el scraper!")
    else:
        print("\n🚨 No se encontró ninguna URL funcional")
