import tkinter as tk
from tkinter import ttk
from puzzle_base import Puzzle8

class InterfazPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle IA - Motor de Búsqueda Avanzado")
        self.root.geometry("1150x650")
        # Paleta de colores moderna
        self.bg_color = "#1E1E2E" # Fondo principal (Gris oscuro)
        self.panel_color = "#282A36" # Fondo de paneles
        self.text_color = "#F8F8F2" # Texto blanco
        self.tile_color = "#6272A4" # Fichas (Azul/Púrpura)
        self.success_color = "#50FA7B" # Fichas correctas (Verde neón)
        self.empty_color = "#1E1E2E" # Hueco (Se camufla con el fondo)
        
        self.root.configure(bg=self.bg_color, padx=20, pady=20)
        
        self.juego = Puzzle8()
        self.estado_inicial = self.juego.estado_inicial
        self.estado_fisico = list(self.estado_inicial)
        self.pasos_solucion = []
        self.indice_paso = 0
        
        self.construir_interfaz()
        self.actualizar_tablero_visual(self.estado_fisico)

    def construir_interfaz(self):
        # ESTILOS DE TKINTER
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.text_color)
        style.configure("TButton", font=("Arial", 10, "bold"), padding=5)

        # ==========================================
        # PANEL IZQUIERDO: Tablero y Controles
        # ==========================================
        panel_izquierdo = ttk.Frame(self.root)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        frame_controles = ttk.Frame(panel_izquierdo)
        frame_controles.pack(pady=10)
        
        ttk.Label(frame_controles, text="Algoritmo:", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5)
        self.combo_algoritmo = ttk.Combobox(frame_controles, values=["BFS (Anchura)", "A* (Manhattan)"], state="readonly", width=15)
        self.combo_algoritmo.current(0)
        self.combo_algoritmo.grid(row=0, column=1, padx=5)
        
        ttk.Button(frame_controles, text="1. Iniciar Inteligencia", command=self.iniciar_busqueda).grid(row=0, column=2, padx=5)
        self.btn_paso = ttk.Button(frame_controles, text="2. Mover 1 Ficha ►", command=self.siguiente_movimiento, state=tk.DISABLED)
        self.btn_paso.grid(row=0, column=3, padx=5)
        self.btn_animar = ttk.Button(frame_controles, text="Resolver Solo ⏩", command=self.animar_todo, state=tk.DISABLED)
        self.btn_animar.grid(row=0, column=4, padx=5)
        ttk.Button(frame_controles, text="Reiniciar Tablero", command=self.reiniciar).grid(row=0, column=5, padx=5)

        # Tablero visual 3x3
        self.frame_tablero = tk.Frame(panel_izquierdo, bg=self.panel_color, bd=5, relief=tk.FLAT)
        self.frame_tablero.pack(pady=30)
        
        self.casillas = []
        for i in range(3):
            fila_labels = []
            for j in range(3):
                lbl = tk.Label(self.frame_tablero, text="", font=("Helvetica", 45, "bold"), 
                               width=4, height=2, relief=tk.RAISED, bd=3)
                lbl.grid(row=i, column=j, padx=4, pady=4)
                fila_labels.append(lbl)
            self.casillas.append(fila_labels)

        # ==========================================
        # PANEL DERECHO: Trazabilidad (Para el Profesor)
        # ==========================================
        panel_derecho = tk.Frame(self.root, bg=self.panel_color, width=420, bd=2, relief=tk.SUNKEN, padx=10, pady=10)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        panel_derecho.pack_propagate(False)

        ttk.Label(panel_derecho, text="📊 MÉTRICAS DEL ALGORITMO", font=("Arial", 12, "bold"), background=self.panel_color).pack(anchor=tk.W)
        self.lbl_estado = ttk.Label(panel_derecho, text="Esperando ejecución...\n\n", background=self.panel_color, font=("Arial", 10))
        self.lbl_estado.pack(anchor=tk.W, pady=10)

        ttk.Label(panel_derecho, text="Ruta Óptima Encontrada:", font=("Arial", 10, "bold"), background=self.panel_color).pack(anchor=tk.W)
        self.txt_ruta = tk.Text(panel_derecho, height=4, width=45, font=("Consolas", 9), bg="#000000", fg="#00FF00")
        self.txt_ruta.pack(pady=5)

        ttk.Label(panel_derecho, text="Nodos Visitados (Memoria IA):", font=("Arial", 10, "bold"), background=self.panel_color).pack(anchor=tk.W, pady=(10,0))
        self.txt_visitados = tk.Text(panel_derecho, height=12, width=45, font=("Consolas", 9), bg="#000000", fg="#00FF00")
        self.txt_visitados.pack(pady=5)

    def actualizar_tablero_visual(self, estado):
        """Mapea la tupla a la cuadrícula con colores y estilos."""
        for i in range(3):
            for j in range(3):
                idx = i * 3 + j
                valor = estado[idx]
                
                if valor == 0:
                    # El hueco se camufla con el fondo
                    self.casillas[i][j].config(text="", bg=self.empty_color, relief=tk.FLAT) 
                else:
                    # Si la ficha está en su posición final correcta, se pinta de verde
                    if valor == self.juego.objetivo[idx]:
                        self.casillas[i][j].config(text=str(valor), bg=self.success_color, fg="#000000", relief=tk.RAISED)
                    else:
                        # Si no, se pinta del color azul/púrpura por defecto
                        self.casillas[i][j].config(text=str(valor), bg=self.tile_color, fg=self.text_color, relief=tk.RAISED)

    def iniciar_busqueda(self):
        """La IA calcula toda la ruta en milisegundos y prepara la animación física."""
        self.txt_ruta.delete(1.0, tk.END)
        self.txt_visitados.delete(1.0, tk.END)
        self.txt_ruta.insert(tk.END, "Calculando... Esto puede tardar unos segundos en BFS.\n")
        self.root.update()
        
        algoritmo = self.combo_algoritmo.get()
        motor = self.juego.resolver_bfs() if "BFS" in algoritmo else self.juego.resolver_astar()
        
        # Ejecutar la IA en silencio hasta encontrar la meta
        camino_final = []
        expandidos = 0
        ultimo_estado = None
        
        # Guardamos un fragmento de los visitados para no saturar la memoria gráfica de Tkinter
        historial_visitados = []
        
        try:
            while True:
                estado_act, camino, frontera, visitados, expandidos = next(motor)
                ultimo_estado = estado_act
                camino_final = camino
                # Solo guardamos 1 de cada 50 estados para que la caja de texto no se trabe
                if expandidos % 50 == 0:
                    historial_visitados.append(str(estado_act))
        except StopIteration:
            pass

        # Mostrar métricas al profesor
        self.lbl_estado.config(text=f"✅ Búsqueda Completada\nNodos expandidos en memoria: {expandidos}\nCosto de la ruta óptima: {len(camino_final)} pasos")
        
        self.txt_ruta.delete(1.0, tk.END)
        self.txt_ruta.insert(tk.END, f"{camino_final}")
        
        self.txt_visitados.insert(tk.END, "\n".join(historial_visitados))
        self.txt_visitados.insert(tk.END, "\n... (Búsqueda Finalizada) ...")
        self.txt_visitados.see(tk.END)

        # Habilitar los botones físicos
        self.pasos_solucion = camino_final
        self.indice_paso = 0
        self.estado_fisico = list(self.estado_inicial)
        self.btn_paso.config(state=tk.NORMAL)
        self.btn_animar.config(state=tk.NORMAL)

    def mover_ficha_fisica(self, accion):
        """Mueve estrictamente una sola ficha en la pantalla."""
        idx_vacio = self.estado_fisico.index(0)
        
        if accion == "Arriba": nuevo_idx = idx_vacio - 3
        elif accion == "Abajo": nuevo_idx = idx_vacio + 3
        elif accion == "Izquierda": nuevo_idx = idx_vacio - 1
        elif accion == "Derecha": nuevo_idx = idx_vacio + 1
        
        # Intercambio físico de la ficha con el hueco
        self.estado_fisico[idx_vacio], self.estado_fisico[nuevo_idx] = self.estado_fisico[nuevo_idx], self.estado_fisico[idx_vacio]
        self.actualizar_tablero_visual(tuple(self.estado_fisico))

    def siguiente_movimiento(self):
        """Ejecuta un paso de la solución al presionar el botón."""
        if self.indice_paso < len(self.pasos_solucion):
            accion = self.pasos_solucion[self.indice_paso]
            self.mover_ficha_fisica(accion)
            self.indice_paso += 1
            
            if self.indice_paso == len(self.pasos_solucion):
                self.btn_paso.config(state=tk.DISABLED)
                self.btn_animar.config(state=tk.DISABLED)

    def animar_todo(self):
        """Reproduce la solución automáticamente."""
        self.btn_paso.config(state=tk.DISABLED)
        self.btn_animar.config(state=tk.DISABLED)
        
        if self.indice_paso < len(self.pasos_solucion):
            accion = self.pasos_solucion[self.indice_paso]
            self.mover_ficha_fisica(accion)
            self.indice_paso += 1
            self.root.after(300, self.animar_todo) # Retraso de 300ms para ver el movimiento fluido

    def reiniciar(self):
        """Genera un nuevo tablero aleatorio y bloquea los botones."""
        self.juego = Puzzle8()
        self.estado_inicial = self.juego.estado_inicial
        self.estado_fisico = list(self.estado_inicial)
        self.actualizar_tablero_visual(self.estado_fisico)
        
        self.txt_ruta.delete(1.0, tk.END)
        self.txt_visitados.delete(1.0, tk.END)
        self.lbl_estado.config(text="Esperando ejecución...\n\n")
        
        self.btn_paso.config(state=tk.DISABLED)
        self.btn_animar.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazPuzzle(root)
    root.mainloop()