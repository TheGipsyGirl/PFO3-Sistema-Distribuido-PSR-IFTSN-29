
import socket
import json
import sys
from concurrent.futures import ThreadPoolExecutor

HOST = "127.0.0.1"


def procesar_tarea(tarea):
    tipo = tarea.get("tipo")
    numeros = tarea.get("numeros", [])

    if not isinstance(numeros, list) or any(
        isinstance(n, bool) or not isinstance(n, (int, float))
        for n in numeros
    ):
        return {"estado": "error", "mensaje": "Numeros invalidos"}

    if tipo == "sumar":
        resultado = sum(numeros)

    elif tipo == "multiplicar":
        resultado = 1
        for numero in numeros:
            resultado *= numero

    elif tipo == "promedio":
        if not numeros:
            return {"estado": "error", "mensaje": "Lista vacia"}
        resultado = sum(numeros) / len(numeros)

    else:
        return {"estado": "error", "mensaje": "Tarea desconocida"}

    return {"estado": "ok", "resultado": resultado}


def atender_conexion(conexion, direccion, nombre):
    with conexion:
        try:
            conexion.settimeout(10)

            with conexion.makefile("r", encoding="utf-8") as entrada:
                linea = entrada.readline()

            if not linea:
                return

            tarea = json.loads(linea)
            print(f"[{nombre}] Procesando: {tarea}")

            respuesta = procesar_tarea(tarea)

            conexion.sendall(
                (json.dumps(respuesta) + "\n").encode("utf-8")
            )

        except (OSError, ValueError, TypeError) as error:
            print(f"[{nombre}] Error: {error}")


def iniciar_worker(puerto):
    nombre = f"Worker-{puerto}"

    with ThreadPoolExecutor(max_workers=4) as pool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
            )
            servidor.bind((HOST, puerto))
            servidor.listen()

            print(f"{nombre} escuchando en {HOST}:{puerto}")
            print("Pool de 4 hilos activo")

            while True:
                conexion, direccion = servidor.accept()
                pool.submit(
                    atender_conexion, conexion, direccion, nombre
                )


if __name__ == "__main__":
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    iniciar_worker(puerto)
