# ChatBot con ChatterBot

Este proyecto implementa un chatbot simple utilizando la biblioteca ChatterBot en Python. El chatbot está configurado para responder a saludos básicos y mantener una conversación simple.

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

## Notas Adicionales

- El comando `-v "$(pwd):/app"` monta el directorio actual del proyecto dentro del contenedor, lo que permite que el chatbot acceda a los archivos necesarios.