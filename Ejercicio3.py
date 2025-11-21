# * Ejercicio1Generador de Graficos Estadisticos. Por: Rebeca rodríguez. Para: ProgramacionV-UBA *
# Este script crea una aplicación de escritorio para la visualización y análisis estadístico 
# de datos utilizando Tkinter para la interfaz gráfica y Matplotlib para generar los gráficos.
# Permite al usuario ingresar una lista de números, calcular la media, mediana y moda, 
# y visualizar los datos en gráficos de barras, líneas o pastel, con validación de datos y manejo de errores.

import requests
from bs4 import BeautifulSoup
import time # Para manejar la pausa entre reintentos, si fuera necesario

# --- CONFIGURACIÓN REQUERIDA ---
# 1. Reemplaza esta URL con la dirección del blog que deseas escanear.
# URL EJEMPLO FUNCIONAL: Xataka (Blog de tecnología en español)
BLOG_URL = "https://www.xataka.com/" 
# 2. Reemplaza el selector CSS con el que corresponde a los títulos de los artículos en la página.
# Selector FUNCIONAL para Xataka: busca el enlace <a> dentro del título principal de la ficha del artículo.
TITLE_SELECTOR = "h2.abstract-title a"
# --- FIN DE CONFIGURACIÓN ---

def obtener_titulos_blog(url, selector, num_articulos=5):
    """
    Visita la URL del blog, extrae los títulos de los artículos y los imprime.
    
    Args:
        url (str): La URL principal del blog.
        selector (str): El selector CSS para encontrar los títulos de los artículos.
        num_articulos (int): El número máximo de artículos a extraer.
    """
    print(f"\n{'='*50}")
    print(f"Buscando los primeros {num_articulos} artículos en: {url}")
    print(f"Selector utilizado: {selector}")
    print(f"{'='*50}\n")
    
    # 1. Manejo de errores de conexión y respuesta HTTP
    try:
        # Configurar un User-Agent para simular un navegador y evitar ser bloqueado
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        # Validación de la respuesta HTTP
        if response.status_code != 200:
            print(f"  Error HTTP: No se pudo acceder a la página. Código de estado: {response.status_code}")
            return
            
        # Forzar la codificación a UTF-8 por seguridad
        response.encoding = response.apparent_encoding
        
    except requests.exceptions.RequestException as e:
        print(f"  Error de Conexión: No se pudo conectar a la URL '{url}'.")
        print(f"Detalles del error: {e}")
        return

    # 2. Parsing (Análisis) del HTML
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Busca todos los elementos que coincidan con el selector
        articulos = soup.select(selector)
        
    except Exception as e:
        print(f"  Error al procesar el HTML con BeautifulSoup: {e}")
        return

    # 3. Extracción y Formato de Salida
    titulos_encontrados = []
    
    if not articulos:
        print(f" Advertencia: No se encontraron artículos con el selector '{selector}'.")
        print("Asegúrate de que el selector CSS (TITLE_SELECTOR) es correcto para el blog.")
        return

    for i, articulo in enumerate(articulos):
        if i >= num_articulos:
            break
            
        # Extrae el texto del elemento. El .strip() elimina espacios en blanco innecesarios.
        titulo = articulo.get_text(strip=True)
        
        # Si el elemento es un enlace (<a>), intenta obtener el atributo 'href' (opcional)
        if articulo.name == 'a' and 'href' in articulo.attrs:
            enlace = articulo['href']
        else:
            enlace = "No disponible o no es un enlace"
            
        titulos_encontrados.append(titulo)

        # Formato de salida claro y legible
        salida = f"| TÍTULO {i+1} | {titulo}"
        # Se incluye el formato especial solicitado (entre caracteres especiales)
        print(f"  {salida}  ")
        # print(f"   Enlace: {enlace}\n") # Opcional: mostrar el enlace

    if len(titulos_encontrados) < num_articulos:
        print(f"\n Proceso completado. Se encontraron {len(titulos_encontrados)} títulos (solicitados: {num_articulos}).")
    else:
        print(f"\n Proceso completado. Se encontraron los {num_articulos} títulos solicitados.")
    
# Ejecutar la función principal
if __name__ == "__main__":
    # Instrucciones para el usuario:
    print("\n\n--- INSTRUCCIONES ---")
    print("1. Instala las librerías necesarias con el siguiente comando en tu terminal:")
    print("   pip install requests beautifulsoup4")
    print("2. Las variables BLOG_URL y TITLE_SELECTOR ya están configuradas con un blog de ejemplo (Xataka).")
    print("   ¡Puedes ejecutar el script directamente!")
    print("---------------------\n")
    
    # Llamada a la función
    obtener_titulos_blog(BLOG_URL, TITLE_SELECTOR, 5)