"""
Analizar estructura HTML de MercadoLibre
"""

from bs4 import BeautifulSoup

def analyze_html():
    """Analizar el HTML guardado"""
    
    try:
        with open('mercadolibre_debug.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        print("🔍 ANALIZANDO ESTRUCTURA HTML")
        print("="*50)
        
        # Buscar contenedores
        containers = soup.select(".ui-search-layout__item")
        print(f"Contenedores encontrados: {len(containers)}")
        
        if containers:
            # Analizar el primer contenedor
            first_container = containers[0]
            print(f"\n📦 PRIMER CONTENEDOR:")
            print(f"Tag: {first_container.name}")
            print(f"Clases: {first_container.get('class', [])}")
            
            # Buscar título
            title = first_container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if title:
                print(f"Título encontrado: {title.name} -> {title.get_text(strip=True)[:100]}")
            
            # Buscar precio
            price = first_container.find(class_=lambda x: x and 'price' in x.lower())
            if price:
                print(f"Precio encontrado: {price.get('class', [])} -> {price.get_text(strip=True)[:50]}")
            
            # Buscar enlace
            link = first_container.find('a', href=True)
            if link:
                print(f"Enlace encontrado: {link.get('href')[:100]}")
            
            # Mostrar HTML del contenedor
            print(f"\n📄 HTML del contenedor:")
            print(first_container.prettify()[:1000])
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_html()
