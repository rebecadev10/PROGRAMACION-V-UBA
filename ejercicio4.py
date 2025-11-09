import tkinter as tk
from tkinter import messagebox

#   Fórmulas de Conversión  

def celsius_to_fahrenheit(c):
    """Convierte Celsius a Fahrenheit."""
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    """Convierte Fahrenheit a Celsius."""
    return (f - 32) * 5/9

#   Lógica de la Aplicación (Clase)  

class TemperaturaApp:
    def __init__(self, master):
        self.master = master
        master.title(" Conversor de Temperatura")
        master.geometry("500x700")
        
        # Unidades disponibles para los menús
        self.unidades = ["Celsius", "Fahrenheit"]
        
        # Variables de control de Tkinter
        self.origen_var = tk.StringVar(master)
        self.destino_var = tk.StringVar(master)
        self.origen_var.set(self.unidades[0])  # Valor por defecto: Celsius
        self.destino_var.set(self.unidades[1]) # Valor por defecto: Fahrenheit

        #   Interfaz de Usuario  
        
        # 1. Entrada de Valor
        tk.Label(master, text="Valor a Convertir:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.entrada_valor = tk.Entry(master, width=15, relief=tk.SUNKEN)
        self.entrada_valor.pack(pady=5)

        # 2. Selección de Unidad de Origen
        tk.Label(master, text="Unidad de Origen:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.menu_origen = tk.OptionMenu(master, self.origen_var, *self.unidades)
        self.menu_origen.config(width=10)
        self.menu_origen.pack(pady=5)
        
        # 3. Selección de Unidad de Destino
        tk.Label(master, text="Unidad de Destino:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.menu_destino = tk.OptionMenu(master, self.destino_var, *self.unidades)
        self.menu_destino.config(width=10)
        self.menu_destino.pack(pady=5)
        
        # 4. Botón de Conversión
        tk.Button(master, text="🔄 Convertir", command=self.convertir, 
                  bg='#007ACC', fg='white', font=('Arial', 10, 'bold')).pack(pady=10)
        
        # 5. Etiqueta de Resultado
        tk.Label(master, text="Resultado:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.etiqueta_resultado = tk.Label(master, text=" ", fg="darkgreen", font=('Arial', 12, 'bold'))
        self.etiqueta_resultado.pack(pady=5)

    def convertir(self):
        """Función principal que maneja la conversión, validación y salida."""
        self.etiqueta_resultado.config(text=" ") # Limpiar resultado anterior

        try:
            # 1. Validación de Datos: Verificar que sea un número
            valor_str = self.entrada_valor.get()
            if not valor_str:
                 raise ValueError("Debe ingresar un valor numérico.")
            
            valor = float(valor_str)
            
            # 2. Obtener unidades seleccionadas
            origen = self.origen_var.get()
            destino = self.destino_var.get()
            
            resultado = None
            unidad_destino_simbolo = ""
            
            # 3. Lógica de Conversión
            if origen == destino:
                # Caso de error: Unidades iguales
                raise ValueError("Las unidades de origen y destino no pueden ser iguales.")

            elif origen == "Celsius" and destino == "Fahrenheit":
                resultado = celsius_to_fahrenheit(valor)
                unidad_destino_simbolo = "°F"
                
            elif origen == "Fahrenheit" and destino == "Celsius":
                resultado =fahrenheit_to_celsius(valor)
                unidad_destino_simbolo = "°C"
                
            # 4. Formato de Salida
            # Se presenta el resultado con formato especial (subrayado con '###')
            salida_formateada = f" {resultado:.2f} {unidad_destino_simbolo} "
            self.etiqueta_resultado.config(text=salida_formateada, fg="darkblue")

        except ValueError as e:
            # 5. Manejo de Errores: Mostrar mensaje claro
            error_mensaje = f" ERROR: {e}"
            self.etiqueta_resultado.config(text=error_mensaje, fg="red")
        except Exception as e:
             # Manejo de errores inesperados
            error_mensaje = f" Error Inesperado: {e}"
            self.etiqueta_resultado.config(text=error_mensaje, fg="red")


#   Ejecución de la Aplicación  
if __name__ == "__main__":
    root = tk.Tk()
    app = TemperaturaApp(root)
    root.mainloop()