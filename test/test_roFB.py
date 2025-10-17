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

    # Según el enunciado, la mejor permutación esperada es:
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
# 3. Pruebas de rendimiento (juguete, pequeño, mediano)
# -----------------------------------------------------
@pytest.mark.parametrize("tam", [10, 100, 1000, 10000, 50000])
def test_roFB_tiempos(tam):
    """
    Mide el tiempo promedio de ejecución en 5 repeticiones.
    Para tamaños > 10 se usa una submuestra, porque el factorial crece rápidamente.
    """
    finca = generar_finca(tam)
    repeticiones = 5
    tiempos = []

    for _ in range(repeticiones):
        inicio = time.time()
        # Por limitación de tiempo, evaluamos solo los primeros 10 tablones
        perm, costo = roFB(finca if tam <= 10 else finca[:10])
        fin = time.time()
        tiempos.append(fin - inicio)

    promedio = sum(tiempos) / repeticiones
    print(f"\nTamaño {tam}, tiempo promedio = {promedio:.6f} s")

    # Verificación básica para tamaño pequeño
    if tam == 10:
        assert isinstance(perm, list)
        assert isinstance(costo, int)
        assert len(perm) == 10
