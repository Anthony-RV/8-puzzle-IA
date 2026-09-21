import time
from puzzle_base import Puzzle8

def evaluar_motor_matematico():
    # Fijar la meta de acuerdo con el requerimiento del audio
    iteraciones = 1000
    
    resultados = {
        "A*":  {"tiempo_total": 0.0, "nodos_total": 0, "pasos_total": 0},
        "BFS": {"tiempo_total": 0.0, "nodos_total": 0, "pasos_total": 0}
    }

    print(f"Iniciando evaluación automatizada de {iteraciones} tableros en segundo plano...")
    print("El motor puro está calculando. Por favor, espera...\n")

    # Bucle de evaluación sin interfaz gráfica
    for i in range(iteraciones):
        # 1. Genera aleatoriamente un tablero válido
        juego = Puzzle8() 

        # 2. Resuelve usando A* (A-Estrella)
        inicio_astar = time.time()
        motor_astar = juego.resolver_astar()
        nodos_astar = 0
        camino_astar = []
        try:
            while True:
                _, camino_astar, _, _, nodos_astar = next(motor_astar)
        except StopIteration:
            pass
        fin_astar = time.time()

        resultados["A*"]["tiempo_total"] += (fin_astar - inicio_astar)
        resultados["A*"]["nodos_total"] += nodos_astar
        resultados["A*"]["pasos_total"] += len(camino_astar)

        # 3. Resuelve usando BFS consecutivamente sobre el mismo tablero
        inicio_bfs = time.time()
        motor_bfs = juego.resolver_bfs()
        nodos_bfs = 0
        camino_bfs = []
        try:
            while True:
                _, camino_bfs, _, _, nodos_bfs = next(motor_bfs)
        except StopIteration:
            pass
        fin_bfs = time.time()

        resultados["BFS"]["tiempo_total"] += (fin_bfs - inicio_bfs)
        resultados["BFS"]["nodos_total"] += nodos_bfs
        resultados["BFS"]["pasos_total"] += len(camino_bfs)

        # Monitor de progreso en consola
        if (i + 1) % 50 == 0:
            print(f"Progreso: {i + 1} / {iteraciones} tableros evaluados...")

    # Calcular y mostrar promedios finales
    print("\n" + "="*50)
    print(" RESULTADOS FINALES PROMEDIADOS (MOTOR PURO)")
    print("="*50)
    
    for algoritmo in ["A*", "BFS"]:
        promedio_tiempo = (resultados[algoritmo]["tiempo_total"] / iteraciones) * 1000  # Convertido a milisegundos
        promedio_nodos = resultados[algoritmo]["nodos_total"] / iteraciones
        promedio_pasos = resultados[algoritmo]["pasos_total"] / iteraciones
        
        # Formateando la salida para el informe
        if algoritmo == "A*":
            # Formato en minutos y segundos para comprobar la teoría del profesor
            minutos = int(resultados[algoritmo]["tiempo_total"] // 60)
            segundos = int(resultados[algoritmo]["tiempo_total"] % 60)
            print(f"--- Algoritmo {algoritmo} (Tiempo Total acumulado: {minutos}m {segundos}s) ---")
        else:
            minutos = int(resultados[algoritmo]["tiempo_total"] // 60)
            segundos = int(resultados[algoritmo]["tiempo_total"] % 60)
            print(f"--- Algoritmo {algoritmo} (Tiempo Total acumulado: {minutos}m {segundos}s) ---")

        print(f"Tiempo promedio de Ejecución : {promedio_tiempo:.2f} ms")
        print(f"Promedio de Nodos Expandidos : {promedio_nodos:.0f} nodos")
        print(f"Longitud del Camino          : {promedio_pasos:.1f} pasos\n")

if __name__ == "__main__":
    evaluar_motor_matematico()