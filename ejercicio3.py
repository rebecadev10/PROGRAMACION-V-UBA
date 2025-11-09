import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext # Para mostrar todos los contactos de forma legible

#   Estructura de Datos Global  
agenda_contactos = {}

class AgendaApp:
    def __init__(self, master):
        self.master = master
        master.title(" Agenda de Contactos")
        master.geometry("550x550")
        
        # Estilos comunes para las etiquetas
        font_bold = ('Arial', 10, 'bold')
        
        #   1. Marco de Entrada de Datos  
        marco_entrada = tk.LabelFrame(master, text=" Gestión de Contactos", font=font_bold, padx=10, pady=10)
        marco_entrada.pack(pady=10, padx=20, fill="x")

        # Campo Nombre
        tk.Label(marco_entrada, text="Nombre:", font=font_bold).grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.entry_nombre = tk.Entry(marco_entrada, width=30, relief=tk.SUNKEN)
        self.entry_nombre.grid(row=0, column=1, pady=5, padx=5)

        # Campo Teléfono
        tk.Label(marco_entrada, text="Teléfono:", font=font_bold).grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.entry_telefono = tk.Entry(marco_entrada, width=30, relief=tk.SUNKEN)
        self.entry_telefono.grid(row=1, column=1, pady=5, padx=5)

        # Botones de Acción
        btn_agregar = tk.Button(marco_entrada, text="➕ Agregar Contacto", command=self.agregar_contacto, bg='#4CAF50', fg='white', font=font_bold)
        btn_agregar.grid(row=2, column=0, columnspan=2, pady=10)

        #   2. Marco de Búsqueda  
        marco_busqueda = tk.LabelFrame(master, text="🔍 Buscar Contacto", font=font_bold, padx=10, pady=10)
        marco_busqueda.pack(pady=10, padx=20, fill="x")

        # Campo Nombre para Buscar
        tk.Label(marco_busqueda, text="Buscar Nombre:", font=font_bold).grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.entry_buscar_nombre = tk.Entry(marco_busqueda, width=30, relief=tk.SUNKEN)
        self.entry_buscar_nombre.grid(row=0, column=1, pady=5, padx=5)

        btn_buscar = tk.Button(marco_busqueda, text="Buscar Teléfono", command=self.buscar_contacto, bg='#2196F3', fg='white', font=font_bold)
        btn_buscar.grid(row=1, column=0, columnspan=2, pady=10)

        #   3. Marco de Salida y Visualización  
        marco_salida = tk.LabelFrame(master, text="📃 Resultados y Lista de Contactos", font=font_bold, padx=10, pady=10)
        marco_salida.pack(pady=10, padx=20, fill="both", expand=True)
        
        btn_mostrar = tk.Button(marco_salida, text="Mostrar Todos los Contactos", command=self.mostrar_todos, bg='#FFC107', font=font_bold)
        btn_mostrar.pack(pady=5)

        # Área de resultados (usamos ScrolledText para listas largas)
        self.resultado_area = scrolledtext.ScrolledText(marco_salida, height=10, wrap=tk.WORD, bg='#f0f0f0', font=('Courier', 10))
        self.resultado_area.pack(pady=5, fill="both", expand=True)
        self.resultado_area.insert(tk.END, "  Salida  ")
        self.resultado_area.config(state=tk.DISABLED) # Bloquear edición

    #                       
    #   Funciones de Lógica de la Agenda  
    #                       

    def limpiar_resultado(self):
        """Limpia el área de texto de resultados."""
        self.resultado_area.config(state=tk.NORMAL)
        self.resultado_area.delete(1.0, tk.END)
        self.resultado_area.config(state=tk.DISABLED)

    def mostrar_mensaje(self, mensaje, tipo="INFO"):
        """Muestra un mensaje formateado en el área de resultados."""
        self.resultado_area.config(state=tk.NORMAL)
        
        # Formato de salida (subrayado con ###)
        if tipo == "ERROR":
            texto = f"\n  ERROR: {mensaje} "
            color = "red"
        elif tipo == "SUCCESS":
            texto = f"\n  ÉXITO: {mensaje}"
            color = "green"
        else:
            texto = f"\n {mensaje}"
            color = "black"

        self.resultado_area.insert(tk.END, texto)
        self.resultado_area.config(state=tk.DISABLED)
        # Asegurarse de que el último mensaje sea visible
        self.resultado_area.see(tk.END)


    def agregar_contacto(self):
        """Agrega un nuevo nombre y teléfono al diccionario."""
        nombre = self.entry_nombre.get().strip().title()
        telefono = self.entry_telefono.get().strip()
        
        self.limpiar_resultado()

        # 1. Validación de Datos
        if not nombre:
            self.mostrar_mensaje("El nombre del contacto no puede estar vacío.", tipo="ERROR")
            return
        if not telefono:
            self.mostrar_mensaje("El número de teléfono no puede estar vacío.", tipo="ERROR")
            return

        # 2. Lógica y Manejo de Errores
        if nombre in agenda_contactos:
            self.mostrar_mensaje(f"El contacto '{nombre}' ya existe. ¡No se agregó!", tipo="ERROR")
        else:
            agenda_contactos[nombre] = telefono
            self.mostrar_mensaje(f"Contacto agregado: {nombre} - {telefono}", tipo="SUCCESS")
            # Limpiar entradas después del éxito
            self.entry_nombre.delete(0, tk.END)
            self.entry_telefono.delete(0, tk.END)


    def buscar_contacto(self):
        """Busca el número de teléfono de un contacto."""
        nombre = self.entry_buscar_nombre.get().strip().title()
        
        self.limpiar_resultado()

        # 1. Validación de Datos
        if not nombre:
            self.mostrar_mensaje("Debe ingresar un nombre para buscar.", tipo="ERROR")
            return

        # 2. Lógica y Manejo de Errores
        if nombre in agenda_contactos:
            telefono = agenda_contactos[nombre]
            # Formato de salida para el resultado (subrayado)
            self.mostrar_mensaje(f"Teléfono encontrado para {nombre}: {telefono}", tipo="INFO")
        else:
            self.mostrar_mensaje(f"El contacto '{nombre}' NO fue encontrado.", tipo="ERROR")


    def mostrar_todos(self):
        """Muestra todos los contactos almacenados."""
        self.limpiar_resultado()
        
        self.mostrar_mensaje("  LISTA DE TODOS LOS CONTACTOS  ", tipo="INFO")

        if not agenda_contactos:
            self.mostrar_mensaje("La agenda está vacía.", tipo="INFO")
            return

        # Ordenar contactos alfabéticamente
        contactos_ordenados = sorted(agenda_contactos.items())
        
        self.resultado_area.config(state=tk.NORMAL)
        
        for nombre, telefono in contactos_ordenados:
            # Presentación clara y legible
            linea = f"\n{nombre:<20} : {telefono}"
            self.resultado_area.insert(tk.END, linea)

        self.resultado_area.config(state=tk.DISABLED)
        self.resultado_area.see(tk.END) # Ir al final de la lista
        self.mostrar_mensaje("  FIN DE LA LISTA  ", tipo="INFO")


#   Ejecución de la Aplicación  
if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()