# * Ejercicio1 Editor de texto Por: Rebeca rodríguez. Para: ProgramacionV-UBA * # Este script implementa un editor de texto básico utilizando la biblioteca Tkinter. 
# Incluye funcionalidades de manejo de archivos (Abrir, Guardar), búsqueda/reemplazo de texto con resaltado, 
# y un contador de palabras/caracteres simple.

import tkinter as tk
from tkinter import filedialog, messagebox

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Texto Básico - Gemini")
        self.current_file = None
        
        # --- NUEVA RESTRICCIÓN: Establecer tamaño mínimo de la ventana ---
        self.root.minsize(500, 500) 

        # 1. Crear el área de texto principal
        # wrap='word' asegura que las líneas se rompan en espacios, no a mitad de palabras
        self.text_area = tk.Text(self.root, wrap='word', undo=True)
        self.text_area.pack(fill='both', expand=True)
        
        # 2. Configurar Barras de Desplazamiento
        scrollbar = tk.Scrollbar(self.text_area)
        scrollbar.pack(side='right', fill='y')
        self.text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_area.yview)

        # 3. Configurar Menús
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Menú Archivo
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_command(label="Guardar Como", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)

        # Menú Edición
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edición", menu=edit_menu)
        edit_menu.add_command(label="Buscar / Reemplazar", command=self.open_find_replace_dialog)
        edit_menu.add_command(label="Contar Palabras", command=self.count_words)

        # 4. Configurar el diálogo de Búsqueda/Reemplazo (inicialmente oculto)
        self.setup_find_replace_bar()
        
        # Vincular el evento de cambio de texto para actualizar el conteo o cualquier otra cosa
        self.text_area.bind('<KeyRelease>', self.on_text_change)
        
    # --- Funciones de Archivo ---

    def new_file(self):
        """Crea un nuevo archivo, borrando el contenido actual."""
        self.text_area.delete('1.0', 'end')
        self.current_file = None
        self.root.title("Nuevo Archivo - Editor de Texto Básico")

    def open_file(self):
        """Abre un archivo y carga su contenido en el área de texto."""
        filepath = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if not filepath:
            return
        
        self.text_area.delete('1.0', 'end')
        try:
            with open(filepath, "r", encoding="utf-8") as input_file:
                text = input_file.read()
                self.text_area.insert('1.0', text)
            self.current_file = filepath
            self.root.title(f"{filepath} - Editor de Texto Básico")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def save_file(self):
        """Guarda el archivo actual. Llama a save_file_as si no se ha guardado antes."""
        if self.current_file:
            self._write_to_file(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        """Abre el diálogo 'Guardar como' y guarda el archivo."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if not filepath:
            return
        self._write_to_file(filepath)

    def _write_to_file(self, filepath):
        """Función auxiliar para guardar el contenido del texto."""
        try:
            content = self.text_area.get('1.0', 'end-1c') # -1c omite el salto de línea final
            with open(filepath, "w", encoding="utf-8") as output_file:
                output_file.write(content)
            self.current_file = filepath
            self.root.title(f"{filepath} - Editor de Texto Básico")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    # --- Funciones de Edición ---

    def setup_find_replace_bar(self):
        """Configura la barra de búsqueda y reemplazo en un Frame separado."""
        self.find_frame = tk.Frame(self.root)
        self.find_frame.pack(fill='x', padx=5, pady=5)
        self.find_frame.pack_forget() # Ocultar por defecto

        # Búsqueda
        tk.Label(self.find_frame, text="Buscar:").pack(side='left', padx=(0, 5))
        self.find_entry = tk.Entry(self.find_frame, width=20)
        self.find_entry.pack(side='left', padx=(0, 10))
        self.find_entry.bind('<Return>', lambda event: self.find_text())
        tk.Button(self.find_frame, text="Buscar Siguiente", command=self.find_text).pack(side='left')

        # Reemplazo
        tk.Label(self.find_frame, text="Reemplazar:").pack(side='left', padx=(15, 5))
        self.replace_entry = tk.Entry(self.find_frame, width=20)
        self.replace_entry.pack(side='left', padx=(0, 10))
        tk.Button(self.find_frame, text="Reemplazar", command=self.replace_one).pack(side='left')
        tk.Button(self.find_frame, text="Reemplazar Todo", command=self.replace_all).pack(side='left')
        
        # Cerrar
        tk.Button(self.find_frame, text="X", command=self.close_find_replace_bar).pack(side='right')

    def open_find_replace_dialog(self):
        """Muestra la barra de búsqueda/reemplazo."""
        self.find_frame.pack(fill='x', padx=5, pady=5)
        self.find_entry.focus_set()

    def close_find_replace_bar(self):
        """Oculta la barra de búsqueda/reemplazo y borra el resaltado."""
        self.find_frame.pack_forget()
        self.clear_highlight()

    def find_text(self):
        """Busca el texto ingresado y resalta todas las ocurrencias."""
        self.clear_highlight()
        search_term = self.find_entry.get()
        if not search_term:
            return
        
        start_index = '1.0'
        # Etiqueta 'found' para aplicar el color de fondo
        self.text_area.tag_configure('found', background='yellow')
        
        while True:
            # Buscar desde start_index hasta el final ('end')
            start_index = self.text_area.search(search_term, start_index, stopindex='end')
            
            if not start_index:
                break
                
            # Calcular el índice final del término encontrado
            end_index = f"{start_index}+{len(search_term)}c"
            
            # Aplicar la etiqueta de resaltado
            self.text_area.tag_add('found', start_index, end_index)
            
            # Mover el cursor para la siguiente búsqueda
            start_index = end_index

    def clear_highlight(self):
        """Borra todo el resaltado de la etiqueta 'found'."""
        self.text_area.tag_remove('found', '1.0', 'end')

    def replace_one(self):
        """Reemplaza la primera ocurrencia del término de búsqueda."""
        search_term = self.find_entry.get()
        replace_term = self.replace_entry.get()
        
        if not search_term:
            return
            
        # Buscar la primera ocurrencia desde el inicio
        start_index = self.text_area.search(search_term, '1.0', stopindex='end')
        
        if start_index:
            end_index = f"{start_index}+{len(search_term)}c"
            # Eliminar el término encontrado y insertar el término de reemplazo
            self.text_area.delete(start_index, end_index)
            self.text_area.insert(start_index, replace_term)
            self.find_text() # Volver a buscar y resaltar

    def replace_all(self):
        """Reemplaza todas las ocurrencias del término de búsqueda."""
        search_term = self.find_entry.get()
        replace_term = self.replace_entry.get()
        
        if not search_term:
            return

        # Deshabilitar las actualizaciones para un reemplazo masivo más rápido
        self.text_area.edit_separator() 
        self.text_area.mark_set("insert", "1.0") # Mover cursor al inicio para la búsqueda

        count = 0
        while True:
            # Buscar desde la posición actual del cursor (o "insert")
            start_index = self.text_area.search(search_term, "insert", stopindex='end', count=tk.IntVar())
            
            if not start_index:
                break
            
            end_index = f"{start_index}+{len(search_term)}c"
            
            # Eliminar y Reemplazar
            self.text_area.delete(start_index, end_index)
            self.text_area.insert(start_index, replace_term)
            
            # Mover el punto de inserción para la siguiente búsqueda
            self.text_area.mark_set("insert", f"{start_index}+{len(replace_term)}c")
            count += 1
            
        self.text_area.edit_separator()
        messagebox.showinfo("Reemplazo Completo", f"Se reemplazaron {count} ocurrencia(s).")
        self.find_text() # Volver a buscar y resaltar (con el nuevo contenido)


    def count_words(self):
        """Cuenta el número de palabras en el área de texto."""
        text = self.text_area.get('1.0', 'end-1c') # Obtener todo el texto
        
        # Usar split() sin argumentos es una forma limpia de dividir por cualquier espacio en blanco
        # y manejar múltiples espacios entre palabras.
        words = text.split()
        word_count = len(words)
        
        # Conteo de caracteres (sin espacios) y líneas
        char_count = len("".join(words)) 
        line_count = text.count('\n') + 1 # Contar saltos de línea y sumar 1
        
        messagebox.showinfo(
            "Conteo de Texto",
            f"Estadísticas:\n"
            f"Palabras: **{word_count}**\n"
            f"Caracteres (sin espacios): {char_count}\n"
            f"Líneas: {line_count}"
        )

    # --- Manejo de Eventos ---

    def on_text_change(self, event):
        """Se llama cada vez que el texto cambia (para actualizar el resaltado, por ejemplo)."""
        # Si la barra de búsqueda está visible, actualiza el resaltado
        if self.find_frame.winfo_ismapped():
            self.find_text()


if __name__ == "__main__":
    # Inicialización de la ventana principal
    root = tk.Tk()
    editor = TextEditor(root)
    # Inicia el bucle principal de la aplicación
    root.mainloop()