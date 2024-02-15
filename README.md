# ChatBot con ChatterBot

Este proyecto implementa un chatbot simple utilizando la biblioteca ChatterBot en Python.

El chatbot diseñado con ChatterBot incluye las siguientes funcionalidades,
está enforcado en ser una herramienta de consulta:

1. Capacidad de realizar operaciones básicas de aritmética.
2. Decir la hora actual.
3. Decir la fecha actual.
4. Calcular el número de días entre apartir de la fecha actual y una fecha
dada.
5. Decir la capital de un país.
6. Decir datos curiosos.
7. Decir frases motivacionales.


## Pre-requisitos

Para ejecutar este proyecto, necesitarás Docker instalado en tu sistema.

## Ejecución del ChatBot con Docker

Sigue estos pasos para ejecutar el chatbot dentro de un contenedor Docker.

### 1. Clonar el Repositorio

Primero, clona el repositorio del proyecto a tu máquina local. Puedes hacerlo ejecutando:

```bash
git clone https://el-repositorio.com/chatbot.git
cd chatbot
```

### 2. Construir la Imagen de Docker

Construye la imagen de Docker para el chatbot utilizando el Dockerfile proporcionado en el repositorio. Ejecuta el siguiente comando desde el directorio del proyecto:

```bash
docker build -t chatbot .
```

Este comando construye una imagen Docker llamada `chatbot` basada en las instrucciones del `Dockerfile` en el directorio actual.

### 3. Ejecutar el ChatBot

Una vez construida la imagen, puedes iniciar el chatbot ejecutando:

```bash
docker run --rm -it -v "$(pwd):/app" chatbot
```

Este comando inicia un contenedor Docker basado en la imagen `chatbot`, en modo interactivo, permitiéndote interactuar directamente con el chatbot a través de la terminal.

### Interactuar con el ChatBot

Tras iniciar el contenedor, el chatbot estará listo para recibir tus mensajes. Simplemente escribe tu mensaje en la terminal y el chatbot responderá. Para terminar la conversación y salir del chatbot, escribe "salir".

### Ejemplo de funcionamiento

¡Hola! ¿En qué puedo ayudarte? Escribe 'salir' para terminar.

> ¿Cuánto es 2 más 3?

El resultado es 5

> ¿Qué hora es?

Son las 11:34 p.m.

> ¿Qué día es hoy?

Hoy es Miércoles, 14 de Febrero de 2024.

> ¿Cuántos días faltan para el 15 de febrero del 2024?

Faltan 0 días, 0 horas, 25 minutos y 19 segundos para el 15 de Febrero del 2024.

> ¿Cuál es la capital de México?

Ciudad de México

> Dime un dato curioso

Los loros no solo pueden imitar sonidos humanos, sino que algunos pueden aprender y entender múltiples palabras y frases.

> Dime una frase motivacional

Try not to become a person of success, but rather try to become a person of value.

- Albert Einstein

> salir

¡Hasta luego!

## Notas Adicionales

- El comando `-v "$(pwd):/app"` monta el directorio actual del proyecto dentro del contenedor, lo que permite que el chatbot acceda a los archivos necesarios.