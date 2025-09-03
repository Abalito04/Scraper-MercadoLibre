"""
Verificar contenido del CSV exportado
"""

import pandas as pd

def check_csv():
    """Verificar el CSV exportado"""
    
    try:
        df = pd.read_csv('productos.csv')
        
        print("📊 ANÁLISIS DEL CSV EXPORTADO")
        print("="*50)
        
        print(f"Total de productos: {len(df)}")
        print(f"Columnas: {df.columns.tolist()}")
        
        print("\n🔍 PRIMERAS 3 FILAS:")
        print(df[['title', 'price_text', 'price']].head(3))
        
        print(f"\n💰 ANÁLISIS DE PRECIOS:")
        print(f"Precios extraídos (price): {df['price'].notna().sum()}/{len(df)}")
        print(f"Precios en texto (price_text): {df['price_text'].notna().sum()}/{len(df)}")
        
        if df['price'].notna().sum() > 0:
            print(f"Precio mínimo: ${df['price'].min():,.0f}")
            print(f"Precio máximo: ${df['price'].max():,.0f}")
            print(f"Precio promedio: ${df['price'].mean():,.0f}")
        
        print(f"\n📍 ANÁLISIS DE UBICACIÓN:")
        print(f"Ubicaciones encontradas: {df['location'].notna().sum()}/{len(df)}")
        if df['location'].notna().sum() > 0:
            print("Ubicaciones únicas:")
            print(df['location'].value_counts().head(5))
        
        print(f"\n🏷️ ANÁLISIS DE CONDICIÓN:")
        print(f"Condiciones encontradas: {df['condition'].notna().sum()}/{len(df)}")
        if df['condition'].notna().sum() > 0:
            print("Condiciones únicas:")
            print(df['condition'].value_counts().head(5))
        
        print(f"\n🔗 ANÁLISIS DE URLS:")
        print(f"URLs encontradas: {df['url'].notna().sum()}/{len(df)}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_csv()
