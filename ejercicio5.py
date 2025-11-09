# * Ejercicio5 Juego adivinanzas de colores Por: Rebeca rodríguez. Para: ProgramacionV-UBA *
import tkinter as tk
import random

class JuegoAdivinanzaColor:
    def __init__(self, maestro):
        self.maestro = maestro
        maestro.title("Juego de Adivinanza de Colores")
        maestro.geometry("450x400")
        
        # Colores disponibles y su "temperatura" para las pistas
        self.colores_disponibles = {
            "Rojo": "Cálido", 
            "Azul": "Frío", 
            "Verde": "Frío", 
            "Amarillo": "Cálido"
        }
        self.lista_colores = list(self.colores_disponibles.keys())
        
        # Mapeo de nombres en español a nombres en inglés válidos para Tkinter
        self.mapa_color_tk = {
            "Rojo": "red",
            "Azul": "blue",
            "Verde": "green",
            "Amarillo": "yellow"
        }
        
        self.color_secreto = ""
        self.intentos = 0
        self.intentos_maximos = 3
        
        # --- 1. Interfaz de Usuario ---
        
        # Título/Instrucciones
        tk.Label(maestro, text="Adivina el Color Secreto", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Frame para contener los elementos del juego (pista, resultado, botones de colores)
        self.marco_elementos_juego = tk.Frame(maestro)

        # Área de Pistas y Resultado
        self.etiqueta_pista = tk.Label(self.marco_elementos_juego, text="Adivina el color. Intentos restantes: 3", fg="black", font=('Arial', 10), wraplength=400)
        self.etiqueta_pista.pack(pady=5)
        
        self.etiqueta_resultado = tk.Label(self.marco_elementos_juego, text="", fg="black", font=('Arial', 14, 'bold')) 
        self.etiqueta_resultado.pack(pady=10)
        
        # Botones de Colores
        tk.Label(self.marco_elementos_juego, text="Selecciona tu Intento:", font=('Arial', 10, 'bold')).pack(pady=5)
        
        self.marco_botones_colores = tk.Frame(self.marco_elementos_juego)
        self.marco_botones_colores.pack(pady=10)
        
        # Crear los botones para cada color usando el mapeo corregido
        self.botones_color = {}
        for nombre_color in self.lista_colores:
            color_fondo = self.mapa_color_tk.get(nombre_color, "white") 
            
            btn = tk.Button(self.marco_botones_colores, text=nombre_color, 
                            command=lambda c=nombre_color: self.hacer_intento(c), 
                            bg=color_fondo, fg='white', width=10, state=tk.DISABLED, relief=tk.RAISED)
            
            btn.pack(side=tk.LEFT, padx=5)
            self.botones_color[nombre_color] = btn
            
        # Botón de Iniciar/Reiniciar Juego (siempre visible)
        self.btn_iniciar = tk.Button(maestro, text="Iniciar Juego", command=self.iniciar_juego, 
                                     bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'))
        self.btn_iniciar.pack(pady=20)
        
        # Inicialmente, el frame con los elementos del juego está oculto
        self.ocultar_elementos_juego()

    # --- 2. Funciones de Lógica del Juego ---

    def mostrar_elementos_juego(self):
        """Muestra los elementos del juego (pista, resultado, botones de colores)."""
        self.marco_elementos_juego.pack(pady=10)

    def ocultar_elementos_juego(self):
        """Oculta los elementos del juego."""
        self.marco_elementos_juego.pack_forget()

    def iniciar_juego(self):
        """Reinicia el juego y selecciona un nuevo color secreto."""
        self.mostrar_elementos_juego() # Mostrar elementos del juego
        
        self.color_secreto = random.choice(self.lista_colores)
        self.intentos = 0
        
        # Resetear etiquetas
        self.etiqueta_pista.config(text=f"Adivina el color. Intentos restantes: {self.intentos_maximos}", fg="black")
        self.etiqueta_resultado.config(text="", fg="black")
        
        # Habilitar botones de colores y cambiar texto de botón de control
        self.btn_iniciar.config(text="Reiniciar Juego", bg='#FF9800')
        for btn in self.botones_color.values():
            btn.config(state=tk.NORMAL)

    def hacer_intento(self, color_intento):
        """Procesa el intento del usuario y proporciona pistas."""
        
        if not self.color_secreto:
            self.etiqueta_pista.config(text="Presiona 'Reiniciar Juego' para comenzar.", fg="red")
            return

        self.intentos += 1
        restantes = self.intentos_maximos - self.intentos

        if color_intento == self.color_secreto:
            # Éxito
            mensaje_res = f"Felicidades! Adivinaste el color: {self.color_secreto}."
            self.etiqueta_resultado.config(text=f"{mensaje_res}", fg="green")
            self.etiqueta_pista.config(text=f"Ganaste en {self.intentos} intento(s)!")
            self.terminar_juego()
        else:
            # Intento incorrecto
            
            # Deshabilitar el botón del color ya intentado
            self.botones_color[color_intento].config(state=tk.DISABLED)

            if restantes > 0:
                # Proporcionar Pista
                pista = self.generar_pista(color_intento)
                
                self.etiqueta_pista.config(text=f"Intento Incorrecto. Intentos restantes: {restantes}. Pista: {pista}", fg="orange")
            else:
                # Fallo: Se acabaron los intentos
                mensaje_res = f"Game Over. El color secreto era: {self.color_secreto}."
                
                self.etiqueta_resultado.config(text=f"{mensaje_res}", fg="red")
                self.etiqueta_pista.config(text="No quedan más intentos.")
                self.terminar_juego()

    def generar_pista(self, color_intento):
        """Genera una pista basada en la 'temperatura' del color."""
        
        temperatura_intento = self.colores_disponibles[color_intento]
        temperatura_secreto = self.colores_disponibles[self.color_secreto]
        
        pista = ""
        
        # Pista de temperatura (Cálido vs. Frío)
        if temperatura_intento == temperatura_secreto:
            pista = "El color secreto tiene la misma 'temperatura' de color (Cálido/Frío)."
        else:
            pista = f"El color secreto es mas {temperatura_secreto}."

        # Pista adicional dentro de la misma temperatura (si aplica)
        if temperatura_intento == temperatura_secreto:
            if self.color_secreto == "Rojo" or self.color_secreto == "Azul":
                 pista += " Pista: El color secreto es primario."
            elif self.color_secreto == "Verde" or self.color_secreto == "Amarillo":
                 pista += " Pista: El color secreto es primario o secundario."

        return pista

    def terminar_juego(self):
        """Deshabilita los botones de color al finalizar el juego."""
        for btn in self.botones_color.values():
            btn.config(state=tk.DISABLED)

# --- 3. Ejecución de la Aplicación ---
if __name__ == "__main__":
    raiz = tk.Tk()
    app = JuegoAdivinanzaColor(raiz)
    raiz.mainloop()