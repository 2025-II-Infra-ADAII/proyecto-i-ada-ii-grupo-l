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
    Devuelve (pi, costo)
    """
    pass
def roPD(finca):
    """
    Programaci´on din´amica.
    Devuelve (pi, costo)
    """
    pass