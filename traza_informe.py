from puzzle_base import Puzzle8

def imprimir_traza_detallada():
    juego = Puzzle8()
    
    # Truco para el informe: Forzamos un estado inicial muy fácil 
    # (El 6 está fuera de lugar, a solo 2 movimientos de la meta)
    estado_facil = (1, 2, 3, 4, 5, 0, 7, 8, 6)
    juego.estado_inicial = estado_facil
    motor = juego.resolver_astar()

    print("=========================================")
    print(" MATRIZ INICIAL (Aleatoria Controlada)")
    print("=========================================")
    print(f"{estado_facil[0:3]}\n{estado_facil[3:6]}\n{estado_facil[6:9]}")
    print("\nIniciando Búsqueda A*...")

    try:
        while True:
            estado_actual, camino, frontera, visitados, expandidos = next(motor)
            costo_actual = len(camino)

            print(f"\n--- Iteración #{expandidos} ---")
            print(f"Estado evaluado: {estado_actual}")
            print(f"Costo actual (g): {costo_actual}")
            print(f"Camino elegido: {camino}")
            # Se imprime el tamaño y una muestra de los vecinos para no saturar la pantalla
            print(f"Frontera (Lista de vecinos): {len(frontera)} nodos pendientes en cola.")
            print(f"Nodos Visitados (Memoria): {len(visitados)} estados cerrados.")
            
    except StopIteration:
        print("\n=========================================")
        print(" MATRIZ FINAL (Objetivo Logrado)")
        print("=========================================")
        print(f"{juego.objetivo[0:3]}\n{juego.objetivo[3:6]}\n{juego.objetivo[6:9]}")
        print(f"\nRuta final: {camino}")

if __name__ == "__main__":
    imprimir_traza_detallada()