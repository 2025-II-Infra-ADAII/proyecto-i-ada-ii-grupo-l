# Informe de Implementación — Problema del Riego Óptimo

# 0. Descripción del problema

---

El **problema del riego óptimo** consiste en programar el orden en que se riegan los tablones de una finca, de manera que se minimice el sufrimiento de los cultivos al retrasar el riego. Cada tablón tiene:

- $ts_i$: tiempo máximo que puede sobrevivir sin riego (supervivencia).
- $tr_i$: tiempo necesario para ser regado.
- $p_i$: prioridad del tablón (1 a 4, siendo 4 la más alta).

El costo por sufrimiento de un tablón iii es:

$$
CRF[i]=pi⋅max⁡(0,(ti+tri)−tsi)
$$

donde $t_i$ es el tiempo de inicio de su riego. El objetivo es encontrar la permutación de los tablones que minimice el costo total:

$$
CRF_\Pi = \sum_{i=0}^{n-1} CRF[i]
$$

# 1. Lenguaje y herramientas usadas

---

- **Lenguaje:** Python 3.
- **Bibliotecas estándar:** `itertools` para generar permutaciones, `time` para medir el tiempo de ejecución y `random` para generar los tablones aleatoriamente.
- **Estructuras usadas:** listas y tuplas para representar la finca.
- **Motivación de elección:** Python permite implementar rápidamente algoritmos de prueba como fuerza bruta, además de facilitar el uso de librerías de testing (`pytest`) y pipelines de integración continua.

# 2. Estructura del proyecto

---

El proyecto se organizó en módulos, siguiendo la recomendación del enunciado:

```bash
riego_optimo/
│
├── src/
│   ├── problema_riego.py # Solución por fuerza bruta, algoritmo voraz y programación dinámica
│   └── main.py        # Entrada/salida de archivos
│
├── tests/
│   ├── test_roFB.py   # Pruebas unitarias con pytest
│   ├── test_roV.py   # Pruebas unitarias con pytest
│   └── test_roPD.py   # Pruebas unitarias con pytest
│
├── docs/
│   ├── Informe_Complejidad.md
│   └── Informe_implementación.md     # Informe en formato markdown
│
├── README.md
└── .github/
    └── workflows/
        └── ci.yml     # Pipeline de integración continua

```

# 3. Ejecución del proyecto

---

El programa se ejecuta desde consola con el archivo `main.py`.

### Ejemplo de uso:

```bash
python main.py entrada.txt salida.txt
```

### Formato de entrada (`entrada.txt`)

La entrada vendrá en un archivo de texto con n + 1 líneas:

```
5 --> n
10,3,4 --> ts0,tr0,p0
5,3,3 --> ts1,tr1,p1
2,2,1
8,1,1
6,4,2
----------------------
ts(n-1),tr(n-1),p(n-1)
(es decir, primera lınea n, luego n liıneas con los valores de cada tablón separados por comas).
```

### Formato de salida (`salida.txt`)

La salida se deberá producir en un archivo de texto con n + 1 líneas:

```
14 --> Costo
2 --> pi0
1 --> pi1
3 ...
0 ...
4 --> pi (n-1)
```

# 4. Ideas de solución

---

## a) Solución ingenua (fuerza bruta)

El enfoque consiste en generar **todas las permutaciones** posibles de los tablones:

$$
\Pi = \langle \pi_0, \pi_1, \dots, \pi_{n-1}\rangle
$$

Para cada permutación se calculan los tiempos de inicio (t_{\pi_j}) de acuerdo con:

$$
t_{\pi_0} = 0, \quad t_{\pi_j} = t_{\pi_{j-1}} + tr_{\pi_{j-1}} \quad (j=1,\dots,n-1)
$$

Luego, el costo de cada tablón se evalúa con:

$$
CRF[i] = p_i \cdot \max \Big( 0, (t_i + tr_i) - ts_i \Big)
$$

y se suma para obtener el costo total $CRF_\Pi$.

Finalmente, se escoge la permutación con menor costo.

- **Complejidad temporal:** $O(n! \cdot n)$ (muy costosa, solo viable para $n \leq 10$).
- **Correctitud:** garantiza encontrar la solución óptima.

**Ejemplo:** con la entrada de 5 tablones mostrada arriba, la mejor permutación encontrada fue (2,1,3,0,4), con un costo total de 14.

---

## b) Solución dinámica

## c) Solución voraz

# 5. Partes importantes del código

---

## Cálculo del costo de una permutación

```python
def compute_cost_for_permutation(finca, perm):
    n = len(finca)
    t_start = [0] * n
    tiempo = 0
    for idx in perm:
        t_start[idx] = tiempo
        tiempo += finca[idx][1]  # sumar tr_i

    costo = 0
    for i in range(n):
        ts_i, tr_i, p_i = finca[i]
        retraso = (t_start[i] + tr_i) - ts_i
        if retraso > 0:
            costo += p_i * retraso
    return costo

```

👉 Aquí se implementa la fórmula matemática del costo de cada tablón.

---

## Función principal por fuerza bruta

```python
import itertools

def roFB(finca):
    n = len(finca)
    indices = list(range(n))
    best_perm, best_cost = [], float("inf")

    for perm in itertools.permutations(indices):
        costo = compute_cost_for_permutation(finca, perm)
        if costo < best_cost:
            best_cost = costo
            best_perm = list(perm)

    return best_perm, best_cost

```

👉 Esta función genera todas las permutaciones con `itertools.permutations`, evalúa cada una con `compute_cost_for_permutation` y selecciona la mejor. Retorna la permutación óptima y su costo asociado, cumpliendo con el formato del enunciado.

# 6. Pipeline de compilación/ejecución

---

Se definió un pipeline simple de integración continua en **GitHub Actions** para verificar que el proyecto se ejecute sin errores (no incluye pruebas de rendimiento ni validación).

Archivo: `.github/workflows/ci.yml`

```yaml
name: Knapsack CI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Run knapsack main script
        run: |
          python knapsack_report.py
```

# 7. Conclusión parcial

---

La solución por **fuerza bruta (roFB)**:

- Fue implementada en Python de manera clara y modular.
- Sigue exactamente las definiciones matemáticas del enunciado.
- Garantiza obtener la programación de riego óptima.
- Aunque es computacionalmente ineficiente para instancias grandes, sirve como referencia de comparación para las soluciones **voraz** y **dinámica**.
