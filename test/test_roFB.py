import time
import random
import pytest
from problema_riego import roFB

# -----------------------------------------------------
# 1. Prueba del ejemplo del enunciado
# -----------------------------------------------------
def test_roFB_ejemplo():
    """
    Verifica que la solución de fuerza bruta funcione con el ejemplo dado.
    """
    finca = [
        (10, 3, 4),
        (5, 3, 3),
        (2, 2, 1),
        (8, 1, 1),
        (6, 4, 2)
    ]
    perm, costo = roFB(finca)

    esperado_perm = [2, 1, 3, 0, 4]
    esperado_costo = 14

    assert costo == esperado_costo, f"Costo esperado {esperado_costo}, obtenido {costo}"
    assert perm == esperado_perm, f"Permutación esperada {esperado_perm}, obtenida {perm}"

# -----------------------------------------------------
# 2. Generador de fincas sintéticas
# -----------------------------------------------------
def generar_finca(n):
    """
    Genera una finca sintética de n tablones.
    ts: tiempo de supervivencia [5, 50]
    tr: tiempo de regado [1, 10]
    p : prioridad [1, 4]
    """
    return [(random.randint(5, 50),
             random.randint(1, 10),
             random.randint(1, 4)) for _ in range(n)]

# -----------------------------------------------------
# 3. Pruebas de rendimiento
# -----------------------------------------------------
@pytest.mark.parametrize("tam", [5, 6, 7, 8, 9, 10, 100])
def test_roFB_tiempos(tam):
    finca = generar_finca(tam)
    repeticiones = 3
    tiempos = []

    if tam > 10:
        print(f"\nTamaño {tam}: fuerza bruta no ejecutada (tiempo factorialmente prohibitivo).")
        pytest.skip("No ejecutable en la práctica")
        return

    for _ in range(repeticiones):
        inicio = time.perf_counter()
        perm, costo = roFB(finca)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)

    promedio = sum(tiempos) / repeticiones
    print(f"Tamaño {tam}, tiempo promedio = {promedio:.6f} s")
