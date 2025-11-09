import tkinter as tk
from tkinter import messagebox
import calendar
from datetime import datetime

#   Funciones de Lógica y Manejo de Errores  

def mostrar_calendario():
    """Obtiene los datos y muestra el calendario (mes o año) en la GUI."""
    # 1. Limpiar el área de salida
    resultado_text.config(state=tk.NORMAL)
    resultado_text.delete(1.0, tk.END)

    try:
        # 2. Validación de Datos (Año)
        year_str = entrada_año.get()
        if not year_str.isdigit():
            raise ValueError("El año debe ser un número entero.")
        
        año = int(year_str)
        if año <= 0:
            raise ValueError("El año debe ser un número positivo.")
        
        # 3. Lógica principal
        opcion = modo_var.get()
        calendario_generado = ""
        
        if opcion == 1:  # Mostrar Mes
            month_str = entrada_mes.get()
            if not month_str.isdigit():
                 raise ValueError("El mes debe ser un número entero.")
                 
            mes = int(month_str)
            
            # 4. Validación de Datos (Mes)
            if not (1 <= mes <= 12):
                raise ValueError("El mes debe estar entre 1 y 12.")

            # Generar el calendario del mes
            cal = calendar.TextCalendar(calendar.MONDAY)
            calendario_generado = cal.formatmonth(año, mes)
            
        elif opcion == 2:  # Mostrar Año
            # Generar el calendario del año
            cal = calendar.TextCalendar(calendar.MONDAY)
            calendario_generado = cal.formatyear(año, 2, 1, 6) # w=2, l=1, c=6, m=3
        
        else:
            raise ValueError("Debe seleccionar si desea ver el mes o el año completo.")

        # 5. Formato de Salida
        salida_formateada = f"\n CALENDARIO DE {año}{' - MES ' + str(mes) if opcion == 1 else ''} \n\n"
        salida_formateada += calendario_generado
        salida_formateada += f"\nFIN DEL CALENDARIO \n"
        
        resultado_text.insert(tk.END, salida_formateada)
        resultado_text.config(state=tk.DISABLED) # Bloquear edición
        
    except ValueError as e:
        # 6. Manejo de Errores (Mensajes claros)
        mensaje_error = f"🚫 Error de Validación: {e}"
        resultado_text.insert(tk.END, mensaje_error)
        resultado_text.config(state=tk.DISABLED)

#   Configuración de la Interfaz Gráfica (Tkinter)  

# Ventana principal
ventana = tk.Tk()
ventana.title("🗓️ Generador de Calendario")
ventana.geometry("700x800")

# Variables de control
modo_var = tk.IntVar(value=1) # 1 para Mes, 2 para Año. Por defecto Mes
año_actual = datetime.now().year
mes_actual = datetime.now().month

# 1. Marco de Controles
marco_controles = tk.Frame(ventana, padx=10, pady=10)
marco_controles.pack(pady=10)

# Campo Año
tk.Label(marco_controles, text="Año: ", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
entrada_año = tk.Entry(marco_controles, width=10, relief=tk.SOLID)
entrada_año.insert(0, str(año_actual))
entrada_año.grid(row=0, column=1, sticky='w', padx=5, pady=5)

# Campo Mes (opcional)
tk.Label(marco_controles, text="Mes (1-12): ", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
entrada_mes = tk.Entry(marco_controles, width=10, relief=tk.SOLID)
entrada_mes.insert(0, str(mes_actual))
entrada_mes.grid(row=1, column=1, sticky='w', padx=5, pady=5)

# Opciones (Radiobuttons)
tk.Label(marco_controles, text="Mostrar: ", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=5)

tk.Radiobutton(marco_controles, text="Mes Específico", variable=modo_var, value=1).grid(row=2, column=1, sticky='w', padx=5)
tk.Radiobutton(marco_controles, text="Año Completo", variable=modo_var, value=2).grid(row=2, column=2, sticky='w', padx=5)

# Botón Generar
boton_generar = tk.Button(marco_controles, text="Generar Calendario", command=mostrar_calendario, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'))
boton_generar.grid(row=3, column=0, columnspan=3, pady=15)

# 2. Área de Resultado
tk.Label(ventana, text="  Resultado  ", font=('Arial', 10, 'bold')).pack()

# Text Widget para el calendario
resultado_text = tk.Text(ventana, height=25, width=100, relief=tk.SUNKEN, bg='#f0f0f0', font=('Courier', 10), state=tk.DISABLED)
resultado_text.pack(pady=10, padx=20)

# Ejecutar la ventana al iniciar
ventana.mainloop()