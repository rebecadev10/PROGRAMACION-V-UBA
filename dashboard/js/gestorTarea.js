 // Clave de localStorage para almacenar las tareas
        const STORAGE_KEY = 'tareasList'; 
        // Estado actual del filtro ('todas', 'pendientes', 'completadas')
        let filtroActual = 'todas';

        // 1. Persistencia de Datos (Inicialización)
        // Función para cargar las tareas de localStorage o usar las predeterminadas
       function cargarTareas() {
            const tareasGuardadas = localStorage.getItem(STORAGE_KEY);
            if (tareasGuardadas) {
                try {
                    // Si hay datos en localStorage, intenta cargarlos.
                    return JSON.parse(tareasGuardadas);
                } catch (e) {
                    console.error("Error al parsear tareas de localStorage:", e);
                    // CAMBIO: Si hay un error, devuelve un array vacío
                    return [];
                }
            }
            // CAMBIO: Si no hay nada en localStorage, devuelve un array vacío
            return [];
        }

        // Función para guardar las tareas en localStorage
        function guardarTareas() {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(tareas));
        }

        // Array de objetos para representar las tareas (cargado desde localStorage)
        let tareas = cargarTareas();

        // Referencias a elementos del DOM (del código original)
        const inputNuevaTarea = document.getElementById('nuevaTarea');
        const btnAgregarTarea = document.getElementById('agregarTarea');
        const listaTareas = document.getElementById('listaTareas');
        const mensajeDiv = document.getElementById('mensaje');
        const mensajeErrorInput = document.getElementById('mensajeErrorInput');
        const totalTareas = document.getElementById('totalTareas');
        const tareasPendientes = document.getElementById('tareasPendientes');
        const tareasCompletadas = document.getElementById('tareasCompletadas');

        // Referencias a elementos de filtro (NUEVOS)
        const filtroTodas = document.getElementById('filtroTodas');
        const filtroPendientes = document.getElementById('filtroPendientes');
        const filtroCompletadas = document.getElementById('filtroCompletadas');


        // --- Funciones Auxiliares (Modificadas/Añadidas) ---

        // Función para mostrar mensajes (del código original)
        function mostrarMensaje(mensaje, tipo) {
            mensajeDiv.textContent = mensaje;
            mensajeDiv.className = `mensaje ${tipo}`;
            
            setTimeout(() => {
                mensajeDiv.textContent = '';
                mensajeDiv.className = 'mensaje';
            }, 3000);
        }

        // Función para mostrar/ocultar error en el input (del código original)
        function mostrarErrorInput(mostrar) {
            if (mostrar) {
                inputNuevaTarea.classList.add('error');
                mensajeErrorInput.style.display = 'block';
            } else {
                inputNuevaTarea.classList.remove('error');
                mensajeErrorInput.style.display = 'none';
            }
        }

        // Función para actualizar los contadores (del código original)
        function actualizarContadores() {
            const total = tareas.length;
            const completadas = tareas.filter(tarea => tarea.completada).length;
            const pendientes = total - completadas;
            
            totalTareas.textContent = total;
            tareasCompletadas.textContent = completadas;
            tareasPendientes.textContent = pendientes;
        }

        // Función para agregar una nueva tarea (Modificada para guardar)
        function agregarTarea(descripcion) {
            if (!descripcion.trim()) {
                mostrarErrorInput(true);
                mostrarMensaje('Por favor, ingresa una descripción para la tarea', 'error');
                inputNuevaTarea.focus();
                return;
            }
            
            mostrarErrorInput(false);
            
            const nuevaTarea = {
                descripcion: descripcion.trim(),
                completada: false
            };
            
            tareas.push(nuevaTarea);
            guardarTareas(); // GUARDA EN LOCALSTORAGE
            mostrarMensaje('Tarea agregada correctamente', 'exito');
            inputNuevaTarea.value = '';
            renderizarTareas();
        }

        // Función para marcar una tarea como completada (Modificada para guardar)
        function marcarTareaCompletada(indiceVisible) {
            const tareaFiltrada = tareasVisibles()[indiceVisible];
            // Encontrar el índice real de la tarea en el array 'tareas'
            const indiceReal = tareas.findIndex(t => t === tareaFiltrada);

            if (indiceReal >= 0 && indiceReal < tareas.length) {
                tareas[indiceReal].completada = true;
                guardarTareas(); // GUARDA EN LOCALSTORAGE
                mostrarMensaje(`Tarea "${tareas[indiceReal].descripcion}" marcada como completada`, 'exito');
                renderizarTareas();
            } else {
                mostrarMensaje('Índice de tarea no válido', 'error');
            }
        }

        // Función para eliminar una tarea (Modificada para guardar)
        function eliminarTarea(indiceVisible) {
            const tareaFiltrada = tareasVisibles()[indiceVisible];
            // Encontrar el índice real de la tarea en el array 'tareas'
            const indiceReal = tareas.findIndex(t => t === tareaFiltrada);

            if (indiceReal >= 0 && indiceReal < tareas.length) {
                const tareaEliminada = tareas[indiceReal];
                tareas.splice(indiceReal, 1);
                guardarTareas(); // GUARDA EN LOCALSTORAGE
                mostrarMensaje(`Tarea "${tareaEliminada.descripcion}" eliminada`, 'exito');
                renderizarTareas();
            } else {
                mostrarMensaje('Índice de tarea no válido', 'error');
            }
        }
        
        // --- 2. Implementación de Filtros ---

        // Función para obtener las tareas según el filtro actual
        function tareasVisibles() {
            switch (filtroActual) {
                case 'pendientes':
                    return tareas.filter(tarea => !tarea.completada);
                case 'completadas':
                    return tareas.filter(tarea => tarea.completada);
                case 'todas':
                default:
                    return tareas;
            }
        }

        // Función para actualizar la clase 'activo' de los botones de filtro
        function actualizarBotonesFiltro() {
            document.querySelectorAll('.boton-filtro').forEach(btn => {
                btn.classList.remove('activo');
            });

            switch (filtroActual) {
                case 'pendientes':
                    filtroPendientes.classList.add('activo');
                    break;
                case 'completadas':
                    filtroCompletadas.classList.add('activo');
                    break;
                case 'todas':
                default:
                    filtroTodas.classList.add('activo');
                    break;
            }
        }

        // Función para cambiar el filtro y re-renderizar
        function cambiarFiltro(nuevoFiltro) {
            filtroActual = nuevoFiltro;
            actualizarBotonesFiltro();
            renderizarTareas();
        }

        // Función para listar todas las tareas (MODIFICADA para usar filtros)
        function renderizarTareas() {
            listaTareas.innerHTML = '';
            
            const tareasAmostrar = tareasVisibles();
            
            if (tareas.length === 0) {
                listaTareas.innerHTML = '<div class="sin-tareas">No hay tareas en la lista. ¡Agrega una nueva tarea!</div>';
                actualizarContadores();
                return;
            }

            if (tareasAmostrar.length === 0) {
                 listaTareas.innerHTML = '<div class="sin-tareas">No hay tareas que coincidan con el filtro actual.</div>';
                 actualizarContadores(); // Los contadores deben reflejar el total real, no el filtrado
                 return;
            }
            
            tareasAmostrar.forEach((tarea, indiceVisible) => {
                const elemento = document.createElement('div');
                elemento.className = 'tarea';
                
                // Nota: El índice 'indiceVisible' solo es el índice dentro del array filtrado
                // Las funciones marcarTareaCompletada y eliminarTarea deben usar este índice visible para encontrar la tarea real.
                
                elemento.innerHTML = `
                    <div class="tarea-info">
                        <span class="tarea-indice">${indiceVisible + 1}</span>
                        <span class="tarea-descripcion ${tarea.completada ? 'tarea-completada' : ''}">${tarea.descripcion}</span>
                    </div>
                    <div class="tarea-estado ${tarea.completada ? 'estado-completada' : 'estado-pendiente'}">
                        ${tarea.completada ? 'Completada' : 'Pendiente'}
                    </div>
                    <div class="tarea-acciones">
                        ${!tarea.completada ? `<button class="boton-accion boton-completar" onclick="marcarTareaCompletada(${indiceVisible})">Completar</button>` : ''}
                        <button class="boton-accion boton-eliminar" onclick="eliminarTarea(${indiceVisible})">Eliminar</button>
                    </div>
                `;
                
                listaTareas.appendChild(elemento);
            });
            
            actualizarContadores();
        }

        // Event Listeners (Modificados/Añadidos)
        btnAgregarTarea.addEventListener('click', () => {
            agregarTarea(inputNuevaTarea.value);
        });

        inputNuevaTarea.addEventListener('keypress', (e) => {
            mostrarErrorInput(false);
            
            if (e.key === 'Enter') {
                agregarTarea(inputNuevaTarea.value);
            }
        });

        inputNuevaTarea.addEventListener('focus', () => {
            mostrarErrorInput(false);
        });

        // Event Listeners para los filtros (NUEVOS)
        filtroTodas.addEventListener('click', () => cambiarFiltro('todas'));
        filtroPendientes.addEventListener('click', () => cambiarFiltro('pendientes'));
        filtroCompletadas.addEventListener('click', () => cambiarFiltro('completadas'));


        

        document.addEventListener('DOMContentLoaded', () => {
// Inicializar la aplicación
        actualizarBotonesFiltro(); // Establecer el filtro inicial
        renderizarTareas(); // Mostrar las tareas iniciales/cargadas
        })
