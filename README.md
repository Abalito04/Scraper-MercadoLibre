# 🚀 MercadoLibre Scraper - Argentina

**Scraper profesional** para MercadoLibre Argentina desarrollado con **requests + BeautifulSoup** y **interfaz gráfica Tkinter**.

## ✨ Características

- 🔍 **Búsqueda avanzada** con múltiples filtros
- 💰 **Filtros de precio** (mínimo y máximo)
- 📱 **Filtros de condición** (nuevo, usado, reacondicionado)
- 📊 **Ordenamiento** por relevancia, precio ascendente/descendente
- 📄 **Paginación** configurable (hasta 20 páginas)
- 📁 **Exportación** a CSV y Excel
- 🎨 **Interfaz gráfica** moderna y intuitiva
- 🛡️ **Anti-detección** con User-Agents rotativos
- ⚡ **Sin dependencias** de navegadores (Chrome/Selenium)

## 🛠️ Tecnologías

- **Python 3.8+**
- **requests** - HTTP requests
- **BeautifulSoup4** - Parsing HTML
- **pandas** - Manipulación de datos
- **openpyxl** - Exportación a Excel
- **Tkinter** - Interfaz gráfica

## 📦 Instalación

### 1. Clonar/Descargar
```bash
git clone <repository-url>
cd MercadoLibre-Scraper
```

### 2. Instalar dependencias
```bash
# Windows
install.bat

# Linux/Mac
pip install -r requirements.txt
```

### 3. Ejecutar
```bash
# Interfaz gráfica
python main.py

# Solo scraper (línea de comandos)
python scraper.py
```

## 🎯 Uso

### Interfaz Gráfica
1. **Ejecutar** `python main.py`
2. **Configurar** parámetros de búsqueda:
   - Término de búsqueda
   - Número de páginas
   - Rango de precios
   - Condición del producto
   - Ordenamiento
3. **Hacer clic** en "🔍 Iniciar Búsqueda"
4. **Exportar** resultados a CSV/Excel

### Línea de Comandos
```python
from scraper import MercadoLibreScraper

scraper = MercadoLibreScraper()

# Búsqueda básica
products = scraper.search_products(
    query="notebook",
    max_pages=3
)

# Búsqueda con filtros
products = scraper.search_products(
    query="smartphone",
    max_pages=5,
    min_price=50000,
    max_price=200000,
    condition="nuevo",
    sort_by="price_asc"
)

# Exportar
scraper.export_to_csv(products, "productos.csv")
scraper.export_to_excel(products, "productos.xlsx")
```

## 📊 Parámetros de Búsqueda

| Parámetro | Descripción | Valores |
|-----------|-------------|---------|
| `query` | Término de búsqueda | Texto libre |
| `max_pages` | Máximo de páginas | 1-20 |
| `min_price` | Precio mínimo | Número (pesos argentinos) |
| `max_price` | Precio máximo | Número (pesos argentinos) |
| `condition` | Condición del producto | `all`, `nuevo`, `usado` |
| `sort_by` | Ordenamiento | `relevance`, `price_asc`, `price_desc` |

## 📁 Estructura del Proyecto

```
MercadoLibre-Scraper/
├── scraper.py          # Core del scraper
├── main.py             # Interfaz gráfica
├── requirements.txt    # Dependencias
├── install.bat        # Instalador Windows
├── README.md          # Documentación
└── productos.csv      # Resultados exportados
```

## 🔧 Configuración Avanzada

### Personalizar User-Agents
```python
# En scraper.py, modificar la lista de User-Agents
self.user_agents = [
    'Tu User-Agent personalizado aquí',
    # ... más User-Agents
]
```

### Ajustar delays
```python
# Modificar tiempos de espera entre requests
time.sleep(random.uniform(2, 4))  # 2-4 segundos
```

## 🚨 Limitaciones y Consideraciones

- **Respetar robots.txt** de MercadoLibre
- **No hacer requests excesivos** (máximo 20 páginas por búsqueda)
- **Usar filtros** para reducir resultados
- **Exportar datos** para análisis offline

## 📝 Logs

El scraper genera logs detallados en `scraper.log`:
- Requests realizados
- Productos encontrados
- Errores y advertencias
- Estadísticas de uso

## 🤝 Contribuciones

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## ⚠️ Disclaimer

Este scraper es para **uso educativo y personal**. Respeta los términos de servicio de MercadoLibre y las leyes de tu jurisdicción.

## 🆘 Soporte

- **Issues**: Reportar bugs en GitHub
- **Discussions**: Preguntas y sugerencias
- **Wiki**: Documentación adicional

---

**Desarrollado con ❤️ para la comunidad argentina**
