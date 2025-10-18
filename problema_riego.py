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
    # Finca = Secuencia de tablones
    # Ti = tupla (ts,tr,p)
    # CRF[i] = p * max(0,(ti^II + tr) - ts)
    n = len(finca)
    DP = {}
    parent = {}


    DP[0] = (0, 0)  # caso base
    parent[0] = -1

    for mask in range(1, 1 << n):
        DP[mask] = (float("inf"), 0)
        for i in range(n):
            if mask & (1 << i):
                prev_mask = mask ^ (1 << i)
                if prev_mask not in DP:
                    continue

                costo_prev, tiempo_prev = DP[prev_mask]
                ts, tr, p = finca[i]

                t_final = tiempo_prev + tr
                retraso = max(0, t_final - ts)
                costo_nuevo = costo_prev + p * retraso

                if costo_nuevo < DP[mask][0]:
                    DP[mask] = (costo_nuevo, t_final)
                    parent[mask] = (prev_mask, i)

    mask_completo = (1 << n) - 1
    costo_minimo, _ = DP[mask_completo]

    permutacion = []
    mask_actual = mask_completo

    while mask_actual != 0:
        prev_mask, idx_tablon = parent[mask_actual]
        permutacion.append(idx_tablon)
        mask_actual = prev_mask

    permutacion.reverse()
    return permutacion, costo_minimo