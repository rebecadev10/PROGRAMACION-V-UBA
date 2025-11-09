import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os

#   Clase principal de la aplicación  

class ToDoApp:
    def __init__(self, master):
        self.master = master
        master.title(" Gestor de Tareas Pendientes")
        master.geometry("400x550")
        
        # Estructura de datos: Lista para almacenar [tarea_nombre, completada_bool]
        self.tareas = []
        self.archivo_tareas = "tasks.txt"
        
        # 1. Marco de Entrada de Tareas  
        marco_entrada = tk.LabelFrame(master, text=" Nueva Tarea", padx=10, pady=10)
        marco_entrada.pack(pady=10, padx=20, fill="x")

        self.entrada_tarea = tk.Entry(marco_entrada, width=35, relief=tk.SUNKEN)
        self.entrada_tarea.grid(row=0, column=0, padx=5, pady=5)

        tk.Button(marco_entrada, text="Añadir", command=self.agregar_tarea, 
                  bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=5, pady=5)

        #   2. Marco de Visualización y Control  
        marco_lista = tk.LabelFrame(master, text=" Tareas Pendientes", padx=10, pady=10)
        marco_lista.pack(pady=10, padx=20, fill="both", expand=True)

        # Listbox para mostrar tareas
        self.listbox_tareas = tk.Listbox(marco_lista, height=15, width=45, selectmode=tk.SINGLE, 
                                        font=('Courier', 10), relief=tk.FLAT)
        self.listbox_tareas.pack(side=tk.LEFT, fill="both", expand=True)

        # Barra de desplazamiento (Scrollbar)
        scrollbar = tk.Scrollbar(marco_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_tareas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_tareas.yview)

        #   3. Marco de Botones de Acción  
        marco_acciones = tk.Frame(master)
        marco_acciones.pack(pady=10)

        tk.Button(marco_acciones, text=" Completar", command=self.marcar_completada, 
                  bg='#2196F3', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(marco_acciones, text=" Eliminar", command=self.eliminar_tarea, 
                  bg='#F44336', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)

        #   4. Marco de Guardar/Cargar  
        marco_persistencia = tk.Frame(master)
        marco_persistencia.pack(pady=5)

        tk.Button(marco_persistencia, text=" Guardar Tareas", command=self.guardar_tareas, 
                  bg='#FF9800', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(marco_persistencia, text=" Cargar Tareas", command=self.cargar_tareas, 
                  bg='#9E9E9E', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)

        # CAMBIO CLAVE 
           
    #   Lógica de Gestión de Tareas  
    

    def actualizar_listbox(self):
        """Refresca el Listbox con la lista actual de tareas."""
        self.listbox_tareas.delete(0, tk.END)
        for i, (tarea, completada) in enumerate(self.tareas):
            prefix = " - " if completada else  " * "
            display_text = prefix + tarea
            self.listbox_tareas.insert(tk.END, display_text)
            
            # Aplicar formato de salida (color) a las tareas completadas
            if completada:
                self.listbox_tareas.itemconfig(i, {'fg': 'gray', 'bg': '#e0ffe0'}) 
            else:
                self.listbox_tareas.itemconfig(i, {'fg': 'black', 'bg': 'white'})


    def agregar_tarea(self):
        """Agrega una nueva tarea a la lista."""
        tarea = self.entrada_tarea.get().strip()
        
        # Validación de datos: Asegurar que la entrada no esté vacía
        if not tarea:
            messagebox.showwarning(" Entrada Inválida", "La tarea no puede estar vacía.")
            return

        # [nombre_tarea, completada_bool]
        self.tareas.append([tarea, False])
        self.entrada_tarea.delete(0, tk.END)
        self.actualizar_listbox()
        messagebox.showinfo(" Éxito", f"Tarea '{tarea}' añadida.")


    def marcar_completada(self):
        """Marca la tarea seleccionada como completada (True)."""
        try:
            # Obtiene el índice de la tarea seleccionada
            indice_seleccionado = self.listbox_tareas.curselection()[0]
            
            # Marcar como completada
            self.tareas[indice_seleccionado][1] = True 
            
            self.actualizar_listbox()
            messagebox.showinfo(" Tarea Completada", f"Tarea marcada como completada.")
            
        except IndexError:
            # Manejo de errores si no hay tarea seleccionada
            messagebox.showwarning(" Error de Selección", "Debe seleccionar una tarea para marcarla como completada.")


    def eliminar_tarea(self):
        """Elimina la tarea seleccionada de la lista."""
        try:
            indice_seleccionado = self.listbox_tareas.curselection()[0]
            tarea_eliminada = self.tareas[indice_seleccionado][0]
            
            del self.tareas[indice_seleccionado]
            
            self.actualizar_listbox()
            messagebox.showinfo(" Eliminada", f"Tarea '{tarea_eliminada}' eliminada.")
            
        except IndexError:
            # Manejo de errores si no hay tarea seleccionada
            messagebox.showwarning(" Error de Selección", "Debe seleccionar una tarea para eliminar.")


    
    #   Lógica de Persistencia (Guardar/Cargar)  
    

    def guardar_tareas(self):
        """Guarda la lista de tareas en el archivo de texto."""
        try:
            with open(self.archivo_tareas, 'w', encoding='utf-8') as f:
                for tarea, completada in self.tareas:
                    # Formato de salida: [True/False] Tarea_Nombre
                    f.write(f"[{completada}] {tarea}\n")
            
            # Formato de salida: Mensaje claro con formato especial
            messagebox.showinfo("💾 Guardado Exitoso", f"Tareas guardadas en: {self.archivo_tareas}")
            
        except Exception as e:
            # Manejo de errores
            messagebox.showerror(" Error de Archivo", f"Error al guardar tareas: {e}")


    def cargar_tareas(self, mostrar_mensaje=True):
        """Carga la lista de tareas desde el archivo de texto."""
        if not os.path.exists(self.archivo_tareas):
            if mostrar_mensaje:
                # Se mantiene el mensaje de "Archivo No Encontrado", pero solo se muestra si el usuario
                # intenta cargar manualmente
                messagebox.showinfo(" Archivo No Encontrado", "No se encontró el archivo de tareas. La lista en memoria no ha cambiado.")
            return

        try:
            self.tareas = []
            with open(self.archivo_tareas, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        # Parsear el formato: [True/False] Tarea_Nombre
                        estado_str = line[1:line.find(']')]
                        completada = True if estado_str.lower() == 'true' else False
                        tarea_nombre = line[line.find(']') + 2:]
                        self.tareas.append([tarea_nombre, completada])
            
            self.actualizar_listbox()
            if mostrar_mensaje:
                # Formato de salida: Mensaje claro con formato especial
                messagebox.showinfo(" Carga Exitosa", f"Tareas cargadas desde: {self.archivo_tareas}")

        except Exception as e:
            # Manejo de errores
            messagebox.showerror(" Error de Carga", f"Error al cargar tareas: {e}. Lista vaciada.")
            self.tareas = []
            self.actualizar_listbox()


#   Ejecución de la Aplicación  
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()