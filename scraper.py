"""
Scraper de MercadoLibre Argentina usando requests + BeautifulSoup
Solo extrae: título, precio limpio, URL
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import random
from urllib.parse import quote_plus


class MercadoLibreScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def _build_url(self, query, page=1, sort_by="relevance"):
        """Construir URL de búsqueda"""
        base_url = "https://listado.mercadolibre.com.ar"
        
        # Codificar query
        encoded_query = quote_plus(query)
        
        # Construir URL
        if page == 1:
            url = f"{base_url}/{encoded_query}"
        else:
            url = f"{base_url}/{encoded_query}_Desde_{(page-1)*50+1}"
        
        # Agregar ordenamiento
        if sort_by == "price_asc":
            url += "_OrderId_PRICE_ASC"
        elif sort_by == "price_desc":
            url += "_OrderId_PRICE_DESC"
        
        return url
    
    def _clean_price(self, price_text):
        """Extraer precio limpio del texto completo - VERSIÓN CORREGIDA"""
        try:
            # Buscar precios con formato argentino (ej: $1.618.695)
            price_pattern = r'\$([\d]{1,3}(?:\.\d{3})*)'
            price_matches = re.findall(price_pattern, price_text)
            
            print(f"Precios encontrados con regex corregida: {price_matches}")
            
            if not price_matches:
                print(f"No se encontraron precios válidos en: {price_text}")
                return None
            
            # Tomar el PRIMER precio (precio original, no la oferta)
            first_price = price_matches[0]
            print(f"Primer precio encontrado: {first_price}")
            
            # Limpiar el precio - SOLO NÚMEROS Y PUNTOS
            cleaned = re.sub(r'[^\d.]', '', first_price)
            print(f"Precio limpio: {cleaned}")
            
            # Convertir formato argentino (puntos como separadores de miles)
            if '.' in cleaned:
                # Remover todos los puntos (separadores de miles)
                cleaned = cleaned.replace('.', '')
                print(f"Puntos removidos (formato argentino): {cleaned}")
            
            # Convertir a float
            price_float = float(cleaned)
            print(f"Precio convertido a float: {price_float}")
            
            # Verificar que el precio sea razonable (entre 100 y 10,000,000 pesos)
            if 100 <= price_float <= 10000000:
                print(f"Precio válido: ${price_float:,.0f}")
                return price_float
            else:
                print(f"Precio fuera de rango: {price_float}")
                return None
                
        except Exception as e:
            print(f"Error limpiando precio '{price_text}': {e}")
            return None
    
    def _detect_condition_advanced(self, container, title, price_text):
        """Detectar condición en múltiples lugares: título, precio, atributos, badges"""
        try:
            # 1. BUSCAR EN ATRIBUTOS/BADGES DE CONDICIÓN (PRIORIDAD ALTA)
            condition_selectors = [
                ".condition-badge",
                ".product-condition", 
                ".item-condition",
                ".condition-label",
                ".status-badge",
                ".product-status",
                "[data-testid*='condition']",
                ".ui-pdp-seller__item-description",
                ".ui-pdp-seller__item-title"
            ]
            
            condition_from_badge = None
            for selector in condition_selectors:
                elem = container.select_one(selector)
                if elem:
                    badge_text = elem.get_text(strip=True).lower()
                    if any(word in badge_text for word in ['usado', 'used', 'nuevo', 'new', 'reacondicionado']):
                        condition_from_badge = badge_text
                        print(f"Condición encontrada en badge: {badge_text}")
                        break
            
            # 2. BUSCAR EN EL TEXTO COMPLETO DEL CONTENEDOR
            container_text = container.get_text().lower()
            
            # 3. ANÁLISIS INTELIGENTE COMBINADO
            text_to_analyze = f"{title} {price_text} {container_text}".lower()
            
            # Patrones para condición NUEVA
            new_patterns = [
                r'\b(nuevo|new|original|originales|sellado|sellados|sealed|factory|fábrica)\b',
                r'\b(garantía|warranty|garantizado|garantizada)\b',
                r'\b(estado perfecto|perfect condition|mint|excelente)\b'
            ]
            
            # Patrones para condición USADA
            used_patterns = [
                r'\b(usado|used|segunda mano|second hand|pre-owned|preowned)\b',
                r'\b(seminuevo|semi-nuevo|like new|como nuevo)\b',
                r'\b(estado bueno|good condition|funcionando|working)\b',
                r'\b(para repuesto|for parts|spare parts)\b'  # ¡NUEVO PATRÓN!
            ]
            
            # Patrones para condición REACONDICIONADA
            refurbished_patterns = [
                r'\b(reacondicionado|refurbished|remanufactured|restored)\b',
                r'\b(reparado|repaired|rebuilt|reconstruido)\b',
                r'\b(garantía limitada|limited warranty|reconditioned)\b'
            ]
            
            # Buscar coincidencias
            new_matches = sum(len(re.findall(pattern, text_to_analyze)) for pattern in new_patterns)
            used_matches = sum(len(re.findall(pattern, text_to_analyze)) for pattern in used_patterns)
            refurbished_matches = sum(len(re.findall(pattern, text_to_analyze)) for pattern in refurbished_patterns)
            
            # 4. PRIORIZAR CONDICIÓN DEL BADGE SI EXISTE
            if condition_from_badge:
                if any(word in condition_from_badge for word in ['usado', 'used']):
                    print(f"✅ Condición detectada desde badge: Usado (Confianza: Muy Alta)")
                    return "Usado"
                elif any(word in condition_from_badge for word in ['nuevo', 'new']):
                    print(f"✅ Condición detectada desde badge: Nuevo (Confianza: Muy Alta)")
                    return "Nuevo"
                elif any(word in condition_from_badge for word in ['reacondicionado', 'refurbished']):
                    print(f"✅ Condición detectada desde badge: Reacondicionado (Confianza: Muy Alta)")
                    return "Reacondicionado"
            
            # 5. ANÁLISIS POR PATRONES SI NO HAY BADGE
            if new_matches > 0 and new_matches > used_matches and new_matches > refurbished_matches:
                condition = "Nuevo"
                confidence = "Alta"
            elif used_matches > 0 and used_matches > new_matches and used_matches > refurbished_matches:
                condition = "Usado"
                confidence = "Alta"
            elif refurbished_matches > 0 and refurbished_matches > new_matches and refurbished_matches > used_matches:
                condition = "Reacondicionado"
                confidence = "Alta"
            else:
                # Análisis adicional basado en contexto
                if any(word in text_to_analyze for word in ['oferta', 'descuento', 'liquidación']):
                    condition = "Nuevo (Probable)"
                    confidence = "Media"
                elif any(word in text_to_analyze for word in ['cuotas', 'financiación', 'tarjeta']):
                    condition = "Nuevo (Probable)"
                    confidence = "Media"
                else:
                    condition = "No especificada"
                    confidence = "Baja"
            
            print(f"Condición detectada por patrones: {condition} (Confianza: {confidence})")
            return condition
            
        except Exception as e:
            print(f"Error detectando condición avanzada: {e}")
            return "No especificada"
    
    def _extract_products(self, soup):
        """Extraer productos de la página"""
        products = []
        
        # Buscar contenedores de productos
        containers = soup.select("li.ui-search-layout__item")
        
        if not containers:
            print("No se encontraron contenedores de productos")
            return products
        
        print(f"Encontrados {len(containers)} contenedores de productos")
        
        for container in containers:
            try:
                product = {}
                
                # Titulo - SELECTOR EXACTO
                title_elem = container.select_one("h3.poly-component__title-wrapper")
                if title_elem:
                    product['title'] = title_elem.get_text(strip=True)
                
                # Precio - SELECTOR EXACTO
                price_elem = container.select_one(".poly-component__price")
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    product['price_text'] = price_text
                    product['price'] = self._clean_price(price_text)
                
                # Condición - DETECCIÓN INTELIGENTE EN MÚLTIPLES LUGARES
                condition = self._detect_condition_advanced(container, product.get('title', ''), product.get('price_text', ''))
                product['condition'] = condition
                
                # URL - SELECTOR EXACTO
                link_elem = container.select_one("a.poly-component__title")
                if link_elem:
                    href = link_elem.get('href')
                    if href:
                        product['url'] = href  # URL completa ya está en href
                
                if product.get('title'):
                    products.append(product)
                    print(f"Producto encontrado: {product.get('title', '')[:50]}...")
                    print(f"  Precio: {product.get('price_text', 'N/A')[:30]}")
                    print(f"  Precio limpio: {product.get('price', 'N/A')}")
                    print(f"  Condición: {product.get('condition', 'N/A')}")
                    
            except Exception as e:
                print(f"Error procesando producto: {e}")
                continue
        
        return products
    
    def search_products(self, query, max_pages=3, min_price=None, max_price=None, sort_by="relevance", condition_filter="all"):
        """Buscar productos con filtros de precio y condición"""
        all_products = []
        
        for page in range(1, max_pages + 1):
            try:
                print(f"\n--- Página {page} ---")
                
                # Construir URL
                url = self._build_url(query, page, sort_by)
                print(f"URL: {url}")
                
                # Hacer request
                response = self.session.get(url)
                response.raise_for_status()
                
                # Parsear HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extraer productos
                products = self._extract_products(soup)
                
                if products:
                    all_products.extend(products)
                    print(f"Página {page}: {len(products)} productos")
                else:
                    print(f"Página {page}: No se encontraron productos")
                    break
                
                # Delay aleatorio
                if page < max_pages:
                    delay = random.uniform(1, 3)
                    print(f"Esperando {delay:.1f} segundos...")
                    time.sleep(delay)
                
            except Exception as e:
                print(f"Error en página {page}: {e}")
                continue
        
        # Aplicar filtros de precio y condición
        filtered_products = []
        for product in all_products:
            # Filtro de precio
            price = product.get('price')
            if min_price and price and price < min_price:
                continue
            if max_price and price and price > max_price:
                continue
            
            # Filtro de condición
            if condition_filter != "all":
                product_condition = product.get('condition', '').lower()
                if condition_filter not in product_condition:
                    continue
            
            filtered_products.append(product)
        
        all_products = filtered_products
        
        print(f"\nTotal productos después de filtros: {len(all_products)}")
        print(f"Filtros aplicados: Precio({min_price or 'sin límite'}-{max_price or 'sin límite'}), Condición({condition_filter})")
        return all_products
    
    def export_to_csv(self, products, filename="productos.csv"):
        if products:
            df = pd.DataFrame(products)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Exportado a CSV: {filename}")
            return True
        return False
    
    def export_to_excel(self, products, filename="productos.xlsx"):
        if products:
            df = pd.DataFrame(products)
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"Exportado a Excel: {filename}")
            return True
        return False


if __name__ == "__main__":
    print("Probando scraper con EXTRACCIÓN COMPLETA...")
    
    scraper = MercadoLibreScraper()
    
    try:
        # Prueba con extracción completa
        products = scraper.search_products(
            query="notebook",
            max_pages=1
        )
        
        if products:
            print(f"EXITO: {len(products)} productos")
            scraper.export_to_csv(products)
        else:
            print("No se encontraron productos")
    
    except Exception as e:
        print(f"Error: {e}")
