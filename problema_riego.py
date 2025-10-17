from itertools import permutations

def roFB(finca):
    """
    Fuerza bruta: recibe `finca` (lista de tuplas (ts,tr,p))
    Devuelve (pi, costo)
    """
    # Aquí más adelante se implementa fuerza bruta
    pass


def roV(finca):
    """
    Algoritmo voraz propuesto.
    Recibe `finca` (lista de tuplas (ts,tr,p)).
    Devuelve (orden, costo).
    """

    n = len(finca)
    # Orden voraz: mayor prioridad con menor supervivencia primero
    orden = sorted(range(n), key=lambda i: finca[i][2] / finca[i][0], reverse=True)

    tiempo_actual = 0
    costo_total = 0
    for i in orden:
        ts, tr, p = finca[i]
        fin = tiempo_actual + tr
        penalizacion = p * max(0, fin - ts)
        costo_total += penalizacion
        tiempo_actual = fin

    return orden, costo_total


def roPD(finca):
    """
    Programación dinámica.
    Devuelve (pi, costo)
    """
    # Aquí más adelante se implementa programación dinámica
    pass


# ------------------------------
# Utilidades de entrada/salida
# ------------------------------

def leer_finca(nombre_archivo):
    finca = []
    with open(nombre_archivo, "r") as f:
        n = int(f.readline().strip())
        for _ in range(n):
            ts, tr, p = map(int, f.readline().strip().split(","))
            finca.append((ts, tr, p))
    return finca


def escribir_salida(nombre_archivo, costo, orden):
    with open(nombre_archivo, "w") as f:
        f.write(str(costo) + "\n")
        for i in orden:
            f.write(str(i) + "\n")


def ejecutar_voraz(entrada, salida):
    finca = leer_finca(entrada)
    orden, costo = roV(finca)
    escribir_salida(salida, costo, orden)


# ------------------------------
# Ejemplo de ejecución directa
# ------------------------------
if __name__ == "__main__":
    ejecutar_voraz("entrada.txt", "salida.txt")
