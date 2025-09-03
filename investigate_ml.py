"""
Investigación Profunda de MercadoLibre
Para encontrar la estructura real de URLs
"""

import requests
from bs4 import BeautifulSoup
import re

def investigate_mercadolibre():
    """Investigar la página principal de MercadoLibre"""
    
    print("🔍 INVESTIGANDO ESTRUCTURA REAL DE MERCADOLIBRE")
    print("="*60)
    
    # 1. Página principal
    print("\n1️⃣ PAGINA PRINCIPAL:")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get("https://www.mercadolibre.com.ar", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar formulario de búsqueda
            search_form = soup.find('form')
            if search_form:
                print("✅ Formulario de búsqueda encontrado")
                action = search_form.get('action', 'No action')
                print(f"Action: {action}")
                
                # Buscar input de búsqueda
                search_input = soup.find('input', {'name': re.compile(r'q|query|search', re.I)})
                if search_input:
                    print(f"✅ Input de búsqueda: {search_input.get('name')}")
            
            # Buscar enlaces de categorías
            categories = soup.find_all('a', href=re.compile(r'computacion|tecnologia|notebook|laptop', re.I))
            if categories:
                print(f"✅ Enlaces de categorías encontrados: {len(categories)}")
                for cat in categories[:3]:
                    print(f"   - {cat.get('href')} -> {cat.get_text(strip=True)[:50]}")
            
            # Buscar enlaces de búsqueda
            search_links = soup.find_all('a', href=re.compile(r'search|buscar|listado', re.I))
            if search_links:
                print(f"✅ Enlaces de búsqueda encontrados: {len(search_links)}")
                for link in search_links[:3]:
                    print(f"   - {link.get('href')} -> {link.get_text(strip=True)[:50]}")
            
            # Buscar JavaScript que construya URLs
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and ('search' in script.string.lower() or 'url' in script.string.lower()):
                    print("✅ Script con lógica de búsqueda encontrado")
                    break
            
        else:
            print(f"❌ Error al acceder a página principal: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Probar búsqueda directa
    print("\n2️⃣ BÚSQUEDA DIRECTA:")
    test_urls = [
        "https://www.mercadolibre.com.ar/s/notebook",
        "https://www.mercadolibre.com.ar/s?q=notebook",
        "https://www.mercadolibre.com.ar/s?query=notebook",
        "https://www.mercadolibre.com.ar/s?search=notebook",
        "https://www.mercadolibre.com.ar/s?keywords=notebook",
        "https://www.mercadolibre.com.ar/s?term=notebook",
        "https://www.mercadolibre.com.ar/s?text=notebook",
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"URL: {url}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                if "notebook" in content.lower() or "laptop" in content.lower():
                    print("✅ EXITO: Contenido encontrado")
                    if "ui-search-results" in content:
                        print("✅ Encontrado: ui-search-results")
                    break
                else:
                    print("❌ No se encontró contenido relevante")
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)
    
    print("\n🏁 INVESTIGACIÓN COMPLETADA")

if __name__ == "__main__":
    investigate_mercadolibre()
