# * Ejercicio4WebScraperLibros. Por: Rebeca rodríguez. Para: ProgramacionV-UBA *
# Este script está diseñado para recopilar datos de productos (libros) de un sitio web de comercio electrónico de prueba.
# Extrae el título, precio, rating (estrellas) y enlace de las primeras tres páginas,
# maneja la paginación y guarda los resultados en un archivo CSV para su posterior análisis de sentimientos.

import requests
from bs4 import BeautifulSoup
import csv
import time
import re # Usado para extraer el rating numérico

# --- CONFIGURACIÓN DE PARÁMETROS ---
BASE_URL = "https://books.toscrape.com/catalogue/"
START_PAGE = 1
MAX_PAGES = 3
CSV_FILENAME = "datos_libros.csv"
# Tiempo de espera entre peticiones para ser un "buen ciudadano" del web scraping
SLEEP_TIME = 1 
# --- FIN DE CONFIGURACIÓN ---

def rating_to_int(rating_class):
    """Convierte la clase del rating (ej: 'One', 'Two') a un valor numérico (1, 2)."""
    # Expresión regular para encontrar el nombre de la clase de rating
    match = re.search(r'star-rating (\w+)', rating_class)
    if not match:
        return 0

    rating_word = match.group(1)
    ratings = {
        'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
    }
    return ratings.get(rating_word, 0)

def scrape_books(base_url, start_page, max_pages):
    """
    Navega por las páginas del catálogo, extrae los datos de los libros y devuelve la lista.
    """
    all_books_data = []
    
    print(f"\n{'='*60}")
    print(f"INICIANDO WEB SCRAPING EN {base_url}")
    print(f"Extrayendo datos de la página {start_page} hasta la página {max_pages}...")
    print(f"{'='*60}\n")

    for page_num in range(start_page, max_pages + 1):
        if page_num == 1:
            # La primera página tiene una URL ligeramente diferente
            current_url = "https://books.toscrape.com/index.html"
        else:
            # Páginas subsiguientes
            current_url = f"{base_url}page-{page_num}.html"

        print(f"➡️ Procesando página: {current_url}")

        # 1. Manejo de errores y petición HTTP
        try:
            response = requests.get(current_url, timeout=10)
            
            if response.status_code != 200:
                print(f"  ERROR HTTP al acceder a la página {page_num}: Código {response.status_code}")
                # Si no se puede acceder a la página, se interrumpe el proceso de paginación
                break 
                
        except requests.exceptions.RequestException as e:
            print(f"  ERROR DE CONEXIÓN al acceder a la página {page_num}: {e}")
            break

        # 2. Parsing del HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Selector para encontrar cada contenedor de libro
        book_containers = soup.select('article.product_pod')

        if not book_containers:
            print(f"⚠️ Advertencia: No se encontraron contenedores de libros en la página {page_num}. Terminando.")
            break

        # 3. Extracción de datos por libro
        for container in book_containers:
            try:
                # Título y Enlace
                title_tag = container.select_one('h3 a')
                title = title_tag['title'].strip()
                # El enlace es relativo, se convierte a absoluto
                relative_link = title_tag['href']
                # Se utiliza re.sub para manejar el caso de la página 1 donde el enlace es un nivel superior
                absolute_link = requests.compat.urljoin(current_url, relative_link)
                
                # Precio
                price_text = container.select_one('p.price_color').get_text(strip=True)
                # Limpiar el símbolo de moneda (ej: '£51.77' -> '51.77')
                price = price_text.replace('£', '') 

                # Rating (Estrellas)
                # El rating está en una clase del elemento <p>
                rating_class = container.select_one('p.star-rating')['class'][1] # La clase Two/Three/etc. es la segunda
                rating = rating_to_int(rating_class)

                all_books_data.append({
                    'titulo': title,
                    'precio': price,
                    'rating_estrellas': rating,
                    'enlace': absolute_link
                })
                
            except Exception as e:
                # Manejo de errores para un libro específico (ej: falta un campo)
                print(f"   Error al extraer datos de un libro en la página {page_num}: {e}")
                continue

        print(f"    {len(book_containers)} libros extraídos de la página {page_num}. Total: {len(all_books_data)}")
        
        # Pausa antes de pasar a la siguiente página
        if page_num < max_pages:
            time.sleep(SLEEP_TIME)

    return all_books_data

def save_to_csv(data, filename):
    """Guarda la lista de diccionarios en un archivo CSV."""
    if not data:
        print("  No hay datos para guardar.")
        return

    # Definir los encabezados del CSV basados en las claves del diccionario
    fieldnames = ['titulo', 'precio', 'rating_estrellas', 'enlace']
    
    # Manejo de errores al escribir el archivo
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(data)
            
        # Formato de salida legible
        print(f"\n{'*'*60}")
        print(f"   Datos guardados exitosamente en el archivo: {filename}  ")
        print(f"  Total de registros guardados: {len(data)}  ")
        print(f"{'*'*60}")

    except IOError as e:
        print(f"  ERROR: No se pudo escribir en el archivo CSV '{filename}'. Detalles: {e}")


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    # Instrucciones de configuración
    print("\n--- CONFIGURACIÓN INICIAL ---")
    print("Asegúrate de tener instaladas las librerías:")
    print("   pip install requests beautifulsoup4")
    print("-----------------------------\n")

    # Obtener los datos
    book_data = scrape_books(BASE_URL, START_PAGE, MAX_PAGES)
    
    # Guardar los datos si se encontró alguno
    if book_data:
        save_to_csv(book_data, CSV_FILENAME)