# * Ejercicio2Generador de códigos QR. Por: Rebeca rodríguez. Para: ProgramacionV-UBA *
import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog
import qrcode
import os

#   Lógica y Funciones  

# URL de Python (Fija)
PYTHON_URL = "https://www.python.org/"

class QRGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Generador de Códigos QR Personalizados")
        master.geometry("500x400")
        
        # Colores por defecto
        self.fill_color = "#000000"  # Negro
        self.back_color = "#FFFFFF"  # Blanco

        #   Interfaz de Controles  
        
        # 1. Etiqueta URL
        tk.Label(master, text="URL de Enlace:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        tk.Label(master, text=PYTHON_URL, fg="blue", relief=tk.SUNKEN).grid(row=0, column=1, columnspan=2, sticky='ew', padx=10, pady=5)

        # 2. Entrada de Tamaño (Box Size)
        tk.Label(master, text="Tamaño (Box Size, ej: 10):", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_size = tk.Entry(master, width=10)
        self.entry_size.insert(0, "10") # Valor por defecto
        self.entry_size.grid(row=1, column=1, sticky='w', padx=10, pady=5)
        
        # 3. Selector de Color de Relleno (Fill Color)
        tk.Label(master, text="Color de Relleno:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.btn_fill_color = tk.Button(master, text="Seleccionar Color", command=self.choose_fill_color)
        self.btn_fill_color.grid(row=2, column=1, sticky='w', padx=10, pady=5)
        self.fill_color_preview = tk.Label(master, text=self.fill_color, bg=self.fill_color, width=8, relief=tk.SUNKEN)
        self.fill_color_preview.grid(row=2, column=2, sticky='w', padx=10, pady=5)
        
        # 4. Selector de Color de Fondo (Background Color)
        tk.Label(master, text="Color de Fondo:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.btn_back_color = tk.Button(master, text="Seleccionar Color", command=self.choose_back_color)
        self.btn_back_color.grid(row=3, column=1, sticky='w', padx=10, pady=5)
        self.back_color_preview = tk.Label(master, text=self.back_color, bg=self.back_color, width=8, relief=tk.SUNKEN)
        self.back_color_preview.grid(row=3, column=2, sticky='w', padx=10, pady=5)
        
        # 5. Botón Generar
        tk.Button(master, text="🎨 Generar y Guardar QR", command=self.generate_and_save_qr, 
                  bg='#4CAF50', fg='white', font=('Arial', 12, 'bold')).grid(row=4, column=0, columnspan=3, pady=20)
                  
        # 6. Área de Mensajes de Salida
        self.message_label = tk.Label(master, text="", fg="darkgreen", font=('Arial', 10))
        self.message_label.grid(row=5, column=0, columnspan=3, pady=10)


    def choose_fill_color(self):
        """Abre el selector de color para el relleno del QR."""
        color_code = colorchooser.askcolor(title="Seleccionar Color de Relleno")
        if color_code:
            self.fill_color = color_code[1]
            self.fill_color_preview.config(bg=self.fill_color, text=self.fill_color)
            
    def choose_back_color(self):
        """Abre el selector de color para el fondo del QR."""
        color_code = colorchooser.askcolor(title="Seleccionar Color de Fondo")
        if color_code:
            self.back_color = color_code[1]
            self.back_color_preview.config(bg=self.back_color, text=self.back_color)

    def generate_and_save_qr(self):
        """Genera el código QR con las configuraciones del usuario y lo guarda en un archivo."""
        self.message_label.config(text="") # Limpiar mensajes previos

        # 1. Validación de Datos (Box Size/Tamaño)
        try:
            box_size_str = self.entry_size.get()
            if not box_size_str or not box_size_str.isdigit():
                raise ValueError("El tamaño (Box Size) debe ser un número entero positivo.")
            
            box_size = int(box_size_str)
            if box_size <= 0:
                raise ValueError("El tamaño debe ser mayor que cero.")

        except ValueError as e:
            # Manejo de errores
            self.message_label.config(text=f"🛑 Error: {e}", fg="red")
            return
            
        # 2. Validación y Obtención de Colores
        fill = self.fill_color
        back = self.back_color

        # 3. Generación del objeto QR
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=box_size,
                border=4,
            )
            
            # Enlazar a la URL de Python
            qr.add_data(PYTHON_URL)
            qr.make(fit=True)

            # Crear la imagen con los colores personalizados
            img = qr.make_image(fill_color=fill, back_color=back)
            
            # 4. Diálogo para guardar el archivo
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialfile="python_qr_code"
            )
            
            if file_path:
                img.save(file_path)
                
                # 5. Formato de Salida y Confirmación
                message = f"✅ Código QR generado y guardado en:\n***{file_path}***"
                self.message_label.config(text=message, fg="darkgreen")
            else:
                self.message_label.config(text="⚠️ Operación cancelada. El archivo no fue guardado.", fg="orange")


        except Exception as e:
            # Manejo de errores generales (ej. problemas con PIL/qrcode)
            self.message_label.config(text=f"❌ Error inesperado al generar QR: {e}", fg="red")
            messagebox.showerror("Error de Generación", f"Ocurrió un error: {e}")


#   Ejecución de la Aplicación  
if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()