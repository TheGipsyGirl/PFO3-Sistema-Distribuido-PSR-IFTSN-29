
import socket
import json
import itertools
import threading
from concurrent.futures import ThreadPoolExecutor

HOST = "127.0.0.1"
PORT = 5000

WORKERS = [
    ("127.0.0.1", 5001),
    ("127.0.0.1", 5002)
]

turnos = itertools.cycle(WORKERS)
lock = threading.Lock()


def enviar_a_worker(tarea):
    with lock:
        worker = next(turnos)

    try:
        with socket.create_connection(worker, timeout=5) as conexion:
            conexion.settimeout(10)

            mensaje = json.dumps(tarea) + "\n"
            conexion.sendall(mensaje.encode("utf-8"))

            with conexion.makefile("r", encoding="utf-8") as entrada:
                respuesta = entrada.readline()

            if not respuesta:
                raise ConnectionError("Worker sin respuesta")

            resultado = json.loads(respuesta)
            resultado["worker"] = worker[1]

            return resultado

    except (OSError, ValueError) as error:
        return {
            "estado": "error",
            "mensaje": f"Error con worker {worker[1]}: {error}"
        }


def atender_cliente(conexion, direccion):
    print(f"Cliente conectado: {direccion}")

    with conexion:
        try:
            conexion.settimeout(15)

            with conexion.makefile("r", encoding="utf-8") as entrada:
                linea = entrada.readline()

            if not linea:
                return

            tarea = json.loads(linea)
            print(f"Tarea recibida: {tarea}")

            respuesta = enviar_a_worker(tarea)

            conexion.sendall(
                (json.dumps(respuesta) + "\n").encode("utf-8")
            )

        except (OSError, ValueError) as error:
            print(f"Error: {error}")

    print("Cliente desconectado")


def iniciar_servidor():
    with ThreadPoolExecutor(max_workers=8) as pool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
            )
            servidor.bind((HOST, PORT))
            servidor.listen()

            print(f"Servidor principal en {HOST}:{PORT}")
            print("Workers disponibles: 5001 y 5002")

            while True:
                conexion, direccion = servidor.accept()
                pool.submit(atender_cliente, conexion, direccion)


if __name__ == "__main__":
    iniciar_servidor()
