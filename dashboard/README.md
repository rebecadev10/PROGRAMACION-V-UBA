#  Dashboard Modular Interactivo en Vanilla JS

Este proyecto es un **Dashboard Modular e Interactivo** desarrollado íntegramente con **JavaScript Puro (Vanilla JS)**, HTML5 y CSS3. Integra cuatro módulos funcionales complejos en una única interfaz cohesiva, demostrando el manejo avanzado del DOM, la persistencia de datos y el consumo de APIs asíncronas.

---

##  Cómo Ejecutar la Aplicación

No se requiere instalación de paquetes (npm/yarn) o dependencias externas.

1.  **Descargar el Proyecto:** Asegúrate de tener la estructura completa de archivos (`index.html`, carpetas `css/` y `js/`).
2.  **Abrir con Live Server (Recomendado):** Para garantizar que el módulo de Cuestionario (que carga un JSON local) y las llamadas a APIs funcionen correctamente, abre el proyecto usando un servidor local (por ejemplo, la extensión Live Server de VS Code).
3.  **Ejecución Directa:** Alternativamente, puedes hacer doble clic en el archivo **`index.html`** para abrirlo directamente en tu navegador.

---

##  Estructura del Proyecto y Decisiones de Diseño

El proyecto sigue una arquitectura **modular** estricta, asegurando la **separación de responsabilidades** (SoC).

###  Estructura de Archivos

El proyecto se organiza con una carpeta `css/` y una carpeta `js/`.

* **`index.html`:** La página principal que contiene la estructura del dashboard (cuadrícula 2x2) y sirve como *router* visual.
* **`css/style.css`:** Archivo maestro de estilos, donde residen las **Variables CSS (`:root`)** para la coherencia visual.
* **`js/` (Carpeta de Lógica):** Contiene un archivo `.js` para la lógica de cada módulo (ej. `gestorTarea.js`, `controlCitas.js`).
* **`js/preguntas.json`:** Contenido de la trivia.

###  Decisiones Clave de Diseño

* **Diseño Responsivo (CSS Grid):** Se usó **CSS Grid** en el `index.html` para la disposición inicial 2x2, con un enfoque **Mobile First** que colapsa la cuadrícula a una sola columna en pantallas pequeñas.
* **JavaScript Puro (Vanilla JS):** Todo el *frontend* se maneja con Vanilla JS, enfocándose en la **Manipulación Avanzada del DOM** (`document.createElement`) y la gestión de eventos eficientes (como el uso de `input` y `change` en el conversor).

---

##  APIs Utilizadas

Este proyecto consume dos servicios públicos de APIs:

| Módulo | API Utilizada | Propósito | Seguridad |
| :--- | :--- | :--- | :--- |
| **Citas Inspiradoras** | **ZenQuotes API** | Obtener una frase célebre aleatoria. | No requiere clave. |
| **Conversor de Divisas** | **Frankfurter API** | Obtener tasas de cambio en tiempo real. | No requiere clave. |

###  Consideración de Seguridad (CORS)

* Para garantizar que el **Módulo de Citas** funcione en cualquier navegador o entorno de host local, se implementó un **Proxy CORS** (`https://api.allorigins.win/raw?url=...`) para envolver la URL de ZenQuotes. Esto resuelve el problema de la política de mismo origen (`Same-Origin Policy`) de forma eficiente con JavaScript Puro.

---

##  Requisitos Técnicos Implementados

* **Persistencia:** El Gestor de Tareas utiliza **`localStorage`** con `JSON.stringify/parse` para guardar el estado de las tareas.
* **Asincronía:** Los módulos 2 y 3 usan **`async/await`** y **`fetch`** dentro de bloques **`try...catch`** para manejar las promesas de red de forma no bloqueante y robusta.
* **Validación y UX:** El Conversor de Divisas tiene validación de entradas numéricas y utiliza eventos **`input` / `change`** para calcular y actualizar el resultado en tiempo real, mejorando la usabilidad.