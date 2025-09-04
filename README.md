# 🚀 Scraper MercadoLibre Argentina

**Scraper profesional** para extraer productos de MercadoLibre Argentina usando **requests + BeautifulSoup** con interfaz gráfica **Tkinter**.

## ✨ Características

- 🔍 **Búsqueda inteligente**: Extrae productos por término de búsqueda
- 💰 **Filtros de precio**: Rango mínimo y máximo personalizable
- 📊 **Ordenamiento**: Por relevancia, precio ascendente/descendente
- 💾 **Exportación múltiple**: CSV, Excel (XLSX) y JSON
- 🎨 **Interfaz gráfica**: Tkinter moderno y fácil de usar
- 🚫 **Sin Selenium**: Usa requests + BeautifulSoup (más estable)
- 🇦🇷 **Formato argentino**: Maneja precios con separadores de miles

## 🛠️ Tecnologías

- **Python 3.8+**
- **requests**: HTTP requests
- **BeautifulSoup4**: Parsing HTML
- **pandas**: Manipulación de datos
- **openpyxl**: Exportación a Excel
- **Tkinter**: Interfaz gráfica

## 📦 Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/tu-usuario/scraper-mercadolibre.git
cd scraper-mercadolibre
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar
```bash
python main.py
```

## 🚀 Uso

### Interfaz Gráfica (Recomendado)
```bash
python main.py
```

### Línea de Comandos
```bash
python scraper.py
```

## 📋 Funcionalidades

### 🔍 Búsqueda
- **Término**: Cualquier producto (notebook, celular, etc.)
- **Páginas**: Hasta 10 páginas (configurable)
- **Filtros**: Precio mínimo y máximo
- **Condición**: Nuevo, Usado, Reacondicionado, o Todos
- **Orden**: Relevancia, precio ↑↓

### 💾 Exportación
- **CSV**: Formato estándar con encoding UTF-8
- **Excel**: Archivo .xlsx con formato profesional
- **JSON**: Estructura de datos completa

### 📊 Datos Extraídos
- **Título**: Nombre completo del producto
- **Precio**: Precio limpio en pesos argentinos
- **URL**: Enlace directo al producto

## 🎯 Ejemplos de Uso

### Búsqueda Básica
```python
from scraper import MercadoLibreScraper

scraper = MercadoLibreScraper()
products = scraper.search_products(
    query="notebook",
    max_pages=3
)
```

### Con Filtros de Precio y Condición
```python
# Solo productos usados
products = scraper.search_products(
    query="notebook",
    max_pages=2,
    min_price=50000,
    max_price=200000,
    condition_filter="usado"
)

# Solo productos nuevos
products = scraper.search_products(
    query="celular",
    max_pages=3,
    condition_filter="nuevo"
)
```

### Exportación
```python
# CSV
scraper.export_to_csv(products, "productos.csv")

# Excel
scraper.export_to_csv(products, "productos.xlsx")
```

## 📁 Estructura del Proyecto

```
scraper-mercadolibre/
├── main.py              # Interfaz gráfica Tkinter
├── scraper.py           # Lógica del scraper
├── requirements.txt     # Dependencias Python
├── README.md           # Este archivo
└── .gitignore          # Archivos a ignorar
```

## 🔧 Configuración

### Headers Personalizados
```python
self.session.headers.update({
    'User-Agent': 'Tu User-Agent personalizado',
    'Accept-Language': 'es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3',
})
```

### Delays Configurables
```python
# Delay entre páginas (1-3 segundos)
delay = random.uniform(1, 3)
time.sleep(delay)
```

## ⚠️ Consideraciones

- **Respeto**: Usar delays razonables entre requests
- **Términos de Servicio**: Cumplir con las políticas de MercadoLibre
- **Uso Responsable**: No sobrecargar los servidores
- **Propósito Educativo**: Solo para aprendizaje y uso personal

## 🐛 Solución de Problemas

### Error de Codificación
```bash
# En Windows, usar encoding UTF-8
python -X utf8 main.py
```

### Dependencias Faltantes
```bash
pip install --upgrade -r requirements.txt
```

### Problemas de Red
- Verificar conexión a internet
- Revisar firewall/antivirus
- Usar VPN si es necesario

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! 

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **MercadoLibre**: Por proporcionar la plataforma
- **BeautifulSoup**: Por el excelente parser HTML
- **Python Community**: Por las librerías increíbles

## 📞 Contacto

- **GitHub**: [@Abalito04](https://github.com/Abalito04)
- **Email**: abalito95@gmail.com
- **Proyecto**: [Link al proyecto](https://github.com/Abalito04/Scraper-MercadoLibre)

---

⭐ **¡Si te gusta el proyecto, dale una estrella en GitHub!** ⭐
