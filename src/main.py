# src/main.py
from laberinto import Laberinto
from interfaz import Interfaz
from busqueda_ciega import bfs, dfs, ucs, imprimir_metricas

def main():
    print("INICIANDO ENTORNO PAC-MAN")
    mi_laberinto = Laberinto('mapas/mapa_facil.txt')
    app = Interfaz(mi_laberinto)
    app.dibujar()
    app.reproducir_inicio()
    
    # Aquí van los algoritmos de búsqueda

    app.mantener_abierta()

if __name__ == "__main__":
    main()