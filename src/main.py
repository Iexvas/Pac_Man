# src/main.py
from laberinto import Laberinto
from interfaz import Interfaz

def main():
    print("INICIANDO ENTORNO PAC-MAN")
    
    mi_laberinto = Laberinto('mapas/mapa_facil.txt')
    mi_laberinto.mostrar_consola()
    
    print("\nMapa cargado en memoria:")
    mi_laberinto.mostrar_consola()
    app = Interfaz(mi_laberinto)
    app.mantener_abierta()

if __name__ == "__main__":
    main()