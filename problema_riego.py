
def roFB(finca):
    """
    Fuerza bruta: recibe finca (lista de tuplas (ts, tr, p))
    Devuelve (pi, costo), donde:
      - pi: lista con el orden de riego de los tablones
      - costo: costo total de la solución
    """
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
