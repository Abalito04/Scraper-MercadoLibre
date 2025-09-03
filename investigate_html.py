"""
Investigación de Estructura HTML Real de MercadoLibre
Para encontrar los selectores CSS correctos
"""

import requests
from bs4 import BeautifulSoup
import re

def investigate_html_structure():
    """Investigar la estructura HTML real de MercadoLibre"""
    
    print("🔍 INVESTIGANDO ESTRUCTURA HTML REAL")
    print("="*60)
    
    url = "https://listado.mercadolibre.com.ar/notebook"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = response.text
            
            print(f"\nTamaño del contenido: {len(content)} caracteres")
            
            # 1. Buscar contenedores de productos
            print("\n1️⃣ BUSCANDO CONTENEDORES DE PRODUCTOS:")
            
            # Selectores antiguos
            old_selectors = [
                ".ui-search-results__item",
                ".ui-search-layout__item",
                "[data-testid='results-item']"
            ]
            
            for selector in old_selectors:
                elements = soup.select(selector)
                print(f"   {selector}: {len(elements)} elementos")
            
            # 2. Buscar nuevos selectores
            print("\n2️⃣ BUSCANDO NUEVOS SELECTORES:")
            
            # Buscar elementos con clases que contengan "item", "product", "result"
            item_classes = soup.find_all(class_=re.compile(r'item|product|result|card', re.I))
            if item_classes:
                print(f"   Elementos con clases de item/product/result: {len(item_classes)}")
                for i, elem in enumerate(item_classes[:3]):
                    classes = ' '.join(elem.get('class', []))
                    print(f"      {i+1}. Clases: {classes}")
            
            # 3. Buscar elementos con data-testid
            print("\n3️⃣ BUSCANDO DATA-TESTID:")
            testid_elements = soup.find_all(attrs={"data-testid": True})
            if testid_elements:
                print(f"   Elementos con data-testid: {len(testid_elements)}")
                for i, elem in enumerate(testid_elements[:5]):
                    testid = elem.get('data-testid')
                    tag = elem.name
                    classes = ' '.join(elem.get('class', []))
                    print(f"      {i+1}. {tag} data-testid='{testid}' class='{classes}'")
            
            # 4. Buscar títulos de productos
            print("\n4️⃣ BUSCANDO TÍTULOS DE PRODUCTOS:")
            title_selectors = [
                "h1", "h2", "h3", "h4", "h5", "h6",
                ".title", ".name", ".product-title", ".item-title",
                "[class*='title']", "[class*='name']"
            ]
            
            for selector in title_selectors:
                elements = soup.select(selector)
                if elements:
                    print(f"   {selector}: {len(elements)} elementos")
                    for i, elem in enumerate(elements[:2]):
                        text = elem.get_text(strip=True)[:50]
                        if text and len(text) > 5:
                            print(f"      {i+1}. {text}")
            
            # 5. Buscar precios
            print("\n5️⃣ BUSCANDO PRECIOS:")
            price_selectors = [
                ".price", ".cost", ".value", ".amount",
                "[class*='price']", "[class*='cost']", "[class*='value']"
            ]
            
            for selector in price_selectors:
                elements = soup.select(selector)
                if elements:
                    print(f"   {selector}: {len(elements)} elementos")
                    for i, elem in enumerate(elements[:2]):
                        text = elem.get_text(strip=True)[:30]
                        if text and any(char.isdigit() for char in text):
                            print(f"      {i+1}. {text}")
            
            # 6. Buscar enlaces
            print("\n6️⃣ BUSCANDO ENLACES:")
            links = soup.find_all('a', href=True)
            product_links = [link for link in links if 'mercadolibre.com.ar' in link.get('href')]
            if product_links:
                print(f"   Enlaces de productos: {len(product_links)}")
                for i, link in enumerate(product_links[:3]):
                    href = link.get('href')
                    text = link.get_text(strip=True)[:50]
                    print(f"      {i+1}. {href} -> {text}")
            
            # 7. Guardar HTML para análisis manual
            print("\n7️⃣ GUARDANDO HTML PARA ANÁLISIS:")
            with open("mercadolibre_debug.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("   HTML guardado en: mercadolibre_debug.html")
            
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    investigate_html_structure()
