// Autor: Rebeca Rodríguez
// Descripción: Módulo Conversor de Divisas 
// Implementa Promesas (fetch/async/await) para obtener tasas de cambio en tiempo real.

// Monedas principales que soportará el conversor
const MONEDAS_SOPORTADAS = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY'];
const URL_BASE_API = 'https://api.frankfurter.app/latest';

// 1. Referencias del DOM (TODOS EN ESPAÑOL)
const entradaCantidad = document.getElementById('cantidad');
const selectorMonedaOrigen = document.getElementById('monedaOrigen');
const selectorMonedaDestino = document.getElementById('monedaDestino');
const botonConvertir = document.getElementById('botonConvertir');
const botonIntercambio = document.getElementById('botonIntercambio');
const salidaResultado = document.getElementById('salidaResultado');
const textoTasaCambio = document.getElementById('tasaCambio');
const areaMensajes = document.getElementById('areaMensajes');
const textoMensaje = document.getElementById('textoMensaje');
const cajaResultado = document.getElementById('cajaResultado');

// 2. Funciones de Utilidad

/**
 * Rellena los selectores de moneda con las opciones disponibles.
 */
function llenarSelectoresMoneda() {
    MONEDAS_SOPORTADAS.forEach(moneda => {
        const opcionOrigen = new Option(moneda, moneda);
        const opcionDestino = new Option(moneda, moneda);
        selectorMonedaOrigen.add(opcionOrigen);
        selectorMonedaDestino.add(opcionDestino);
    });

    // Establecer valores predeterminados
    selectorMonedaOrigen.value = 'USD';
    selectorMonedaDestino.value = 'EUR';
}

/**
 * Muestra un mensaje temporal en la interfaz de usuario.
 * @param {string} mensaje - El mensaje a mostrar.
 * @param {string} tipo - 'error' o 'informacion'.
 */
function mostrarMensaje(mensaje, tipo = 'error') {
    textoMensaje.textContent = mensaje;
    
    // Remueve las clases de estado antiguas y aplica la nueva
    areaMensajes.classList.remove('mensaje-error', 'mensaje-informacion');
    areaMensajes.classList.add(tipo === 'error' ? 'mensaje-error' : 'mensaje-informacion');
    
    areaMensajes.style.display = 'block';
    
    // Ocultar mensaje después de 5 segundos
    setTimeout(() => {
        areaMensajes.style.display = 'none';
    }, 5000);
}

/**
 * Actualiza el estado de carga y deshabilita la UI.
 * @param {boolean} cargando - Si está cargando o no.
 */
function establecerCarga(cargando) {
    botonConvertir.disabled = cargando;
    botonIntercambio.disabled = cargando;
    entradaCantidad.disabled = cargando;
    selectorMonedaOrigen.disabled = cargando;
    selectorMonedaDestino.disabled = cargando;
    
    botonConvertir.textContent = cargando ? 'Convirtiendo...' : 'Convertir';
    if (cargando) {
        salidaResultado.textContent = '...';
        textoTasaCambio.textContent = 'Obteniendo tasas...';
    }
}

// 3. Lógica Principal (Uso de Promesas con async/await)

/**
 * Realiza la conversión de divisas consumiendo la API Frankfurter.
 * @async
 */
async function convertirDivisa() {
    const cantidad = parseFloat(entradaCantidad.value);
    const origen = selectorMonedaOrigen.value;
    const destino = selectorMonedaDestino.value;

    // 1. Validación inicial
    if (isNaN(cantidad) || cantidad <= 0) {
        mostrarMensaje('Por favor, ingresa una cantidad válida.', 'error');
        return;
    }
    if (origen === destino) {
         mostrarMensaje('Las monedas de origen y destino no pueden ser iguales.', 'error');
         salidaResultado.textContent = `${cantidad.toFixed(2)} ${destino}`;
         textoTasaCambio.textContent = 'Tasa: 1.00';
         return;
    }

    establecerCarga(true);

    // 2. Construcción de la URL de la API
    const urlApi = `${URL_BASE_API}?amount=${cantidad}&from=${origen}&to=${destino}`;

    try {
        // 3. Petición a la API (fetch retorna una Promesa)
        const respuesta = await fetch(urlApi); 

        // 4. Manejo de error HTTP
        if (!respuesta.ok) {
            throw new Error(`Error en la solicitud HTTP: ${respuesta.status}`);
        }

        // 5. Parseo de la respuesta (response.json() retorna una Promesa)
        const datos = await respuesta.json(); 

        // 6. Extracción y cálculo
        const cantidadConvertida = datos.rates[destino]; 
                                                        
        // Tasa unitaria (1 [ORIGEN] = X [DESTINO])
        const tasaBase = cantidadConvertida / cantidad; 

        // 7. Mostrar resultados y aplicar estilos de éxito
        salidaResultado.textContent = `${cantidadConvertida.toFixed(2)} ${destino}`;
        textoTasaCambio.textContent = `1 ${origen} = ${tasaBase.toFixed(4)} ${destino}`;
        
        // Estilo de éxito (Color verde)
        cajaResultado.style.backgroundColor = '#ecfdf5'; 
        cajaResultado.style.border = '1px solid #a7f3d0'; 
        salidaResultado.style.color = '#065f46'; 

    } catch (error) {
        console.error("Error en la conversión:", error);
        mostrarMensaje(`Fallo al obtener la tasa de cambio. Error: ${error.message}`, 'error');
        salidaResultado.textContent = 'ERROR';
        textoTasaCambio.textContent = '';
        
        // Estilo de error (Color rojo)
        cajaResultado.style.backgroundColor = '#fee2e2'; 
        cajaResultado.style.border = '1px solid #fca5a5'; 
        salidaResultado.style.color = '#dc2626'; 

    } finally {
        // 8. Finaliza el estado de carga
        establecerCarga(false);
    }
}

// 4. Inicialización y Event Listeners

/**
 * Intercambia los valores de los selectores de moneda.
 */
function intercambiarDivisas() {
    const valorOrigen = selectorMonedaOrigen.value;
    const valorDestino = selectorMonedaDestino.value;
    selectorMonedaOrigen.value = valorDestino;
    selectorMonedaDestino.value = valorOrigen;
    convertirDivisa(); // Ejecuta la conversión inmediatamente después de intercambiar
}

document.addEventListener('DOMContentLoaded', () => {
    llenarSelectoresMoneda();
    
    // Evento para el botón de convertir
    botonConvertir.addEventListener('click', convertirDivisa);

    // Evento para el botón de intercambio
    botonIntercambio.addEventListener('click', intercambiarDivisas);

    // Eventos para inputs y selects para actualizar en tiempo real
    

    // Realiza la primera conversión al cargar la página
    convertirDivisa();
});