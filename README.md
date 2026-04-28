# 🔍 MercadoLibre Scraper

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-4.12-brightgreen?style=flat-square)](https://www.crummy.com/software/BeautifulSoup/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

> **EN:** A Python tool that automatically scrapes product listings from [MercadoLibre](https://www.mercadolibre.com.ar/) and exports the results to a clean Excel/CSV file ready for analysis.
>
> **ES:** Herramienta en Python que extrae automáticamente publicaciones de [MercadoLibre](https://www.mercadolibre.com.ar/) y exporta los resultados a un archivo Excel/CSV listo para analizar.

---

## ✨ Features · Características

- ✅ Scrapes **product titles, prices, links, and seller info** from search results
- ✅ Supports **pagination** — scrapes multiple pages automatically
- ✅ Exports clean data to **Excel (.xlsx) and CSV**
- ✅ Built-in **duplicate removal** and data cleaning
- ✅ Simple CLI interface — just enter a search keyword
- ✅ Respects rate limits with request delays

---

## 📸 Example Output · Ejemplo de salida

| Title | Price (ARS) | Link | Seller |
|-------|------------|------|--------|
| Casco Moto LS2 FF320 | $ 85,000 | mercadolibre.com/... | TiendaMotos |
| Casco Bell MX-9 | $ 120,000 | mercadolibre.com/... | HelmetsPro |
| ... | ... | ... | ... |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/Abalito04/Scraper-MercadoLibre.git
cd Scraper-MercadoLibre

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the scraper
python main.py
```

### Usage

```bash
$ python main.py

🔍 Enter search keyword: casco moto
📄 How many pages to scrape? [default: 5]: 3

⏳ Scraping page 1...
⏳ Scraping page 2...
⏳ Scraping page 3...

✅ Done! 147 products found.
💾 Saved to: casco_moto_2025-09-04.xlsx
```

---

## 📦 Dependencies

```
requests==2.31.0
beautifulsoup4==4.12.2
pandas==2.0.3
openpyxl==3.1.2
lxml==4.9.3
urllib3==2.0.7
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
Scraper-MercadoLibre/
├── main.py              # Entry point — CLI interface
├── scraper.py           # Core scraping logic
├── requirements.txt     # Python dependencies
├── .gitignore
└── README.md
```

---

## 🔧 How It Works · Cómo funciona

1. **User inputs** a search keyword and number of pages
2. **`scraper.py`** sends HTTP requests to MercadoLibre search results
3. **BeautifulSoup** parses the HTML and extracts product data
4. **Pandas** cleans, deduplicates and structures the data
5. **Output** is exported to `.xlsx` and `.csv` with timestamp in filename

---

## 📌 Notes

- This scraper is intended for **personal and educational use only**
- MercadoLibre's structure may change over time and require selector updates
- Add delays between requests to avoid getting rate-limited

---

## 👨‍💻 Author

**Matias Abalo** — [@Abalito04](https://github.com/Abalito04)

🌐 [Portfolio](https://matiabalo.up.railway.app/) · ✉️ [abalito95@gmail.com](mailto:abalito95@gmail.com)
