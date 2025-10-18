# Informe de Complejidad - Problema de Riego Óptimo

## 1. Fuerza Bruta

---

### Complejidad Temporal T(n)

Para un conjunto de ( n ) tablones:

1. Generar todas las permutaciones posibles de los índices $0, 1, 2, \dots, n-1$ tiene un costo de: $O(n!)$
2. **Evaluación del costo para cada permutación:**
    
    La función `compute_cost_for_permutation` recorre todos los tablones dos veces:
    
    - Una vez para calcular los tiempos de inicio $(O(n))$.
    - Otra vez para calcular el costo $(O(n))$.
    
    Por tanto, el costo de evaluar una permutación es:
    
    $$
    (O(n))
    $$
    
3. **Costo total del algoritmo:**

$$
O(n! \times n) = O(n \cdot n!)
$$

### 🔹 Ejemplo de crecimiento

| n | $n!$   | $n·n!$ (operaciones aproximadas) |
| --- |--------|----------------------------------|
| 4 | 24     | 96                               |
| 6 | 720    | 4320                             |
| 8 | 40320  | 322560                           |
| 10 | 3.6×10⁶ | 3.6×10⁷                          |

El crecimiento factorial vuelve al algoritmo **inviable para n mayores a 10**, pues el tiempo de ejecución crece exponencialmente.

### Complejidad Espacial S(n)

- Cada permutación se genera y procesa una a la vez por `itertools.permutations`, lo que evita almacenar todas las permutaciones en memoria.
- Se usa memoria proporcional a:
    - La lista `finca` → (O(n))
    - La lista temporal `perm` → (O(n))
    - Variables auxiliares (enteros, listas temporales pequeñas)

Por tanto:

$$
\text{Complejidad espacial } = O(n)
$$

### Corrección del algoritmo

El método de fuerza bruta **garantiza la solución óptima**, ya que explora exhaustivamente **todas las posibles permutaciones** del orden de riego y selecciona la de menor costo.

Formalmente:

$$
\text{roFB}(F) = \arg\min_{\Pi \in S_n} CRF_{\Pi}
$$

donde $S_n$ es el conjunto de todas las permutaciones de $n$ elementos.

Por lo tanto, el algoritmo es **correcto y completo**, aunque **ineficiente para grandes valores de $n$**.

---

# 2. Programación Dinámica

## Complejidad Temporal T(n)

- $S$ tiene una cantidad $2^n$  de subconjuntos posibles dado por las `mask` .
- Para cada subconjunto se itera sobre los tablones activos.
- Para cada tablón se busca tomar su tiempo, donde en el peor caso puede haber varios pero el número total de estados `(mask)` crece proporcionalmente al número de combinaciones distintas.

Teniendo esto en cuenta, la complejidad T(n) de la solución dinámica es de:

$$
T(n) = O(n*2^n)
$$

## Complejidad Espacial S(n)

- En memoria se almacena un valor $DP[S]$ por cada conjunto $S$
- $DP$ guarda al menos un valor por cada combinación posible de `(mask, t)`

Por lo tanto, la complejidad espacial S(n) es de:

$$
S(n) = O(2^n)
$$

---

## 3. Algoritmo voraz (greedy por razón valor/peso)

### Complejidad temporal

El algoritmo voraz comienza calculando la razón valor/peso de cada objeto, lo que requiere:
\[
O(n)
\]

Luego, se ordenan los objetos según esta razón, lo cual domina el costo total, ya que el ordenamiento eficiente requiere:
\[
O(n \log n)
\]

Finalmente, se recorre la lista ordenada para llenar la mochila, con un costo lineal:
\[
O(n)
\]

Por tanto, la complejidad total es:
\[
T(n) = O(n \log n)
\]

Esto convierte al algoritmo voraz en el más eficiente en tiempo entre las tres aproximaciones. Sin embargo, a diferencia de la programación dinámica, no garantiza la solución óptima, ya que tomar siempre el objeto con mejor razón local no asegura la mejor combinación global.

### Complejidad espacial

- Lista de objetos con razón valor/peso: \(O(n)\).
- No se requiere matriz adicional.

Así:
\[
S(n) = O(n)
\]

---

## 4. Resumen comparativo

| Estrategia            | Complejidad temporal | Complejidad espacial                   |
| --------------------- | -------------------- | -------------------------------------- |
| Fuerza bruta          | $\(O(n \cdot 2^n)\)$   | $\(O(n)\)$                               |
| Programación dinámica | $\(O(n \cdot W)\) $    | $\(O(n \cdot W)\) ó \(O(W)\)$ optimizado |
| Voraz                 | $\(O(n \log n)\) $    | $\(O(n)\)$                               |

---

### 4.1 Analisis mediante gráficas

Comparacion teorica de complejidades en tiempo y espacio para las tres estrategias implementadas.

![Comparativa de tiempo](imagenes/g1.png)

Analisis de DP con W con n fijo

![Comparativa DP](imagenes/g2.png)

Recordar incluir la comparacion de tiempos con respecto a lo implementado. No se incluye en este ejemplo.


Comparacion teorica de complejidades en caso practico y teorico de PD.

|[Comparativa complejidad](imagenes/PD1.png)

---

## 5. Conclusiones

### Programación bruta:

La solución por fuerza bruta genera todas las permutaciones posibles, por lo tanto su complejidad temporal es
$O(n!⋅n)$.
Se verificó experimentalmente que el tiempo crece factorialmente: la ejecución es factible hasta $n=10$.
Para n mayores, el algoritmo resulta impracticable: por ejemplo, $n=100$ implicaría 9.3×10¹⁵⁷ permutaciones, lo que hace imposible su ejecución en cualquier computador actual.
El enfoque de fuerza bruta sirve como **referencia base** para comparar las soluciones **voraces** y de **programación dinámica**, permitiendo verificar la corrección de sus resultados.

### Programación dinámica:

En el punto de vista del costo computacional un costo de $O(n*2^n)$ hace que para tamaños pequeños de tablones sea mucho más eficiente que la solucion bruta, sin embargo, cuando $numeroTablones > 20$, entonces el tiempo crece tanto que resulta inviable y casi imposible de calcular.

### Programación voraz:

- El **algoritmo voraz** es eficiente en tiempo y espacio, pero no garantiza la solución óptima.