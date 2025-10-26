// Autor: Rebeca Rodríguez
// Descripción: Módulo Cuestionario Interactivo. Carga 30 preguntas de JSON y selecciona 5 al azar.


// CONFIGURACIÓN Y ESTADO GLOBAL

const RUTA_JSON_PREGUNTAS = './js/preguntas.json'; // Ruta al nuevo archivo
const CANTIDAD_PREGUNTAS_A_MOSTRAR = 5;

let bancoCompletoPreguntas = []; // Almacenará las 30 preguntas del JSON
let preguntasData = [];          // Almacenará las 5 preguntas seleccionadas para el reto
let indicePreguntaActual = 0;
let puntuacion = 0;
let respuestaSeleccionada = null; 


// 1. REFERENCIAS DEL DOM 

const contenedorQuiz = document.getElementById('contenedor-quiz');
const contadorPregunta = document.getElementById('contador-pregunta');
const puntuacionActual = document.getElementById('puntuacion-actual');
const textoPregunta = document.getElementById('texto-pregunta');
const contenedorOpciones = document.getElementById('contenedor-opciones');
const feedbackMensaje = document.getElementById('feedback-mensaje');
const botonSiguiente = document.getElementById('botonSiguiente');
const areaPregunta = document.getElementById('area-pregunta');
const areaResultadoFinal = document.getElementById('area-resultado-final');
const resumenPuntuacion = document.getElementById('resumen-puntuacion');
const botonReiniciar = document.getElementById('botonReiniciar');


// 2. LÓGICA DE CARGA ASÍNCRONA


/**
 * Carga el banco completo de preguntas desde el archivo JSON.
 * @async
 */
async function cargarBancoDePreguntas() {
    textoPregunta.textContent = "Cargando preguntas desde el archivo de datos...";
    
    try {
        const respuesta = await fetch(RUTA_JSON_PREGUNTAS);
        
        if (!respuesta.ok) {
            throw new Error(`Error HTTP ${respuesta.status}: No se pudo acceder al archivo JSON.`);
        }
        
        bancoCompletoPreguntas = await respuesta.json();

        if (!Array.isArray(bancoCompletoPreguntas) || bancoCompletoPreguntas.length < CANTIDAD_PREGUNTAS_A_MOSTRAR) {
            throw new Error(`El archivo JSON no tiene al menos ${CANTIDAD_PREGUNTAS_A_MOSTRAR} preguntas válidas.`);
        }
        
        // Una vez cargadas, iniciamos el cuestionario
        iniciarCuestionario();

    } catch (error) {
        console.error("Fallo al cargar el banco de preguntas:", error);
        mostrarError(`Fallo crítico al cargar las preguntas. ${error.message}`);
    }
}

/**
 * Selecciona 5 preguntas al azar del banco completo para el reto actual.
 */
function seleccionarPreguntasAleatorias() {
    // 1. Mezclar el banco completo
    const bancoMezclado = mezclarArray(bancoCompletoPreguntas.slice());
    
    // 2. Tomar solo las primeras 5
    preguntasData = bancoMezclado.slice(0, CANTIDAD_PREGUNTAS_A_MOSTRAR);
}


// 3. FLUJO DEL CUESTIONARIO


/**
 * Inicia el estado del cuestionario y selecciona y muestra la primera pregunta.
 */
function iniciarCuestionario() {
    seleccionarPreguntasAleatorias(); // Escoge 5 nuevas preguntas
    
    indicePreguntaActual = 0;
    puntuacion = 0;
    respuestaSeleccionada = null;
    
    // Configuración inicial de la UI
    areaResultadoFinal.style.display = 'none';
    areaPregunta.style.display = 'block';
    feedbackMensaje.style.display = 'none';
    
    actualizarPuntuacion();
    mostrarPreguntaActual();
}

/**
 * Muestra la pregunta actual y sus opciones.
 */
function mostrarPreguntaActual() {
    if (indicePreguntaActual >= preguntasData.length) {
        mostrarResultadoFinal();
        return;
    }

    const pregunta = preguntasData[indicePreguntaActual];
    
    // Reiniciar estado visual y de control
    botonSiguiente.disabled = true;
    feedbackMensaje.style.display = 'none';
    respuestaSeleccionada = null;
    
    // 1. Actualizar texto de la pregunta y contador
    textoPregunta.textContent = `${indicePreguntaActual + 1}. ${pregunta.pregunta}`;
    contadorPregunta.textContent = `Pregunta ${indicePreguntaActual + 1} de ${preguntasData.length}`;
    
    // 2. Mezclar opciones (para que no siempre aparezcan en el mismo orden)
    const opcionesMezcladas = mezclarArray(pregunta.opciones.slice());
    
    // 3. Renderizar botones de opción
    contenedorOpciones.innerHTML = '';
    opcionesMezcladas.forEach(opcion => {
        const boton = document.createElement('button');
        boton.classList.add('boton-opcion');
        boton.textContent = opcion;
        boton.addEventListener('click', () => seleccionarRespuesta(boton, opcion, pregunta.respuesta_correcta));
        contenedorOpciones.appendChild(boton);
    });
}

/**
 * Maneja la selección de respuesta por parte del usuario.
 * @param {HTMLElement} botonClickeado - El botón que el usuario seleccionó.
 * @param {string} respuestaUsuario - El texto de la respuesta seleccionada.
 * @param {string} respuestaCorrecta - El texto de la respuesta correcta.
 */
function seleccionarRespuesta(botonClickeado, respuestaUsuario, respuestaCorrecta) {
    if (respuestaSeleccionada !== null) return; 

    respuestaSeleccionada = respuestaUsuario;
    
    // Deshabilitar todos los botones de opción
    Array.from(contenedorOpciones.children).forEach(btn => btn.disabled = true);

    const esCorrecta = respuestaUsuario === respuestaCorrecta;

    if (esCorrecta) {
        puntuacion++;
        mostrarFeedback(true, "¡Respuesta Correcta! 🎉");
        botonClickeado.classList.add('feedback-correcto');
    } else {
        mostrarFeedback(false, `Incorrecto. La respuesta correcta era: ${respuestaCorrecta}`);
        botonClickeado.classList.add('feedback-incorrecto');
        
        // Resaltar la respuesta correcta
        Array.from(contenedorOpciones.children).forEach(btn => {
            if (btn.textContent === respuestaCorrecta) {
                btn.classList.add('feedback-correcto');
            }
        });
    }

    actualizarPuntuacion();
    botonSiguiente.disabled = false; // Permite avanzar
}

/**
 * Avanza a la siguiente pregunta.
 */
function siguientePregunta() {
    indicePreguntaActual++;
    mostrarPreguntaActual();
}

/**
 * Muestra la puntuación final del usuario.
 */
function mostrarResultadoFinal() {
    areaPregunta.style.display = 'none';
    areaResultadoFinal.style.display = 'block';
    
    const totalPreguntas = preguntasData.length;
    resumenPuntuacion.textContent = `Has respondido ${puntuacion} de ${totalPreguntas} preguntas correctamente.`;
    
    if (puntuacion === totalPreguntas) {
        document.getElementById('titulo-final').textContent = "¡Felicidades, Eres un Experto! 🏆";
    } else if (puntuacion >= totalPreguntas / 2) {
        document.getElementById('titulo-final').textContent = "¡Buen Trabajo! 👍";
    } else {
        document.getElementById('titulo-final').textContent = "¡Sigue Practicando! 💪";
    }
}



// 4. FUNCIONES DE UTILIDAD


/**
 * Muestra un mensaje de error si la carga falla.
 */
function mostrarError(mensaje) {
    textoPregunta.textContent = mensaje;
    contenedorOpciones.innerHTML = '';
    botonSiguiente.style.display = 'none';
    puntuacionActual.style.display = 'none';
    contadorPregunta.style.display = 'none';
}

/**
 * Actualiza la visualización de la puntuación.
 */
function actualizarPuntuacion() {
    puntuacionActual.textContent = `Puntos: ${puntuacion}`;
}

/**
 * Mezcla aleatoriamente un array (Algoritmo Fisher-Yates).
 * @param {Array} array - El array a mezclar.
 * @returns {Array} El array mezclado.
 */
function mezclarArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

/**
 * Muestra el feedback de Correcto/Incorrecto.
 * @param {boolean} esCorrecto - Indica si la respuesta fue correcta.
 * @param {string} mensaje - El mensaje a mostrar.
 */
function mostrarFeedback(esCorrecto, mensaje) {
    feedbackMensaje.textContent = mensaje;
    feedbackMensaje.classList.remove('feedback-correcto', 'feedback-incorrecto');
    feedbackMensaje.classList.add(esCorrecto ? 'feedback-correcto' : 'feedback-incorrecto');
    feedbackMensaje.style.display = 'block';
}



// 5. EVENTOS E INICIALIZACIÓN

document.addEventListener('DOMContentLoaded', () => {
    // Eventos de control
    botonSiguiente.addEventListener('click', siguientePregunta);
    // El botón Reiniciar ahora vuelve a seleccionar 5 preguntas nuevas
    botonReiniciar.addEventListener('click', iniciarCuestionario); 
    
    // Iniciar el flujo de la aplicación cargando el JSON
    cargarBancoDePreguntas();
});