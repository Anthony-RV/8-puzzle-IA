import random
import collections
import heapq

class Puzzle8:
    def __init__(self):
        # El estado objetivo definido en el informe (0 es el hueco al final)
        self.objetivo = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.estado_inicial = self.generar_tablero_valido()

    def es_resoluble(self, tablero):
        """Calcula la paridad de inversiones para garantizar que el tablero tenga solución."""
        inversiones = 0
        fichas = [f for f in tablero if f != 0]
        
        for i in range(len(fichas)):
            for j in range(i + 1, len(fichas)):
                if fichas[i] > fichas[j]:
                    inversiones += 1
                    
        return inversiones % 2 == 0

    def generar_tablero_valido(self):
        """Genera tableros aleatorios hasta encontrar uno resoluble."""
        tablero = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        while True:
            random.shuffle(tablero)
            tupla_tablero = tuple(tablero)
            if self.es_resoluble(tupla_tablero) and tupla_tablero != self.objetivo:
                return tupla_tablero

    def obtener_sucesores(self, estado):
        """Genera los nodos hijos moviendo el hueco (0). Retorna: (nuevo_estado, accion, costo)"""
        sucesores = []
        idx_vacio = estado.index(0)
        fila, col = divmod(idx_vacio, 3)

        movimientos = {
            "Arriba": (-1, 0, idx_vacio - 3),
            "Abajo": (1, 0, idx_vacio + 3),
            "Izquierda": (0, -1, idx_vacio - 1),
            "Derecha": (0, 1, idx_vacio + 1)
        }

        for accion, (df, dc, nuevo_idx) in movimientos.items():
            if 0 <= fila + df < 3 and 0 <= col + dc < 3:
                nuevo_estado = list(estado)
                nuevo_estado[idx_vacio], nuevo_estado[nuevo_idx] = nuevo_estado[nuevo_idx], nuevo_estado[idx_vacio]
                sucesores.append((tuple(nuevo_estado), accion, 1))
                
        return sucesores

    def heuristica_manhattan(self, estado):
        """Calcula la suma de distancias de cada ficha a su posición final ideal."""
        distancia = 0
        for i, valor in enumerate(estado):
            if valor == 0: continue
            fila_act, col_act = divmod(i, 3)
            fila_obj, col_obj = divmod(self.objetivo.index(valor), 3)
            distancia += abs(fila_act - fila_obj) + abs(col_act - col_obj)
        return distancia

    def resolver_bfs(self):
        """Búsqueda a lo Ancho (No informada). Implementa Cola FIFO."""
        frontera = collections.deque([(self.estado_inicial, [])])
        visitados = set()
        nodos_expandidos = 0

        while frontera:
            estado_actual, camino = frontera.popleft()
            
            if estado_actual in visitados: continue
            
            visitados.add(estado_actual)
            nodos_expandidos += 1

            yield estado_actual, camino, list(frontera), visitados, nodos_expandidos

            if estado_actual == self.objetivo:
                break

            for sucesor, accion, costo in self.obtener_sucesores(estado_actual):
                if sucesor not in visitados:
                    frontera.append((sucesor, camino + [accion]))

    def resolver_astar(self):
        """Algoritmo A* (Informada). Implementa Cola de Prioridad y Distancia Manhattan."""
        contador = 0
        frontera = []
        h_inicial = self.heuristica_manhattan(self.estado_inicial)
        heapq.heappush(frontera, (h_inicial, contador, self.estado_inicial, [], 0))
        
        visitados = set()
        nodos_expandidos = 0

        while frontera:
            f, _, estado_actual, camino, g = heapq.heappop(frontera)

            if estado_actual in visitados: continue

            visitados.add(estado_actual)
            nodos_expandidos += 1

            yield estado_actual, camino, frontera, visitados, nodos_expandidos

            if estado_actual == self.objetivo:
                break

            for sucesor, accion, costo in self.obtener_sucesores(estado_actual):
                if sucesor not in visitados:
                    nuevo_g = g + costo
                    nuevo_h = self.heuristica_manhattan(sucesor)
                    nuevo_f = nuevo_g + nuevo_h
                    contador += 1
                    heapq.heappush(frontera, (nuevo_f, contador, sucesor, camino + [accion], nuevo_g))  