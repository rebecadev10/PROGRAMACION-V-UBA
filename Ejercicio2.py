# * Ejercicio2 Generador de Gráficos Estadísticos. Por: Rebeca Rodríguez. Para: ProgramaciónV-UBA *
# Este script crea una aplicación de escritorio para la visualización y análisis estadístico 
# de datos utilizando Tkinter para la interfaz gráfica y Matplotlib para generar los gráficos.
# Permite al usuario ingresar una lista de números, calcular la media, mediana y moda, 
# y visualizar los datos en gráficos de barras, líneas o pastel, con validación de datos y manejo de errores.

import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
import re 

class DataVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador y Analizador Estadístico")
        self.data = []
        self.chart_type = tk.StringVar(value="barras") # Tipo de gráfico predeterminado
        
        # Inicializar Matplotlib Figure
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas_widget = None # Para almacenar el widget del gráfico

        self._setup_ui()
        
        # --- CORRECCIÓN CLAVE: Manejar el cierre de la ventana ---
        # Registra la función on_closing para que se llame cuando el usuario intente cerrar la ventana.
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing) 

    def on_closing(self):
        """
        Función para cerrar la aplicación limpiamente.
        Cierra la figura de Matplotlib y destruye la ventana de Tkinter.
        """
        try:
            # Cerrar explícitamente la figura de Matplotlib para liberar recursos
            plt.close(self.fig)
        except Exception:
            # Ignorar si la figura ya estaba cerrada
            pass
            
        # Destruir la ventana principal de Tkinter
        self.root.destroy()

    def _setup_ui(self):
        """Configura todos los elementos de la interfaz de usuario (frames, widgets)."""
        
        # --- Frame de Entrada y Controles ---
        control_frame = tk.Frame(self.root, padx=10, pady=10, borderwidth=2, relief="groove")
        control_frame.pack(fill='x')
        
        # Etiqueta e Input de Datos
        tk.Label(control_frame, text="Datos (Números separados por coma/espacio):").grid(row=0, column=0, sticky='w', pady=5)
        self.data_entry = tk.Entry(control_frame, width=50)
        self.data_entry.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky='ew')
        
        # Selector de Tipo de Gráfico
        tk.Label(control_frame, text="Tipo de Gráfico:").grid(row=2, column=0, sticky='w', pady=5)
        
        tk.Radiobutton(control_frame, text="Barras", variable=self.chart_type, value="barras").grid(row=2, column=1, sticky='w')
        tk.Radiobutton(control_frame, text="Línea", variable=self.chart_type, value="linea").grid(row=2, column=2, sticky='w')
        tk.Radiobutton(control_frame, text="Pastel (Frecuencia)", variable=self.chart_type, value="pastel").grid(row=3, column=1, sticky='w')

        # Botón de Generación
        tk.Button(control_frame, text="Generar Gráfico y Estadísticas", command=self.process_data, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=3, pady=10, sticky='ew')

        # --- Frame de Resultados Estadísticos ---
        stats_frame = tk.Frame(self.root, padx=10, pady=10, borderwidth=2, relief="sunken")
        stats_frame.pack(fill='x', pady=(0, 10))
        
        # Etiquetas de resultados (inicialmente vacías)
        tk.Label(stats_frame, text="RESULTADOS ESTADÍSTICOS", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
        
        tk.Label(stats_frame, text="Media:").grid(row=1, column=0, sticky='w', padx=5)
        self.media_label = tk.Label(stats_frame, text="---", font=('Courier', 10, 'underline'))
        self.media_label.grid(row=1, column=1, sticky='w', padx=5)
        
        tk.Label(stats_frame, text="Mediana:").grid(row=2, column=0, sticky='w', padx=5)
        self.mediana_label = tk.Label(stats_frame, text="---", font=('Courier', 10, 'underline'))
        self.mediana_label.grid(row=2, column=1, sticky='w', padx=5)

        tk.Label(stats_frame, text="Moda:").grid(row=3, column=0, sticky='w', padx=5)
        self.moda_label = tk.Label(stats_frame, text="---", font=('Courier', 10, 'underline'))
        self.moda_label.grid(row=3, column=1, sticky='w', padx=5)
        
        # --- Contenedor del Gráfico ---
        self._initialize_plot_canvas()

    def _initialize_plot_canvas(self):
        """Inicializa el lienzo de Matplotlib dentro de Tkinter."""
        
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()
            
        # Limpiar la figura antes de la nueva visualización
        self.fig.clf() 
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Gráfico de Datos (Vacío)")
        
        # Crear el widget de lienzo de Tkinter
        canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = canvas
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _validate_and_parse_data(self):
        """
        Valida la entrada del usuario y convierte la cadena a una lista de flotantes.
        Manejo de errores: Muestra messagebox si la validación falla.
        """
        raw_input = self.data_entry.get().strip()
        
        if not raw_input:
            messagebox.showerror("Error de Datos", "Por favor, ingrese una lista de números.")
            return False

        # Reemplazar comas por espacios para simplificar la división
        clean_input = raw_input.replace(',', ' ')
        
        numbers = []
        try:
            # Intentar convertir cada segmento a float
            for item in clean_input.split():
                if item: # Evitar doble espacio
                    numbers.append(float(item))
            
            if not numbers:
                 messagebox.showerror("Error de Datos", "La entrada no contiene números válidos.")
                 return False

            self.data = np.array(numbers)
            return True
        
        except ValueError:
            # Si float() falla en cualquier elemento
            messagebox.showerror("Error de Datos", "Asegúrese de ingresar solo números (enteros o decimales).")
            return False

    def calculate_stats(self):
        """Calcula la media, mediana y moda de los datos ingresados."""
        if len(self.data) == 0:
            return 0, 0, "N/A"

        # Media (Promedio)
        media = np.mean(self.data)
        
        # Mediana
        mediana = np.median(self.data)
        
        # Moda (valor más frecuente)
        counts = Counter(self.data)
        max_count = max(counts.values())
        modas = [key for key, value in counts.items() if value == max_count]
        
        # Formato de salida para la moda
        if len(modas) == len(self.data):
             moda_str = "No hay moda (todos los valores son únicos)"
        elif len(modas) == 1:
            moda_str = f"{modas[0]}"
        else:
            moda_str = ", ".join(map(str, sorted(modas))) # Múltiples modas
            
        return media, mediana, moda_str

    def plot_data(self):
        """Genera el gráfico Matplotlib según el tipo seleccionado."""
        
        self.fig.clf() # Limpiar la figura anterior
        self.ax = self.fig.add_subplot(111)
        chart_title = ""
        
        # Lógica de Ploteo
        if self.chart_type.get() == "barras":
            # Gráfico de barras simple (asume que los datos son valores y el índice es la categoría)
            x = np.arange(len(self.data))
            self.ax.bar(x, self.data, color='skyblue')
            self.ax.set_xticks(x)
            self.ax.set_xticklabels([f"Dato {i+1}" for i in x], rotation=45, ha="right")
            self.ax.set_ylabel("Valor")
            chart_title = "Gráfico de Barras"
            
        elif self.chart_type.get() == "linea":
            # Gráfico de línea
            self.ax.plot(self.data, marker='o', linestyle='-', color='purple')
            self.ax.set_xlabel("Índice de Dato")
            self.ax.set_ylabel("Valor")
            chart_title = "Gráfico de Línea"
            
        elif self.chart_type.get() == "pastel":
            # Gráfico de pastel (requiere datos de frecuencia)
            counts = Counter(self.data)
            labels = [f"{k} ({v})" for k, v in counts.items()]
            sizes = counts.values()
            
            self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
            self.ax.axis('equal') # Asegura que el pastel sea circular
            chart_title = "Gráfico de Pastel (Frecuencia de Valores)"
        
        self.ax.set_title(chart_title, fontsize=14)
        self.fig.tight_layout() # Ajuste automático para evitar superposiciones
        self.canvas_widget.draw()

    def process_data(self):
        """Función principal llamada por el botón para validar, calcular y graficar."""
        
        # 1. Validación de Datos
        if not self._validate_and_parse_data():
            # Limpiar etiquetas si la validación falla
            self._update_stats_labels(0, 0, "---") 
            self._initialize_plot_canvas() # Mostrar un gráfico vacío
            return

        # 2. Cálculo Estadístico
        media, mediana, moda_str = self.calculate_stats()
        
        # 3. Actualización de Etiquetas
        self._update_stats_labels(media, mediana, moda_str)
        
        # 4. Generación y Visualización del Gráfico
        self.plot_data()
        
    def _update_stats_labels(self, media, mediana, moda_str):
        """
        Actualiza las etiquetas de estadísticas con el formato especial requerido.
        """
        # Formatear números a 2 decimales
        media_str = f"*{media:.2f}*" if isinstance(media, (float, int)) else str(media)
        mediana_str = f"*{mediana:.2f}*" if isinstance(mediana, (float, int)) else str(mediana)
        
        # Formato de salida: El valor final entre caracteres especiales (*)
        self.media_label.config(text=f"  {media_str}  ")
        self.mediana_label.config(text=f"  {mediana_str}  ")
        self.moda_label.config(text=f"  {moda_str}  ")


if __name__ == "__main__":
    # Asegúrate de que matplotlib no use un backend interactivo antes de Tkinter
    # plt.switch_backend('Agg') 
    
    root = tk.Tk()
    app = DataVisualizer(root)
    root.mainloop()