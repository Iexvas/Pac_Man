# src/main.py
from laberinto import Laberinto
from interfaz import Interfaz
from busqueda_ciega import bfs, dfs, ucs, imprimir_metricas
from busqueda_informada import a_estrella, gbfs

def main():
    print("INICIANDO ENTORNO PAC-MAN")
    mi_laberinto = Laberinto('mapas/mapa_facil.txt')
    app = Interfaz(mi_laberinto)

    ruta_a, explorados_a, metrica_a = a_estrella(mi_laberinto)
    imprimir_metricas("A*", metrica_a, bool(ruta_a))

    ruta_g, explorados_g, metrica_g = gbfs(mi_laberinto)
    imprimir_metricas("GBFS", metrica_g, bool(ruta_g))

    app.dibujar()

    if ruta_a:
        app.dibujar_rastro(explorados_a, ruta_a)
    
    app.reproducir_inicio()
    
    app.mantener_abierta()

if __name__ == "__main__":
    main()