import time
import random
import pytest
from problema_riego import roV

# -----------------------------------------------------
# 1. Prueba del ejemplo del enunciado
# -----------------------------------------------------
def test_roV_ejemplo():
    """
    Verifica que el algoritmo voraz produzca la salida esperada
    para el ejemplo 1 del enunciado.
    """
    finca = [
        (10, 3, 4),
        (5, 3, 3),
        (2, 2, 1),
        (8, 1, 1),
        (6, 4, 2)
    ]

    orden, costo = roV(finca)

    # Resultado calculado manualmente:
    esperado_orden = [1, 2, 0, 4, 3]
    esperado_costo = 20

    assert costo == esperado_costo, f"Costo esperado {esperado_costo}, obtenido {costo}"
    assert orden == esperado_orden, f"Orden esperado {esperado_orden}, obtenido {orden}"

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
# 3. Pruebas de rendimiento (juguete, pequeño, mediano, grande, extra grande)
# -----------------------------------------------------
@pytest.mark.parametrize("tam", [10, 100, 1000, 10000, 50000])
def test_roV_tiempos(tam):
    """
    Mide el tiempo promedio de ejecución de la función voraz (roV)
    en 5 repeticiones para distintos tamaños de finca.
    """
    finca = generar_finca(tam)
    repeticiones = 5
    tiempos = []

    for _ in range(repeticiones):
        inicio = time.time()
        orden, costo = roV(finca)
        fin = time.time()
        tiempos.append(fin - inicio)

    promedio = sum(tiempos) / repeticiones
    print(f"\nTamaño {tam}, tiempo promedio (roV) = {promedio:.6f} s")

    # Verificación básica
    assert isinstance(orden, list)
    assert isinstance(costo, int)
    assert len(orden) == tam

# -----------------------------------------------------
# 4. Prueba de consistencia: nunca debe generar índices repetidos
# -----------------------------------------------------
def test_roV_indices_unicos():
    """
    Comprueba que el orden generado por roV tenga índices únicos y válidos.
    """
    finca = generar_finca(20)
    orden, _ = roV(finca)

    assert len(orden) == len(set(orden)), "Hay índices repetidos en el orden generado"
    assert all(0 <= i < len(finca) for i in orden), "Índices fuera de rango"
