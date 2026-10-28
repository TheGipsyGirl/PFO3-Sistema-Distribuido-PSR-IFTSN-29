
import socket
import json

HOST = "127.0.0.1"
PORT = 5000


def enviar_tarea(tipo, numeros):
    tarea = {
        "tipo": tipo,
        "numeros": numeros
    }

    try:
        with socket.create_connection((HOST, PORT), timeout=5) as cliente:
            cliente.settimeout(15)

            mensaje = json.dumps(tarea) + "\n"
            cliente.sendall(mensaje.encode("utf-8"))

            with cliente.makefile("r", encoding="utf-8") as entrada:
                respuesta = entrada.readline()

            if not respuesta:
                raise ConnectionError("Servidor sin respuesta")

            return json.loads(respuesta)

    except (OSError, ValueError) as error:
        return {"estado": "error", "mensaje": str(error)}


def main():
    while True:
        print("\n--- SISTEMA DISTRIBUIDO DE TAREAS ---")
        print("1. Sumar numeros")
        print("2. Multiplicar numeros")
        print("3. Calcular promedio")
        print("4. Salir")

        opcion = input("Elegi una opcion: ")

        if opcion == "4":
            print("Programa finalizado.")
            break

        operaciones = {
            "1": "sumar",
            "2": "multiplicar",
            "3": "promedio"
        }

        if opcion not in operaciones:
            print("Opcion invalida.")
            continue

        try:
            entrada = input("Ingresa numeros separados por espacios: ")
            numeros = [float(n) for n in entrada.split()]

            respuesta = enviar_tarea(operaciones[opcion], numeros)

            if respuesta.get("estado") == "ok":
                print("Resultado:", respuesta["resultado"])
                print("Procesado por worker:", respuesta["worker"])
            else:
                print("Error:", respuesta.get("mensaje"))

        except ValueError:
            print("Ingresa solamente numeros validos.")


if __name__ == "__main__":
    main()
