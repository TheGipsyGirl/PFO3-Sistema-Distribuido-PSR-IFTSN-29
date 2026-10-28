
# PFO 3 – Rediseño como Sistema Distribuido

**Materia:** Programación sobre Redes  
**Trabajo:** PFO 3 – Arquitectura Cliente-Servidor

## Descripción

Este proyecto implementa un sistema de procesamiento
distribuido de tareas utilizando Python y sockets TCP.

El cliente envía operaciones a un servidor principal,
que distribuye las solicitudes entre dos servidores
workers independientes mediante Round Robin.

Cada worker utiliza un pool de 4 hilos para procesar
las tareas y devolver los resultados.

## Funcionalidades

- Sumar números.
- Multiplicar números.
- Calcular promedios.
- Enviar y recibir información mediante sockets TCP.
- Intercambiar datos en formato JSON.
- Distribuir tareas entre dos workers.
- Procesar múltiples solicitudes mediante hilos.

## Tecnologías utilizadas

- Python
- Sockets TCP
- JSON
- ThreadPoolExecutor
- Threading

## Estructura del proyecto

- servidor.py: recibe las solicitudes y distribuye las tareas.
- worker.py: procesa las operaciones solicitadas.
- cliente.py: permite enviar tareas y recibir resultados.
- diagrama_arquitectura.png: representa la arquitectura propuesta.

## Ejecución

Abrir cuatro terminales y ejecutar:

Terminal 1 - Worker 1:

    python worker.py 5001

Terminal 2 - Worker 2:

    python worker.py 5002

Terminal 3 - Servidor principal:

    python servidor.py

Terminal 4 - Cliente:

    python cliente.py

## Diagrama de arquitectura

![Diagrama del sistema](diagrama_arquitectura.png)

El diseño conceptual incluye clientes web y móviles,
Nginx/HAProxy, servidores workers con pools de hilos,
RabbitMQ y almacenamiento mediante PostgreSQL y S3.

El prototipo implementa la comunicación TCP entre un
cliente, un servidor principal y dos workers.

Nginx/HAProxy, RabbitMQ, PostgreSQL y S3 forman parte
del diseño propuesto, pero no están integrados en el código.

## Pruebas realizadas

Se comprobaron las operaciones de suma, multiplicación
y promedio.

También se verificó que el servidor principal distribuye
las tareas alternativamente entre los workers de los
puertos 5001 y 5002.

## Conclusión

El proyecto permitió aplicar los conceptos de
arquitectura cliente-servidor, comunicación mediante
sockets TCP y distribución de tareas entre servidores.

La implementación demuestra cómo un servidor principal
puede coordinar distintos workers para procesar
solicitudes de los clientes.
