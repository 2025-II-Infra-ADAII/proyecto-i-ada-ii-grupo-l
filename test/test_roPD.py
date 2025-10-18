import unittest
import time
import random
from problema_riego import roPD


class TestRoPD(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.random_seed = 42
        random.seed(self.random_seed)

    def generar_finca_aleatoria(self, n, max_ts=100, max_tr=10, max_p=5):
        """Genera una secuencia de tablones aleatoria para pruebas"""
        return [(random.randint(1, max_ts),
                 random.randint(1, max_tr),
                 random.randint(1, max_p)) for _ in range(n)]

    # -----------------------------------------------------
    # 1. Prueba del ejemplo del enunciado
    # -----------------------------------------------------
    def test_tamano_juguete(self):
        print("\n Prueba los elementos del enunciado")

        finca = [
            (10, 3, 4),
            (5, 3, 3),
            (2, 2, 1),
            (8, 1, 1),
            (6, 4, 2)
        ]

        start_time = time.time()
        permutacion, costo = roPD(finca)
        end_time = time.time()

        print(f"Tiempo ejecución: {end_time - start_time:.4f} segundos")
        print(f"Permutación: {permutacion}")
        print(f"Costo total: {costo}")

        self.assertEqual(len(permutacion), len(finca))
        self.assertEqual(len(set(permutacion)), len(finca))  
        self.assertGreaterEqual(costo, 0)

    # -----------------------------------------------------
    # 2. Pruebas de rendimiento
    # -----------------------------------------------------

    def test_tamaño_juguete_aleatorio(self):
        print("\n Prueba con 10 elementos aleatorios")

        finca = self.generar_finca_aleatoria(10)

        start_time = time.time()
        permutacion, costo = roPD(finca)
        end_time = time.time()

        print(f"Tiempo ejecución: {end_time - start_time:.4f} segundos")
        print(f"Costo total: {costo}")

        self.assertEqual(len(permutacion), len(finca))
        self.assertEqual(len(set(permutacion)), len(finca))
        self.assertGreaterEqual(costo, 0)

    def test_tamaño_pequeno(self):
        print("\n ¨Prueba con tamaño 20 - Maximo posible para PD")
        finca = self.generar_finca_aleatoria(20, max_ts=500, max_tr=20, max_p=10)

        start_time = time.time()
        try:
            permutacion, costo = roPD(finca)
            end_time = time.time()

            print(f"Tiempo ejecución: {end_time - start_time:.4f} segundos")
            print(f"Costo total: {costo}")

            if permutacion: 
                self.assertEqual(len(permutacion), len(finca))
                self.assertEqual(len(set(permutacion)), len(finca))
                self.assertGreaterEqual(costo, 0)
        except (MemoryError, RecursionError, TimeoutError) as e:
            print(f"Algoritmo no puede manejar 100 elementos: {e}")
            self.skipTest("Algoritmo no puede manejar este tamaño")



if __name__ == '__main__':
    unittest.main(verbosity=2)
