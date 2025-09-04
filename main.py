"""
Interfaz Gráfica para Scraper de MercadoLibre
Solo 3 columnas: Título, Precio, URL
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
from scraper import MercadoLibreScraper


class MercadoLibreGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scraper MercadoLibre Argentina")
        self.root.geometry("900x700")
        
        # Variables
        self.products = []
        self.scraper = MercadoLibreScraper()
        self.sort_column = None  # Columna actualmente ordenada
        self.sort_order = "none"  # "none", "asc", "desc"
        
        # Crear interfaz
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Frame de búsqueda
        search_frame = ttk.LabelFrame(main_frame, text="Búsqueda", padding="10")
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        # Término de búsqueda
        ttk.Label(search_frame, text="Buscar:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.search_var = tk.StringVar(value="notebook")
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Páginas
        ttk.Label(search_frame, text="Páginas:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.pages_var = tk.StringVar(value="3")
        pages_spin = ttk.Spinbox(search_frame, from_=1, to=10, textvariable=self.pages_var, width=5)
        pages_spin.grid(row=0, column=3, padx=(0, 10))
        
        # Botón de búsqueda
        self.search_button = ttk.Button(search_frame, text="Buscar", command=self.start_search)
        self.search_button.grid(row=0, column=4)
        
        # Frame de filtros
        filters_frame = ttk.LabelFrame(main_frame, text="Filtros", padding="10")
        filters_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Precio mínimo
        ttk.Label(filters_frame, text="Precio mínimo:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.min_price_var = tk.StringVar()
        ttk.Entry(filters_frame, textvariable=self.min_price_var, width=15).grid(row=0, column=1, padx=(0, 10))
        
        # Precio máximo
        ttk.Label(filters_frame, text="Precio máximo:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.max_price_var = tk.StringVar()
        ttk.Entry(filters_frame, textvariable=self.max_price_var, width=15).grid(row=0, column=3, padx=(0, 10))
        
        # Filtro de Condición
        ttk.Label(filters_frame, text="Condición:").grid(row=0, column=4, sticky=tk.W, padx=(10, 5))
        self.condition_var = tk.StringVar(value="all")
        condition_combo = ttk.Combobox(filters_frame, textvariable=self.condition_var, 
                                      values=["all", "nuevo", "usado", "reacondicionado"], width=15)
        condition_combo.grid(row=0, column=5)
        
        # Frame de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Treeview para resultados (4 COLUMNAS: Título, Precio, Condición, URL)
        columns = ("Titulo", "Precio", "Condicion", "URL")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas - todas clickeables
        self.tree.heading("Titulo", text="Título del Producto ↑↓", command=lambda: self.sort_by_column("title"))
        self.tree.heading("Precio", text="Precio ↑↓", command=lambda: self.sort_by_column("price"))
        self.tree.heading("Condicion", text="Condición ↑↓", command=lambda: self.sort_by_column("condition"))
        self.tree.heading("URL", text="Enlace")
        
        # Configurar ancho de columnas
        self.tree.column("Titulo", width=350)
        self.tree.column("Precio", width=120)
        self.tree.column("Condicion", width=120)
        self.tree.column("URL", width=250)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid del treeview y scrollbar
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Frame de botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Botones de exportación
        ttk.Button(buttons_frame, text="Exportar a CSV", 
                  command=lambda: self.export_results("csv")).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Exportar a Excel", 
                  command=lambda: self.export_results("excel")).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Exportar a JSON", 
                  command=lambda: self.export_results("json")).pack(side=tk.LEFT)
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo para buscar")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def start_search(self):
        """Iniciar búsqueda en hilo separado"""
        if not self.search_var.get().strip():
            messagebox.showerror("Error", "Ingrese un término de búsqueda")
            return
        
        # Deshabilitar botón durante búsqueda
        self.search_button.config(state="disabled")
        self.status_var.set("Buscando...")
        
        # Limpiar resultados anteriores
        self.products = []
        self.update_results()
        
        # Iniciar búsqueda en hilo separado
        thread = threading.Thread(target=self.perform_search)
        thread.daemon = True
        thread.start()
    
    def perform_search(self):
        """Realizar búsqueda"""
        try:
            # Obtener parámetros
            query = self.search_var.get().strip()
            max_pages = int(self.pages_var.get())
            min_price = self.min_price_var.get().strip()
            max_price = self.max_price_var.get().strip()
            condition_filter = self.condition_var.get()
            
            # Convertir precios a números
            min_price = int(min_price) if min_price else None
            max_price = int(max_price) if max_price else None
            
            # Realizar búsqueda
            self.products = self.scraper.search_products(
                query=query,
                max_pages=max_pages,
                min_price=min_price,
                max_price=max_price,
                sort_by="relevance",  # Siempre buscar por relevancia, ordenar localmente
                condition_filter=condition_filter
            )
            
            # Actualizar interfaz en hilo principal
            self.root.after(0, self.search_completed)
            
        except Exception as e:
            self.root.after(0, lambda: self.search_error(str(e)))
    
    def search_completed(self):
        """Búsqueda completada"""
        self.search_button.config(state="normal")
        # Resetear ordenamiento
        self.sort_column = None
        self.sort_order = "none"
        self.update_column_headers()
        self.update_results()
        
        if self.products:
            self.status_var.set(f"Búsqueda completada: {len(self.products)} productos encontrados")
        else:
            self.status_var.set("Búsqueda completada: No se encontraron productos")
    
    def search_error(self, error_msg):
        """Error en búsqueda"""
        self.search_button.config(state="normal")
        self.status_var.set("Error en la búsqueda")
        messagebox.showerror("Error", f"Error durante la búsqueda:\n{error_msg}")
    
    def sort_by_column(self, column):
        """Ordenar productos por la columna especificada"""
        if not self.products:
            return
        
        # Si es la misma columna, cambiar orden; si es diferente, empezar con ascendente
        if self.sort_column == column:
            if self.sort_order == "asc":
                self.sort_order = "desc"
            else:
                self.sort_order = "asc"
        else:
            self.sort_column = column
            self.sort_order = "asc"
        
        # Ordenar según la columna
        if column == "price":
            # Ordenar por precio (numérico)
            if self.sort_order == "asc":
                self.products.sort(key=lambda x: x.get('price', 0) or 0)
            else:
                self.products.sort(key=lambda x: x.get('price', 0) or 0, reverse=True)
        elif column == "title":
            # Ordenar por título (alfabético)
            if self.sort_order == "asc":
                self.products.sort(key=lambda x: x.get('title', '').lower())
            else:
                self.products.sort(key=lambda x: x.get('title', '').lower(), reverse=True)
        elif column == "condition":
            # Ordenar por condición (agrupar)
            if self.sort_order == "asc":
                self.products.sort(key=lambda x: x.get('condition', '').lower())
            else:
                self.products.sort(key=lambda x: x.get('condition', '').lower(), reverse=True)
        
        # Actualizar indicadores visuales
        self.update_column_headers()
        
        # Actualizar la tabla
        self.update_results()
    
    def update_column_headers(self):
        """Actualizar los indicadores visuales de las columnas"""
        # Resetear todos los headers
        self.tree.heading("Titulo", text="Título del Producto ↑↓")
        self.tree.heading("Precio", text="Precio ↑↓")
        self.tree.heading("Condicion", text="Condición ↑↓")
        
        # Actualizar la columna activa
        if self.sort_column == "title":
            arrow = "↑" if self.sort_order == "asc" else "↓"
            self.tree.heading("Titulo", text=f"Título del Producto {arrow}")
        elif self.sort_column == "price":
            arrow = "↑" if self.sort_order == "asc" else "↓"
            self.tree.heading("Precio", text=f"Precio {arrow}")
        elif self.sort_column == "condition":
            arrow = "↑" if self.sort_order == "asc" else "↓"
            self.tree.heading("Condicion", text=f"Condición {arrow}")
    
    def update_results(self):
        """Actualizar tabla de resultados (4 COLUMNAS: Título, Precio, Condición, URL)"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar productos
        for product in self.products:
            # Título (truncado si es muy largo)
            title = product.get('title', '')
            if len(title) > 50:
                title = title[:47] + "..."
            
            # Precio (formateado correctamente)
            price = product.get('price', 0)
            if price and price > 0:
                price_display = f"${price:,.0f}"
            else:
                price_display = "N/A"
            
            # Condición (mostrar tal como está)
            condition = product.get('condition', 'N/A')
            
            # URL (truncada para mostrar)
            url = product.get('url', '')
            if len(url) > 40:
                url_display = url[:37] + "..."
            else:
                url_display = url
            
            # Insertar en la tabla (4 VALORES: Título, Precio, Condición, URL)
            self.tree.insert("", tk.END, values=(title, price_display, condition, url_display))
    
    def export_results(self, format_type):
        """Exportar resultados"""
        if not self.products:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=f".{format_type}",
                filetypes=[
                    ("CSV files", "*.csv") if format_type == "csv" else
                    ("Excel files", "*.xlsx") if format_type == "excel" else
                    ("JSON files", "*.json")
                ]
            )
            
            if filename:
                if format_type == "csv":
                    self.scraper.export_to_csv(self.products, filename)
                elif format_type == "excel":
                    self.scraper.export_to_excel(self.products, filename)
                elif format_type == "json":
                    import json
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.products, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("Éxito", f"Resultados exportados a {filename}")
                self.status_var.set(f"Exportado a {os.path.basename(filename)}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")


def main():
    root = tk.Tk()
    app = MercadoLibreGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
