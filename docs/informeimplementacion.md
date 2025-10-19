# Informe de Implementación — Problema del Riego Óptimo

## 0. Descripción del problema

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

## 1. Lenguaje y herramientas usadas

---

- **Lenguaje:** Python 3.
- **Bibliotecas estándar:** `itertools` para generar permutaciones, `time` para medir el tiempo de ejecución y `random` para generar los tablones aleatoriamente.
- **Estructuras usadas:** listas y tuplas para representar la finca.
- **Motivación de elección:** Python permite implementar rápidamente algoritmos de prueba como fuerza bruta, además de facilitar el uso de librerías de testing (`pytest`) y pipelines de integración continua.

## 2. Estructura del proyecto

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

## 3. Ejecución del proyecto

---

El programa se ejecuta desde consola con el archivo `main.py`.

#### Ejemplo de uso:

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

## 4. Ideas de solución

---

### a) Solución ingenua (fuerza bruta)

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

##### Ejemplo de crecimiento

| n | $n!$   | $n·n!$ (operaciones aproximadas) |
| --- |--------|----------------------------------|
| 4 | 24     | 96                               |
| 6 | 720    | 4320                             |
| 8 | 40320  | 322560                           |
| 10 | 3.6×10⁶ | 3.6×10⁷                          |

El crecimiento factorial vuelve al algoritmo **inviable para n mayores a 10**, pues el tiempo de ejecución crece exponencialmente.

---

### b) Solución dinámica

El enfoque por solución dinámica consiste en descomponer el problema en subproblemas más pequeños, en este caso calculando la permutación de cada tablón: 

Definimos todo subconjunto para $S ⊆{0,…,n−1}$:

- Donde $DP[S] =$ mínimo $CRF$ al regar las tareas del conjunto $S$

Posteriormente, si en la solución optima, el utimo tablon en regar es $j ∈ S$ entonces:

- La penalización añadida a $j$  es:
$$DP[S\setminus\{j\}]+pj​⋅max(0,(C(S∖{j})+trj​)−tsj​).$$

- El tiempo acumulado antes de empezar $j$ es $(S\setminus\{j\})$
- Al no conocer cual es el ultimo $j$, tomamos el mínimo sobre todos los $j ∈ S$:

$$
DP[S] = min(DP[S\setminus\{j\}] + p_i*max(0,(C(S\setminus\{j\})+tr_j)+ts_j)
$$

#### Reconstrucción de la permutación óptima

Al calcular $DP[S]$ se guarda para cada $S$ el indice $j*S$. 

Empezando desde $S=(0,…,n−1)$ reconstruyendo la permutación de forma iterativa.

- $j1=j∗(S)$ es la última tarea en la solución óptima de $S$
- Se reemplaza $S <= S\setminus\{j\}$

Al final obteniendo así el orden inverso, lo que retorna la permutación $II$ completa.

#### Ejemplo:

sea $F_1:$

| **$i$** | **$ts_i$** | **$tr_i$** | **$p_i$** |
| --- | --- | --- | --- |
| 0 | 10 | 3 | 4 |
| 1 | 5 | 3 | 3 |
| 2 | 2 | 2 | 1 |
| 3 | 8 | 1 | 1 |
| 4 | 6 | 4 | 2 |

**Caso base:** $DP[∅, 0] = 0$ 

Para cada subconjunto S y cada tablón j ∈ S:

$$
DP[S, t_{final}] = min(DP[S\{j, t_{anterior}] + p_j × max(0, (t_{anterior} + tr_j) - ts_j))
$$

**Subconjuntos de tamaño 1:**

- DP[{2}, 2] = 0 + 1×max(0, 2-2) = 0 (regar tablón 2 primero)
- DP[{3}, 1] = 0 + 1×max(0, 1-8) = 0 (regar tablón 3 primero)
- DP[{1}, 3] = 0 + 3×max(0, 3-5) = 0 (regar tablón 1 primero)

**Subconjuntos de tamaño 2:**

- DP[{2,1}, 5] = DP[{2}, 2] + 3×max(0, 5-5) = 0 + 0 = 0
- DP[{2,3}, 3] = DP[{2}, 2] + 1×max(0, 3-8) = 0 + 0 = 0

Y así sucesivamente hasta alcanzar el conjunto completo {0,1,2,3,4}.

#### Resultado final:

Según el código implementado, al evaluar todos los subconjuntos posibles y reconstruir la permutación óptima desde el estado final, se obtiene:

- **Permutación óptima:** (2, 1, 3, 0, 4)
- **Costo total:** 14


### c) Solución voraz

El enfoque **voraz** busca construir una solución de forma **rápida y aproximada**, tomando decisiones locales que se espera conduzcan a un resultado cercano al óptimo.

En este problema, el algoritmo selecciona el orden de riego según una **regla de prioridad**, sin explorar todas las permutaciones posibles como la fuerza bruta ni usar almacenamiento intermedio como la dinámica.

#### Idea principal

Cada tablón $i$ se describe por:

- $ts_i$ : tiempo máximo que puede sobrevivir sin riego,
- $tr_i$: tiempo de regado,
- $p_i$ : prioridad o importancia del tablón.

El algoritmo considera que un tablón es **más urgente** si tiene una alta prioridad y un bajo tiempo de supervivencia.

Por ello, se define la **razón voraz**:

                                                                              $Ri = \frac{p_i}{ts_i}$

El algoritmo ordena los tablones de forma descendente según esta razón, y luego calcula el costo total en ese orden.

#### Ejemplo de ejecución

Para la finca  $F_1 = \langle (10,3,4), (5,3,3), (2,2,1), (8,1,1), (6,4,2) \rangle$ :

1. Se calculan las razones $p_i/ts_i$:
    - Tablón 0: 0.4
    - Tablón 1: 0.6
    - Tablón 2: 0.5
    - Tablón 3: 0.125
    - Tablón 4: 0.333
2. Se ordenan de forma descendente: **(1, 2, 0, 4, 3)**
3. Al calcular el costo según esta secuencia:
    - Costo total obtenido por el algoritmo voraz: **20**
    - Costo óptimo (fuerza bruta): **14**

El resultado es cercano al óptimo, pero no exacto, demostrando la naturaleza aproximada del enfoque voraz.

#### Complejidad

- **Ordenamiento:**  $O(n \log n)$
- **Cálculo del costo:**  $O(n)$
- **Complejidad total:  $T(n) = O(n \log n)$**

Este algoritmo es significativamente más rápido que la fuerza bruta $(O(n!))$ y más simple que la programación dinámica.

#### Observaciones

- El método voraz obtiene soluciones **óptimas en algunos casos simples** (por ejemplo, cuando la prioridad y supervivencia están equilibradas).
- En casos más complejos, produce soluciones **cercanas al óptimo**, pero no exactas.
- A cambio, ofrece una **excelente relación costo/tiempo**, siendo apropiado para problemas con grandes cantidades de tablones.

## 5. Partes importantes del código

---

### Cálculo del costo de una permutación

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

Aquí se implementa la fórmula matemática del costo de cada tablón.

### Función principal por fuerza bruta

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

### Función principal por programación dinámica

```python
def roPD(finca):
    #Finca = Secuencia de tablones
    #Ti = tupla (ts,tr,p)
    #CRF[i] = p * max(0,(ti^II + tr) - ts) 
    n = len(finca)
    DP = {}
    parent = {}

    DP[(0, 0)] = 0 # caso base
    parent[(0, 0)] = -1
    
    for mask in range(1, 1 << n):
        tablones_en_mask = [i for i in range(n) if mask & (1 << i)]
        
        for i in tablones_en_mask:
            prev_mask = mask ^ (1 << i)

            if prev_mask == 0:
                prev_tiempos = [0]
            else:
                prev_tiempos = [t for (s, t) in DP.keys() if s == prev_mask]
            
            for t_anterior in prev_tiempos:
                if (prev_mask, t_anterior) not in DP:
                    continue
                
                costo_anterior = DP[(prev_mask, t_anterior)]
                ts, tr, p = finca[i]
                
                t_inicio = t_anterior
                t_final = t_inicio + tr
                retraso = max(0, t_final - ts)
                costo_suficiencia = p * retraso
                costo_nuevo = costo_anterior + costo_suficiencia

                if (mask, t_final) not in DP or DP[(mask, t_final)] > costo_nuevo:
                    DP[(mask, t_final)] = costo_nuevo
                    parent[(mask, t_final)] = (prev_mask, t_anterior, i)

    mask_completo = (1 << n) - 1
    costo_minimo = float('inf')
    tiempo_optimo = -1
    
    for (mask, t_final) in DP.keys():
        if mask == mask_completo and DP[(mask, t_final)] < costo_minimo:
            costo_minimo = DP[(mask, t_final)]
            tiempo_optimo = t_final

    permutacion = []
    mask_actual = mask_completo
    tiempo_actual = tiempo_optimo
    
    while mask_actual != 0:
        prev_mask, prev_tiempo, idx_tablon = parent[(mask_actual, tiempo_actual)]
        permutacion.append(idx_tablon)
        mask_actual = prev_mask
        tiempo_actual = prev_tiempo
    
    permutacion.reverse()
    return permutacion, costo_minimo
```

Esta función busca la **permutación optima**, haciendo uso de `mask` el cual representa los subproblemas (tablones regados) y `dp(mask)` devuelve el costo mínimo total de regar ese tablón. De forma que, se prueban todas las posibles opciones para elegir la **solución optima**.

Usando el diccionario `parent`, el algoritmo reconstruye la **permutación óptima** recorriendo los estados desde el final (`mask_completo`) hacia atrás, hasta llegar al estado vacío `(0,0)`.

Esta función genera todas las permutaciones con `itertools.permutations`, evalúa cada una con `compute_cost_for_permutation` y selecciona la mejor. Retorna la permutación óptima y su costo asociado, cumpliendo con el formato del enunciado.

---

### Función principal por programación voraz

```python
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
```

Esta función implementa el **algoritmo voraz**, el cual ordena los tablones de acuerdo con una **razón de prioridad** dada por `(pᵢ / tsᵢ)`, donde los tablones con mayor prioridad y menor tiempo de supervivencia se riegan primero.
De esta forma, se genera una **secuencia de riego aproximada** sin evaluar todas las permutaciones posibles.

Durante la ejecución, se calcula el **costo total** acumulando penalizaciones por retraso mediante la expresión `p * max(0, fin - ts)`.
El algoritmo devuelve el **orden obtenido** y su **costo asociado**, proporcionando una solución eficiente con complejidad **O(n log n)**, aunque no siempre óptima.


## 6. Pipeline de compilación/ejecución

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

## 7. Conclusión parcial

---

La solución por **fuerza bruta (roFB)**:

- Fue implementada en Python de manera clara y modular.
- Sigue exactamente las definiciones matemáticas del enunciado.
- Garantiza obtener la programación de riego óptima.
- Aunque es computacionalmente ineficiente para instancias grandes, sirve como referencia de comparación para las soluciones **voraz** y **dinámica**.

La solución **dinámica (roPD)**:

- Fue implementada de forma concisa en Python.
- Identifica la subestructura óptima.
- Evalúa cada permutación para encontrar la solución optima.
- Garantiza una solución óptima.
- Muestra una gran optimización en costo computacional y tiempo de ejecución respecto a la solución por fuerza bruta.

La solución **voraz (roV)**:

- Fue implementada en Python de forma sencilla, eficiente y modular.
- Utiliza una **regla de prioridad** basada en la razón *(pᵢ / tsᵢ)* para determinar el orden de riego.
- Permite obtener soluciones **rápidas y razonablemente buenas** sin evaluar todas las combinaciones posibles.
- Su **complejidad O(n log n)** la hace adecuada para **instancias grandes**, donde la fuerza bruta o la dinámica serían demasiado costosas.
- Aunque **no garantiza siempre la solución óptima**, mantiene una **buena relación entre calidad y tiempo de ejecución**.
- Resulta útil como método aproximado en escenarios donde la **rapidez de respuesta** es más importante que la precisión absoluta.