from typing import List, Tuple
import itertools

Tablon = Tuple[int, int, int]  # (ts, tr, p)

def compute_cost_for_permutation(finca: List[Tablon], perm: List[int]) -> int:
    """
    Calcula el costo CRF para una permutación dada.
    """
    n = len(finca)
    t_start = [0] * n
    tiempo = 0
    for idx in perm:
        t_start[idx] = tiempo
        tiempo += finca[idx][1]  # sumar tiempo de regado

    costo = 0
    for i in range(n):
        ts_i, tr_i, p_i = finca[i]
        retraso = (t_start[i] + tr_i) - ts_i
        if retraso > 0:
            costo += p_i * retraso
    return costo

def roFB(finca: List[Tablon]) -> Tuple[List[int], int]:
    """
    Fuerza bruta: recibe finca (lista de tuplas (ts, tr, p))
    Devuelve (pi, costo), donde:
      - pi: lista con el orden de riego de los tablones
      - costo: costo total de la solución
    """
    n = len(finca)
    indices = list(range(n))
    best_perm = []
    best_cost = float("inf")

    for perm in itertools.permutations(indices):
        costo = compute_cost_for_permutation(finca, perm)
        if costo < best_cost:
            best_cost = costo
            best_perm = list(perm)

    return best_perm, best_cost

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
