// Autor: Rebeca Rodríguez
// Descripción: Muestra citas inspiradoras. Implementa fetch, async/await y try/catch.
// Utiliza un Proxy CORS y un parámetro anti-caché para garantizar citas únicas.

// ============================
// Referencias del DOM

const btnCita = document.getElementById("btnCitaDelDia");
const modal = document.getElementById("modalCita");
const citaContenido = document.getElementById("citaContenido");
const citaAutor = document.getElementById("citaAutor");


// Función para obtener una cita de la API (Async/Await, Try/Catch)

async function obtenerCita() {
    try {
        // URL de la API de citas que queremos usar
        const ZENQUOTES_URL = 'https://zenquotes.io/api/random';
        
        // Generamos un timestamp único para evitar la caché del navegador/proxy
        const CACHE_BUSTER = new Date().getTime(); 
        
        // ⭐ URL FINAL: Proxy CORS + API URL + Parámetro anti-caché
        const PROXY_URL = `https://api.allorigins.win/raw?url=${ZENQUOTES_URL}&cache=${CACHE_BUSTER}`;

        // 1. Solicitud asíncrona usando fetch
        const respuesta = await fetch(PROXY_URL);

        // 2. Verificación de respuesta HTTP (ej. 404, 500)
        if (!respuesta.ok) {
            throw new Error(`Error HTTP: ${respuesta.status}. El proxy o la API fallaron.`);
        }

        // 3. Parseamos la respuesta JSON
        const data = await respuesta.json();

        // 4. Verificación de la estructura de datos (ZenQuotes devuelve un array)
        if (!Array.isArray(data) || data.length === 0) {
            throw new Error("La API devolvió una respuesta vacía o con formato inesperado.");
        }

        // 5. Extracción de los datos (la cita es 'q', el autor es 'a')
        const cita = data[0].q;
        const autor = data[0].a;

        // 6. Mostramos la cita
        mostrarCita(cita, autor);
    } catch (error) {
        // 7. Manejo de errores de red (Failed to fetch) o errores lanzados
        console.error("Error al obtener la cita:", error.message);

        // Mostramos un mensaje de error amigable
        mostrarCita(
            "No se pudo cargar la cita. Verifica tu conexión o el estado del servicio de proxy.",
            `Detalle del error: ${error.message}`
        );
    }
}


// Función para mostrar la cita en el modal
function mostrarCita(texto, autor) {
    if (!modal || !citaContenido || !citaAutor) return;

    citaContenido.textContent = `"${texto}"`;
    citaAutor.textContent = `— ${autor}`;
    modal.style.display = "block"; // mostramos el modal
}


//  Función para cerrar el modal

function cerrarModal() {
    if (modal) {
        modal.style.display = "none";
    }
}


//  Eventos (Solo al hacer clic)


// Llamar a la API SOLO al hacer clic en el botón.
if (btnCita) {
    btnCita.addEventListener("click", obtenerCita);
}

// Cerramos el modal si el usuario hace clic fuera del contenido
window.addEventListener("click", (evento) => {
    if (evento.target === modal) {
        cerrarModal();
    }
});

// Hacemos visible la función cerrarModal() para el onclick del HTML
window.cerrarModal = cerrarModal;